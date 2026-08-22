#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "academy.json"


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def description(source: Path) -> str:
    for raw in (source / "distribution.yaml").read_text(encoding="utf-8").splitlines():
        if raw.strip().startswith("description:"):
            value = raw.split(":", 1)[1].strip().strip('"').strip("'")
            return value
    raise ValueError(f"missing distribution description: {source}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Install all or selected Hermes Academy profiles.")
    parser.add_argument("profiles", nargs="*", help="Profile names to install. Omit for the complete Academy.")
    parser.add_argument("--category")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    manifest = load_manifest()
    profiles = manifest["profiles"]

    if args.list:
        print(f"Hermes Academy {manifest['version']} - {len(profiles)} profiles")
        for category in sorted({p['category'] for p in profiles}):
            print(f"\n{category}")
            for p in sorted((x for x in profiles if x['category'] == category), key=lambda x: x['name']):
                print(f"  {p['name']:<38} {p['display_name']}")
        return 0

    if args.profiles and args.category:
        parser.error("choose explicit profiles or --category, not both")
    catalog = {p['name']: p for p in profiles}
    if args.category:
        selected = [p for p in profiles if p['category'] == args.category]
        if not selected:
            parser.error(f"unknown category: {args.category}")
    elif args.profiles:
        unknown = sorted(set(args.profiles) - set(catalog))
        if unknown:
            parser.error("unknown profile(s): " + ", ".join(unknown))
        selected = [catalog[name] for name in args.profiles]
    else:
        selected = profiles

    hermes = shutil.which("hermes")
    if not hermes:
        print("error: 'hermes' was not found on PATH", file=sys.stderr)
        return 2

    for item in selected:
        name = item['name']
        source = ROOT / "profiles" / name
        command = [hermes, "profile", "install", str(source), "--alias", "--yes"]
        if args.force:
            command.append("--force")
        print(f"\n==> Installing {name}")
        run(command)
        run([hermes, "profile", "describe", name, "--text", description(source)])

    print(f"\nInstalled {len(selected)} Hermes Academy profile(s).")
    print(f"Dean: {manifest['orchestrator']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
