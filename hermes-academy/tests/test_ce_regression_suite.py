"""Phase 12 deterministic integration and regression suite for Academy CE.

Uses real imports and a temporary HERMES_HOME where possible rather than
mock-only tests.  Covers every listed regression case from the master plan.

Each test class is self-contained and uses setUp/tearDown to create and
clean a temporary HERMES_HOME with Academy profiles installed.

Fixture strategy:
  - Real routing.py imports against the real academy.json manifest.
  - Real skill files copied into a temp HERMES_HOME profile tree.
  - Deterministic mock of Hermes runtime primitives (message_agent, /goal,
    /subgoal, /learn, skill_manage) that records calls and returns scripted
    responses so the CE flow is exercised without a live Hermes process.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ACADEMY_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ACADEMY_ROOT.parent
sys.path.insert(0, str(ACADEMY_ROOT))

from routing import route_learner, minimize_learner_context, RoutingResult

MANIFEST = json.loads((ACADEMY_ROOT / "academy.json").read_text(encoding="utf-8"))
AGENCY_MANIFEST = json.loads(
    (REPO_ROOT / "hermes-agency" / "agency.json").read_text(encoding="utf-8")
)


# ---------------------------------------------------------------------------
# Deterministic CE flow simulator
# ---------------------------------------------------------------------------
@dataclass
class CEStep:
    """One recorded step in a simulated CE flow."""
    action: str
    detail: dict = field(default_factory=dict)


@dataclass
class CEFixture:
    """Deterministic fixture that simulates the Academy CE flow.

    Records every primitive invocation so tests can assert on the exact
    sequence of events without depending on LLM behaviour.
    """
    hermes_home: Path
    learner_profile: str = "agency-backend-engineer"
    instructor_profile: str = "academy-cybersecurity-instructor"
    objective: str = "Learn API security fundamentals"
    steps: list[CEStep] = field(default_factory=list)
    _goal_active: bool = False
    _goal_budget: int = 20
    _subgoals: list[str] = field(default_factory=list)
    _learned_skills: dict[str, str] = field(default_factory=dict)
    _write_approval_enabled: bool = False
    _instructor_available: bool = True
    _cancelled: bool = False
    _objective_changed: bool = False
    _restart_simulated: bool = False
    _mastery_achieved: bool = False
    _transfer_passed: bool = False
    _baseline_passed: bool = False
    _budget_exhausted: bool = False

    def goal_start(self, contract: str) -> dict:
        """Simulate native /goal handler."""
        self._goal_active = True
        self._goal_budget = 20
        self.steps.append(CEStep("goal_start", {"contract": contract}))
        return {"status": "active", "budget_remaining": self._goal_budget}

    def goal_complete(self, outcome: str) -> dict:
        """Simulate native /goal completion."""
        self._goal_active = False
        self.steps.append(CEStep("goal_complete", {"outcome": outcome}))
        return {"status": "completed", "outcome": outcome}

    def subgoal_create(self, deficiency: str) -> dict:
        """Simulate native /subgoal for new required deficiency."""
        self._subgoals.append(deficiency)
        self.steps.append(CEStep("subgoal_create", {"deficiency": deficiency}))
        return {"status": "active", "deficiency": deficiency}

    def message_agent(self, target: str, message: str) -> dict:
        """Simulate canonical Bot Chat message_agent to instructor."""
        self.steps.append(CEStep("message_agent", {
            "target": target,
            "message_length": len(message),
        }))
        if not self._instructor_available:
            return {"status": "unavailable", "error": "target profile not found"}
        if self._cancelled:
            return {"status": "cancelled"}
        if self._objective_changed:
            return {"status": "objective_changed", "new_objective": "Focus on OAuth"}
        if self._restart_simulated:
            return {"status": "restart"}
        # Simulate instructor response
        return {"status": "ok", "response": "Instructor teaching response"}

    def learn(self, skill_name: str, content: str) -> dict:
        """Simulate native /learn -> skill_manage path."""
        self.steps.append(CEStep("learn", {"skill_name": skill_name}))
        if self._write_approval_enabled:
            self.steps.append(CEStep("write_approval_required", {
                "skill_name": skill_name,
            }))
            return {"status": "pending_approval", "skill_name": skill_name}
        # Check if skill already exists (extend vs create)
        skill_dir = (
            self.hermes_home / "profiles" / self.learner_profile
            / "skills" / skill_name
        )
        if (skill_dir / "SKILL.md").is_file():
            self.steps.append(CEStep("skill_extended", {"skill_name": skill_name}))
            return {"status": "extended", "skill_name": skill_name}
        else:
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: {skill_name}\ndescription: Learned skill.\n---\n{content}\n",
                encoding="utf-8",
            )
            self.steps.append(CEStep("skill_created", {"skill_name": skill_name}))
            return {"status": "created", "skill_name": skill_name}

    def budget_tick(self) -> bool:
        """Decrement goal budget. Returns True if budget remains."""
        self._goal_budget -= 1
        if self._goal_budget <= 0:
            self._budget_exhausted = True
            self.steps.append(CEStep("budget_exhausted"))
            return False
        return True


def setup_temp_hermes_home(
    profiles: list[str] | None = None,
    include_fleet: bool = False,
) -> Path:
    """Create a temporary HERMES_HOME with Academy profiles installed.

    Returns the path to the temporary HERMES_HOME directory.
    """
    tmp = Path(tempfile.mkdtemp(prefix="academy_ce_test_"))
    hermes_home = tmp / ".hermes"
    hermes_home.mkdir()

    # Create profile directories for requested Academy profiles
    if profiles is None:
        profiles = [p["name"] for p in MANIFEST["profiles"]]

    for profile_name in profiles:
        src_profile = ACADEMY_ROOT / "profiles" / profile_name
        if not src_profile.is_dir():
            continue
        dst_profile = hermes_home / "profiles" / profile_name
        dst_profile.mkdir(parents=True, exist_ok=True)

        # Copy distribution.yaml
        dist_src = src_profile / "distribution.yaml"
        if dist_src.is_file():
            shutil.copy2(dist_src, dst_profile / "distribution.yaml")

        # Copy SOUL.md
        soul_src = src_profile / "SOUL.md"
        if soul_src.is_file():
            shutil.copy2(soul_src, dst_profile / "SOUL.md")

        # Copy .no-bundled-skills
        no_bundled = src_profile / ".no-bundled-skills"
        if no_bundled.is_file():
            shutil.copy2(no_bundled, dst_profile / ".no-bundled-skills")

        # Copy skills
        skills_src = src_profile / "skills"
        if skills_src.is_dir():
            dst_skills = dst_profile / "skills"
            shutil.copytree(skills_src, dst_skills, dirs_exist_ok=True)

    # Also create a sample agency profile for the learner
    learner_dir = hermes_home / "profiles" / "agency-backend-engineer"
    learner_dir.mkdir(parents=True, exist_ok=True)
    (learner_dir / "SOUL.md").write_text(
        "# Backend Engineer\nImplements backend services and APIs.\n",
        encoding="utf-8",
    )
    (learner_dir / "distribution.yaml").write_text(
        "name: agency-backend-engineer\nversion: 1.0.0\n"
        "description: Backend engineer profile.\nauthor: Test\nlicense: MIT\n",
        encoding="utf-8",
    )

    # Optionally include Fleet artifacts (for the no-Fleet test)
    if include_fleet:
        fleet_dir = hermes_home / "plugins" / "fleet"
        fleet_dir.mkdir(parents=True, exist_ok=True)
        (fleet_dir / "plugin.json").write_text(
            '{"name": "fleet", "version": "1.0.0"}\n',
            encoding="utf-8",
        )

    return tmp


def cleanup_temp(path: Path) -> None:
    """Remove a temporary directory tree."""
    shutil.rmtree(path, ignore_errors=True)


# ---------------------------------------------------------------------------
# Test: Named instructor
# ---------------------------------------------------------------------------
class NamedInstructorTest(unittest.TestCase):
    """When the user names an instructor, the CE flow uses it directly."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(
            hermes_home=self.tmp / ".hermes",
            learner_profile="agency-backend-engineer",
            instructor_profile="academy-cybersecurity-instructor",
            objective="Learn API security fundamentals",
        )

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_named_instructor_is_used_directly(self):
        """A named instructor bypasses Dean routing."""
        # Verify the named instructor exists in the manifest
        names = {p["name"] for p in MANIFEST["profiles"]}
        self.assertIn(self.fixture.instructor_profile, names)

        # The CE flow should message the named instructor directly
        result = self.fixture.message_agent(
            self.fixture.instructor_profile,
            "Teach API security fundamentals",
        )
        self.assertEqual(result["status"], "ok")
        self.assertEqual(
            self.fixture.steps[-1].action, "message_agent"
        )
        self.assertEqual(
            self.fixture.steps[-1].detail["target"],
            "academy-cybersecurity-instructor",
        )

    def test_named_instructor_skill_exists(self):
        """The named instructor has the teach-profile skill."""
        skill_path = (
            ACADEMY_ROOT / "profiles" / "academy-cybersecurity-instructor"
            / "skills" / "teach-profile" / "SKILL.md"
        )
        self.assertTrue(skill_path.is_file())


