"""Regression tests for CE learner-skill preservation and current docs."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
LEARNER = (ROOT / "shared-skills" / "academy-continuing-education" / "SKILL.md").read_text(encoding="utf-8")
ARCH = (REPO / "docs" / "CONTINUING_EDUCATION_ARCHITECTURE.md").read_text(encoding="utf-8")
GUIDE = (REPO / "docs" / "CONTINUING_EDUCATION.md").read_text(encoding="utf-8")



class LearnerSkillPreservationTests(unittest.TestCase):
    def test_inventory_before_learn_is_required(self):
        self.assertIn("Before `/learn`, record the learner's current skill names", LEARNER)

    def test_unrelated_skills_must_be_preserved(self):
        self.assertIn("preserve every unrelated existing skill", LEARNER)
        self.assertIn("must not delete, consolidate, rename, relocate, or overwrite unrelated learner skills", LEARNER)

    def test_post_learn_verifies_unrelated_skills(self):
        self.assertIn("every unrelated skill recorded before `/learn` still exists afterward", LEARNER)

    def test_skill_loss_fails_closed(self):
        self.assertIn("fails closed", LEARNER)
        self.assertIn("Do not report successful learning", LEARNER)

    def test_architecture_has_preservation_invariant(self):
        self.assertIn("**Learner skill preservation.**", ARCH)
        self.assertIn("unexplained loss, relocation, or overwrite fails the Continuing Education", ARCH.replace("\n", " "))

    def test_transport_is_no_longer_documented_as_deferred(self):
        self.assertIn("## Transport decision (selected)", ARCH)
        self.assertIn("canonical Bot Chat + native", ARCH)
        self.assertNotIn("## Transport decision (deferred)", ARCH)

    def test_docs_preserve_standard_release_compatibility_boundary(self):
        self.assertIn("Compatibility with the standard Hermes release is not yet guaranteed", GUIDE)
        self.assertIn("Compatibility with the standard Hermes release is not yet guaranteed", ARCH)
        self.assertIn("**Standard installation target.**", ARCH)


if __name__ == "__main__":
    unittest.main()