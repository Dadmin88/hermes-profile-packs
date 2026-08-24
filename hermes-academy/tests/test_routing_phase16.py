"""Phase 16 release regressions for Academy Dean routing policy."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
DEAN_ROUTING_SKILL = (
    ACADEMY_ROOT
    / "profiles"
    / "academy-dean"
    / "skills"
    / "faculty-routing"
    / "SKILL.md"
)
sys.path.insert(0, str(ACADEMY_ROOT))

from routing import route_learner  # noqa: E402


class Phase16RoutingRegressionTests(unittest.TestCase):
    def test_natural_science_interdisciplinary_request_uses_science_broad_faculty(self):
        result = route_learner(
            "agency-research-analyst",
            "Compare physics, chemistry, and biology evidence for one scientific model",
        )
        self.assertEqual(result.faculty, "academy-natural-sciences-professor")
        self.assertTrue(result.approximate)
        self.assertIn("science", result.reason)

    def test_technology_interdisciplinary_request_uses_technology_broad_faculty(self):
        result = route_learner(
            "agency-backend-engineer",
            "Learn cybersecurity and Kubernetes distributed systems together",
        )
        self.assertEqual(result.faculty, "academy-computer-science-professor")
        self.assertTrue(result.approximate)
        self.assertIn("technology", result.reason)

    def test_cross_category_request_never_falls_into_unrelated_natural_sciences_chair(self):
        result = route_learner(
            "agency-project-manager",
            "Learn cybersecurity and project management for a secure delivery program",
        )
        self.assertIsNone(result.faculty)
        self.assertFalse(result.approximate)
        self.assertIn("multiple Academy domains", result.reason)

    def test_manifest_override_is_authoritative_for_specialist_routing(self):
        manifest = {
            "routing": {
                "specialist_preferences": {
                    "cybersecurity": "academy-physics-professor",
                },
                "broad_chairs": [],
            },
            "profiles": [
                {
                    "name": "academy-physics-professor",
                    "category": "science",
                    "role": "Custom manifest target used only by this test.",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "academy.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = route_learner(
                "agency-security-engineer",
                "Learn cybersecurity fundamentals",
                manifest_path=path,
            )

        self.assertEqual(result.faculty, "academy-physics-professor")
        self.assertFalse(result.approximate)

    def test_missing_specialist_uses_installed_category_fallback(self):
        result = route_learner(
            "agency-security-engineer",
            "Learn cybersecurity threat modeling",
            installed_profiles={"academy-computer-science-professor"},
        )
        self.assertEqual(result.faculty, "academy-computer-science-professor")
        self.assertTrue(result.approximate)
        self.assertIn("not installed", result.reason)

    def test_missing_specialist_and_fallback_fail_closed(self):
        result = route_learner(
            "agency-security-engineer",
            "Learn cybersecurity threat modeling",
            installed_profiles={"academy-history-professor"},
        )
        self.assertIsNone(result.faculty)
        self.assertFalse(result.approximate)

    def test_role_fallback_requires_unambiguous_exact_word_overlap(self):
        manifest = {
            "routing": {"specialist_preferences": {}, "broad_chairs": []},
            "profiles": [
                {
                    "name": "academy-alpha",
                    "category": "professional",
                    "role": "Teaches release planning and delivery sequencing.",
                },
                {
                    "name": "academy-beta",
                    "category": "professional",
                    "role": "Teaches release planning and launch coordination.",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "academy.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = route_learner(
                "agency-generalist",
                "Improve release planning",
                manifest_path=path,
            )

        self.assertIsNone(result.faculty)
        self.assertIn("equally close", result.reason)

    def test_role_fallback_ignores_uninstalled_profiles(self):
        manifest = {
            "routing": {"specialist_preferences": {}, "broad_chairs": []},
            "profiles": [
                {
                    "name": "academy-alpha",
                    "category": "professional",
                    "role": "Teaches release planning and delivery sequencing.",
                },
                {
                    "name": "academy-beta",
                    "category": "professional",
                    "role": "Teaches unrelated creative fundamentals.",
                },
            ],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "academy.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = route_learner(
                "agency-generalist",
                "Improve release planning and delivery sequencing",
                manifest_path=path,
                installed_profiles={"academy-beta"},
            )

        self.assertIsNone(result.faculty)
        self.assertIn("No installed Academy faculty", result.reason)


class InstalledDeanContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = DEAN_ROUTING_SKILL.read_text(encoding="utf-8")

    def test_installed_skill_does_not_depend_on_pack_root_routing_file(self):
        self.assertIn(
            "It is **not** a runtime dependency of the installed Dean profile",
            self.skill,
        )
        self.assertIn(
            "must not be assumed to exist after profile installation",
            self.skill,
        )

    def test_cross_category_contract_fails_closed(self):
        self.assertIn("**Cross-category objectives fail closed.**", self.skill)
        self.assertIn(
            "never route an unrelated cross-domain request to Natural Sciences",
            self.skill,
        )

    def test_missing_faculty_contract_uses_only_safe_installed_fallback(self):
        self.assertIn("**Missing specialist fallback.**", self.skill)
        self.assertIn("safe category fallback", self.skill)
        self.assertIn("report no safe installed match", self.skill)

    def test_dean_reply_contract_is_machine_legible_without_new_runtime(self):
        self.assertIn("FACULTY: academy-cybersecurity-instructor", self.skill)
        self.assertIn("MATCH: exact", self.skill)
        self.assertIn("FACULTY: NONE", self.skill)
        self.assertIn("MATCH: blocked", self.skill)
        self.assertIn("does not add a routing daemon", self.skill)


if __name__ == "__main__":
    unittest.main()
