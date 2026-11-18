#!/usr/bin/env python3
"""Review and selectively sync SOUL/skill source without native destructive update.

Read-only by default. Source must be a local Profile Packs checkout, and
installed distribution metadata must point to that exact source. This is a
scoped content sync, NOT an all-purpose replacement for Hermes profile update:
distribution versions/configuration, jobs, deletions and user-added skills
are intentionally untouched.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
from uuid import uuid4

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INSTALLED = Path.home() / ".hermes/profiles"
DEFAULT_BACKUPS = Path.home() / ".hermes/backups/reviewed-profile-sync"
BACKUP_ID = re.compile(r"^\d{8}T\d{6}Z-[0-9a-f]{8}$")


def sha(data: bytes | None) -> str | None:
    return hashlib.sha256(data).hexdigest() if data is not None else None


def safe_parts(relative: str) -> tuple[str, ...]:
    path = PurePosixPath(relative)
    parts = path.parts
    if not parts or path.is_absolute() or any(p in (".", "..") for p in parts):
        raise ValueError("invalid relative source path")
    if relative != "/".join(parts):
        raise ValueError("non-canonical relative source path")
    if relative != "SOUL.md" and (len(parts) < 3 or parts[0] != "skills"):
        raise ValueError("only SOUL.md and named skill files may be synced")
    return parts


def no_symlink_path(root: Path, relative: str) -> Path:
    parts = safe_parts(relative)
    p = root
    if root.is_symlink() or not root.is_dir():
        raise ValueError("unsafe profile root")
    for component in parts:
        p = p / component
        if p.is_symlink():
            raise ValueError(f"symlinked profile path blocked: {relative}")
    return p


def read_optional_file(path: Path) -> bytes | None:
    if path.is_symlink():
        raise ValueError(f"symlinked file blocked: {path.name}")
    if not path.exists():
        return None
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"non-regular file blocked: {path.name}")
    return path.read_bytes()


def catalog(source: Path) -> dict[str, Path]:
    data = json.loads((source / "capabilities/profiles.json").read_text(encoding="utf-8"))
    result = {}
    for row in data["profiles"]:
        name, rel = row["profile"], row["path"]
        if not re.fullmatch(r"(agency|academy|council)-[a-z0-9-]+|hermes-wear", name):
            raise ValueError(f"invalid catalog identity: {name}")
        relpath = PurePosixPath(rel)
        parts = relpath.parts
        if (not parts or relpath.is_absolute() or ".." in parts
                or rel != "/".join(parts)):
            raise ValueError(f"unsafe source catalog path: {name}")
        src = source
        for part in parts:
            src = src / part
            if src.is_symlink():
                raise ValueError(f"symlinked source catalog path: {name}")
        if not src.is_dir() or not src.resolve().is_relative_to(source.resolve()):
            raise ValueError(f"unsafe source distribution: {name}")
        if name in result:
            raise ValueError(f"duplicate source identity: {name}")
        result[name] = src
    return result


def matches_source(installed_dir: Path, source_dir: Path, name: str) -> bool:
    if installed_dir.is_symlink() or not installed_dir.is_dir():
        return False
    manifest = installed_dir / "distribution.yaml"
    raw = read_optional_file(manifest)
    if raw is None:
        return False
    loaded = yaml.safe_load(raw.decode("utf-8-sig")) or {}
    if not isinstance(loaded, dict) or loaded.get("name") != name:
        raise ValueError(f"installed manifest identity mismatch: {name}")
    return loaded.get("source") == str(source_dir)


def source_units(source_dir: Path) -> dict[str, Path]:
    result = {}
    soul = source_dir / "SOUL.md"
    if not soul.is_file() or soul.is_symlink():
        raise ValueError("source SOUL.md missing or symlinked")
    result["SOUL.md"] = soul
    skills = source_dir / "skills"
    if skills.exists():
        if skills.is_symlink() or not skills.is_dir():
            raise ValueError("unsafe source skills directory")
        for entry in sorted(skills.rglob("*")):
            if entry.is_symlink():
                raise ValueError("source skill tree contains a symlink")
            if entry.name != "SKILL.md" or not entry.is_file():
                continue
            unit = entry.parent.relative_to(source_dir).as_posix()
            if unit in result:
                raise ValueError("duplicate skill unit")
            result[unit] = entry.parent
    return result


def unit_files(source_dir: Path, unit: str, path: Path) -> list[tuple[str, bytes, int]]:
    files = [path] if unit == "SOUL.md" else sorted(p for p in path.rglob("*") if p.is_file())
    if not files:
        raise ValueError(f"empty source unit: {unit}")
    result = []
    for file in files:
        if file.is_symlink():
            raise ValueError(f"symlink in source unit: {unit}")
        relative = file.relative_to(source_dir).as_posix()
        safe_parts(relative)
        mode = stat.S_IMODE(file.stat().st_mode)
        if not stat.S_ISREG(file.stat().st_mode):
            raise ValueError(f"non-file source unit: {relative}")
        result.append((relative, file.read_bytes(), 0o700 if (mode & 0o111) else 0o600))
    return result


def build(source: Path, installed: Path, profile: str | None, requested: list[str]):
    roster = catalog(source)
    names = [profile] if profile else sorted(roster)
    if profile and profile not in roster:
        raise ValueError(f"profile not in source catalog: {profile}")
    if requested and not profile:
        raise ValueError("--unit requires --profile")
    if requested and len(requested) != len(set(requested)):
        raise ValueError("duplicate --unit selection")
    units_out = []
    skip = Counter()
    for name in names:
        source_dir = roster[name]
        target_dir = installed / name
        if not matches_source(target_dir, source_dir, name):
            if profile:
                raise ValueError(f"installed distribution missing or source differs: {name}")
            skip["not_installed_or_unmatched"] += 1
            continue
        candidates = source_units(source_dir)
        selections = sorted(requested) if requested else sorted(candidates)
        for unit in selections:
            if unit not in candidates:
                raise ValueError(f"unknown source unit for {name}: {unit}")
            files = []
            for rel, fresh, mode in unit_files(source_dir, unit, candidates[unit]):
                target = no_symlink_path(target_dir, rel)
                previous = read_optional_file(target)
                state = "add" if previous is None else "same" if previous == fresh else "replace"
                files.append({
                    "relative": rel, "before": previous, "after": fresh,
                    "mode": stat.S_IMODE(target.stat().st_mode) if previous is not None else mode,
                    "old_sha": sha(previous), "new_sha": sha(fresh), "state": state,
                    "path": target,
                })
            units_out.append({
                "profile": name, "unit": unit, "files": files,
                "source_manifest_sha": sha((source_dir / "distribution.yaml").read_bytes()),
                "installed_manifest_sha": sha((target_dir / "distribution.yaml").read_bytes())
            })
    return units_out, skip


def fingerprint(units) -> str:
    public = [{
        "profile": u["profile"], "unit": u["unit"],
        "source_manifest": u["source_manifest_sha"],
        "installed_manifest": u["installed_manifest_sha"],
        "files": [{"path": f["relative"], "old": f["old_sha"], "new": f["new_sha"]}
                  for f in u["files"]]
    } for u in units]
    return sha(json.dumps(public, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def summary(units, skip, selected):
    counts = Counter(f["state"] for unit in units for f in unit["files"])
    per_unit = []
    for unit in units:
        count = Counter(f["state"] for f in unit["files"])
        if selected or count["replace"] or count["add"]:
            per_unit.append({
                "profile": unit["profile"], "unit": unit["unit"],
                "replace": count["replace"], "add": count["add"], "same": count["same"]
            })
    return {
        "mode": "preview", "matched_profiles": len({u["profile"] for u in units}),
        "units_seen": len(units), "files": dict(counts),
        "skipped_profiles": dict(skip), "units": per_unit[:25],
        "units_truncated": len(per_unit) > 25,
        "plan_sha256": fingerprint(units) if selected else None,
    }


def print_diff(units, max_lines=220):
    shown = 0
    for unit in units:
        for file in unit["files"]:
            if file["state"] == "same":
                continue
            try:
                before = (file["before"] or b"").decode("utf-8").splitlines(keepends=True)
                after = file["after"].decode("utf-8").splitlines(keepends=True)
            except UnicodeDecodeError:
                print("BINARY DIFFERENCE: " + unit["profile"] + "/" + file["relative"])
                continue
            for line in difflib.unified_diff(before, after,
                    fromfile="installed/" + unit["profile"] + "/" + file["relative"],
                    tofile="source/" + unit["profile"] + "/" + file["relative"]):
                if shown >= max_lines:
                    print("[diff truncated; select a smaller unit]")
                    return
                print(line, end="")
                shown += 1


def atomic_write(path: Path, content: bytes, mode: int):
    fd, temporary = tempfile.mkstemp(prefix=".reviewed-sync-", dir=path.parent)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def backup_folder(root: Path) -> Path:
    if root.is_symlink():
        raise ValueError("symlinked backup directory")
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    dest = root / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8])
    dest.mkdir(mode=0o700)
    return dest


def apply(units, source: Path, installed: Path, backups: Path, approved: str):
    if not units or approved != fingerprint(units):
        raise ValueError("approved plan hash does not match exact current source/installed bytes")
    modifications = [(u, f) for u in units for f in u["files"] if f["state"] != "same"]
    if not modifications:
        return {"status": "already_current", "changed": 0}
    if len(modifications) > 500:
        raise ValueError("batch exceeds 500 files; use smaller units")

    # Re-read every source and installed target before creating any backup.
    rebuilt, skipped = build(source=source,
                            installed=installed, profile=units[0]["profile"],
                            requested=[u["unit"] for u in units])
    if skipped or fingerprint(rebuilt) != approved:
        raise ValueError("source or installed files changed since approval")

    folder = backup_folder(backups)
    manifest = []
    for i, (unit, file) in enumerate(modifications):
        name = f"{i:04d}.bak"
        if file["before"] is not None:
            atomic_write(folder / name, file["before"], 0o600)
        manifest.append({
            "profile": unit["profile"], "relative": file["relative"],
            "existed": file["before"] is not None, "backup": name if file["before"] is not None else None,
            "before": file["old_sha"], "after": file["new_sha"], "mode": file["mode"]
        })
    atomic_write(folder / "manifest.json",
                 (json.dumps({"version": 1, "files": manifest}, indent=2) + "\n").encode(), 0o600)
    written = []
    try:
        for unit, file in modifications:
            path = file["path"]
            # Fail rather than follow existing symlinked parents.
            checked = no_symlink_path(installed / unit["profile"], file["relative"])
            if checked != path or sha(read_optional_file(checked)) != file["old_sha"]:
                raise ValueError(f"concurrent change at {unit['profile']}/{file['relative']}")
            checked.parent.mkdir(parents=True, exist_ok=True)
            atomic_write(checked, file["after"], file["mode"])
            written.append(file)
            if sha(read_optional_file(checked)) != file["new_sha"]:
                raise ValueError("readback mismatch")
    except Exception:
        for file in reversed(written):
            if sha(read_optional_file(file["path"])) == file["new_sha"]:
                if file["before"] is None:
                    file["path"].unlink()
                else:
                    atomic_write(file["path"], file["before"], file["mode"])
        raise
    return {"status": "applied", "changed": len(modifications), "backup_id": folder.name}


def rollback(installed: Path, backups: Path, id: str):
    if not BACKUP_ID.fullmatch(id):
        raise ValueError("invalid backup identifier")
    if backups.is_symlink():
        raise ValueError("symlinked backup root")
    folder = backups / id
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError("backup not found")
    record = json.loads((folder / "manifest.json").read_text())
    if record.get("version") != 1 or not isinstance(record.get("files"), list):
        raise ValueError("unsupported backup manifest")
    if len(record["files"]) > 500:
        raise ValueError("oversized backup manifest")
    changes = []
    seen = set()
    for file in record["files"]:
        profile, rel = file["profile"], file["relative"]
        if not re.fullmatch(r"(agency|academy|council)-[a-z0-9-]+|hermes-wear", profile):
            raise ValueError("unsafe rollback profile")
        target = no_symlink_path(installed / profile, rel)
        if (profile, rel) in seen:
            raise ValueError("duplicate backup file")
        seen.add((profile, rel))
        if sha(read_optional_file(target)) != file["after"]:
            raise ValueError("rollback blocked: destination changed after sync")
        original = None
        if file["existed"]:
            if not re.fullmatch(r"[0-9]{4}\.bak", file["backup"] or ""):
                raise ValueError("invalid backup filename")
            saved = folder / file["backup"]
            original = read_optional_file(saved)
            if original is None or sha(original) != file["before"]:
                raise ValueError("rollback blocked: backup mismatch")
        changes.append((target, original, file["mode"]))
    for target, original, mode in changes:
        if original is None:
            target.unlink()
        else:
            atomic_write(target, original, mode)
    return {"status": "restored", "files": len(changes)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=ROOT)
    parser.add_argument("--installed", type=Path, default=DEFAULT_INSTALLED)
    parser.add_argument("--backup-root", type=Path, default=DEFAULT_BACKUPS)
    parser.add_argument("--profile", help="exact installed catalog profile")
    parser.add_argument("--unit", action="append", default=[], help="SOUL.md or skills/<skill>")
    parser.add_argument("--diff", action="store_true", help="bounded, selected text diffs")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--rollback", metavar="BACKUP_ID")
    parser.add_argument("--approve-plan", help="exact SHA-256 from scoped preview")
    args = parser.parse_args()
    os.umask(0o077)
    source = args.source.resolve()
    installed = args.installed.expanduser()
    backup_root = args.backup_root.expanduser()
    if installed.is_symlink() or not installed.is_dir():
        parser.error("unsafe/missing installed profile root")
    if args.rollback:
        if args.profile or args.unit or args.apply or args.approve_plan or args.diff:
            parser.error("--rollback cannot be combined with other operations")
        result = rollback(installed, backup_root, args.rollback)
    else:
        units, skipped = build(source, installed, args.profile, args.unit)
        selected = bool(args.profile and args.unit)
        result = summary(units, skipped, selected)
        if args.diff and not selected:
            parser.error("--diff requires exact --profile and --unit")
        if args.apply:
            if not selected or not args.approve_plan:
                parser.error("--apply requires --profile, --unit and --approve-plan")
            if not re.fullmatch(r"[a-f0-9]{64}", args.approve_plan):
                parser.error("invalid plan hash")
            # Source is passed explicitly; never infer from an installed path.
            result = apply(units, source, installed, backup_root, args.approve_plan)
        elif args.approve_plan:
            parser.error("--approve-plan is only used with --apply")
        if args.diff:
            print_diff(units)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, yaml.YAMLError) as exc:
        print(f"Profile sync blocked: {exc}", file=sys.stderr)
        raise SystemExit(1)
