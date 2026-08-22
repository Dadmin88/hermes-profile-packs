#!/usr/bin/env python3
"""Install Hermes Agency profiles into Hermes Agent."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "agency.json"


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True)


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def profile_source(name: str) -> Path:
    return ROOT / "profiles" / name


def distribution_description(source: Path) -> str:
    manifest = source / "distribution.yaml"
    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("description:"):
            continue
        value = line.split(":", 1)[1].strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        return value.replace(r'\"', '"')
    raise ValueError(f"distribution is missing a description: {manifest}")


def print_roster(profiles: list[dict]) -> None:
    categories: dict[str, list[dict]] = {}
    for profile in profiles:
        categories.setdefault(profile["category"], []).append(profile)

    for category in sorted(categories):
        print(f"\n{category}")
        for profile in sorted(categories[category], key=lambda item: item["name"]):
            print(f"  {profile['name']:<34} {profile['display_name']}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install all or selected Hermes Agency profiles."
    )
    parser.add_argument(
        "profiles",
        nargs="*",
        help="Profile names to install. Omit to install the complete Agency.",
    )
    parser.add_argument(
        "--category",
        help="Install every profile in one category, such as engineering or design.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available profiles and exit.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-apply distributions over existing profiles.",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    all_profiles = manifest["profiles"]

    if args.list:
        print(f"Hermes Agency {manifest['version']} - {len(all_profiles)} profiles")
        print_roster(all_profiles)
        return 0

    if args.profiles and args.category:
        parser.error("choose explicit profiles or --category, not both")

    catalog = {item["name"]: item for item in all_profiles}

    if args.category:
        requested_items = [
            item for item in all_profiles if item["category"] == args.category
        ]
        if not requested_items:
            categories = ", ".join(sorted({item["category"] for item in all_profiles}))
            parser.error(
                f"unknown category '{args.category}'. Available categories: {categories}"
            )
    elif args.profiles:
        unknown = sorted(set(args.profiles) - set(catalog))
        if unknown:
            parser.error("unknown profile(s): " + ", ".join(unknown))
        requested_items = [catalog[name] for name in args.profiles]
    else:
        requested_items = all_profiles

    hermes = shutil.which("hermes")
    if not hermes:
        print("error: 'hermes' was not found on PATH", file=sys.stderr)
        return 2

    for item in requested_items:
        name = item["name"]
        source = profile_source(name)
        distribution = source / "distribution.yaml"

        if not distribution.is_file():
            print(f"error: invalid profile distribution: {source}", file=sys.stderr)
            return 2

        command = [
            hermes,
            "profile",
            "install",
            str(source),
            "--alias",
            "--yes",
        ]
        if args.force:
            command.append("--force")

        print(f"\n==> Installing {name}")
        run(command)
        run(
            [
                hermes,
                "profile",
                "describe",
                name,
                "--text",
                distribution_description(source),
            ]
        )

    print(f"\nInstalled {len(requested_items)} Hermes Agency profile(s).")
    print(f"Orchestrator: {manifest['orchestrator']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
