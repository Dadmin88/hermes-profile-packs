"""Tests for the Academy shared-skill packaging mechanism."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
MANIFEST = json.loads((ROOT / "academy.json").read_text(encoding="utf-8"))
INSTALLER = ROOT / "install.py"
VALIDATOR = ROOT / "validate.py"
AGENCY_PROFILES = REPO_ROOT / "hermes-agency" / "profiles"


class SharedSkillManifestTests(unittest.TestCase):
    """Validate the shared_skills manifest structure."""

    def test_shared_skills_field_exists(self):
        self.assertIn("shared_skills", MANIFEST)
        self.assertIsInstance(MANIFEST["shared_skills"], list)
        self.assertGreater(len(MANIFEST["shared_skills"]), 0)

    def test_shared_skill_entries_have_required_fields(self):
        required = {"name", "canonical_source", "description", "targets"}
        for skill in MANIFEST["shared_skills"]:
            with self.subTest(skill=skill.get("name", "?")):
                self.assertTrue(required.issubset(set(skill.keys())))

    def test_shared_skill_names_are_valid(self):
        import re
        name_re = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
        for skill in MANIFEST["shared_skills"]:
            with self.subTest(skill=skill["name"]):
                self.assertRegex(skill["name"], name_re)

    def test_shared_skill_names_are_unique(self):
        names = [s["name"] for s in MANIFEST["shared_skills"]]
        self.assertEqual(len(names), len(set(names)))

    def test_canonical_sources_exist(self):
        for skill in MANIFEST["shared_skills"]:
            with self.subTest(skill=skill["name"]):
                path = ROOT / skill["canonical_source"]
                self.assertTrue(path.is_file(), f"missing: {path}")

    def test_canonical_source_frontmatter_matches_manifest_name(self):
        for skill in MANIFEST["shared_skills"]:
            with self.subTest(skill=skill["name"]):
                path = ROOT / skill["canonical_source"]
                text = path.read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                parts = text.split("---\n", 2)
                self.assertGreaterEqual(len(parts), 3)
                fm_name = None
                for line in parts[1].splitlines():
                    if line.startswith("name:"):
                        fm_name = line.split(":", 1)[1].strip()
                        break
                self.assertEqual(fm_name, skill["name"])

    def test_target_modes_are_known(self):
        valid_modes = {"agency-ce-participants", "academy-faculty-except-dean"}
        for skill in MANIFEST["shared_skills"]:
            with self.subTest(skill=skill["name"]):
                self.assertIn(skill["targets"]["mode"], valid_modes)

    def test_target_exceptions_are_lists(self):
        for skill in MANIFEST["shared_skills"]:
            with self.subTest(skill=skill["name"]):
                exceptions = skill["targets"].get("exceptions", [])
                self.assertIsInstance(exceptions, list)


class SharedSkillTargetResolutionTests(unittest.TestCase):
    """Validate that target resolution produces the expected profiles."""

    def test_academy_faculty_except_dean_excludes_dean(self):
        skill = next(
            s for s in MANIFEST["shared_skills"]
            if s["targets"]["mode"] == "academy-faculty-except-dean"
        )
        academy_names = {p["name"] for p in MANIFEST["profiles"]}
        expected = sorted(academy_names - {"academy-dean"})
        # Import the resolver from the installer
        sys.path.insert(0, str(ROOT))
        from install import _resolve_shared_skill_targets
        actual = _resolve_shared_skill_targets(skill, MANIFEST["profiles"])
        self.assertEqual(actual, expected)
        self.assertNotIn("academy-dean", actual)

    def test_agency_ce_participants_covers_agency_roster(self):
        skill = next(
            s for s in MANIFEST["shared_skills"]
            if s["targets"]["mode"] == "agency-ce-participants"
        )
        sys.path.insert(0, str(ROOT))
        from install import _resolve_shared_skill_targets
        actual = _resolve_shared_skill_targets(skill, MANIFEST["profiles"])
        # Should include all agency profiles
        self.assertTrue(all(n.startswith("agency-") for n in actual))
        agency_manifest = json.loads(
            (REPO_ROOT / "hermes-agency" / "agency.json").read_text(encoding="utf-8")
        )
        self.assertEqual(len(actual), len(agency_manifest["profiles"]))

    def test_exceptions_are_excluded(self):
        # Create a modified skill with an exception
        sys.path.insert(0, str(ROOT))
        from install import _resolve_shared_skill_targets
        base_skill = next(
            s for s in MANIFEST["shared_skills"]
            if s["targets"]["mode"] == "academy-faculty-except-dean"
        )
        modified = {
            **base_skill,
            "targets": {
                **base_skill["targets"],
                "exceptions": ["academy-mathematics-professor"],
            },
        }
        result = _resolve_shared_skill_targets(modified, MANIFEST["profiles"])
        self.assertNotIn("academy-mathematics-professor", result)


class SharedSkillByteIdentityTests(unittest.TestCase):
    """Validate that materialized copies match canonical sources."""

    def test_all_materialized_copies_match_canonical(self):
        for skill in MANIFEST["shared_skills"]:
            name = skill["name"]
            canonical = ROOT / skill["canonical_source"]
            canonical_bytes = canonical.read_bytes()

            # Check academy profiles
            for profile in MANIFEST["profiles"]:
                if profile["name"] == "academy-dean" and skill["targets"]["mode"] == "academy-faculty-except-dean":
                    continue
                materialized = ROOT / "profiles" / profile["name"] / "skills" / name / "SKILL.md"
                if materialized.is_file():
                    with self.subTest(skill=name, profile=profile["name"]):
                        self.assertEqual(
                            materialized.read_bytes(),
                            canonical_bytes,
                            f"byte mismatch: {name} in {profile['name']}",
                        )

    def test_shared_skill_not_in_dean_for_faculty_mode(self):
        """The teach-profile skill should not be in academy-dean."""
        dean_skill = ROOT / "profiles" / "academy-dean" / "skills" / "teach-profile" / "SKILL.md"
        self.assertFalse(dean_skill.is_file(), "teach-profile should not be in academy-dean")


class SharedSkillInstallerTests(unittest.TestCase):
    """Test the installer's shared-skill materialization."""

    def _run_installer(self, *args: str):
        env = os.environ.copy()
        result = subprocess.run(
            [sys.executable, str(INSTALLER), *args],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        return result

    def test_list_shows_shared_skills(self):
        result = self._run_installer("--list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Shared skills:", result.stdout)
        self.assertIn("academy-continuing-education", result.stdout)
        self.assertIn("teach-profile", result.stdout)

    def test_skip_shared_skills_flag(self):
        """--skip-shared-skills should not error."""
        # We can't fully test installation without hermes, but we can test
        # that the flag is accepted
        result = self._run_installer("--list", "--skip-shared-skills")
        self.assertEqual(result.returncode, 0, result.stderr)


class SharedSkillValidatorTests(unittest.TestCase):
    """Test the validator's shared-skill checks."""

    def _run_validator(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(VALIDATOR)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_validator_passes_with_current_state(self):
        result = self._run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_validator_detects_missing_canonical_source(self):
        """Temporarily remove a canonical source and verify the validator catches it."""
        import shutil
        skill_dir = ROOT / "shared-skills" / "academy-continuing-education"
        backup = skill_dir / "SKILL.md.bak"
        skill_file = skill_dir / "SKILL.md"
        try:
            skill_file.rename(backup)
            result = self._run_validator()
            self.assertEqual(result.returncode, 1)
            self.assertIn("canonical source not found", result.stderr)
        finally:
            if backup.exists():
                backup.rename(skill_file)

    def test_validator_detects_byte_mismatch(self):
        """Corrupt a materialized copy and verify the validator catches it."""
        target = ROOT / "profiles" / "academy-mathematics-professor" / "skills" / "teach-profile" / "SKILL.md"
        if not target.is_file():
            self.skipTest("teach-profile not yet materialized in academy-mathematics-professor")
        original = target.read_bytes()
        try:
            target.write_text("corrupted content\n", encoding="utf-8")
            result = self._run_validator()
            self.assertEqual(result.returncode, 1)
            self.assertIn("byte mismatch", result.stderr)
        finally:
            target.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
