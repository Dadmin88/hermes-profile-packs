#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "academy.json"
REPO_ROOT = ROOT.parent
AGENCY_PROFILES_DIR = REPO_ROOT / "hermes-agency" / "profiles"
NAME_RE = re.compile(r"^academy-[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FORBIDDEN = [
    re.compile(r"/(?:home|media)/(?:kyle|dadmin)(?:/|$)", re.I),
    re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
]
VALID_TARGET_MODES = {"agency-ce-participants", "academy-faculty-except-dean"}


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


def _resolve_shared_skill_targets(
    shared_skill: dict,
    academy_profile_names: set[str],
) -> list[str]:
    """Resolve target profile names for a shared skill."""
    targets = shared_skill["targets"]
    mode = targets["mode"]
    exceptions = set(targets.get("exceptions", []))

    if mode == "agency-ce-participants":
        if not AGENCY_PROFILES_DIR.is_dir():
            return []
        names = {p.name for p in AGENCY_PROFILES_DIR.iterdir() if p.is_dir()}
    elif mode == "academy-faculty-except-dean":
        names = academy_profile_names - {"academy-dean"}
    else:
        return []

    return sorted(names - exceptions)


def validate_routing(manifest: dict, errors: list[str]) -> None:
    """Validate manifest-owned Academy routing policy and installed Dean parity."""
    routing = manifest.get("routing")
    if not isinstance(routing, dict):
        errors.append("manifest is missing routing object")
        return

    profiles = {
        profile.get("name"): profile
        for profile in manifest.get("profiles", [])
        if isinstance(profile, dict) and isinstance(profile.get("name"), str)
    }
    profile_names = set(profiles)

    broad_chairs = routing.get("broad_chairs")
    if not isinstance(broad_chairs, list):
        errors.append("routing.broad_chairs must be a list")
        broad_chairs = []
    for name in broad_chairs:
        if name not in profile_names:
            errors.append(f"routing broad chair is not an Academy profile: {name!r}")

    category_fallbacks = routing.get("category_fallbacks")
    if not isinstance(category_fallbacks, dict):
        errors.append("routing.category_fallbacks must be an object")
        category_fallbacks = {}

    declared_categories = set(manifest.get("categories", {}))
    expected_fallback_categories = declared_categories - {"coordination"}
    actual_fallback_categories = set(category_fallbacks)
    if actual_fallback_categories != expected_fallback_categories:
        errors.append(
            "routing.category_fallbacks category mismatch: "
            f"missing={sorted(expected_fallback_categories-actual_fallback_categories)} "
            f"extra={sorted(actual_fallback_categories-expected_fallback_categories)}"
        )

    for category, name in category_fallbacks.items():
        profile = profiles.get(name)
        if profile is None:
            errors.append(
                f"routing category fallback {category!r} references missing profile {name!r}"
            )
            continue
        if profile.get("category") != category:
            errors.append(
                f"routing category fallback {category!r} points to {name!r} "
                f"in category {profile.get('category')!r}"
            )

    preferences = routing.get("specialist_preferences")
    if not isinstance(preferences, dict):
        errors.append("routing.specialist_preferences must be an object")
        preferences = {}
    for topic, name in preferences.items():
        if not isinstance(topic, str) or not topic:
            errors.append(f"routing specialist preference has invalid topic: {topic!r}")
        if name not in profile_names:
            errors.append(
                f"routing specialist preference {topic!r} references missing profile {name!r}"
            )

    # The runtime Dean distribution must carry the human-readable fallback
    # policy because pack-root routing.py is deliberately not a runtime
    # dependency after profile installation.
    dean_skill = (
        ROOT
        / "profiles"
        / "academy-dean"
        / "skills"
        / "faculty-routing"
        / "SKILL.md"
    )
    if not dean_skill.is_file():
        errors.append("academy-dean: missing faculty-routing skill")
        return
    dean_text = dean_skill.read_text(encoding="utf-8")
    for category, name in category_fallbacks.items():
        readable_category = category.replace("-", " ")
        marker = f"{readable_category} → `{name}`"
        if marker not in dean_text:
            errors.append(
                f"academy-dean/faculty-routing missing manifest fallback marker: {marker}"
            )
    if "not** a runtime dependency of the installed Dean profile" not in dean_text:
        errors.append(
            "academy-dean/faculty-routing must state that pack-root routing.py "
            "is not an installed runtime dependency"
        )


