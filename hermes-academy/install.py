#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "academy.json"
REPO_ROOT = ROOT.parent
AGENCY_MANIFEST = REPO_ROOT / "hermes-agency" / "agency.json"


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


# ---------------------------------------------------------------------------
# Shared-skill materialization
# ---------------------------------------------------------------------------

def _resolve_shared_skill_targets(
    shared_skill: dict,
    academy_profiles: list[dict],
) -> list[str]:
    """Return the list of profile names that should receive this shared skill."""
    targets = shared_skill["targets"]
    mode = targets["mode"]
    exceptions = set(targets.get("exceptions", []))

    if mode == "agency-ce-participants":
        if not AGENCY_MANIFEST.is_file():
            raise FileNotFoundError(
                f"Agency manifest not found: {AGENCY_MANIFEST}. "
                "Shared skills targeting agency profiles require the agency pack."
            )
        agency = json.loads(AGENCY_MANIFEST.read_text(encoding="utf-8"))
        names = [p["name"] for p in agency.get("profiles", [])]
    elif mode == "academy-faculty-except-dean":
        names = [p["name"] for p in academy_profiles if p["name"] != "academy-dean"]
    else:
        raise ValueError(f"unknown shared-skill target mode: {mode}")

    return sorted(set(names) - exceptions)


def materialize_shared_skills(manifest: dict) -> int:
    """Copy canonical shared skills into target profiles.

    Returns the number of materialized copies written.
    """
    shared_skills = manifest.get("shared_skills", [])
    if not shared_skills:
        return 0

    academy_profiles = manifest.get("profiles", [])
    count = 0

    for shared_skill in shared_skills:
        name = shared_skill["name"]
        canonical = ROOT / shared_skill["canonical_source"]
        if not canonical.is_file():
            print(
                f"error: shared skill canonical source missing: {canonical}",
                file=sys.stderr,
            )
            return -1

        canonical_bytes = canonical.read_bytes()
        targets = _resolve_shared_skill_targets(shared_skill, academy_profiles)

        for profile_name in targets:
            # Determine which pack owns this profile
            if profile_name.startswith("agency-"):
                profile_dir = REPO_ROOT / "hermes-agency" / "profiles" / profile_name
            elif profile_name.startswith("academy-"):
                profile_dir = ROOT / "profiles" / profile_name
            else:
                print(
                    f"warning: skipping unknown profile namespace: {profile_name}",
                    file=sys.stderr,
                )
                continue

            if not profile_dir.is_dir():
                print(
                    f"warning: target profile directory missing: {profile_dir}",
                    file=sys.stderr,
                )
                continue

            skill_dir = profile_dir / "skills" / name
            skill_file = skill_dir / "SKILL.md"

            # Only write if the canonical bytes differ from what is on disk
            if skill_file.is_file() and skill_file.read_bytes() == canonical_bytes:
                continue

            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_file.write_bytes(canonical_bytes)
            count += 1

    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Install all or selected Hermes Academy profiles.")
    parser.add_argument("profiles", nargs="*", help="Profile names to install. Omit for the complete Academy.")
    parser.add_argument("--category")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--skip-shared-skills",
        action="store_true",
        help="Skip shared-skill materialization.",
    )
    args = parser.parse_args()
    manifest = load_manifest()
    profiles = manifest["profiles"]

    if args.list:
        print(f"Hermes Academy {manifest['version']} - {len(profiles)} profiles")
        for category in sorted({p['category'] for p in profiles}):
            print(f"\n{category}")
            for p in sorted((x for x in profiles if x['category'] == category), key=lambda x: x['name']):
                print(f"  {p['name']:<38} {p['display_name']}")
        shared = manifest.get("shared_skills", [])
        if shared:
            print(f"\nShared skills: {len(shared)}")
            for s in shared:
                print(f"  {s['name']:<38} targets={s['targets']['mode']}")
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

    # Materialize shared skills unless skipped
    if not args.skip_shared_skills:
        shared_count = materialize_shared_skills(manifest)
        if shared_count < 0:
            return 2
        if shared_count > 0:
            print(f"\nMaterialized {shared_count} shared-skill cop(ies).")

    print(f"\nInstalled {len(selected)} Hermes Academy profile(s).")
    print(f"Dean: {manifest['orchestrator']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