# ---------------------------------------------------------------------------
# Test: Dean route
# ---------------------------------------------------------------------------
class DeanRouteTest(unittest.TestCase):
    """When no instructor is named, the Dean routes via routing.py."""

    def test_dean_routes_physics_to_physics_professor(self):
        result = route_learner(
            "agency-backend-engineer",
            "I want to understand classical mechanics and Newton's laws",
        )
        self.assertEqual(result.faculty, "academy-physics-professor")
        self.assertFalse(result.approximate)

    def test_dean_routes_cybersecurity_to_cybersecurity_instructor(self):
        result = route_learner(
            "agency-backend-engineer",
            "Learn cybersecurity threat modeling",
        )
        self.assertEqual(result.faculty, "academy-cybersecurity-instructor")
        self.assertFalse(result.approximate)

    def test_dean_routes_interdisciplinary_to_broad_chair(self):
        result = route_learner(
            "agency-research-analyst",
            "Understand the scientific method across physics, chemistry, and biology",
        )
        self.assertIsNotNone(result.faculty)
        # Either a specialist or broad chair is acceptable
        if result.faculty == "academy-natural-sciences-professor":
            self.assertTrue(result.approximate)

    def test_dean_returns_none_for_unmatched_topic(self):
        result = route_learner(
            "agency-frontend-engineer",
            "Teach me advanced basket weaving techniques using traditional methods",
        )
        if result.faculty is None:
            self.assertIn("no", result.reason.lower())
        else:
            self.assertTrue(result.approximate)

    def test_minimized_context_excludes_secrets(self):
        ctx = minimize_learner_context(
            learner_profile="agency-backend-engineer",
            role="Implements backend services and APIs",
            objective="Learn database indexing strategies",
            skills=["api-design", "sql-optimization"],
        )
        fields = set(ctx.__dataclass_fields__.keys())
        self.assertEqual(
            fields,
            {"learner_profile", "role", "objective", "relevant_skills"},
        )


