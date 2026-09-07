from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
PROFILE = ROOT / "profiles" / "agency-hermes-config-manager"
ROLE_SKILLS = {"hermes-config-inventory", "profile-selection-and-change-plan", "bulk-config-rollout", "config-verification-and-rollback"}
ROUTING_IDS = {"hermes-config-manager-ownership", "hermes-config-manager-botfather-boundary", "hermes-config-manager-automation-boundary", "hermes-config-manager-support-boundary", "hermes-config-manager-infrastructure-boundary", "hermes-config-manager-orchestrator-boundary"}


class HermesConfigManagerProfileTests(unittest.TestCase):
    def test_profile_is_registered_as_non_backbone_engineering_specialist(self):
        manifest = json.loads((ROOT / "agency.json").read_text(encoding="utf-8"))
        entries = [item for item in manifest["profiles"] if item["name"] == "agency-hermes-config-manager"]
        self.assertEqual(entries, [{"name": "agency-hermes-config-manager", "display_name": "Hermes Configuration Manager", "category": "engineering"}])
        self.assertNotIn("agency-hermes-config-manager", manifest["backbone_profiles"])

    def test_distribution_contains_only_approved_profile_capabilities(self):
        actual = {path.parent.name for path in (PROFILE / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, ROLE_SKILLS | {"academy-continuing-education"})
        distribution = (PROFILE / "distribution.yaml").read_text(encoding="utf-8")
        self.assertIn("name: agency-hermes-config-manager", distribution)
        self.assertIn("  - academy-continuing-education", distribution)
        self.assertNotIn("model:", distribution)
        self.assertNotIn("provider:", distribution)

    def test_role_contract_requires_preview_approval_verification_and_secret_safety(self):
        content = "\n".join(path.read_text(encoding="utf-8") for path in [PROFILE / "SOUL.md", *sorted(PROFILE.glob("skills/*/SKILL.md"))]).lower()
        for phrase in ("dry-run", "exact target list", "read back every", "rollback", "exclude this active profile", "never place an api key in a command argument", "never directly edit configuration yaml"):
            self.assertIn(phrase, content)
        for neighbor in ("agency-botfather", "agency-automation-engineer", "agency-tools-engineer", "agency-platform-engineer", "agency-technical-support-engineer", "agency-infrastructure-engineer", "agency-orchestrator"):
            self.assertIn(neighbor, content)

    def test_cli_recommender_executes_all_routing_boundaries(self):
        routing = json.loads((ROOT / "evals" / "routing.json").read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in routing["cases"] if case["id"].startswith("hermes-config-manager-")}
        self.assertEqual(set(cases), ROUTING_IDS)
        for case_id in sorted(ROUTING_IDS):
            case = cases[case_id]
            with self.subTest(case=case_id):
                result = subprocess.run([sys.executable, str(REPO_ROOT / "install.py"), "--pack", "agency", "--recommend", case["task"], "--limit", "1", "--json"], cwd=REPO_ROOT, text=True, capture_output=True, check=False)
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(payload["recommendations"][0]["name"], case["expected_profile"])


if __name__ == "__main__":
    unittest.main()