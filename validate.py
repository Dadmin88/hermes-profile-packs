#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEXT_SUFFIXES = {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".toml", ".cfg", ".ini", ".sh"}
FORBIDDEN_NAMES = {"auth.json", "auth.lock", ".env", "state.db", "projects.db", "gateway.pid", "gateway.lock"}
PATTERNS = [
    ("personal home path", re.compile(r"/(?:home|media)/(?:kyle|dadmin)(?:/|$)", re.IGNORECASE)),
    ("private key", re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY")),
    ("GitHub token", re.compile(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}")),
    ("OpenAI-style secret", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
]


def main() -> int:
    errors: list[str] = []
    packs = json.loads((ROOT / "packs.json").read_text(encoding="utf-8"))["packs"]
    for pack in packs:
        pack_dir = ROOT / pack["path"]
        if not pack_dir.is_dir():
            errors.append(f"missing pack directory: {pack['path']}")
            continue
        namespace = pack["namespace"][:-1]
        manifest = ROOT / pack["manifest"]
        if not manifest.is_file():
            errors.append(f"missing pack manifest: {pack['manifest']}")
        profile_dir = pack_dir / "profiles"
        for child in profile_dir.iterdir():
            if child.is_dir() and not child.name.startswith(namespace):
                errors.append(f"wrong namespace in {pack['path']}: {child.name}")
        validator = pack_dir / "validate.py"
        if validator.is_file():
            result = subprocess.run([sys.executable, str(validator)], cwd=pack_dir)
            if result.returncode:
                errors.append(f"pack validator failed: {pack['name']}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.name in FORBIDDEN_NAMES:
            errors.append(f"runtime/private filename committed: {path.relative_to(ROOT)}")
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {".gitignore", ".no-bundled-skills"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for label, pattern in PATTERNS:
            if pattern.search(text):
                errors.append(f"{label} found in {path.relative_to(ROOT)}")

    if errors:
        print("\nRepository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
