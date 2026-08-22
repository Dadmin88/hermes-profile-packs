#!/usr/bin/env python3
"""Validate the static integrity and scope boundaries of Hermes Agency."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PROFILE_RE = re.compile(r"^agency-[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EVAL_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REVISION_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED_DISTRIBUTION_FIELDS = ("name", "version", "description", "author", "license")
SOURCE_FIELDS = ("Canonical source", "Reviewed revision", "Review date", "Upstream author", "License")
ROUTING_ACTIONS = {
    "resolve-profile-presence",
    "route-same-profile-to-ready-node",
    "place-same-profile-then-route",
    "reselect-node-without-changing-profile",
    "decompose-and-resolve-profile-presence",
    "report-missing-specialization",
}
FORBIDDEN_LEGACY_ROOTS = {
    "default_staff",
    "deploy",
    "docker",
    "hermes-agency",
    "packages",
    "src",
    "web",
}


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return {}
    except json.JSONDecodeError as exc:
        errors.append(f"invalid JSON in {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"expected JSON object in {path}")
        return {}
    return value


def scalar_fields(path: Path, errors: list[str]) -> dict[str, str]:
    """Read the simple top-level scalar YAML used by distribution.yaml."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return {}

    result: dict[str, str] = {}
    for line in lines:
        if not line or line[0].isspace() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        result[key] = value
    return result


def frontmatter_name(path: Path, errors: list[str]) -> str | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        errors.append(f"missing required file: {path}")
        return None

    if not lines or lines[0].strip() != "---":
        errors.append(f"missing YAML frontmatter in {path}")
        return None

    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        errors.append(f"unterminated YAML frontmatter in {path}")
        return None

    for line in lines[1:end]:
        if line.startswith("name:"):
            value = line.split(":", 1)[1].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            return value

    errors.append(f"frontmatter is missing name in {path}")
    return None


def source_fields(path: Path, errors: list[str]) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return

    values: dict[str, str] = {}
    for field in SOURCE_FIELDS:
        match = re.search(rf"(?mi)^\s*-?\s*{re.escape(field)}:\s*`?([^`\n]+?)`?\s*$", text)
        if not match:
            errors.append(f"SOURCE.md is missing '{field}' in {path}")
            continue
        values[field] = match.group(1).strip()

    revision = values.get("Reviewed revision")
    if revision and not REVISION_RE.fullmatch(revision):
        errors.append(f"invalid reviewed revision in {path}: {revision}")

    review_date = values.get("Review date")
    if review_date and not DATE_RE.fullmatch(review_date):
        errors.append(f"invalid review date in {path}: {review_date}")


def validate_routing_evals(root: Path, roster_set: set[str], errors: list[str]) -> int:
    eval_path = root / "evals" / "routing.json"
    data = load_json(eval_path, errors)
    if not data:
        return 0

    if data.get("schema_version") != 1:
        errors.append(
            f"unsupported routing eval schema_version={data.get('schema_version')!r} in {eval_path}"
        )

    cases = data.get("cases", [])
    if not isinstance(cases, list) or not cases:
        errors.append(f"routing evals must contain a non-empty cases list: {eval_path}")
        return 0

    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        label = f"routing eval case #{index + 1}"
        if not isinstance(case, dict):
            errors.append(f"{label} is not an object")
            continue

        case_id = case.get("id")
        if not isinstance(case_id, str) or not EVAL_ID_RE.fullmatch(case_id):
            errors.append(f"{label} has invalid id: {case_id!r}")
        elif case_id in seen_ids:
            errors.append(f"duplicate routing eval id: {case_id}")
        else:
            seen_ids.add(case_id)

        task = case.get("task")
        if not isinstance(task, str) or not task.strip():
            errors.append(f"{label} has an empty task")

        expected_profile = case.get("expected_profile")
        if expected_profile is not None and (
            not isinstance(expected_profile, str) or expected_profile not in roster_set
        ):
            errors.append(f"{label} references unknown expected_profile: {expected_profile!r}")

        action = case.get("expected_runtime_action")
        if action not in ROUTING_ACTIONS:
            errors.append(f"{label} has invalid expected_runtime_action: {action!r}")
            continue

        if action == "report-missing-specialization":
            if expected_profile is not None:
                errors.append(
                    f"{label} reports missing specialization but expected_profile is not null"
                )
        elif expected_profile is None:
            errors.append(
                f"{label} expects runtime action {action!r} but has no expected_profile"
            )

    return len(cases)


