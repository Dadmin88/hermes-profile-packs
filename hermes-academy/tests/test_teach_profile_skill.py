"""Focused contract tests for the Academy instructor CE shared skill."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
MANIFEST = json.loads((ACADEMY_ROOT / "academy.json").read_text(encoding="utf-8"))


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        raise AssertionError(f"missing frontmatter key: {key}")
    return match.group(1).strip().strip('"\'')


class TeachProfileSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = CANONICAL.read_text(encoding="utf-8")
        cls.data = CANONICAL.read_bytes()

    def test_frontmatter_is_routing_safe(self):
        self.assertEqual(_frontmatter_value(self.text, "name"), "teach-profile")
        description = _frontmatter_value(self.text, "description")
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith("."))

    def test_human_and_profile_learning_modes_are_distinguished(self):
        self.assertIn("distinguish between a human learner and a Hermes-profile learner", self.text)
        self.assertIn("For a human learner, teach normally", self.text)
        self.assertIn("For a Hermes-profile learner, follow this contract", self.text)

    def test_instructor_authority_is_strictly_bounded(self):
        self.assertIn("Never edit the learner's skills", self.text)
        self.assertIn("Never ask for secrets, credentials, full memory", self.text)
        self.assertIn("The learner owns the `/learn` decision", self.text)
        for forbidden_system in (
            "Fleet",
            "Keryx",
            "Nodescale",
            "Templar",
            "RunAuthority",
            "Run Capsules",
        ):
            self.assertIn(forbidden_system, self.text)

    def test_minimum_sufficient_instruction_is_explicit(self):
        required = (
            "measurable competency transfer, not classroom roleplay",
            "Teach the smallest amount necessary",
            "logical functions, not mandatory conversational stages",
            "If the baseline already proves the requested competency, declare that no instruction is required.",
            "Teach only those gaps.",
            "If a message does none of these, omit it.",
            "Stop immediately once the requested competency is demonstrated.",
            "capability gain per unit of inference",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_transfer_is_required_when_instruction_occurred(self):
        self.assertIn("meaningfully different problem", self.text)
        self.assertIn("Do not accept any of the following as mastery", self.text)
        self.assertIn('"I understand"', self.text)
        self.assertIn("repeating the worked example", self.text)
        self.assertIn("correct only the failed part", self.text)

    def test_baseline_submission_forces_diagnostic_mode(self):
        self.assertIn("enter **BASELINE DIAGNOSTIC MODE** immediately", self.text)
        self.assertIn("Do **not** deliver a broad subject lecture", self.text)
        self.assertIn("Start from the submitted baseline", self.text)
        self.assertIn("Teach only those demonstrated gaps", self.text)
        self.assertIn("give exactly one meaningfully different problem", self.text)
        self.assertIn("do not include its answer key", self.text)

    def test_current_transfer_submission_forces_assessment_mode(self):
        self.assertIn("Current-message mode is authoritative", self.text)
        self.assertIn("enter **ASSESSMENT MODE** immediately", self.text)
        self.assertIn("Do **not** restart the lesson", self.text)
        self.assertIn("Evaluate the exact submitted baseline/transfer evidence", self.text)
        self.assertIn("Cite concrete details from the learner's submission", self.text)
        for outcome in ("**MASTERED**", "**NEEDS_CORRECTION**", "**BLOCKED**"):
            self.assertIn(outcome, self.text)
        self.assertIn("Do not substitute a generic lesson for an assessment", self.text)

    def test_mastery_outcomes_are_explicit_and_bounded(self):
        for outcome in ("**MASTERED**", "**NEEDS_CORRECTION**", "**BLOCKED**"):
            with self.subTest(outcome=outcome):
                self.assertIn(outcome, self.text)
        self.assertIn("Do not declare mastery because a conversation has been long enough", self.text)

    def test_completion_summary_supports_learner_native_learn(self):
        required = (
            "baseline capability already demonstrated",
            "gaps actually taught",
            "transfer evidence",
            "mastery outcome",
            "reusable principles or procedures worth retaining",
            "If the learner already had the capability or the session produced no reusable delta",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)
        self.assertIn("`skill_manage`", self.text)

    def test_all_academy_faculty_except_dean_materialize_canonical_bytes(self):
        names = [profile["name"] for profile in MANIFEST["profiles"]]
        faculty = [name for name in names if name != "academy-dean"]
        self.assertGreater(len(faculty), 0)
        for name in faculty:
            with self.subTest(profile=name):
                materialized = (
                    ACADEMY_ROOT
                    / "profiles"
                    / name
                    / "skills"
                    / "teach-profile"
                    / "SKILL.md"
                )
                self.assertTrue(materialized.is_file(), f"missing {materialized}")
                self.assertEqual(materialized.read_bytes(), self.data)

        dean_copy = (
            ACADEMY_ROOT
            / "profiles"
            / "academy-dean"
            / "skills"
            / "teach-profile"
            / "SKILL.md"
        )
        self.assertFalse(dean_copy.exists())


if __name__ == "__main__":
    unittest.main()
