#!/usr/bin/env python3
"""Safely add native curated personalities to already-installed Hermes profiles.

Default action is read-only. --apply makes only two scoped changes per profile:
agent.personalities.<profile-name> and, if unset, display.personality.
Existing model/provider, integrations, toolsets, comments and selections survive.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import tempfile
from datetime import datetime, timezone
from uuid import uuid4

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from capabilities import load_json, source_profiles  # noqa: E402


def digest(blob: bytes | None) -> str | None:
    return hashlib.sha256(blob).hexdigest() if blob is not None else None


def load_yaml(raw: str) -> dict:
    """Reject duplicated YAML keys rather than silently losing a setting."""
    class StrictLoader(yaml.SafeLoader):
        pass

    def mapping(loader, node):
        result = {}
        for key_node, val_node in node.value:
            key = loader.construct_object(key_node, deep=True)
            if key in result:
                raise ValueError("duplicate YAML mapping key")
            result[key] = loader.construct_object(val_node, deep=True)
        return result

    StrictLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping
    )
    value = yaml.load(raw, Loader=StrictLoader) or {}
    if not isinstance(value, dict):
        raise ValueError("configuration must be a YAML mapping")
    return value


def add_nested(text: str, parent: str, child: dict) -> str:
    """Append a mapping key without reserializing unrelated user YAML."""
    fragment = yaml.safe_dump(child, allow_unicode=True, sort_keys=False, width=120)
    lines = text.splitlines(keepends=True)
    matches = [
        i for i, line in enumerate(lines)
        if re.fullmatch(rf"{re.escape(parent)}:[ \t]*(?:#.*)?", line.rstrip("\r\n"))
    ]
    if len(matches) != 1:
        raise ValueError(f"non-block or ambiguous {parent} YAML section")
    first = matches[0] + 1
    end = next((
        i for i in range(first, len(lines))
        if re.match(r"^[A-Za-z_][A-Za-z0-9_-]*[ \t]*:", lines[i])
    ), len(lines))
    prefix = "".join(lines[:end])
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    indented = "".join("  " + line for line in fragment.splitlines(keepends=True))
    return prefix + indented + "".join(lines[end:])


def add_top(text: str, value: dict) -> str:
    if text.strip() and not text.endswith("\n"):
        text += "\n"
    return text + yaml.safe_dump(value, allow_unicode=True, sort_keys=False, width=120)


def render(existing: bytes | None, name: str, personality: dict) -> tuple[bytes | None, str]:
    raw = existing.decode("utf-8-sig") if existing is not None else ""
    cfg = load_yaml(raw)
    old = copy.deepcopy(cfg)
    agent = cfg.get("agent") or {}
    display = cfg.get("display") or {}
    if not isinstance(agent, dict) or not isinstance(display, dict):
        raise ValueError("agent and display must be mappings")
    presets = agent.get("personalities") or {}
    if not isinstance(presets, dict):
        raise ValueError("agent.personalities must be a mapping")

    had_presets_section = "personalities" in agent
    prior = presets.get(name)
    if prior is not None and prior != personality:
        return None, "preserved different locally customized preset"

    selected = display.get("personality")
    manual = bool(agent.get("system_prompt"))
    activate = "personality" not in display and not manual
    if prior == personality and not activate:
        return None, "already installed; existing selection preserved"
    cfg.setdefault("agent", {}).setdefault("personalities", {})[name] = personality
    if activate:
        cfg.setdefault("display", {})["personality"] = name

    # Keep a JSON source in JSON form; otherwise insert only missing YAML keys.
    if raw.lstrip().startswith("{"):
        candidate = json.dumps(cfg, indent=2, ensure_ascii=False) + "\n"
    else:
        candidate = raw
        if prior is None:
            if "agent" not in old:
                candidate = add_top(candidate, {"agent": {"personalities": {name: personality}}})
            elif not had_presets_section:
                candidate = add_nested(candidate, "agent", {"personalities": {name: personality}})
            else:
                raise ValueError("existing presets need reviewable manual merge")
        if activate:
            if "display" not in old:
                candidate = add_top(candidate, {"display": {"personality": name}})
            else:
                candidate = add_nested(candidate, "display", {"personality": name})

    if load_yaml(candidate) != cfg:
        raise ValueError("native config semantic readback mismatch")
    if candidate.encode("utf-8") == existing:
        return None, "already matching"
    action = "activate" if activate else "add preset; preserve prior selection"
    return candidate.encode("utf-8"), action


def atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
    fd, temp = tempfile.mkstemp(prefix=".personality-", dir=path.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def safe_current(path: Path) -> bytes | None:
    if path.is_symlink():
        raise ValueError("symlinked config rejected")
    if not path.exists():
        return None
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("non-regular config rejected")
    return path.read_bytes()


def plan(source: Path, installed: Path):
    roster = source_profiles(source)
    entries, skipped = [], []
    for name, rel in sorted(roster.items()):
        folder = installed / name
        if not folder.exists():
            continue
        if folder.is_symlink() or not folder.is_dir():
            raise ValueError(f"unsafe installed profile directory: {name}")
        file = folder / "config.yaml"
        old = safe_current(file)
        definition = load_json(source / "personalities" / (name + ".json"))
        native = load_yaml((source / rel / "config.yaml").read_text())
        if native.get("agent", {}).get("personalities", {}).get(name) != definition:
            raise ValueError(f"source/native personality mismatch: {name}")
        try:
            new, action = render(old, name, definition)
        except (ValueError, yaml.YAMLError, UnicodeDecodeError) as exc:
            raise ValueError(f"unsafe config for {name}: {exc}") from exc
        if new is None:
            skipped.append({"profile": name, "status": action})
            continue
        entries.append({
            "profile": name, "path": file, "old": old, "new": new,
            "sha_before": digest(old), "sha_after": digest(new),
            "mode": stat.S_IMODE(file.stat().st_mode) if old is not None else 0o600,
            "action": action,
        })
    return entries, skipped


def store_backup(entries, base: Path) -> Path:
    base.mkdir(mode=0o700, parents=True, exist_ok=True)
    if base.is_symlink():
        raise ValueError("backup directory must not be a symlink")
    os.chmod(base, 0o700)
    folder = base / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8])
    folder.mkdir(mode=0o700)
    rows = []
    for entry in entries:
        name = entry["profile"]
        if entry["old"] is not None:
            atomic_write(folder / (name + ".yaml"), entry["old"], 0o600)
        rows.append({
            "profile": name, "existed": entry["old"] is not None,
            "sha_before": entry["sha_before"], "sha_after": entry["sha_after"],
            "original_mode": entry["mode"],
        })
    atomic_write(folder / "manifest.json", (json.dumps({"entries": rows}, indent=2) + "\n").encode(), 0o600)
    return folder


def restore(installed: Path, backup: Path) -> list[str]:
    if backup.is_symlink() or not backup.is_dir():
        raise ValueError("unsafe backup folder")
    manifest = json.loads((backup / "manifest.json").read_text())
    rows = manifest["entries"]
    for row in rows:
        name = row["profile"]
        if not re.fullmatch(r"(agency|council|academy)-[a-z0-9-]+|hermes-wear", name):
            raise ValueError("unexpected rollback identity")
        cfg = installed / name / "config.yaml"
        if cfg.parent.is_symlink() or not cfg.parent.is_dir():
            raise ValueError(f"unsafe rollback destination: {name}")
        if digest(safe_current(cfg)) != row["sha_after"]:
            raise ValueError(f"rollback blocked: config changed after migration ({name})")
        if row["existed"] and digest((backup / (name + ".yaml")).read_bytes()) != row["sha_before"]:
            raise ValueError(f"rollback blocked: backup integrity mismatch ({name})")
    for row in rows:
        cfg = installed / row["profile"] / "config.yaml"
        if row["existed"]:
            atomic_write(cfg, (backup / (row["profile"] + ".yaml")).read_bytes(), row["original_mode"])
        else:
            cfg.unlink()
    return [row["profile"] for row in rows]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--installed", type=Path, default=Path.home() / ".hermes/profiles")
    parser.add_argument("--backup-root", type=Path, default=Path.home() / ".hermes/backups/profile-personalities")
    op = parser.add_mutually_exclusive_group()
    op.add_argument("--apply", action="store_true")
    op.add_argument("--rollback", type=str, metavar="BACKUP_ID")
    args = parser.parse_args()
    os.umask(0o077)
    source, installed = args.source.resolve(), args.installed
    if installed.is_symlink() or not installed.is_dir():
        parser.error("installed profiles path is absent or unsafe")
    if args.rollback:
        if not re.fullmatch(r"\d{8}T\d{6}Z-[0-9a-f]{8}", args.rollback):
            parser.error("invalid backup ID")
        restored = restore(installed, args.backup_root / args.rollback)
        print(json.dumps({"status": "restored", "count": len(restored), "profiles": restored}))
        return 0
    entries, skipped = plan(source, installed)
    report = {
        "status": "preview", "matched": len(entries) + len(skipped),
        "changes": [{"profile": x["profile"], "action": x["action"]} for x in entries],
        "skipped": skipped,
    }
    if not args.apply or not entries:
        print(json.dumps(report, indent=2))
        return 0
    for entry in entries:
        if digest(safe_current(entry["path"])) != entry["sha_before"]:
            raise ValueError(f"concurrent config edit: {entry['profile']}")
    backup = store_backup(entries, args.backup_root)
    applied = []
    try:
        for entry in entries:
            path = entry["path"]
            if digest(safe_current(path)) != entry["sha_before"]:
                raise ValueError(f"concurrent config edit: {entry['profile']}")
            atomic_write(path, entry["new"], entry["mode"])
            applied.append(entry)
            if digest(safe_current(path)) != entry["sha_after"]:
                raise ValueError(f"config write readback failed: {entry['profile']}")
    except Exception:
        # Roll back the portion already committed, without replacing concurrent edits.
        for entry in reversed(applied):
            if digest(safe_current(entry["path"])) == entry["sha_after"]:
                if entry["old"] is None:
                    entry["path"].unlink()
                else:
                    atomic_write(entry["path"], entry["old"], entry["mode"])
        raise
    report.update(status="applied", backup_id=backup.name, applied=len(applied))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Personality migration blocked: {exc}", file=sys.stderr)
        raise SystemExit(1)
