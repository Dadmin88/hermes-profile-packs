from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "update_readme_counts.py"


class ReadmeCountUpdaterTests(unittest.TestCase):
    def make_repo(self, root: Path) -> None:
        packs = {
            "packs": [
                {"path": "hermes-agency", "manifest": "hermes-agency/agency.json"},
                {"path": "hermes-council", "manifest": "hermes-council/council.json"},
                {"path": "hermes-academy", "manifest": "hermes-academy/academy.json"},
            ]
        }
        (root / "packs.json").write_text(json.dumps(packs), encoding="utf-8")

        fixtures = {"agency": (2, 0), "council": (1, 2), "academy": (3, 4)}
        for pack, (profile_count, skill_count) in fixtures.items():
            pack_dir = root / f"hermes-{pack}"
            profiles_dir = pack_dir / "profiles"
            profiles_dir.mkdir(parents=True)
            profiles = []
            for profile_index in range(profile_count):
                name = f"{pack}-profile-{profile_index}"
                declared_skills = [
                    f"skill-{skill_index}"
                    for skill_index in range(skill_count if profile_index == 0 else 0)
                ]
                profiles.append({"name": name, "jobs": declared_skills})
                profile_dir = profiles_dir / name
                profile_dir.mkdir()
                for skill_name in declared_skills:
                    skill_dir = profile_dir / "skills" / skill_name
                    skill_dir.mkdir(parents=True)
                    (skill_dir / "SKILL.md").write_text("# Test skill\n", encoding="utf-8")
            if pack == "academy":
                shared = profiles_dir / "academy-profile-1" / "skills" / "materialized-shared"
                shared.mkdir(parents=True)
                (shared / "SKILL.md").write_text("# Shared skill\n", encoding="utf-8")
            (pack_dir / f"{pack}.json").write_text(
                json.dumps({"profiles": profiles}), encoding="utf-8"
            )

        (root / "README.md").write_text(
            "# Test\n\n"
            "<!-- profile-counts:start -->\n"
            "stale summary\n"
            "<!-- profile-counts:end -->\n\n"
            "You rarely need all 999 profiles.\n",
            encoding="utf-8",
        )

    def run_script(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(root), *args],
            capture_output=True,
            text=True,
        )

    def test_updates_generated_counts_and_total(self):
        self.assertTrue(SCRIPT.is_file(), "README count updater script is missing")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            result = self.run_script(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            readme = (root / "README.md").read_text(encoding="utf-8")
            self.assertIn("Hermes Agency contains 2 professional specialists.", readme)
            self.assertIn("Hermes Council contains 1 focused profile and 2 purpose-built personal-life skills.", readme)
            self.assertIn("Hermes Academy contains 3 faculty profiles and 4 purpose-built teaching skills.", readme)
            self.assertIn("You rarely need all 6 profiles.", readme)

    def test_check_mode_detects_stale_readme_without_writing(self):
        self.assertTrue(SCRIPT.is_file(), "README count updater script is missing")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            before = (root / "README.md").read_text(encoding="utf-8")
            stale = self.run_script(root, "--check")
            self.assertEqual(stale.returncode, 1)
            self.assertEqual((root / "README.md").read_text(encoding="utf-8"), before)
            self.assertIn("python scripts/update_readme_counts.py", stale.stderr)
            self.assertEqual(self.run_script(root).returncode, 0)
            current = self.run_script(root, "--check")
            self.assertEqual(current.returncode, 0, current.stderr)


if __name__ == "__main__":
    unittest.main()
