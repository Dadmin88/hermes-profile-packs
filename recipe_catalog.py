"""Shared Team Recipe registry, scoring, confidence, and resolution helpers.

This module deliberately has no dependency on the root installer. Both install.py and
recipes.py use it so recipe behavior has one implementation and one confidence policy.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

TIER_ORDER = ("minimal", "recommended", "expanded")
DEFAULT_TIER = "recommended"
CONFIDENT_RECIPE_SCORE = 24
CONFIDENT_RECIPE_MARGIN = 8


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
            [
                self.id.replace("-", " "),
                self.display_name,
                self.description,
                self.when_to_use,
                *self.keywords,
            ]
        ).lower()


def load_recipes(root: Path) -> dict[str, Recipe]:
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
        tiers = {
            tier: tuple(str(name) for name in raw_tiers.get(tier, []))
            for tier in TIER_ORDER
        }
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
    profiles: Iterable[Any],
) -> list[Any]:
    if tier not in TIER_ORDER:
        raise RecipeError(f"unknown tier '{tier}'. Choose: {', '.join(TIER_ORDER)}")
    by_name = {profile.name: profile for profile in profiles}
    selected: list[Any] = []
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


def _score(
    recipe: Recipe,
    query: str,
    *,
    expanded_query: Callable[[str], set[str]],
    tokenize: Callable[[str], set[str]],
    pack_hints: Mapping[str, set[str]],
    pack_display: Mapping[str, str],
) -> tuple[int, list[str]]:
    query_tokens = expanded_query(query)
    keyword_tokens = tokenize(" ".join(recipe.keywords))
    name_tokens = tokenize(recipe.id.replace("-", " ") + " " + recipe.display_name)
    detail_tokens = tokenize(recipe.description + " " + recipe.when_to_use)

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

    raw_tokens = tokenize(query)
    pack_hits = sorted(raw_tokens & pack_hints.get(recipe.pack, set()))
    if pack_hits:
        score += min(8, 2 * len(pack_hits))
        reasons.append(f"{pack_display[recipe.pack]} intent")
    return score, reasons


def recommend_recipes(
    recipes: Iterable[Recipe],
    query: str,
    *,
    expanded_query: Callable[[str], set[str]],
    tokenize: Callable[[str], set[str]],
    pack_hints: Mapping[str, set[str]],
    pack_display: Mapping[str, str],
    limit: int = 5,
    pack_filter: set[str] | None = None,
) -> list[tuple[Recipe, int, list[str]]]:
    if not query.strip():
        raise RecipeError("recommendation query cannot be empty")
    if limit < 1:
        raise RecipeError("--limit must be at least 1")
    ranked: list[tuple[Recipe, int, list[str]]] = []
    for recipe in recipes:
        if pack_filter and recipe.pack not in pack_filter:
            continue
        score, reasons = _score(
            recipe,
            query,
            expanded_query=expanded_query,
            tokenize=tokenize,
            pack_hints=pack_hints,
            pack_display=pack_display,
        )
        if score > 0:
            ranked.append((recipe, score, reasons))
    ranked.sort(key=lambda item: (-item[1], item[0].pack, item[0].id))
    return ranked[:limit]


def confident_recipe_match(
    ranked: list[tuple[Recipe, int, list[str]]],
    *,
    minimum_score: int = CONFIDENT_RECIPE_SCORE,
    minimum_margin: int = CONFIDENT_RECIPE_MARGIN,
) -> tuple[Recipe, int, list[str]] | None:
    """Return the top recipe only when it is strong and meaningfully unambiguous."""
    if not ranked:
        return None
    top = ranked[0]
    if top[1] < minimum_score:
        return None
    if len(ranked) > 1 and top[1] - ranked[1][1] < minimum_margin:
        return None
    return top