def validate(root: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    agency = load_json(root / "agency.json", errors)
    profiles_root = root / "profiles"

    for legacy_root in sorted(FORBIDDEN_LEGACY_ROOTS):
        if (root / legacy_root).exists():
            errors.append(f"legacy/out-of-scope repository root is forbidden: {legacy_root}")

    roster = agency.get("profiles", [])
    if not isinstance(roster, list):
        errors.append("agency.json profiles must be a list")
        roster = []

    roster_names: list[str] = []
    roster_categories: list[str] = []
    roster_by_name: dict[str, dict] = {}
    for index, item in enumerate(roster):
        if not isinstance(item, dict):
            errors.append(f"agency.json profile #{index + 1} is not an object")
            continue
        name = item.get("name")
        category = item.get("category")
        display_name = item.get("display_name")
        if not isinstance(name, str) or not PROFILE_RE.fullmatch(name):
            errors.append(f"invalid profile name in agency.json: {name!r}")
            continue
        if not isinstance(display_name, str) or not display_name.strip():
            errors.append(f"missing display_name for {name}")
        if not isinstance(category, str) or not category:
            errors.append(f"missing category for {name}")
            category = ""
        roster_names.append(name)
        roster_categories.append(category)
        roster_by_name[name] = item

    if len(roster_names) != len(set(roster_names)):
        errors.append("agency.json contains duplicate profile names")

    if agency.get("profile_count") != len(roster_names):
        errors.append(
            f"agency.json profile_count={agency.get('profile_count')!r}, actual roster={len(roster_names)}"
        )

    actual_categories = dict(Counter(roster_categories))
    if agency.get("categories") != actual_categories:
        errors.append(
            f"agency.json categories do not match roster: declared={agency.get('categories')!r}, actual={actual_categories!r}"
        )

    roster_set = set(roster_names)
    backbone = agency.get("backbone_profiles", [])
    if not isinstance(backbone, list) or not all(isinstance(name, str) for name in backbone):
        errors.append("agency.json backbone_profiles must be a string array")
        backbone = []
    if len(backbone) != len(set(backbone)):
        errors.append("agency.json backbone_profiles contains duplicates")
    unknown_backbone = sorted(set(backbone) - roster_set)
    if unknown_backbone:
        errors.append(
            "agency.json backbone_profiles contains unknown profiles: "
            + ", ".join(unknown_backbone)
        )

    filesystem_profiles = (
        {path.name for path in profiles_root.iterdir() if path.is_dir()}
        if profiles_root.is_dir()
        else set()
    )
    if filesystem_profiles != roster_set:
        missing = sorted(roster_set - filesystem_profiles)
        extra = sorted(filesystem_profiles - roster_set)
        if missing:
            errors.append(f"profile directories missing from filesystem: {', '.join(missing)}")
        if extra:
            errors.append(f"profile directories missing from agency.json: {', '.join(extra)}")

    actual_skill_count = 0
    sourced_skill_count = 0
    for name in roster_names:
        profile_dir = profiles_root / name
        distribution = scalar_fields(profile_dir / "distribution.yaml", errors)
        for field in REQUIRED_DISTRIBUTION_FIELDS:
            if not distribution.get(field):
                errors.append(f"{name} distribution.yaml is missing {field}")
        if distribution.get("name") and distribution["name"] != name:
            errors.append(f"{name} distribution identity mismatch: {distribution['name']!r}")
        if distribution.get("version") and distribution["version"] != agency.get("version"):
            errors.append(
                f"{name} distribution version mismatch: {distribution['version']!r} != {agency.get('version')!r}"
            )

        soul_path = profile_dir / "SOUL.md"
        try:
            soul_text = soul_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            errors.append(f"missing required file: {soul_path}")
            soul_text = ""
        if soul_path.exists() and not soul_text:
            errors.append(f"empty SOUL.md: {soul_path}")

        skills_dir = profile_dir / "skills"
        actual_skills: list[str] = []
        if not skills_dir.is_dir():
            errors.append(f"missing skills directory: {skills_dir}")
        else:
            for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
                skill_name = skill_dir.name
                if not SKILL_RE.fullmatch(skill_name):
                    errors.append(f"invalid skill directory name: {skill_dir}")
                skill_file = skill_dir / "SKILL.md"
                if not skill_file.is_file():
                    errors.append(f"missing SKILL.md: {skill_dir}")
                    continue
                declared_name = frontmatter_name(skill_file, errors)
                if declared_name and declared_name != skill_name:
                    errors.append(
                        f"skill identity mismatch in {skill_file}: frontmatter={declared_name!r}, directory={skill_name!r}"
                    )
                source_file = skill_dir / "SOURCE.md"
                if source_file.exists():
                    sourced_skill_count += 1
                    source_fields(source_file, errors)
                actual_skills.append(skill_name)

        if not actual_skills:
            errors.append(f"profile has no bundled skills: {name}")
        if len(actual_skills) != len(set(actual_skills)):
            errors.append(f"profile contains duplicate skill identities: {name}")
        actual_skill_count += len(actual_skills)

    expected_distribution = {
        "format": "hermes-profile-distribution",
        "profile_identity_field": "name",
        "profile_root": "profiles",
        "profile_path_template": "profiles/{name}",
    }
    if agency.get("distribution") != expected_distribution:
        errors.append(
            f"agency.json distribution contract mismatch: {agency.get('distribution')!r}"
        )

    if agency.get("schema_version") != 2:
        errors.append(
            f"agency.json schema_version must be 2, got {agency.get('schema_version')!r}"
        )

    routing_meta = agency.get("routing", {})
    expected_routing = {
        "profile_metadata_template": "profiles/{name}/distribution.yaml",
        "selection_order": ["professional-profile", "eligible-node"],
        "live_presence_owner": "hermes-fleet",
        "missing_presence_behavior": "fleet-locate-or-place",
    }
    if routing_meta != expected_routing:
        errors.append(f"agency.json routing contract mismatch: {routing_meta!r}")
    else:
        metadata_template = routing_meta["profile_metadata_template"]
        for name in roster_names:
            metadata_path = root / metadata_template.format(name=name)
            if not metadata_path.is_file():
                errors.append(
                    f"routing profile metadata path does not exist for {name}: {metadata_path}"
                )

    routing_eval_count = validate_routing_evals(root, roster_set, errors)

    stats = {
        "profiles": len(roster_names),
        "skills": actual_skill_count,
        "sourced_skills": sourced_skill_count,
        "routing_evals": routing_eval_count,
    }
    return errors, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="repository root (default: directory containing validate.py)",
    )
    args = parser.parse_args()

    errors, stats = validate(args.root.resolve())
    if errors:
        print(f"FAIL: {len(errors)} validation error(s)", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "OK: "
        f"{stats['profiles']} profiles, "
        f"{stats['skills']} bundled skills, "
        f"{stats['sourced_skills']} sourced skills, "
        f"{stats['routing_evals']} routing evals"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
