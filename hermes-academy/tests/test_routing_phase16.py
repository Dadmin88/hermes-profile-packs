"""Phase 16 release regressions for deterministic Academy Dean routing."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
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


if __name__ == "__main__":
    unittest.main()