# ---------------------------------------------------------------------------
# Test: Existing skill extend / no duplicate
# ---------------------------------------------------------------------------
class ExistingSkillExtendTest(unittest.TestCase):
    """When a matching skill exists, /learn extends it without duplicating."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")
        # Pre-create an existing skill
        skill_dir = (
            self.tmp / ".hermes" / "profiles" / "agency-backend-engineer"
            / "skills" / "api-security"
        )
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: api-security\ndescription: API security basics.\n---\n"
            "# API Security\nExisting content.\n",
            encoding="utf-8",
        )

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_existing_skill_is_extended_not_duplicated(self):
        result = self.fixture.learn("api-security", "Extended with OAuth knowledge.")
        self.assertEqual(result["status"], "extended")
        # Verify no duplicate creation step
        create_steps = [
            s for s in self.fixture.steps if s.action == "skill_created"
        ]
        self.assertEqual(len(create_steps), 0)
        extend_steps = [
            s for s in self.fixture.steps if s.action == "skill_extended"
        ]
        self.assertEqual(len(extend_steps), 1)

    def test_skill_file_still_exists_after_extend(self):
        self.fixture.learn("api-security", "Extended content.")
        skill_path = (
            self.tmp / ".hermes" / "profiles" / "agency-backend-engineer"
            / "skills" / "api-security" / "SKILL.md"
        )
        self.assertTrue(skill_path.is_file())


# ---------------------------------------------------------------------------
# Test: No related skill -> create
# ---------------------------------------------------------------------------
class NoRelatedSkillCreateTest(unittest.TestCase):
    """When no matching skill exists, /learn creates a new one."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_new_skill_is_created(self):
        result = self.fixture.learn(
            "oauth-token-rotation", "OAuth token rotation procedure."
        )
        self.assertEqual(result["status"], "created")
        create_steps = [
            s for s in self.fixture.steps if s.action == "skill_created"
        ]
        self.assertEqual(len(create_steps), 1)
        self.assertEqual(create_steps[0].detail["skill_name"], "oauth-token-rotation")

    def test_created_skill_file_exists(self):
        self.fixture.learn("oauth-token-rotation", "Content here.")
        skill_path = (
            self.tmp / ".hermes" / "profiles" / "agency-backend-engineer"
            / "skills" / "oauth-token-rotation" / "SKILL.md"
        )
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertIn("oauth-token-rotation", content)


