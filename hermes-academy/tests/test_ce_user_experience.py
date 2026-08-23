"""Nontechnical UX regression tests for Academy CE Phase 13."""
from __future__ import annotations

import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
LEARNER = (
    ACADEMY_ROOT / "shared-skills" / "academy-continuing-education" / "SKILL.md"
).read_text(encoding="utf-8")


class ContinuingEducationUserExperienceTests(unittest.TestCase):
    def test_natural_language_intent_is_primary(self):
        for phrase in (
            "asks this profile to learn",
            "study",
            "take a class",
            "improve at a bounded competency",
            "get better at something",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, LEARNER)

    def test_user_does_not_need_slash_syntax(self):
        self.assertIn("The user should not have to know or type slash-command syntax", LEARNER)
        self.assertIn("Do not expose `/goal`, `/subgoal`, `message_agent`, `/learn`, or `skill_manage`", LEARNER)

    def test_start_message_is_compact_and_outcome_oriented(self):
        self.assertIn(
            "Learning: API security with Cybersecurity Instructor. I'll report back after I can demonstrate it.",
            LEARNER,
        )

    def test_progress_only_reports_meaningful_change(self):
        self.assertIn(
            "The instructor found a gap in my authorization-boundary reasoning. I'm working one more case.",
            LEARNER,
        )
        self.assertIn("Do not send routine status for every exchange", LEARNER)
        self.assertIn("Silence is better than token-burning narration", LEARNER)

    def test_approval_message_is_understandable_without_internal_commands(self):
        self.assertIn(
            "I learned something reusable, but Hermes is waiting for your approval before saving the skill change.",
            LEARNER,
        )

    def test_completion_reports_instructor_objective_assessment_and_learning(self):
        completion = (
            "Continuing education complete. Instructor: Cybersecurity Instructor. "
            "Objective: API authentication and authorization. Assessment: passed on a different design case. "
            "Hermes learning: extended auth-boundary-review."
        )
        self.assertIn(completion, LEARNER)

    def test_already_mastered_path_does_not_fake_training(self):
        self.assertIn(
            "Competency already demonstrated. No instruction or skill update was needed.",
            LEARNER,
        )

    def test_user_interrupt_examples_remain_available(self):
        for phrase in ("Stop the class", "Focus more on OAuth", "Also teach token rotation"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, LEARNER)


if __name__ == "__main__":
    unittest.main()
