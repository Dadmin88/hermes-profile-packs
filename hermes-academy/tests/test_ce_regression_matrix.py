"""Deterministic CE regression matrix for master-plan Phase 12.

These tests cover the behavior owned by Profile Packs: learner/instructor
contracts, Dean routing, source distribution, and the absence of a parallel CE
runtime. Native Hermes runtime mechanics (/goal, /subgoal, /learn, Bot Chat,
write approval) are deliberately referenced rather than reimplemented here.
"""
from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ACADEMY_ROOT.parent
LEARNER_PATH = ACADEMY_ROOT / "shared-skills" / "academy-continuing-education" / "SKILL.md"
INSTRUCTOR_PATH = ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"

import sys
sys.path.insert(0, str(ACADEMY_ROOT))
from routing import route_learner  # noqa: E402


class ContinuingEducationRegressionMatrix(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.learner = LEARNER_PATH.read_text(encoding="utf-8")
        cls.instructor = INSTRUCTOR_PATH.read_text(encoding="utf-8")
        cls.manifest = json.loads((ACADEMY_ROOT / "academy.json").read_text(encoding="utf-8"))

    # Phase 12 core cases -------------------------------------------------
    def test_01_user_names_instructor_directly(self):
        self.assertIn("If the user named an instructor", self.learner)
        self.assertIn("treat that choice as binding", self.learner)
        self.assertIn("Do not silently substitute or message a different instructor", self.learner)

    def test_02_dean_routes_instructor(self):
        result = route_learner(
            "agency-backend-engineer",
            "Improve my cybersecurity threat modeling for API services",
        )
        self.assertEqual(result.faculty, "academy-cybersecurity-instructor")
        self.assertFalse(result.approximate)

    def test_03_related_skill_uses_native_extend_path(self):
        self.assertIn("matching skill was **extended**", self.learner)
        self.assertIn("Prefer extension when native `/learn` identifies an existing relevant skill", self.learner)
        self.assertIn("Do not preselect or force the outcome in Academy logic", self.learner)

    def test_04_no_related_skill_uses_native_create_path(self):
        self.assertIn("new skill was **created**", self.learner)
        self.assertIn("otherwise allow normal `/learn` to create one", self.learner)

    def test_05_write_approval_is_respected(self):
        self.assertIn("`skills.write_approval`", self.learner)
        self.assertIn("Never bypass, auto-approve, or weaken it", self.learner)

    def test_06_more_practice_does_not_complete_early(self):
        self.assertIn("**NEEDS_CORRECTION**", self.instructor)
        self.assertIn("another bounded attempt is warranted", self.instructor)
        self.assertIn("Do not declare mastery because a conversation has been long enough", self.instructor)

    def test_07_new_deficiency_becomes_native_subgoal(self):
        self.assertIn("new required deficiency", self.learner)
        self.assertIn('goal_manage(action="add_subgoal"', self.learner)
        self.assertIn("native `/goal` and `/subgoal` state", self.learner)
        self.assertIn("Do not create subgoals for routine corrections", self.learner)

    def test_08_transfer_pass_is_required_after_instruction(self):
        self.assertIn("meaningfully different problem", self.learner)
        self.assertIn("Do not count acknowledgement", self.learner)
        self.assertIn("including transfer when instruction was required", self.instructor)

    def test_09_budget_exhaustion_pauses_not_succeeds(self):
        self.assertIn("normal bounded goal budget", self.learner)
        self.assertIn("Training paused because the learning objective has not yet been demonstrated.", self.learner)
        self.assertIn("Never convert budget exhaustion into success", self.learner)

    def test_10_teacher_unavailable_has_terminal_outcome(self):
        self.assertIn("unavailable-instructor", self.learner)
        self.assertIn("the instructor is unavailable", self.learner)

    def test_11_missing_teacher_is_never_invented(self):
        self.assertIn("Do not invent a faculty profile that is not installed", self.learner)
        names = {profile["name"] for profile in self.manifest["profiles"]}
        result = route_learner("agency-backend-engineer", "advanced basket weaving")
        if result.faculty is not None:
            self.assertIn(result.faculty, names)
            self.assertTrue(result.approximate)

    def test_12_user_cancel_is_native_goal_control(self):
        self.assertIn("Stop the class", self.learner)
        self.assertIn("native goal/preemption behavior", self.learner)
        self.assertIn("Stop when asked", self.learner)

    def test_13_user_changes_objective_midway(self):
        self.assertIn("Focus more on OAuth", self.learner)
        self.assertIn("Also teach token rotation", self.learner)
        self.assertIn("update the active objective/criteria", self.learner)

    def test_14_goal_restart_state_is_not_reimplemented_in_profile_packs(self):
        self.assertIn("Bot-Chat-only `goal_manage` bridge", self.learner)
        self.assertIn("wraps Hermes' existing `GoalManager`", self.learner)
        self.assertIn("never imitate its loop, persistence, approval, or completion logic", self.learner)
        self.assertNotIn("goal_state.json", self.learner)

    def test_15_bot_chat_resume_is_delegated_to_native_transport(self):
        self.assertIn("canonical Bot Chat", self.learner)
        self.assertIn("native `message_agent`", self.learner)
        self.assertIn("native `/goal` peer-wait behavior", self.learner)

    def test_16_fresh_session_skill_reuse_is_normal_hermes_skill_persistence(self):
        self.assertIn("learner-local skill", self.learner)
        self.assertIn("learner-profile location", self.learner)
        self.assertIn("reusable behavior, procedure, or decision criteria", self.learner)

    def test_17_teacher_store_is_not_authorized_for_learning_writes(self):
        self.assertIn("must never edit this learner's skills", self.learner)
        self.assertIn("The instructor must never write the skill", self.learner)
        self.assertIn("Never edit the learner's skills", self.instructor)

    def test_18_profile_pack_source_never_receives_local_learning(self):
        self.assertIn("Never modify Profile Packs source", self.learner)
        self.assertIn("Do not modify Academy or Agency source distributions", self.learner)

    def test_19_no_recursive_training_chain(self):
        self.assertIn("Do not silently start another class", self.learner)
        self.assertIn("explicit learner decision under the active goal", self.learner)
        self.assertIn("instead of silently starting a recursive second class", self.learner)

    def test_20_no_fleet_runtime_dependency(self):
        python_files = [
            ACADEMY_ROOT / "routing.py",
            ACADEMY_ROOT / "install.py",
            ACADEMY_ROOT / "validate.py",
        ]
        forbidden_import = re.compile(r"^\s*(?:from|import)\s+(?:fleet|keryx|nodescale)(?:\b|\.)", re.I | re.M)
        for path in python_files:
            with self.subTest(path=path.name):
                self.assertIsNone(forbidden_import.search(path.read_text(encoding="utf-8")))
        self.assertIn("Do not depend on a separate distributed runtime", self.learner)

    # Distribution/source integrity --------------------------------------
    def test_21_agency_materialized_copies_match_canonical_source(self):
        canonical = LEARNER_PATH.read_bytes()
        agency_manifest = json.loads(
            (REPO_ROOT / "hermes-agency" / "agency.json").read_text(encoding="utf-8")
        )
        for profile in agency_manifest["profiles"]:
            materialized = (
                REPO_ROOT / "hermes-agency" / "profiles" / profile["name"]
                / "skills" / "academy-continuing-education" / "SKILL.md"
            )
            with self.subTest(profile=profile["name"]):
                self.assertEqual(materialized.read_bytes(), canonical)

    def test_22_instructor_copies_match_canonical_source_and_exclude_dean(self):
        canonical = INSTRUCTOR_PATH.read_bytes()
        for profile in self.manifest["profiles"]:
            materialized = (
                ACADEMY_ROOT / "profiles" / profile["name"] / "skills"
                / "teach-profile" / "SKILL.md"
            )
            if profile["name"] == "academy-dean":
                self.assertFalse(materialized.exists())
            else:
                with self.subTest(profile=profile["name"]):
                    self.assertEqual(materialized.read_bytes(), canonical)

    def test_23_routing_never_returns_profile_absent_from_manifest(self):
        installed = {p["name"] for p in self.manifest["profiles"]}
        objectives = (
            "thermodynamics",
            "query optimization",
            "API authorization security",
            "classical guitar harmony",
            "advanced basket weaving",
            "base jumping",
        )
        for objective in objectives:
            result = route_learner("agency-generalist", objective)
            with self.subTest(objective=objective):
                if result.faculty is not None:
                    self.assertIn(result.faculty, installed)


if __name__ == "__main__":
    unittest.main()
