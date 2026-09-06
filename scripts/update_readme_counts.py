#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

START_MARKER = "<!-- profile-counts:start -->"
END_MARKER = "<!-- profile-counts:end -->"
TOTAL_PATTERN = re.compile(r"You rarely need all \d+ profiles\.")


@dataclass(frozen=True)
class PackCounts:
    profiles: int
    skills: int


def plural(count: int, singular: str, plural_form: str | None = None) -> str:
    noun = singular if count == 1 else (plural_form or f"{singular}s")
    return f"{count} {noun}"


def load_counts(root: Path) -> dict[str, PackCounts]:
    registry = json.loads((root / "packs.json").read_text(encoding="utf-8"))
    counts: dict[str, PackCounts] = {}
    for pack in registry["packs"]:
        pack_dir = root / pack["path"]
        key = pack_dir.name.removeprefix("hermes-")
        manifest = json.loads((root / pack["manifest"]).read_text(encoding="utf-8"))
        profiles = manifest.get("profiles", [])
        profile_count = len(profiles)
        skill_count = sum(len(profile.get("jobs", [])) for profile in profiles)
        counts[key] = PackCounts(profile_count, skill_count)
    return counts


def generated_summary(counts: dict[str, PackCounts]) -> str:
    agency = counts["agency"]
    council = counts["council"]
    academy = counts["academy"]
    return "\n".join(
        [
            START_MARKER,
            f"Hermes Agency contains {plural(agency.profiles, 'professional specialist')}. "
            f"Hermes Council contains {plural(council.profiles, 'focused profile')} and "
            f"{plural(council.skills, 'purpose-built personal-life skill')}. "
            f"Hermes Academy contains {plural(academy.profiles, 'faculty profile')} and "
            f"{plural(academy.skills, 'purpose-built teaching skill')}.",
            END_MARKER,
        ]
    )


def update_readme(root: Path, check: bool = False) -> bool:
    readme_path = root / "README.md"
    original = readme_path.read_text(encoding="utf-8")
    if original.count(START_MARKER) != 1 or original.count(END_MARKER) != 1:
        raise ValueError("README.md must contain exactly one profile-count marker pair")

    start = original.index(START_MARKER)
    end = original.index(END_MARKER, start) + len(END_MARKER)
    counts = load_counts(root)
    updated = original[:start] + generated_summary(counts) + original[end:]

    total = sum(pack.profiles for pack in counts.values())
    updated, replacements = TOTAL_PATTERN.subn(
        f"You rarely need all {total} profiles.", updated, count=1
    )
    if replacements != 1:
        raise ValueError("README.md must contain one 'You rarely need all N profiles.' sentence")

    if updated == original:
        return False
    if check:
        return True
    readme_path.write_text(updated, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update generated profile and skill counts in README.md."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (defaults to this script's parent repository).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with status 1 instead of writing when README.md is stale.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        changed = update_readme(args.root.resolve(), check=args.check)
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"README count update failed: {exc}", file=sys.stderr)
        return 2

    if args.check and changed:
        print(
            "README profile counts are stale. Run: python scripts/update_readme_counts.py",
            file=sys.stderr,
        )
        return 1
    if changed:
        print("Updated README profile counts.")
    else:
        print("README profile counts are current.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