def validate_shared_skills(manifest: dict, errors: list[str]) -> int:
    """Validate shared_skills manifest entries and byte identity.

    Returns the number of shared skills validated.
    """
    shared_skills = manifest.get("shared_skills")
    if shared_skills is None:
        errors.append("manifest is missing shared_skills field")
        return 0
    if not isinstance(shared_skills, list):
        errors.append("shared_skills must be a list")
        return 0

    academy_profile_names = {p["name"] for p in manifest.get("profiles", [])}
    seen_names: set[str] = set()

    for index, skill in enumerate(shared_skills):
        label = f"shared_skill #{index + 1}"

        if not isinstance(skill, dict):
            errors.append(f"{label} is not an object")
            continue

        name = skill.get("name")
        canonical_source = skill.get("canonical_source")
        description = skill.get("description")
        targets = skill.get("targets")

        if not isinstance(name, str) or not SKILL_RE.fullmatch(name):
            errors.append(f"{label} has invalid name: {name!r}")
            continue
        if name in seen_names:
            errors.append(f"{label} duplicate shared skill name: {name}")
        seen_names.add(name)

        if not isinstance(canonical_source, str) or not canonical_source:
            errors.append(f"{label} ({name}) missing canonical_source")
            continue
        canonical_path = ROOT / canonical_source
        if not canonical_path.is_file():
            errors.append(
                f"{label} ({name}) canonical source not found: {canonical_source}"
            )
            continue

        fm = parse_skill(canonical_path)
        if fm.get("name") != name:
            errors.append(
                f"{label} ({name}) frontmatter name mismatch: {fm.get('name')!r}"
            )

        if not isinstance(description, str) or not description.strip():
            errors.append(f"{label} ({name}) missing description")

        if not isinstance(targets, dict):
            errors.append(f"{label} ({name}) missing or invalid targets")
            continue

        mode = targets.get("mode")
        if mode not in VALID_TARGET_MODES:
            errors.append(f"{label} ({name}) invalid target mode: {mode!r}")
            continue

        exceptions = targets.get("exceptions", [])
        if not isinstance(exceptions, list):
            errors.append(f"{label} ({name}) exceptions must be a list")
            exceptions = []

        for exc in exceptions:
            if not isinstance(exc, str):
                errors.append(f"{label} ({name}) non-string exception: {exc!r}")
                continue
            if mode == "agency-ce-participants":
                if not exc.startswith("agency-"):
                    errors.append(
                        f"{label} ({name}) exception {exc!r} does not match agency namespace"
                    )
            elif mode == "academy-faculty-except-dean":
                if exc not in academy_profile_names:
                    errors.append(
                        f"{label} ({name}) exception {exc!r} is not an academy profile"
                    )

        canonical_bytes = canonical_path.read_bytes()
        target_names = _resolve_shared_skill_targets(skill, academy_profile_names)

        for profile_name in target_names:
            if profile_name.startswith("agency-"):
                profile_dir = AGENCY_PROFILES_DIR / profile_name
            elif profile_name.startswith("academy-"):
                profile_dir = ROOT / "profiles" / profile_name
            else:
                continue

            if not profile_dir.is_dir():
                continue

            materialized = profile_dir / "skills" / name / "SKILL.md"
            if not materialized.is_file():
                errors.append(
                    f"{name} not materialized in {profile_name} "
                    f"(expected {materialized.relative_to(REPO_ROOT)})"
                )
                continue

            if materialized.read_bytes() != canonical_bytes:
                errors.append(
                    f"{name} byte mismatch in {profile_name} "
                    f"(canonical != materialized at {materialized.relative_to(REPO_ROOT)})"
                )

    return len(shared_skills)


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("profiles", [])
    names = [p.get("name") for p in entries]

    if manifest.get("profile_count") != len(entries):
        errors.append("profile_count mismatch")
    if sum(manifest.get("categories", {}).values()) != len(entries):
        errors.append("category counts mismatch")
    duplicates = [name for name, count in Counter(names).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate profiles: {duplicates}")
    if manifest.get("orchestrator") not in names:
        errors.append("orchestrator not in roster")

    actual = {p.name for p in (ROOT / "profiles").iterdir() if p.is_dir()}
    if set(names) != actual:
        errors.append(
            "profile directory mismatch: "
            f"missing={sorted(set(names)-actual)} extra={sorted(actual-set(names))}"
        )

    validate_routing(manifest, errors)

    for item in entries:
        name = item["name"]
        if not NAME_RE.fullmatch(name):
            errors.append(f"invalid profile name: {name}")
        root = ROOT / "profiles" / name
        if not (root / ".no-bundled-skills").is_file():
            errors.append(f"{name}: missing .no-bundled-skills")
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

        skills = set()
        for skill in sorted((root / "skills").glob("*/SKILL.md")):
            skill_name = skill.parent.name
            skills.add(skill_name)
            if not SKILL_RE.fullmatch(skill_name):
                errors.append(f"{name}: invalid skill {skill_name}")
            fm = parse_skill(skill)
            if fm.get("name") != skill_name:
                errors.append(f"{name}/{skill_name}: frontmatter name mismatch")
            if not fm.get("description"):
                errors.append(f"{name}/{skill_name}: missing description")

        own_skills = set(item.get("jobs", []))
        shared_skill_names = {s["name"] for s in manifest.get("shared_skills", [])}
        non_shared = skills - shared_skill_names
        if own_skills != non_shared:
            errors.append(f"{name}: jobs do not match non-shared skills")

    validate_shared_skills(manifest, errors)

    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if (
            path.suffix.lower()
            not in {".md", ".yaml", ".yml", ".json", ".py", ".txt"}
            and path.name != ".no-bundled-skills"
        ):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in FORBIDDEN:
            if pattern.search(text):
                errors.append(
                    f"forbidden portable-content pattern in {path.relative_to(ROOT)}"
                )

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    shared_count = len(manifest.get("shared_skills", []))
    print(
        f"Hermes Academy validation passed: {len(entries)} profiles, "
        f"{sum(len(p['jobs']) for p in entries)} skills, {shared_count} shared skills"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
