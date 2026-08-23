"""Phase 13 contract tests for nontechnical conversational UX polish.

Validates that user-facing message templates exist, are free of internal
Hermes terms, and that completion messages carry all required information.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
LEARNER_SKILL = ACADEMY_ROOT / "shared-skills" / "academy-continuing-education" / "SKILL.md"

# Internal Hermes terms that must never appear in user-facing message templates
INTERNAL_TERMS = (
    "/goal",
    "/learn",
    "message_agent",
    "skill_manage",
    "subgoal",
    "peer-wait",
)


def _extract_template_block(text: str, heading: str) -> str:
    """Extract the content under a ### heading within the User-facing messages section."""
    # Find the User-facing messages section
    ux_match = re.search(r"^## User-facing messages\s*$", text, re.MULTILINE)
    if not ux_match:
        raise AssertionError("missing '## User-facing messages' section")
    ux_start = ux_match.end()

    # Find the next ## heading after User-facing messages (ends the section)
    next_h2 = re.search(r"^## (?!User-facing messages)", text[ux_start:], re.MULTILINE)
    ux_text = text[ux_start:ux_start + next_h2.start()] if next_h2 else text[ux_start:]

    # Find the specific ### heading within the section
    heading_pattern = rf"^### {re.escape(heading)}\s*$"
    heading_match = re.search(heading_pattern, ux_text, re.MULTILINE)
    if not heading_match:
        raise AssertionError(f"missing '### {heading}' in User-facing messages section")
    block_start = heading_match.end()

    # Find the next ### or end of section
    next_h3 = re.search(r"^### ", ux_text[block_start:], re.MULTILINE)
    block = ux_text[block_start:block_start + next_h3.start()] if next_h3 else ux_text[block_start:]
    return block


class UserFacingMessagesSectionTests(unittest.TestCase):
    """The User-facing messages section exists and has all required subsections."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")

    def test_user_facing_messages_section_exists(self):
        self.assertIn("## User-facing messages", self.text)

    def test_all_message_types_have_templates(self):
        required_headings = (
            "Start",
            "Progress",
            "Paused / blocked",
            "Approval required",
            "Cancelled",
            "Completion",
            "Interruption handling",
        )
        for heading in required_headings:
            with self.subTest(heading=heading):
                block = _extract_template_block(self.text, heading)
                self.assertGreater(len(block.strip()), 0, f"empty template for '{heading}'")


class InternalTermExclusionTests(unittest.TestCase):
    """User-facing message templates must not contain internal Hermes terms."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")

    def test_no_internal_terms_in_user_facing_section(self):
        """Each subsection of User-facing messages must be free of internal terms.

        This is a structural check: every ### subsection must exist and its
        extracted block must not contain internal terms.  The per-template
        tests below provide finer-grained coverage; this test ensures no
        subsection was accidentally omitted.
        """
        subsections = (
            "Start",
            "Progress",
            "Paused / blocked",
            "Approval required",
            "Cancelled",
            "Completion",
            "Interruption handling",
        )
        for heading in subsections:
            with self.subTest(heading=heading):
                block = _extract_template_block(self.text, heading)
                for term in INTERNAL_TERMS:
                    self.assertNotIn(
                        term, block,
                        f"internal term '{term}' found in '{heading}' template",
                    )

    def test_no_internal_terms_in_start_template(self):
        block = _extract_template_block(self.text, "Start")
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, block)

    def test_no_internal_terms_in_completion_template(self):
        block = _extract_template_block(self.text, "Completion")
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, block)

    def test_no_internal_terms_in_progress_template(self):
        block = _extract_template_block(self.text, "Progress")
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, block)

    def test_no_internal_terms_in_paused_blocked_template(self):
        block = _extract_template_block(self.text, "Paused / blocked")
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, block)

    def test_no_internal_terms_in_approval_required_template(self):
        block = _extract_template_block(self.text, "Approval required")
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, block)

    def test_no_internal_terms_in_cancelled_template(self):
        block = _extract_template_block(self.text, "Cancelled")
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, block)

    def test_no_internal_terms_in_interruption_handling_template(self):
        block = _extract_template_block(self.text, "Interruption handling")
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, block)


