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
    ("OpenAI-style secret", re.compile(r"(?<![A-Za-z0-9_])sk-[A-Za-z0-9_-]{20,}")),
]
RECIPE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RECIPE_TIERS = ("minimal", "recommended", "expanded")


def validate_recipes(profile_to_pack: dict[str, str], pack_keys: set[str]) -> list[str]:
    errors: list[str] = []
    path = ROOT / "recipes.json"
    if not path.is_file():
        return ["missing recipe registry: recipes.json"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid recipes.json: {exc}"]

    if payload.get("schema_version") != 1:
        errors.append("recipes.json schema_version must be 1")
    seen: set[str] = set()
    for index, recipe in enumerate(payload.get("recipes", []), 1):
        recipe_id = str(recipe.get("id", ""))
        label = recipe_id or f"recipe #{index}"
        if not RECIPE_ID.fullmatch(recipe_id):
            errors.append(f"invalid recipe id: {label}")
        if recipe_id in seen:
            errors.append(f"duplicate recipe id: {recipe_id}")
        seen.add(recipe_id)

        pack = str(recipe.get("pack", ""))
        if pack not in pack_keys:
            errors.append(f"{label}: unknown owning pack '{pack}'")

        for field in ("display_name", "description", "when_to_use"):
            if not str(recipe.get(field, "")).strip():
                errors.append(f"{label}: missing {field}")
        for field in ("keywords", "workflow", "success_criteria"):
            value = recipe.get(field)
            if not isinstance(value, list) or not value:
                errors.append(f"{label}: {field} must be a non-empty list")

        tiers = recipe.get("tiers")
        if not isinstance(tiers, dict):
            errors.append(f"{label}: missing tiers object")
            continue
        tier_sets: dict[str, set[str]] = {}
        for tier in RECIPE_TIERS:
            names = tiers.get(tier)
            if not isinstance(names, list) or not names:
                errors.append(f"{label}: tier {tier} must be a non-empty list")
                tier_sets[tier] = set()
                continue
            if len(names) != len(set(names)):
                errors.append(f"{label}: tier {tier} contains duplicate profiles")
            tier_sets[tier] = set(names)
            for name in names:
                actual_pack = profile_to_pack.get(name)
                if actual_pack is None:
                    errors.append(f"{label}: tier {tier} references unknown profile {name}")
                elif actual_pack != pack:
                    errors.append(
                        f"{label}: tier {tier} references {name} from {actual_pack}, not owning pack {pack}"
                    )
        if not tier_sets["minimal"] <= tier_sets["recommended"]:
            errors.append(f"{label}: minimal tier must be a subset of recommended")
        if not tier_sets["recommended"] <= tier_sets["expanded"]:
            errors.append(f"{label}: recommended tier must be a subset of expanded")
    if not seen:
        errors.append("recipes.json must contain at least one recipe")
    return errors


def main() -> int:
    errors: list[str] = []
    packs = json.loads((ROOT / "packs.json").read_text(encoding="utf-8"))["packs"]
    profile_to_pack: dict[str, str] = {}
    pack_keys: set[str] = set()
    for pack in packs:
        pack_dir = ROOT / pack["path"]
        if not pack_dir.is_dir():
            errors.append(f"missing pack directory: {pack['path']}")
            continue
        namespace = pack["namespace"][:-1]
        pack_key = namespace.rstrip("-")
        pack_keys.add(pack_key)
        manifest = ROOT / pack["manifest"]
        if not manifest.is_file():
            errors.append(f"missing pack manifest: {pack['manifest']}")
        else:
            try:
                manifest_payload = json.loads(manifest.read_text(encoding="utf-8"))
                for item in manifest_payload.get("profiles", []):
                    name = str(item.get("name", ""))
                    if name:
                        if name in profile_to_pack:
                            errors.append(f"profile appears in more than one pack: {name}")
                        profile_to_pack[name] = pack_key
            except json.JSONDecodeError as exc:
                errors.append(f"invalid pack manifest {pack['manifest']}: {exc}")
        profile_dir = pack_dir / "profiles"
        for child in profile_dir.iterdir():
            if child.is_dir() and not child.name.startswith(namespace):
                errors.append(f"wrong namespace in {pack['path']}: {child.name}")
        validator = pack_dir / "validate.py"
        if validator.is_file():
            result = subprocess.run([sys.executable, str(validator)], cwd=pack_dir)
            if result.returncode:
                errors.append(f"pack validator failed: {pack['name']}")

    errors.extend(validate_recipes(profile_to_pack, pack_keys))

    readme_count_check = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "update_readme_counts.py"), "--check"],
        cwd=ROOT,
    )
    if readme_count_check.returncode:
        errors.append("README profile counts are stale or could not be verified")

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
