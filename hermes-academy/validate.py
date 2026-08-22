#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "academy.json"
NAME_RE = re.compile(r"^academy-[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN = [re.compile(r"/(?:home|media)/(?:kyle|dadmin)(?:/|$)", re.I), re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY")]


def parse_distribution(path: Path) -> dict[str, str]:
    data = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if ":" in raw and not raw.lstrip().startswith("#"):
            key, value = raw.split(":", 1)
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def parse_skill(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    data = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def main() -> int:
    errors = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("profiles", [])
    names = [p.get("name") for p in entries]
    if manifest.get("profile_count") != len(entries): errors.append("profile_count mismatch")
    if sum(manifest.get("categories", {}).values()) != len(entries): errors.append("category counts mismatch")
    duplicates = [n for n, c in Counter(names).items() if c > 1]
    if duplicates: errors.append(f"duplicate profiles: {duplicates}")
    if manifest.get("orchestrator") not in names: errors.append("orchestrator not in roster")
    actual = {p.name for p in (ROOT / "profiles").iterdir() if p.is_dir()}
    if set(names) != actual: errors.append(f"profile directory mismatch: missing={sorted(set(names)-actual)} extra={sorted(actual-set(names))}")

    for item in entries:
        name = item["name"]
        if not NAME_RE.fullmatch(name): errors.append(f"invalid profile name: {name}")
        root = ROOT / "profiles" / name
        if not (root / ".no-bundled-skills").is_file(): errors.append(f"{name}: missing .no-bundled-skills")
        dist = root / "distribution.yaml"
        soul = root / "SOUL.md"
        if not dist.is_file(): errors.append(f"{name}: missing distribution.yaml"); continue
        if not soul.is_file(): errors.append(f"{name}: missing SOUL.md")
        meta = parse_distribution(dist)
        if meta.get("name") != name: errors.append(f"{name}: distribution name mismatch")
        for field in ("version", "description", "author", "license"):
            if not meta.get(field): errors.append(f"{name}: distribution missing {field}")
        skills = set()
        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            skill_name = skill.parent.name
            skills.add(skill_name)
            if not SKILL_RE.fullmatch(skill_name): errors.append(f"{name}: invalid skill {skill_name}")
            fm = parse_skill(skill)
            if fm.get("name") != skill_name: errors.append(f"{name}/{skill_name}: frontmatter name mismatch")
            if not fm.get("description"): errors.append(f"{name}/{skill_name}: missing description")
        if set(item.get("jobs", [])) != skills: errors.append(f"{name}: jobs do not match skills")

    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc": continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".py", ".txt"} and path.name != ".no-bundled-skills": continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN:
            if pattern.search(text): errors.append(f"forbidden portable-content pattern in {path.relative_to(ROOT)}")

    if errors:
        for error in errors: print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Hermes Academy validation passed: {len(entries)} profiles, {sum(len(p['jobs']) for p in entries)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