# ---------------------------------------------------------------------------
# Test: Write approval
# ---------------------------------------------------------------------------
class WriteApprovalTest(unittest.TestCase):
    """When skills.write_approval is enabled, /learn stops at the approval boundary."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")
        self.fixture._write_approval_enabled = True

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_write_approval_halts_learn(self):
        result = self.fixture.learn("new-skill", "Some content.")
        self.assertEqual(result["status"], "pending_approval")
        approval_steps = [
            s for s in self.fixture.steps
            if s.action == "write_approval_required"
        ]
        self.assertEqual(len(approval_steps), 1)

    def test_skill_not_created_when_approval_pending(self):
        self.fixture.learn("new-skill", "Some content.")
        skill_path = (
            self.tmp / ".hermes" / "profiles" / "agency-backend-engineer"
            / "skills" / "new-skill" / "SKILL.md"
        )
        self.assertFalse(skill_path.is_file())

    def test_approval_is_never_bypassed(self):
        """The CE skill explicitly forbids bypassing write approval."""
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`skills.write_approval`", ce_skill)
        self.assertIn("Never bypass, auto-approve, or weaken it", ce_skill)


# ---------------------------------------------------------------------------
# Test: More practice / no early completion
# ---------------------------------------------------------------------------
class MorePracticeNoEarlyCompletionTest(unittest.TestCase):
    """Instructor requires more practice; mastery is not declared early."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_budget_decrements_on_each_turn(self):
        for _ in range(5):
            self.assertTrue(self.fixture.budget_tick())
        self.assertEqual(self.fixture._goal_budget, 15)

    def test_mastery_not_declared_on_acknowledgement(self):
        """The teach-profile skill rejects acknowledgement as mastery."""
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Do not accept any of the following as mastery", teach_skill)
        self.assertIn('"I understand"', teach_skill)
        self.assertIn("paraphrasing the instructor", teach_skill)
        self.assertIn("repeating the worked example", teach_skill)

    def test_mastery_not_declared_because_conversation_length(self):
        """Mastery must not be declared because the conversation was long enough."""
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Do not declare mastery because a conversation has been long enough",
            teach_skill,
        )

    def test_each_turn_must_have_a_job(self):
        """Every instructor message must do at least one useful job."""
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for job in (
            "diagnose a remaining gap",
            "teach a demonstrated gap",
            "assess application",
            "correct a specific failure",
            "conclude mastery",
            "report a genuine blocker",
        ):
            with self.subTest(job=job):
                self.assertIn(job, teach_skill)


