from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import install
import recipe_catalog
import recipes


class RecipeTests(unittest.TestCase):
    def test_registry_loads_and_ids_are_unique(self):
        loaded = recipes.load_recipes(ROOT)
        self.assertGreaterEqual(len(loaded), 12)
        self.assertEqual(len(loaded), len(set(loaded)))

    def test_tiers_are_monotonic_and_resolve_to_same_pack(self):
        loaded = recipes.load_recipes(ROOT)
        _, profiles = install.load_catalog(ROOT)
        for recipe in loaded.values():
            minimal = set(recipe.tiers["minimal"])
            recommended = set(recipe.tiers["recommended"])
            expanded = set(recipe.tiers["expanded"])
            self.assertTrue(minimal)
            self.assertTrue(minimal <= recommended, recipe.id)
            self.assertTrue(recommended <= expanded, recipe.id)
            for tier in recipes.TIER_ORDER:
                selected = recipes.resolve_recipe_profiles(recipe, tier, profiles)
                self.assertEqual(len(selected), len(recipe.tiers[tier]))
                self.assertTrue(all(profile.pack == recipe.pack for profile in selected))

    def test_recipe_recommendation_prefers_cybersecurity_learning_for_learning_goal(self):
        loaded = recipes.load_recipes(ROOT)
        ranked = recipes.recommend_recipes(loaded.values(), "learn cybersecurity", limit=3)
        self.assertTrue(ranked)
        self.assertEqual(ranked[0][0].id, "cybersecurity-learning")

    def test_recipe_recommendation_returns_agency_software_option_for_build_goal(self):
        loaded = recipes.load_recipes(ROOT)
        ranked = recipes.recommend_recipes(loaded.values(), "build and ship a web app", limit=5)
        self.assertTrue(ranked)
        self.assertTrue(any(item[0].id == "software-delivery" for item in ranked))

    def test_confidence_requires_strength_and_margin(self):
        loaded = list(recipes.load_recipes(ROOT).values())
        self.assertGreaterEqual(len(loaded), 2)
        self.assertIsNone(
            recipe_catalog.confident_recipe_match(
                [(loaded[0], 23, []), (loaded[1], 1, [])]
            )
        )
        self.assertIsNone(
            recipe_catalog.confident_recipe_match(
                [(loaded[0], 30, []), (loaded[1], 25, [])]
            )
        )
        self.assertEqual(
            recipe_catalog.confident_recipe_match(
                [(loaded[0], 32, []), (loaded[1], 20, [])]
            )[0].id,
            loaded[0].id,
        )

    def test_root_installer_promotes_clear_recipe_but_keeps_profile_matches(self):
        loaded = install.load_recipe_catalog(ROOT)
        _, profiles = install.load_catalog(ROOT)
        _, confident, profile_ranked = install.recommend_goal(
            profiles, loaded, "build and ship a web app", limit=6
        )
        self.assertIsNotNone(confident)
        self.assertEqual(confident[0].id, "software-delivery")
        self.assertTrue(profile_ranked)

    def test_root_installer_json_recommendation_is_recipe_aware_and_read_only(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = install.main(["--recommend", "build and ship a web app", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["recipe_match"]["recipe"], "software-delivery")
        self.assertEqual(payload["recipe_match"]["default_tier"], "recommended")
        self.assertTrue(payload["recipe_recommendations"])
        self.assertTrue(payload["recommendations"])

    def test_root_installer_can_resolve_recipe_dry_run(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = install.main(
                ["--recipe", "api-backend", "--tier", "minimal", "--dry-run", "--json"]
            )
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "plan")
        self.assertEqual(payload["recipe"], "api-backend")
        self.assertEqual(payload["tier"], "minimal")
        self.assertIn("agency-backend-engineer", payload["profiles"])

    def test_json_dry_run_is_read_only_and_exact(self):
        output = io.StringIO()
        with redirect_stdout(output):
            code = recipes.main(["api-backend", "--tier", "minimal", "--dry-run", "--json"])
        self.assertEqual(code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "plan")
        self.assertEqual(payload["recipe"], "api-backend")
        self.assertEqual(payload["tier"], "minimal")
        self.assertIn("agency-backend-engineer", payload["profiles"])
        self.assertEqual(payload["stats"]["selected_profiles"], len(payload["profiles"]))


if __name__ == "__main__":
    unittest.main()
