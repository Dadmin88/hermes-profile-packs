import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profiles" / "agency-botfather"
SKILL = PROFILE / "skills" / "profile-pack-authoring"
REVISION = "93eb3b6d3976b115a372598fa5c02c4f6ab63ed2"


class BotFatherProfileTests(unittest.TestCase):
    def test_profile_is_registered_as_an_engineering_specialist(self):
        manifest = json.loads((ROOT / "agency.json").read_text(encoding="utf-8"))
        entries = [
            profile
            for profile in manifest["profiles"]
            if profile["name"] == "agency-botfather"
        ]

        self.assertEqual(
            entries,
            [
                {
                    "name": "agency-botfather",
                    "display_name": "BotFather",
                    "category": "engineering",
                }
            ],
        )
        self.assertEqual(manifest["profile_count"], len(manifest["profiles"]))
        self.assertEqual(
            manifest["categories"]["engineering"],
            sum(profile["category"] == "engineering" for profile in manifest["profiles"]),
        )
        self.assertNotIn("agency-botfather", manifest["backbone_profiles"])

    def test_profile_contains_the_approved_portable_artifacts(self):
        self.assertTrue((PROFILE / "SOUL.md").is_file())
        self.assertTrue((PROFILE / "distribution.yaml").is_file())
        self.assertTrue((PROFILE / ".no-bundled-skills").is_file())
        self.assertTrue((SKILL / "SKILL.md").is_file())
        self.assertTrue((SKILL / "SOURCE.md").is_file())

        distribution = (PROFILE / "distribution.yaml").read_text(encoding="utf-8")
        self.assertIn("name: agency-botfather", distribution)
        self.assertNotIn("model:", distribution)
        self.assertNotIn("provider:", distribution)

    def test_role_contract_has_approval_portability_and_neighbor_boundaries(self):
        soul = (PROFILE / "SOUL.md").read_text(encoding="utf-8")
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        combined = f"{soul}\n{skill}".lower()

        self.assertIn("human approval", combined)
        self.assertIn("portable", combined)
        self.assertIn("another botfather", combined)
        for neighbor in (
            "agency-orchestrator",
            "agency-ai-engineer",
            "agency-tools-engineer",
            "agency-open-source-maintainer",
        ):
            self.assertIn(neighbor, soul)

        self.assertNotIn("hermes profile create", combined)
        self.assertNotIn("config set model", combined)
        self.assertNotIn("disable_protected", combined)

    def test_source_note_preserves_pinned_mit_provenance(self):
        source = (SKILL / "SOURCE.md").read_text(encoding="utf-8")
        self.assertIn("https://github.com/techjanitor/botmaker", source)
        self.assertIn(REVISION, source)
        self.assertIn("License: MIT", source)
        self.assertIn("Copyright (c) 2026 techjanitor", source)
        self.assertIn("Permission is hereby granted", source)
        self.assertIn("THE SOFTWARE IS PROVIDED \"AS IS\"", source)

    def test_routing_evals_cover_ownership_and_neighbor_boundaries(self):
        routing = json.loads((ROOT / "evals" / "routing.json").read_text(encoding="utf-8"))
        cases = {case["id"]: case["expected_profile"] for case in routing["cases"]}
        self.assertEqual(cases["botfather-ownership"], "agency-botfather")
        self.assertEqual(
            cases["botfather-orchestrator-boundary"], "agency-orchestrator"
        )
        self.assertEqual(cases["botfather-ai-engineer-boundary"], "agency-ai-engineer")
        self.assertEqual(
            cases["botfather-tools-engineer-boundary"], "agency-tools-engineer"
        )
        self.assertEqual(
            cases["botfather-maintainer-boundary"], "agency-open-source-maintainer"
        )


if __name__ == "__main__":
    unittest.main()
