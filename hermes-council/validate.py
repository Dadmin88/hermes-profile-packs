#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "council.json"
NAME_RE = re.compile(r"^council-[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN = [
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password)\s*[:=]\s*[\"'][^\"']{8,}"),
]


def parse_distribution(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if ":" not in raw or raw.lstrip().startswith("#"):
            continue
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


def parse_skill_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()
    return data


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("profiles", [])
    names = [item.get("name") for item in entries]

    if manifest.get("profile_count") != len(entries):
        errors.append("manifest profile_count does not match profiles list")
    duplicates = [name for name, count in Counter(names).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate manifest profiles: {duplicates}")
    if manifest.get("orchestrator") not in names:
        errors.append("manifest orchestrator is not installed in roster")

    expected = set(names)
    actual = {p.name for p in (ROOT / "profiles").iterdir() if p.is_dir()}
    if expected != actual:
        errors.append(f"profile directory mismatch: missing={sorted(expected-actual)} extra={sorted(actual-expected)}")

    for item in entries:
        name = item["name"]
        if not NAME_RE.fullmatch(name):
            errors.append(f"invalid Council profile name: {name}")
            continue
        root = ROOT / "profiles" / name
        dist = root / "distribution.yaml"
        soul = root / "SOUL.md"
        if not dist.is_file():
            errors.append(f"{name}: missing distribution.yaml")
            continue
        if not soul.is_file():
            errors.append(f"{name}: missing SOUL.md")
        meta = parse_distribution(dist)
        if meta.get("name") != name:
            errors.append(f"{name}: distribution name mismatch")
        for field in ("version", "description", "author", "license"):
            if not meta.get(field):
                errors.append(f"{name}: distribution missing {field}")

        skill_root = root / "skills"
        skill_names: set[str] = set()
        for skill in sorted(skill_root.glob("*/SKILL.md")):
            skill_name = skill.parent.name
            skill_names.add(skill_name)
            if not SKILL_RE.fullmatch(skill_name):
                errors.append(f"{name}: invalid skill name {skill_name}")
            frontmatter = parse_skill_frontmatter(skill)
            if frontmatter.get("name") != skill_name:
                errors.append(f"{name}/{skill_name}: skill frontmatter name mismatch")
            if not frontmatter.get("description"):
                errors.append(f"{name}/{skill_name}: skill frontmatter missing description")
        if not skill_names:
            errors.append(f"{name}: no profile-specific skills")
        jobs = set(item.get("jobs", []))
        if jobs != skill_names:
            errors.append(f"{name}: jobs do not match skills: jobs={sorted(jobs)} skills={sorted(skill_names)}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN:
            if pattern.search(text):
                errors.append(f"forbidden portable-content pattern in {path.relative_to(ROOT)}: {pattern.pattern}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Hermes Council validation passed: {len(entries)} profiles, {sum(len(p['jobs']) for p in entries)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
