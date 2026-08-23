"""Focused contract tests for the Academy learner CE shared skill."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ACADEMY_ROOT.parent
CANONICAL = ACADEMY_ROOT / "shared-skills" / "academy-continuing-education" / "SKILL.md"
ACADEMY_MANIFEST = json.loads((ACADEMY_ROOT / "academy.json").read_text(encoding="utf-8"))
AGENCY_MANIFEST = json.loads(
    (REPO_ROOT / "hermes-agency" / "agency.json").read_text(encoding="utf-8")
)


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        raise AssertionError(f"missing frontmatter key: {key}")
    return match.group(1).strip().strip('"\'')


class ContinuingEducationSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = CANONICAL.read_text(encoding="utf-8")
        cls.data = CANONICAL.read_bytes()

    def test_frontmatter_is_routing_safe(self):
        self.assertEqual(
            _frontmatter_value(self.text, "name"),
            "academy-continuing-education",
        )
        description = _frontmatter_value(self.text, "description")
        self.assertLessEqual(len(description), 60)
        self.assertTrue(description.endswith("."))
        self.assertEqual(
            description,
            "MUST load first for Academy learning or go-learn requests.",
        )

    def test_native_hermes_primitives_are_the_only_learning_path(self):
        for marker in ("`/goal`", "`message_agent`", "`/learn`", "`skill_manage`"):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)
        for forbidden in (
            "candidate-skill registry",
            "alternate message bus",
            "parallel memory store",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertIn(forbidden, self.text)

    def test_minimum_sufficient_instruction_contract_is_explicit(self):
        required = (
            "competency-transfer system, not a school simulation",
            "minimum instruction required",
            "Baseline before teaching",
            "If the baseline already demonstrates the competency strongly enough, stop.",
            "Do not require fixed lesson lengths",
            "Stop as soon as the completion contract is satisfied.",
            "If there is no reusable delta, skip `/learn`.",
            "minimum inference cost",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, self.text)

    def test_peer_wait_and_no_duplicate_request_contract_is_explicit(self):
        self.assertIn("allow native `/goal` peer-wait behavior to park the goal", self.text)
        self.assertIn("Do not send duplicate requests", self.text)
        self.assertIn("burn turns", self.text)
        self.assertIn("declare success while waiting", self.text)

    def test_authority_and_source_isolation_are_explicit(self):
        self.assertIn("must never edit this learner's skills", self.text)
        self.assertIn("Learning must remain local to this learner", self.text)
        self.assertIn("Never modify Profile Packs source", self.text)
        self.assertIn("Do not ask the instructor to write it", self.text)
        for forbidden_system in (
            "Fleet",
            "Keryx",
            "Nodescale",
            "Templar",
            "RunAuthority",
            "Run Capsules",
        ):
            self.assertIn(forbidden_system, self.text)

    def test_every_agency_profile_materializes_the_canonical_bytes(self):
        names = [profile["name"] for profile in AGENCY_MANIFEST["profiles"]]
        self.assertGreater(len(names), 0)
        for name in names:
            with self.subTest(profile=name):
                materialized = (
                    REPO_ROOT
                    / "hermes-agency"
                    / "profiles"
                    / name
                    / "skills"
                    / "academy-continuing-education"
                    / "SKILL.md"
                )
                self.assertTrue(materialized.is_file(), f"missing {materialized}")
                self.assertEqual(materialized.read_bytes(), self.data)

    def test_manifest_targets_agency_ce_participants(self):
        entry = next(
            skill
            for skill in ACADEMY_MANIFEST["shared_skills"]
            if skill["name"] == "academy-continuing-education"
        )
        self.assertEqual(entry["targets"]["mode"], "agency-ce-participants")


if __name__ == "__main__":
    unittest.main()