class CompletionMessageContractTests(unittest.TestCase):
    """Completion messages must name instructor, topic, assessment result, and skill."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.completion = _extract_template_block(cls.text, "Completion")

    def test_completion_names_instructor(self):
        self.assertIn("{Instructor}", self.completion)

    def test_completion_names_topic(self):
        self.assertIn("{Topic}", self.completion)

    def test_completion_includes_assessment_result(self):
        self.assertIn("Assessment result", self.completion)

    def test_completion_includes_skill_name(self):
        self.assertIn("skill name", self.completion)

    def test_completion_distinguishes_created_vs_extended(self):
        self.assertIn("created/extended", self.completion)

    def test_completion_handles_no_reusable_delta(self):
        self.assertIn("No new skill needed", self.completion)


class StartMessageContractTests(unittest.TestCase):
    """Start messages must be compact and name the instructor and topic."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.start = _extract_template_block(cls.text, "Start")

    def test_start_names_instructor(self):
        self.assertIn("{Instructor}", self.start)

    def test_start_names_topic(self):
        self.assertIn("{Topic}", self.start)

    def test_start_is_compact(self):
        """The start template should be one line, not a paragraph."""
        lines = [l.strip() for l in self.start.strip().splitlines() if l.strip() and not l.strip().startswith("#")]
        # Should be essentially one template line (plus maybe a description line)
        template_lines = [l for l in lines if l.startswith("`")]
        self.assertLessEqual(len(template_lines), 1, "start template should be a single line")


class InterruptionHandlingTests(unittest.TestCase):
    """Interruption phrases must map to defined natural-language responses."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.interruption = _extract_template_block(cls.text, "Interruption handling")

    def test_stop_the_class_is_handled(self):
        self.assertIn("Stop the class", self.text)

    def test_focus_change_is_handled(self):
        self.assertIn("Shifting focus", self.interruption)

    def test_topic_addition_is_handled(self):
        self.assertIn("Adding", self.interruption)

    def test_interruption_messages_are_nontechnical(self):
        for term in INTERNAL_TERMS:
            with self.subTest(term=term):
                self.assertNotIn(term, self.interruption)


class PausedBlockedMessageTests(unittest.TestCase):
    """Paused/blocked messages must explain what happened and what to do next."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.paused = _extract_template_block(cls.text, "Paused / blocked")

    def test_budget_exhaustion_mentions_resume(self):
        self.assertIn("resume", self.paused.lower())

    def test_budget_exhaustion_mentions_cancel(self):
        self.assertIn("cancel", self.paused.lower())

    def test_external_blocker_explains_unblock_condition(self):
        self.assertIn("unblock condition", self.paused)


class ApprovalRequiredMessageTests(unittest.TestCase):
    """Approval-required messages must be clear about what needs approval."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.approval = _extract_template_block(cls.text, "Approval required")

    def test_approval_mentions_skill(self):
        self.assertIn("skill", self.approval.lower())

    def test_approval_mentions_approve_and_decline(self):
        self.assertIn("Approve", self.approval)
        self.assertIn("decline", self.approval.lower())


class NaturalLanguageOnlyContractTests(unittest.TestCase):
    """The skill explicitly requires natural language for user-facing messages."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.text = LEARNER_SKILL.read_text(encoding="utf-8")

    def test_natural_language_only_is_stated(self):
        self.assertIn(
            "All ordinary messages to the user must be natural language",
            self.text,
        )

    def test_mechanism_is_invisible_to_user(self):
        self.assertIn("the mechanism is invisible", self.text)

    def test_never_expose_internal_terms_is_stated(self):
        self.assertIn("Never expose internal Hermes terms", self.text)


if __name__ == "__main__":
    unittest.main()
