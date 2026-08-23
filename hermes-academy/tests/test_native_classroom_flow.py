"""Phase 7-9 contract tests for native Academy classroom orchestration."""
from __future__ import annotations

import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
LEARNER_SKILL = ACADEMY_ROOT / "shared-skills" / "academy-continuing-education" / "SKILL.md"
INSTRUCTOR_SKILL = ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"


class NativeGoalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.learner = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.instructor = INSTRUCTOR_SKILL.read_text(encoding="utf-8")

    def test_real_native_goal_and_subgoal_handlers_are_required(self):
        self.assertIn('goal_manage(action="set"', self.learner)
        self.assertIn('goal_manage(action="add_subgoal"', self.learner)
        self.assertIn("native `/goal` and `/subgoal` state", self.learner)
        self.assertIn("wraps Hermes' existing `GoalManager`", self.learner)
        self.assertIn("never imitate its loop, persistence, approval, or completion logic", self.learner)
        self.assertIn("Do not create a second orchestration loop around it", self.learner)

    def test_completion_contract_inputs_are_explicit(self):
        for marker in (
            "this learner's profile/role",
            "the target competency",
            "the selected instructor",
            "domain-appropriate evidence",
            "budget-exhausted",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.learner)

    def test_subgoal_is_only_for_new_required_deficiency(self):
        self.assertIn("new required deficiency", self.learner)
        self.assertIn("Do not create subgoals for routine corrections", self.learner)

    def test_goal_budget_never_becomes_false_success(self):
        self.assertIn("normal bounded goal budget", self.learner)
        self.assertIn(
            "Training paused because the learning objective has not yet been demonstrated.",
            self.learner,
        )
        self.assertIn("Never convert budget exhaustion into success", self.learner)


class NativeClassroomLoopTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.learner = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.instructor = INSTRUCTOR_SKILL.read_text(encoding="utf-8")

    def test_transport_is_native_message_agent_and_peer_wait(self):
        self.assertIn("native `message_agent` in canonical Bot Chat", self.learner)
        self.assertIn("native `/goal` peer-wait behavior", self.learner)
        self.assertIn("Do not send duplicate requests", self.learner)
        self.assertIn("burn turns", self.learner)

    def test_no_acknowledgement_ping_pong(self):
        self.assertIn("acknowledgement turns", self.learner)
        self.assertIn("acknowledgement ping-pong", self.instructor)
        self.assertIn("If a message does none of these, omit it", self.instructor)

    def test_user_visibility_is_concise_not_chatty(self):
        self.assertIn("Keep user-visible status concise", self.learner)
        self.assertIn("Do not narrate every Bot message", self.learner)
        self.assertIn("Learning: Backend Engineer → API security with Cybersecurity Instructor.", self.learner)

    def test_user_can_interrupt_or_change_objective(self):
        for marker in (
            "Stop the class",
            "Focus more on OAuth",
            "Also teach token rotation",
            "native goal/preemption behavior",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.learner)

    def test_every_instructor_message_has_a_job(self):
        for marker in (
            "diagnose a remaining gap",
            "teach a demonstrated gap",
            "assess application",
            "correct a specific failure",
            "conclude mastery",
            "report a genuine blocker",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.instructor)


class NativeLearnHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.learner = LEARNER_SKILL.read_text(encoding="utf-8")
        cls.instructor = INSTRUCTOR_SKILL.read_text(encoding="utf-8")

    def test_learn_happens_only_after_real_transfer(self):
        self.assertIn("meaningfully different problem", self.learner)
        self.assertIn("Stop as soon as the completion contract is satisfied", self.learner)
        self.assertIn("If there is no reusable delta, skip `/learn`", self.learner)
        self.assertIn("including transfer when instruction was required", self.instructor)

    def test_write_approval_is_never_bypassed(self):
        self.assertIn("`skills.write_approval`", self.learner)
        self.assertIn("normal Hermes approval boundary", self.learner)
        self.assertIn("Never bypass, auto-approve, or weaken it", self.learner)

    def test_create_and_extend_are_both_native_outcomes(self):
        self.assertIn("matching skill was **extended**", self.learner)
        self.assertIn("new skill was **created**", self.learner)
        self.assertIn("Prefer extension when native `/learn` identifies an existing relevant skill", self.learner)
        self.assertIn("Do not preselect or force the outcome in Academy logic", self.learner)

    def test_result_verification_is_complete(self):
        for marker in (
            "skill name",
            "purpose",
            "learner-profile location",
            "reusable behavior, procedure, or decision criteria",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.learner)

    def test_teacher_never_writes_the_skill(self):
        self.assertIn("The instructor must never write the skill", self.learner)
        self.assertIn("The learner owns the `/learn` decision", self.instructor)


class NoParallelRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.learner = LEARNER_SKILL.read_text(encoding="utf-8")

    def test_no_parallel_academy_runtime_is_introduced(self):
        for marker in (
            "Do not create a scheduler",
            "training database",
            "candidate-skill registry",
            "parallel memory store",
            "alternate message bus",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.learner)

    def test_forbidden_distributed_dependencies_remain_forbidden(self):
        for marker in (
            "Fleet",
            "Keryx",
            "Nodescale",
            "Templar",
            "RunAuthority",
            "Run Capsules",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.learner)


if __name__ == "__main__":
    unittest.main()
