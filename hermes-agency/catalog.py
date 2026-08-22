#!/usr/bin/env python3
"""Emit the runtime-facing Hermes Agency profile catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENCY_PATH = ROOT / "agency.json"
CONTENT_DIGEST_SCHEMA = "hermes-agency-profile-content.v1"
_CONTENT_FILES = ("SOUL.md", "config.yaml", "mcp.json", ".no-bundled-skills")
_CONTENT_DIRS = ("skills", "cron")


def _load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _yaml_scalar(value: str) -> str:
    value = value.strip()
    if value.startswith('"'):
        parsed = json.loads(value)
        if not isinstance(parsed, str):
            raise ValueError("distribution scalar must be a string")
        return parsed
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def _distribution_metadata(path: Path) -> dict[str, str]:
    wanted = {"name", "version", "description"}
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line or raw_line[0].isspace() or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        if key in wanted:
            values[key] = _yaml_scalar(value)
    missing = wanted - set(values)
    if missing:
        raise ValueError(f"{path}: missing distribution fields: {', '.join(sorted(missing))}")
    if any(not values[key].strip() for key in wanted):
        raise ValueError(f"{path}: distribution identity fields must be nonempty")
    return values


def _validate_distribution_identity(
    metadata: dict[str, str], expected_name: str, expected_version: str
) -> None:
    if metadata.get("name") != expected_name or metadata.get("version") != expected_version:
        raise ValueError(f"{expected_name}: distribution identity does not match Agency catalog")


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _profile_content_files(profile_dir: Path) -> list[Path]:
    if not profile_dir.is_dir() or profile_dir.is_symlink():
        raise ValueError(f"{profile_dir}: profile directory is invalid")

    soul = profile_dir / "SOUL.md"
    skills = profile_dir / "skills"
    if not soul.is_file() or soul.is_symlink():
        raise ValueError(f"{profile_dir}: SOUL.md is missing or invalid")
    if not skills.is_dir() or skills.is_symlink():
        raise ValueError(f"{profile_dir}: skills directory is missing or invalid")

    files: list[Path] = []
    for relative in _CONTENT_FILES:
        path = profile_dir / relative
        if path.is_symlink():
            raise ValueError(f"{path}: content identity does not permit symlinks")
        if path.exists():
            if not path.is_file():
                raise ValueError(f"{path}: expected a regular file")
            files.append(path)

    for relative in _CONTENT_DIRS:
        directory = profile_dir / relative
        if directory.is_symlink():
            raise ValueError(f"{directory}: content identity does not permit symlinks")
        if not directory.exists():
            continue
        if not directory.is_dir():
            raise ValueError(f"{directory}: expected a directory")
        for path in directory.rglob("*"):
            if path.is_symlink():
                raise ValueError(f"{path}: content identity does not permit symlinks")
            if path.is_file():
                files.append(path)
            elif not path.is_dir():
                raise ValueError(f"{path}: unsupported profile content entry")

    return sorted(files, key=lambda path: path.relative_to(profile_dir).as_posix())


def profile_content_digest(profile_dir: Path, name: str, version: str) -> str:
    """Hash the stable Agency-owned behavior bytes for one profile distribution."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("profile content identity requires a nonempty name")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("profile content identity requires a nonempty version")

    files = [
        {
            "path": path.relative_to(profile_dir).as_posix(),
            "sha256": _file_sha256(path),
            "executable": bool(path.stat().st_mode & 0o111),
        }
        for path in _profile_content_files(profile_dir)
    ]
    material = {
        "schema": CONTENT_DIGEST_SCHEMA,
        "name": name,
        "version": version,
        "files": files,
    }
    payload = json.dumps(
        material,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _profile_capabilities(profile_dir: Path) -> list[str]:
    skills_dir = profile_dir / "skills"
    if not skills_dir.is_dir() or skills_dir.is_symlink():
        raise ValueError(f"{profile_dir}: skills directory is missing or invalid")

    capabilities: list[str] = []
    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        if skill_dir.is_symlink():
            raise ValueError(f"{skill_dir}: capability directories may not be symlinks")
        if not (skill_dir / "SKILL.md").is_file():
            raise ValueError(f"{skill_dir}: capability is missing SKILL.md")
        capabilities.append(skill_dir.name)

    if not capabilities:
        raise ValueError(f"{profile_dir}: profile has no bundled capabilities")
    return capabilities


def build_catalog() -> dict:
    agency = _load_json(AGENCY_PATH)
    agency_profiles = agency.get("profiles")
    if not isinstance(agency_profiles, list):
        raise ValueError("agency.json must contain a profile array")

    agency_names = [item.get("name") for item in agency_profiles if isinstance(item, dict)]
    if len(agency_names) != len(agency_profiles) or len(set(agency_names)) != len(agency_names):
        raise ValueError("agency.json contains invalid or duplicate profile names")

    backbone_profiles = agency.get("backbone_profiles", [])
    if not isinstance(backbone_profiles, list) or not all(
        isinstance(name, str) for name in backbone_profiles
    ):
        raise ValueError("agency.json backbone_profiles must be a string array")
    if len(backbone_profiles) != len(set(backbone_profiles)):
        raise ValueError("agency.json backbone_profiles contains duplicates")
    unknown_backbone = set(backbone_profiles) - set(agency_names)
    if unknown_backbone:
        raise ValueError(
            "agency.json backbone_profiles contains unknown profiles: "
            + ", ".join(sorted(unknown_backbone))
        )
    backbone_set = set(backbone_profiles)

    distribution = agency["distribution"]
    routing = agency["routing"]
    profile_root = ROOT / distribution["profile_root"]
    path_template = distribution["profile_path_template"]
    version = agency["version"]

    entries = []
    for profile in agency_profiles:
        name = profile["name"]
        category = profile.get("category")
        if not isinstance(category, str) or not category:
            raise ValueError(f"{name}: category is invalid")

        relative_path = path_template.format(name=name)
        profile_dir = profile_root / name
        manifest_path = profile_dir / "distribution.yaml"
        metadata = _distribution_metadata(manifest_path)
        _validate_distribution_identity(metadata, name, version)
        entries.append(
            {
                "name": name,
                "version": version,
                "category": category,
                "priority": "backbone" if name in backbone_set else "standard",
                "description": metadata["description"],
                "distribution_path": relative_path,
                "content_digest": profile_content_digest(profile_dir, name, version),
                "capabilities": _profile_capabilities(profile_dir),
            }
        )

    entries.sort(key=lambda item: item["name"])
    return {
        "schema_version": 2,
        "content_digest_schema": CONTENT_DIGEST_SCHEMA,
        "agency": {
            "name": agency["name"],
            "version": version,
            "profile_count": agency["profile_count"],
            "orchestrator": agency["orchestrator"],
        },
        "distribution": {
            "format": distribution["format"],
            "profile_identity_field": distribution["profile_identity_field"],
            "profile_path_template": path_template,
        },
        "routing": {
            "selection_order": routing["selection_order"],
            "live_presence_owner": routing["live_presence_owner"],
            "missing_presence_behavior": routing["missing_presence_behavior"],
        },
        "profiles": entries,
    }


def _filter_catalog(catalog: dict, profile_name: str | None, category: str | None) -> dict:
    if profile_name and category:
        raise ValueError("choose either --profile or --category")
    profiles = catalog["profiles"]
    if profile_name:
        profiles = [profile for profile in profiles if profile["name"] == profile_name]
        if not profiles:
            raise ValueError(f"unknown profile: {profile_name}")
    elif category:
        profiles = [profile for profile in profiles if profile["category"] == category]
        if not profiles:
            raise ValueError(f"unknown or empty category: {category}")
    filtered = dict(catalog)
    filtered["profiles"] = profiles
    return filtered


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Emit the Fleet-facing Hermes Agency runtime catalog.")
    parser.add_argument("--profile", help="emit one profile by stable profile name")
    parser.add_argument("--category", help="emit profiles in one category")
    parser.add_argument("--compact", action="store_true", help="emit compact JSON")
    args = parser.parse_args(argv)

    try:
        catalog = _filter_catalog(build_catalog(), args.profile, args.category)
    except (KeyError, OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))

    if args.compact:
        print(json.dumps(catalog, separators=(",", ":"), sort_keys=True))
    else:
        print(json.dumps(catalog, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
