#!/usr/bin/env python3
"""Discover and install validated Hermes Profile Pack team recipes.

Recipes are portable composition advice. They reference the existing profile catalog
and reuse the root installer's selection/install machinery; they do not maintain a
second profile roster or create runtime state.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys
from typing import Iterable

import install as profile_installer

ROOT = Path(__file__).resolve().parent
RECIPE_FILE = ROOT / "recipes.json"
TIER_ORDER = ("minimal", "recommended", "expanded")


class RecipeError(ValueError):
    """User-facing recipe error."""


@dataclass(frozen=True)
class Recipe:
    id: str
    display_name: str
    pack: str
    description: str
    when_to_use: str
    keywords: tuple[str, ...]
    tiers: dict[str, tuple[str, ...]]
    workflow: tuple[str, ...]
    success_criteria: tuple[str, ...]
    optional_routines: tuple[str, ...]

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "display_name": self.display_name,
            "pack": self.pack,
            "description": self.description,
            "when_to_use": self.when_to_use,
            "keywords": list(self.keywords),
            "tiers": {tier: list(self.tiers[tier]) for tier in TIER_ORDER},
            "workflow": list(self.workflow),
            "success_criteria": list(self.success_criteria),
            "optional_routines": list(self.optional_routines),
        }

    def searchable_text(self) -> str:
        return " ".join(
            [self.id.replace("-", " "), self.display_name, self.description, self.when_to_use, *self.keywords]
        ).lower()


def load_recipes(root: Path = ROOT) -> dict[str, Recipe]:
    path = root / "recipes.json"
    if not path.is_file():
        raise RecipeError(f"missing recipe registry: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise RecipeError("unsupported recipes.json schema_version")

    recipes: dict[str, Recipe] = {}
    for item in payload.get("recipes", []):
        recipe_id = str(item.get("id", ""))
        if not recipe_id:
            raise RecipeError("recipe is missing id")
        if recipe_id in recipes:
            raise RecipeError(f"duplicate recipe id: {recipe_id}")
        raw_tiers = item.get("tiers", {})
        tiers = {tier: tuple(str(name) for name in raw_tiers.get(tier, [])) for tier in TIER_ORDER}
        recipes[recipe_id] = Recipe(
            id=recipe_id,
            display_name=str(item.get("display_name") or recipe_id),
            pack=str(item.get("pack") or ""),
            description=str(item.get("description") or ""),
            when_to_use=str(item.get("when_to_use") or ""),
            keywords=tuple(str(value) for value in item.get("keywords", [])),
            tiers=tiers,
            workflow=tuple(str(value) for value in item.get("workflow", [])),
            success_criteria=tuple(str(value) for value in item.get("success_criteria", [])),
            optional_routines=tuple(str(value) for value in item.get("optional_routines", [])),
        )
    return recipes


def resolve_recipe_profiles(
    recipe: Recipe,
    tier: str,
    profiles: Iterable[profile_installer.Profile],
) -> list[profile_installer.Profile]:
    if tier not in TIER_ORDER:
        raise RecipeError(f"unknown tier '{tier}'. Choose: {', '.join(TIER_ORDER)}")
    by_name = {profile.name: profile for profile in profiles}
    selected: list[profile_installer.Profile] = []
    for name in recipe.tiers[tier]:
        profile = by_name.get(name)
        if profile is None:
            raise RecipeError(f"recipe {recipe.id} references unavailable profile: {name}")
        if profile.pack != recipe.pack:
            raise RecipeError(
                f"recipe {recipe.id} belongs to {recipe.pack} but references {name} from {profile.pack}"
            )
        selected.append(profile)
    return selected


def _score(recipe: Recipe, query: str) -> tuple[int, list[str]]:
    query_tokens = profile_installer.expanded_query(query)
    keyword_tokens = profile_installer.tokenize(" ".join(recipe.keywords))
    name_tokens = profile_installer.tokenize(recipe.id.replace("-", " ") + " " + recipe.display_name)
    detail_tokens = profile_installer.tokenize(recipe.description + " " + recipe.when_to_use)

    keyword_hits = sorted(query_tokens & keyword_tokens)
    name_hits = sorted(query_tokens & name_tokens)
    detail_hits = sorted(query_tokens & detail_tokens)

    score = len(keyword_hits) * 10 + len(name_hits) * 8 + len(detail_hits) * 3
    reasons: list[str] = []
    if keyword_hits:
        reasons.append("recipe intent: " + ", ".join(keyword_hits[:4]))
    if name_hits:
        reasons.append("recipe name: " + ", ".join(name_hits[:3]))
    if detail_hits:
        reasons.append("description: " + ", ".join(detail_hits[:3]))

    raw_query = " ".join(query.lower().split())
    if raw_query and len(raw_query) >= 4 and raw_query in recipe.searchable_text():
        score += 15
        reasons.insert(0, "exact phrase match")

    raw_tokens = profile_installer.tokenize(query)
    pack_hits = sorted(raw_tokens & profile_installer.PACK_HINTS.get(recipe.pack, set()))
    if pack_hits:
        score += min(8, 2 * len(pack_hits))
        reasons.append(f"{profile_installer.PACK_DISPLAY[recipe.pack]} intent")
    return score, reasons


def recommend_recipes(
    recipes: Iterable[Recipe], query: str, *, limit: int = 5
) -> list[tuple[Recipe, int, list[str]]]:
    if not query.strip():
        raise RecipeError("recommendation query cannot be empty")
    if limit < 1:
        raise RecipeError("--limit must be at least 1")
    ranked: list[tuple[Recipe, int, list[str]]] = []
    for recipe in recipes:
        score, reasons = _score(recipe, query)
        if score > 0:
            ranked.append((recipe, score, reasons))
    ranked.sort(key=lambda item: (-item[1], item[0].pack, item[0].id))
    return ranked[:limit]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Choose a proven small Hermes team recipe without installing the whole catalog."
    )
    parser.add_argument("recipe", nargs="?", help="Recipe id, for example software-delivery.")
    parser.add_argument("--list", action="store_true", help="List available recipes and exit.")
    parser.add_argument("--recommend", metavar="TEXT", help="Recommend recipes for a plain-language goal.")
    parser.add_argument("--tier", choices=TIER_ORDER, default="recommended", help="Recipe size tier (default: recommended).")
    parser.add_argument("--limit", type=int, default=5, help="Maximum recipe recommendations (default: 5).")
    parser.add_argument("--dry-run", action="store_true", help="Resolve the exact recipe profile plan without installing.")
    parser.add_argument("--yes", action="store_true", help="Install the exact resolved recipe selection.")
    parser.add_argument("--force", action="store_true", help="Re-apply selected distributions over existing profiles.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON and never prompt.")
    return parser


def _emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2, sort_keys=True))


def _recipe_plan(
    recipe: Recipe,
    tier: str,
    selected: list[profile_installer.Profile],
    all_profiles: list[profile_installer.Profile],
) -> dict:
    return {
        "status": "plan",
        "recipe": recipe.id,
        "display_name": recipe.display_name,
        "pack": recipe.pack,
        "tier": tier,
        "profiles": [profile.name for profile in selected],
        "stats": profile_installer.selected_stats(selected, all_profiles),
        "workflow": list(recipe.workflow),
        "success_criteria": list(recipe.success_criteria),
        "optional_routines": list(recipe.optional_routines),
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        recipes = load_recipes()
        packs, profiles = profile_installer.load_catalog()

        read_modes = int(args.list) + int(args.recommend is not None)
        if read_modes > 1:
            raise RecipeError("choose only one of --list or --recommend")
        if read_modes and args.recipe:
            raise RecipeError("recipe id cannot be combined with --list or --recommend")
        if read_modes and (args.dry_run or args.yes or args.force):
            raise RecipeError("read-only recipe discovery cannot be combined with install flags")

        if args.list:
            ordered = sorted(recipes.values(), key=lambda recipe: (recipe.pack, recipe.id))
            if args.json:
                _emit({"recipe_count": len(ordered), "recipes": [recipe.as_dict() for recipe in ordered]})
            else:
                current = None
                for recipe in ordered:
                    if recipe.pack != current:
                        print(f"\n{profile_installer.PACK_DISPLAY[recipe.pack]}")
                        current = recipe.pack
                    print(f"  {recipe.id:<28} {recipe.display_name}")
                    print(f"    {recipe.description}")
            return 0

        if args.recommend is not None:
            ranked = recommend_recipes(recipes.values(), args.recommend, limit=args.limit)
            if args.json:
                _emit(
                    {
                        "query": args.recommend,
                        "recommendation_count": len(ranked),
                        "recommendations": [
                            {
                                "recipe": recipe.id,
                                "display_name": recipe.display_name,
                                "pack": recipe.pack,
                                "score": score,
                                "reasons": reasons,
                                "recommended_profiles": list(recipe.tiers["recommended"]),
                            }
                            for recipe, score, reasons in ranked
                        ],
                    }
                )
            else:
                if not ranked:
                    print("No confident recipe recommendations found.")
                    return 0
                print(f"Recommended team recipes for: {args.recommend}")
                for recipe, score, reasons in ranked:
                    print(f"  {recipe.id:<28} {recipe.display_name}  score={score}")
                    print("    " + ("; ".join(reasons[:3]) or recipe.description))
            return 0

        if not args.recipe:
            raise RecipeError("choose a recipe id, --list, or --recommend")
        recipe = recipes.get(args.recipe)
        if recipe is None:
            raise RecipeError(f"unknown recipe: {args.recipe}")
        selected = resolve_recipe_profiles(recipe, args.tier, profiles)
        plan = _recipe_plan(recipe, args.tier, selected, profiles)

        if args.json:
            if args.dry_run or not args.yes:
                _emit(plan)
        else:
            print(f"{recipe.display_name} [{recipe.id}] - {args.tier}")
            print(recipe.description)
            print("\nExact profile plan:")
            for profile in selected:
                print(f"  - {profile.name} ({profile.display_name})")
            stats = plan["stats"]
            print(
                f"\nSelected {stats['selected_profiles']} of {stats['available_profiles']} catalog profiles "
                f"(~{profile_installer.format_bytes(stats['estimated_source_bytes'])} source payload)."
            )
            if recipe.optional_routines:
                print("\nOptional runtime ideas (never auto-installed):")
                for routine in recipe.optional_routines:
                    print(f"  - {routine}")

        if args.dry_run or not args.yes:
            if not args.dry_run and not args.json:
                print("\nRead-only plan. Re-run with --yes to install this exact recipe tier.")
            return 0

        code, results = profile_installer.install_selected(
            selected, packs, force=args.force, json_mode=args.json
        )
        if args.json:
            _emit(
                {
                    **plan,
                    "status": "ok" if code == 0 else "error",
                    "returncode": code,
                    "packs": results,
                }
            )
        elif code == 0:
            print(f"\nInstalled {len(selected)} profile(s) from recipe {recipe.id}.")
        return code

    except (RecipeError, profile_installer.CLIError, json.JSONDecodeError, OSError) as exc:
        if args.json:
            print(json.dumps({"status": "error", "error": str(exc)}), file=sys.stderr)
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
