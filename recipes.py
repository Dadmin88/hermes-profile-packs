#!/usr/bin/env python3
"""Discover and install validated Hermes Profile Pack team recipes.

Recipes are portable composition advice. They reference the existing profile catalog
and reuse the root installer's selection/install machinery; they do not maintain a
second profile roster or create runtime state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Iterable

import install as profile_installer
import recipe_catalog
from recipe_catalog import Recipe, RecipeError, TIER_ORDER

ROOT = Path(__file__).resolve().parent
RECIPE_FILE = ROOT / "recipes.json"


def load_recipes(root: Path = ROOT) -> dict[str, Recipe]:
    return recipe_catalog.load_recipes(root)


def resolve_recipe_profiles(
    recipe: Recipe,
    tier: str,
    profiles: Iterable[profile_installer.Profile],
) -> list[profile_installer.Profile]:
    return recipe_catalog.resolve_recipe_profiles(recipe, tier, profiles)


def recommend_recipes(
    recipes: Iterable[Recipe],
    query: str,
    *,
    limit: int = 5,
    pack_filter: set[str] | None = None,
) -> list[tuple[Recipe, int, list[str]]]:
    return recipe_catalog.recommend_recipes(
        recipes,
        query,
        expanded_query=profile_installer.expanded_query,
        tokenize=profile_installer.tokenize,
        pack_hints=profile_installer.PACK_HINTS,
        pack_display=profile_installer.PACK_DISPLAY,
        limit=limit,
        pack_filter=pack_filter,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Choose a proven small Hermes team recipe without installing the whole catalog."
    )
    parser.add_argument("recipe", nargs="?", help="Recipe id, for example software-delivery.")
    parser.add_argument("--list", action="store_true", help="List available recipes and exit.")
    parser.add_argument("--recommend", metavar="TEXT", help="Recommend recipes for a plain-language goal.")
    parser.add_argument("--pack", action="append", help="Filter recipes by pack; repeatable.")
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
        pack_filter = profile_installer.filter_packs(args.pack)

        read_modes = int(args.list) + int(args.recommend is not None)
        if read_modes > 1:
            raise RecipeError("choose only one of --list or --recommend")
        if read_modes and args.recipe:
            raise RecipeError("recipe id cannot be combined with --list or --recommend")
        if read_modes and (args.dry_run or args.yes or args.force):
            raise RecipeError("read-only recipe discovery cannot be combined with install flags")

        if args.list:
            ordered = sorted(
                (recipe for recipe in recipes.values() if not pack_filter or recipe.pack in pack_filter),
                key=lambda recipe: (recipe.pack, recipe.id),
            )
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
            ranked = recommend_recipes(
                recipes.values(), args.recommend, limit=args.limit, pack_filter=pack_filter
            )
            confident = recipe_catalog.confident_recipe_match(ranked)
            if args.json:
                _emit(
                    {
                        "query": args.recommend,
                        "recipe_match": (
                            {
                                "recipe": confident[0].id,
                                "display_name": confident[0].display_name,
                                "pack": confident[0].pack,
                                "score": confident[1],
                                "reasons": confident[2],
                            }
                            if confident
                            else None
                        ),
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
                    marker = "  *" if confident and recipe.id == confident[0].id else "   "
                    print(f"{marker} {recipe.id:<28} {recipe.display_name}  score={score}")
                    print("      " + ("; ".join(reasons[:3]) or recipe.description))
                if confident:
                    print(f"\n* Clear recipe match: {confident[0].display_name}")
            return 0

        if not args.recipe:
            raise RecipeError("choose a recipe id, --list, or --recommend")
        recipe = recipes.get(args.recipe)
        if recipe is None:
            raise RecipeError(f"unknown recipe: {args.recipe}")
        if pack_filter and recipe.pack not in pack_filter:
            raise RecipeError(f"recipe {recipe.id} is outside the requested --pack filter")
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
