from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profiles" / "agency-reverse-engineer"
ROLE_SKILLS = {
    "software-artifact-triage",
    "static-binary-analysis",
    "dynamic-behavior-analysis",
    "protocol-format-reconstruction",
}


class ReverseEngineerProfileTests(unittest.TestCase):
    def test_profile_is_registered_as_non_backbone_engineering_specialist(self):
        manifest = json.loads((ROOT / "agency.json").read_text(encoding="utf-8"))
        entries = [item for item in manifest["profiles"] if item["name"] == "agency-reverse-engineer"]
        self.assertEqual(
            entries,
            [{"name": "agency-reverse-engineer", "display_name": "Reverse Engineer", "category": "engineering"}],
        )
        self.assertNotIn("agency-reverse-engineer", manifest["backbone_profiles"])

    def test_profile_contains_approved_skills_and_safe_distribution(self):
        actual = {path.parent.name for path in (PROFILE / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, ROLE_SKILLS | {"academy-continuing-education"})
        distribution = (PROFILE / "distribution.yaml").read_text(encoding="utf-8")
        self.assertIn("name: agency-reverse-engineer", distribution)
        self.assertIn("  - academy-continuing-education", distribution)
        self.assertNotIn("model:", distribution)
        self.assertNotIn("provider:", distribution)

    def test_role_contract_preserves_authorization_containment_and_boundaries(self):
        soul = (PROFILE / "SOUL.md").read_text(encoding="utf-8").lower()
        self.assertIn("authorized", soul)
        self.assertIn("isolated environment", soul)
        self.assertIn("observation from inference", soul)
        for neighbor in (
            "agency-red-team",
            "agency-security-reviewer",
            "agency-security-engineer",
            "agency-security-operations-engineer",
            "agency-integration-engineer",
        ):
            self.assertIn(neighbor, soul)
        for prohibited in ("credential theft", "persistence", "safeguard bypasses"):
            self.assertIn(prohibited, soul)

    def test_routing_evals_cover_ownership_and_neighbor_boundaries(self):
        routing = json.loads((ROOT / "evals" / "routing.json").read_text(encoding="utf-8"))
        cases = {case["id"]: case["expected_profile"] for case in routing["cases"]}
        self.assertEqual(cases["reverse-engineer-ownership"], "agency-reverse-engineer")
        self.assertEqual(cases["reverse-engineer-red-team-boundary"], "agency-red-team")
        self.assertEqual(cases["reverse-engineer-security-review-boundary"], "agency-security-reviewer")
        self.assertEqual(cases["reverse-engineer-integration-boundary"], "agency-integration-engineer")
        self.assertEqual(cases["reverse-engineer-mobile-boundary"], "agency-mobile-engineer")
        self.assertEqual(
            cases["reverse-engineer-security-operations-boundary"],
            "agency-security-operations-engineer",
        )


if __name__ == "__main__":
    unittest.main()