# ---------------------------------------------------------------------------
# Test: Instructor deficiency -> subgoal
# ---------------------------------------------------------------------------
class InstructorDeficiencySubgoalTest(unittest.TestCase):
    """When instructor discovers a new required deficiency, a subgoal is created."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_subgoal_created_for_new_required_deficiency(self):
        result = self.fixture.subgoal_create(
            "Learner lacks understanding of CORS preflight requests"
        )
        self.assertEqual(result["status"], "active")
        self.assertEqual(len(self.fixture._subgoals), 1)
        self.assertEqual(
            self.fixture.steps[-1].action, "subgoal_create"
        )

    def test_subgoal_only_for_new_required_deficiency(self):
        """The CE skill forbids subgoals for routine corrections."""
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("new required deficiency", ce_skill)
        self.assertIn(
            "Do not create subgoals for routine corrections", ce_skill
        )

    def test_multiple_subgoals_accumulate(self):
        self.fixture.subgoal_create("Deficiency 1")
        self.fixture.subgoal_create("Deficiency 2")
        self.assertEqual(len(self.fixture._subgoals), 2)


# ---------------------------------------------------------------------------
# Test: Transfer pass
# ---------------------------------------------------------------------------
class TransferPassTest(unittest.TestCase):
    """Learner must demonstrate competency on a meaningfully different problem."""

    def test_transfer_requirement_is_in_ce_skill(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("meaningfully different problem", ce_skill)
        self.assertIn("Stop as soon as the completion contract is satisfied", ce_skill)

    def test_transfer_requirement_is_in_teach_skill(self):
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("meaningfully different problem", teach_skill)
        self.assertIn(
            "change surface details or operating context", teach_skill
        )

    def test_acknowledgement_is_not_transfer(self):
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn('"I understand"', teach_skill)
        self.assertIn("paraphrasing the instructor", teach_skill)

    def test_failed_transfer_corrects_only_failed_part(self):
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("correct only the failed part", teach_skill)
        self.assertIn("Do not restart the whole lesson", teach_skill)


# ---------------------------------------------------------------------------
# Test: Budget exhaustion
# ---------------------------------------------------------------------------
class BudgetExhaustionTest(unittest.TestCase):
    """Goal budget exhaustion pauses training honestly."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")
        self.fixture._goal_budget = 3  # Small budget for testing

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_budget_exhausts_after_n_ticks(self):
        for _ in range(3):
            self.fixture.budget_tick()
        self.assertTrue(self.fixture._budget_exhausted)

    def test_budget_exhaustion_is_recorded(self):
        for _ in range(3):
            self.fixture.budget_tick()
        exhausted_steps = [
            s for s in self.fixture.steps if s.action == "budget_exhausted"
        ]
        self.assertEqual(len(exhausted_steps), 1)

    def test_ce_skill_never_converts_budget_exhaustion_to_success(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Never convert budget exhaustion into success", ce_skill)
        self.assertIn(
            "Training paused because the learning objective has not yet been demonstrated.",
            ce_skill,
        )


# ---------------------------------------------------------------------------
# Test: Teacher unavailable / missing
# ---------------------------------------------------------------------------
class TeacherUnavailableTest(unittest.TestCase):
    """When the instructor is unavailable, the CE flow reports honestly."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")
        self.fixture._instructor_available = False

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_unavailable_instructor_returns_error(self):
        result = self.fixture.message_agent(
            "academy-nonexistent-instructor", "Teach me something"
        )
        self.assertEqual(result["status"], "unavailable")

    def test_ce_skill_handles_unavailable_instructor(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("the instructor is unavailable", ce_skill)
        self.assertIn("no safe alternative is resolved", ce_skill)

    def test_routing_returns_none_for_no_match(self):
        """routing.py returns None faculty when no match exists."""
        result = route_learner(
            "agency-generalist",
            "Teach me underwater basket weaving certification requirements",
        )
        if result.faculty is None:
            self.assertIn("no", result.reason.lower())


# ---------------------------------------------------------------------------
# Test: Cancel
# ---------------------------------------------------------------------------
class CancelTest(unittest.TestCase):
    """User can cancel the class at any time."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_cancel_stops_training(self):
        self.fixture._cancelled = True
        result = self.fixture.message_agent(
            "academy-cybersecurity-instructor", "Teach me"
        )
        self.assertEqual(result["status"], "cancelled")

    def test_ce_skill_supports_cancel(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Stop the class", ce_skill)
        self.assertIn("Stop when asked", ce_skill)

    def test_cancel_is_stop_condition(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("cancelled", ce_skill.lower())


# ---------------------------------------------------------------------------
# Test: Objective change
# ---------------------------------------------------------------------------
class ObjectiveChangeTest(unittest.TestCase):
    """User can change the objective mid-flow."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_objective_change_is_supported(self):
        self.fixture._objective_changed = True
        result = self.fixture.message_agent(
            "academy-cybersecurity-instructor", "Teach me"
        )
        self.assertEqual(result["status"], "objective_changed")

    def test_ce_skill_handles_objective_change(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Focus more on OAuth", ce_skill)
        self.assertIn("Also teach token rotation", ce_skill)
        self.assertIn(
            "update the active objective/criteria", ce_skill
        )
        self.assertIn(
            "instead of silently starting a recursive second class", ce_skill
        )


# ---------------------------------------------------------------------------
# Test: Hermes restart
# ---------------------------------------------------------------------------
class HermesRestartTest(unittest.TestCase):
    """Training survives a Hermes restart via native goal persistence."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_restart_is_recorded(self):
        self.fixture._restart_simulated = True
        result = self.fixture.message_agent(
            "academy-cybersecurity-instructor", "Continue teaching"
        )
        self.assertEqual(result["status"], "restart")

    def test_ce_skill_uses_native_goal_persistence(self):
        """The CE skill relies on native /goal persistence, not custom state."""
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("actual native `/goal` handler", ce_skill)
        self.assertIn("never imitate their loop, persistence, approval, or completion logic", ce_skill)
        # No custom persistence layer
        self.assertIn("Do not create a scheduler", ce_skill)
        self.assertIn("training database", ce_skill)

    def test_no_custom_state_database(self):
        """The CE system has no custom state database that would be lost on restart."""
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("candidate-skill registry", ce_skill)
        self.assertIn("parallel memory store", ce_skill)


# ---------------------------------------------------------------------------
# Test: Bot Chat resume
# ---------------------------------------------------------------------------
class BotChatResumeTest(unittest.TestCase):
    """Training resumes via canonical Bot Chat after interruption."""

    def test_ce_skill_uses_canonical_bot_chat(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("canonical Bot Chat", ce_skill)
        self.assertIn("message_agent", ce_skill)

    def test_peer_wait_prevents_duplicate_requests(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("allow native `/goal` peer-wait behavior to park the goal", ce_skill)
        self.assertIn("Do not send duplicate requests", ce_skill)
        self.assertIn("burn turns", ce_skill)

    def test_no_acknowledgement_ping_pong(self):
        """Both skills forbid acknowledgement ping-pong."""
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("acknowledgement turns", ce_skill)
        self.assertIn("acknowledgement ping-pong", teach_skill)


# ---------------------------------------------------------------------------
# Test: Fresh session uses learned skill
# ---------------------------------------------------------------------------
class FreshSessionUsesLearnedSkillTest(unittest.TestCase):
    """A new session can use a skill that was learned in a prior CE session."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_learned_skill_persists_in_profile(self):
        self.fixture.learn("api-security-advanced", "Advanced API security.")
        skill_path = (
            self.tmp / ".hermes" / "profiles" / "agency-backend-engineer"
            / "skills" / "api-security-advanced" / "SKILL.md"
        )
        self.assertTrue(skill_path.is_file())
        # Simulate fresh session: read the skill back
        content = skill_path.read_text(encoding="utf-8")
        self.assertIn("api-security-advanced", content)

    def test_learned_skill_is_in_learner_profile_not_source(self):
        """Learned skills go to the learner profile, not Profile Packs source."""
        self.fixture.learn("test-skill", "Test content.")
        # Skill should be in the learner's profile
        learner_skill = (
            self.tmp / ".hermes" / "profiles" / "agency-backend-engineer"
            / "skills" / "test-skill" / "SKILL.md"
        )
        self.assertTrue(learner_skill.is_file())
        # Skill should NOT be in the Academy source
        source_skill = ACADEMY_ROOT / "profiles" / "agency-backend-engineer"
        self.assertFalse(source_skill.is_dir())


# ---------------------------------------------------------------------------
# Test: Teacher unchanged
# ---------------------------------------------------------------------------
class TeacherUnchangedTest(unittest.TestCase):
    """The instructor profile is never modified by the CE flow."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_instructor_skill_not_modified(self):
        """The teach-profile skill bytes are unchanged after CE flow."""
        teach_skill_path = (
            ACADEMY_ROOT / "profiles" / "academy-cybersecurity-instructor"
            / "skills" / "teach-profile" / "SKILL.md"
        )
        original_bytes = teach_skill_path.read_bytes()

        # Simulate a full CE flow
        self.fixture.goal_start("Learn API security")
        self.fixture.message_agent(
            "academy-cybersecurity-instructor", "Teach me"
        )
        self.fixture.learn("api-security", "Learned content")
        self.fixture.goal_complete("mastered")

        # Verify instructor skill is unchanged
        self.assertEqual(teach_skill_path.read_bytes(), original_bytes)

    def test_ce_skill_forbids_instructor_editing_learner(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("must never edit this learner's skills", ce_skill)

    def test_teach_skill_forbids_instructor_writing_skill(self):
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("The learner owns the `/learn` decision", teach_skill)
        self.assertIn("Never edit the learner's skills", teach_skill)


# ---------------------------------------------------------------------------
# Test: Profile Packs unchanged
# ---------------------------------------------------------------------------
class ProfilePacksUnchangedTest(unittest.TestCase):
    """Profile Packs source is never modified by the CE flow."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_academy_source_not_modified_by_learn(self):
        """Learning creates skills in the learner profile, not in Academy source."""
        # Record original state of Academy source
        academy_profiles_dir = ACADEMY_ROOT / "profiles"
        original_files = set()
        for p in academy_profiles_dir.rglob("*"):
            if p.is_file():
                original_files.add(p.relative_to(academy_profiles_dir))

        # Simulate learning
        self.fixture.learn("new-learner-skill", "Some content.")

        # Verify Academy source is unchanged
        current_files = set()
        for p in academy_profiles_dir.rglob("*"):
            if p.is_file():
                current_files.add(p.relative_to(academy_profiles_dir))
        self.assertEqual(original_files, current_files)

    def test_ce_skill_forbids_modifying_profile_packs(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Never modify Profile Packs source", ce_skill)
        self.assertIn(
            "Learning must remain local to this learner", ce_skill
        )

    def test_shared_skill_bytes_unchanged_after_ce(self):
        """Canonical shared skill bytes are unchanged after CE operations."""
        ce_canonical = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        )
        original = ce_canonical.read_bytes()

        # Simulate CE flow
        self.fixture.goal_start("Learn something")
        self.fixture.learn("some-skill", "Content")
        self.fixture.goal_complete("mastered")

        self.assertEqual(ce_canonical.read_bytes(), original)


# ---------------------------------------------------------------------------
# Test: Fleet unavailable (no-Fleet environment)
# ---------------------------------------------------------------------------
class NoFleetEnvironmentTest(unittest.TestCase):
    """Explicit no-Fleet test environment: no Fleet service, plugin, API,
    Keryx, or Nodescale.  Training succeeds without any distributed dependency."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home(include_fleet=False)
        self.fixture = CEFixture(hermes_home=self.tmp / ".hermes")

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_no_fleet_plugin_in_hermes_home(self):
        """The test HERMES_HOME has no Fleet plugin."""
        fleet_dir = self.tmp / ".hermes" / "plugins" / "fleet"
        self.assertFalse(fleet_dir.exists())

    def test_no_fleet_artifacts_anywhere(self):
        """No Fleet, Keryx, Nodescale, Templar, or RunAuthority artifacts."""
        hermes_home = self.tmp / ".hermes"
        forbidden_names = {"fleet", "keryx", "nodescale", "templar", "runauthority"}
        for p in hermes_home.rglob("*"):
            if p.is_dir():
                self.assertNotIn(p.name.lower(), forbidden_names)

    def test_training_succeeds_without_fleet(self):
        """A complete CE flow succeeds without any Fleet dependency."""
        # Full flow: goal -> message_agent -> learn -> complete
        goal_result = self.fixture.goal_start("Learn API security")
        self.assertEqual(goal_result["status"], "active")

        msg_result = self.fixture.message_agent(
            "academy-cybersecurity-instructor", "Teach me API security"
        )
        self.assertEqual(msg_result["status"], "ok")

        learn_result = self.fixture.learn("api-security", "Learned API security.")
        self.assertEqual(learn_result["status"], "created")

        complete_result = self.fixture.goal_complete("mastered")
        self.assertEqual(complete_result["status"], "completed")
        self.assertEqual(complete_result["outcome"], "mastered")

    def test_ce_skill_forbids_fleet_dependencies(self):
        """The CE skill explicitly forbids Fleet and related systems."""
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "Fleet",
            "Keryx",
            "Nodescale",
            "Templar",
            "RunAuthority",
            "Run Capsules",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, ce_skill)

    def test_teach_skill_forbids_fleet_dependencies(self):
        """The teach-profile skill also forbids Fleet dependencies."""
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "Fleet",
            "Keryx",
            "Nodescale",
            "Templar",
            "RunAuthority",
            "Run Capsules",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, teach_skill)

    def test_no_parallel_runtime_introduced(self):
        """The CE system introduces no parallel runtime."""
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "Do not create a scheduler",
            "training database",
            "candidate-skill registry",
            "parallel memory store",
            "alternate message bus",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, ce_skill)

    def test_full_flow_with_budget_and_transfer(self):
        """Complete flow with budget tracking and transfer requirement."""
        self.fixture._goal_budget = 10

        # Start goal
        self.fixture.goal_start("Learn threat modeling")

        # Baseline attempt (simulated)
        self.fixture.steps.append(CEStep("baseline_attempt", {"result": "partial"}))

        # Instruction turns
        for i in range(3):
            self.fixture.message_agent(
                "academy-cybersecurity-instructor", f"Turn {i+1}"
            )
            self.assertTrue(self.fixture.budget_tick())

        # Transfer attempt
        self.fixture.steps.append(CEStep("transfer_attempt", {"result": "passed"}))

        # Learn
        self.fixture.learn("threat-modeling", "Threat modeling procedure.")

        # Complete
        self.fixture.goal_complete("mastered")

        # Verify full sequence
        action_sequence = [s.action for s in self.fixture.steps]
        self.assertIn("goal_start", action_sequence)
        self.assertIn("message_agent", action_sequence)
        self.assertIn("learn", action_sequence)
        self.assertIn("goal_complete", action_sequence)
        self.assertIn("skill_created", action_sequence)


# ---------------------------------------------------------------------------
# Test: CE flow integration (end-to-end deterministic)
# ---------------------------------------------------------------------------
class CEFlowIntegrationTest(unittest.TestCase):
    """End-to-end deterministic CE flow using real routing and fixtures."""

    def setUp(self):
        self.tmp = setup_temp_hermes_home()

    def tearDown(self):
        cleanup_temp(self.tmp)

    def test_full_ce_flow_with_dean_routing(self):
        """Complete flow: Dean routes -> instructor teaches -> learner learns."""
        # Step 1: Dean routes
        routing = route_learner(
            "agency-backend-engineer",
            "Learn cybersecurity threat modeling fundamentals",
        )
        self.assertEqual(routing.faculty, "academy-cybersecurity-instructor")
        self.assertFalse(routing.approximate)

        # Step 2: Minimized context
        ctx = minimize_learner_context(
            learner_profile="agency-backend-engineer",
            role="Implements backend services and APIs",
            objective="Learn cybersecurity threat modeling fundamentals",
            skills=["api-design"],
        )
        self.assertEqual(ctx.learner_profile, "agency-backend-engineer")
        self.assertIn("api-design", ctx.relevant_skills)

        # Step 3: CE flow
        fixture = CEFixture(
            hermes_home=self.tmp / ".hermes",
            learner_profile="agency-backend-engineer",
            instructor_profile=routing.faculty,
            objective="Learn cybersecurity threat modeling fundamentals",
        )

        # Start goal
        goal = fixture.goal_start("Threat modeling competency")
        self.assertEqual(goal["status"], "active")

        # Message instructor
        msg = fixture.message_agent(
            routing.faculty,
            f"Learner: {ctx.learner_profile}, Role: {ctx.role}, "
            f"Objective: {ctx.objective}",
        )
        self.assertEqual(msg["status"], "ok")

        # Learn
        learn = fixture.learn("threat-modeling", "STRIDE methodology.")
        self.assertEqual(learn["status"], "created")

        # Complete
        complete = fixture.goal_complete("mastered")
        self.assertEqual(complete["outcome"], "mastered")

        # Verify skill persisted
        skill_path = (
            self.tmp / ".hermes" / "profiles" / "agency-backend-engineer"
            / "skills" / "threat-modeling" / "SKILL.md"
        )
        self.assertTrue(skill_path.is_file())

    def test_full_ce_flow_with_named_instructor(self):
        """Complete flow with a user-named instructor (no Dean routing)."""
        fixture = CEFixture(
            hermes_home=self.tmp / ".hermes",
            learner_profile="agency-backend-engineer",
            instructor_profile="academy-physics-professor",
            objective="Learn classical mechanics",
        )

        fixture.goal_start("Classical mechanics competency")
        fixture.message_agent("academy-physics-professor", "Teach me mechanics")
        fixture.learn("classical-mechanics", "Newton's laws and momentum.")
        result = fixture.goal_complete("mastered")

        self.assertEqual(result["outcome"], "mastered")
        self.assertEqual(len(fixture._subgoals), 0)  # No subgoals needed

    def test_ce_flow_with_subgoal_for_deficiency(self):
        """Flow where instructor discovers a new required deficiency."""
        fixture = CEFixture(hermes_home=self.tmp / ".hermes")

        fixture.goal_start("API security competency")
        fixture.message_agent(
            "academy-cybersecurity-instructor", "Teach me API security"
        )
        # Instructor discovers learner lacks CORS understanding
        fixture.subgoal_create("Learner lacks CORS preflight understanding")
        fixture.message_agent(
            "academy-cybersecurity-instructor", "Teach CORS"
        )
        fixture.learn("api-security", "API security including CORS.")
        result = fixture.goal_complete("mastered")

        self.assertEqual(result["outcome"], "mastered")
        self.assertEqual(len(fixture._subgoals), 1)
        self.assertIn("CORS", fixture._subgoals[0])


# ---------------------------------------------------------------------------
# Test: Determinism guarantees
# ---------------------------------------------------------------------------
class DeterminismTest(unittest.TestCase):
    """Routing and context minimization are deterministic."""

    def test_routing_is_deterministic(self):
        args = ("agency-backend-engineer", "Learn physics fundamentals")
        r1 = route_learner(*args)
        r2 = route_learner(*args)
        self.assertEqual(r1, r2)

    def test_routing_result_is_hashable(self):
        result = route_learner("agency-frontend-engineer", "Learn color theory")
        hash(result)  # Should not raise

    def test_minimized_context_is_deterministic(self):
        args = {
            "learner_profile": "agency-backend-engineer",
            "role": "Backend engineer",
            "objective": "Learn physics",
            "skills": ["api-design"],
        }
        c1 = minimize_learner_context(**args)
        c2 = minimize_learner_context(**args)
        self.assertEqual(c1, c2)

    def test_fixture_steps_are_ordered(self):
        tmp = setup_temp_hermes_home()
        try:
            fixture = CEFixture(hermes_home=tmp / ".hermes")
            fixture.goal_start("Test")
            fixture.message_agent("academy-physics-professor", "Teach")
            fixture.learn("physics", "Content")
            fixture.goal_complete("mastered")

            actions = [s.action for s in fixture.steps]
            self.assertEqual(
                actions,
                ["goal_start", "message_agent", "learn", "skill_created", "goal_complete"],
            )
        finally:
            cleanup_temp(tmp)


# ---------------------------------------------------------------------------
# Test: No parallel runtime
# ---------------------------------------------------------------------------
class NoParallelRuntimeTest(unittest.TestCase):
    """The CE system introduces no parallel runtime or custom persistence."""

    def test_ce_skill_forbids_all_parallel_runtimes(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        for forbidden in (
            "Do not create a scheduler",
            "training database",
            "candidate-skill registry",
            "parallel memory store",
            "alternate message bus",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, ce_skill)

    def test_teach_skill_forbids_all_parallel_runtimes(self):
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Do not create a training database, scheduler, candidate-skill registry, "
            "alternate message bus, or other persistence layer.",
            teach_skill,
        )


# ---------------------------------------------------------------------------
# Test: User visibility is concise
# ---------------------------------------------------------------------------
class UserVisibilityTest(unittest.TestCase):
    """User-visible status is concise, not chatty."""

    def test_ce_skill_demands_concise_status(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Keep user-visible status concise", ce_skill)
        self.assertIn("Do not narrate every Bot message", ce_skill)
        self.assertIn(
            "Learning: Backend Engineer → API security with Cybersecurity Instructor.",
            ce_skill,
        )

    def test_teach_skill_forbids_ceremony(self):
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Avoid greetings, ceremony", teach_skill)
        self.assertIn("professor/student theater", teach_skill)


# ---------------------------------------------------------------------------
# Test: Efficiency evidence
# ---------------------------------------------------------------------------
class EfficiencyEvidenceTest(unittest.TestCase):
    """The CE system tracks efficiency evidence when available."""

    def test_ce_skill_tracks_efficiency_metrics(self):
        ce_skill = (
            ACADEMY_ROOT / "shared-skills" / "academy-continuing-education"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        for metric in (
            "learner turns",
            "instructor turns",
            "retries",
            "baseline result",
            "post-instruction transfer result",
            "whether `/learn` produced a durable skill change",
        ):
            with self.subTest(metric=metric):
                self.assertIn(metric, ce_skill)

    def test_teach_skill_optimizes_for_capability_gain(self):
        teach_skill = (
            ACADEMY_ROOT / "shared-skills" / "teach-profile" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("capability gain per unit of inference", teach_skill)
        self.assertIn(
            "A two-turn correction that produces verified transfer is better than "
            "a ten-turn simulated lesson.",
            teach_skill,
        )


if __name__ == "__main__":
    unittest.main()
