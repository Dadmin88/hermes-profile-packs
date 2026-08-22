from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import catalog  # noqa: E402


class RuntimeCatalogTests(unittest.TestCase):
    def test_catalog_is_complete_and_runtime_focused(self):
        manifest = json.loads((ROOT / "agency.json").read_text(encoding="utf-8"))
        value = catalog.build_catalog()
        self.assertEqual(value["schema_version"], 2)
        self.assertEqual(
            value["content_digest_schema"],
            "hermes-agency-profile-content.v1",
        )
        self.assertEqual(value["agency"]["profile_count"], manifest["profile_count"])
        self.assertEqual(len(value["profiles"]), manifest["profile_count"])
        self.assertEqual(
            value["routing"]["selection_order"],
            ["professional-profile", "eligible-node"],
        )
        self.assertEqual(value["routing"]["live_presence_owner"], "hermes-fleet")
        self.assertEqual(value["routing"]["missing_presence_behavior"], "fleet-locate-or-place")

        names = [profile["name"] for profile in value["profiles"]]
        self.assertEqual(names, sorted(names))
        self.assertEqual(len(names), len(set(names)))

        for profile in value["profiles"]:
            with self.subTest(profile=profile["name"]):
                self.assertEqual(profile["version"], value["agency"]["version"])
                self.assertTrue(profile["description"].strip())
                self.assertTrue(profile["capabilities"])
                self.assertEqual(profile["capabilities"], sorted(set(profile["capabilities"])))
                self.assertEqual(len(profile["content_digest"]), 64)
                self.assertEqual(profile["content_digest"], profile["content_digest"].lower())
                self.assertTrue(
                    all(character in "0123456789abcdef" for character in profile["content_digest"])
                )
                profile_dir = ROOT / profile["distribution_path"]
                self.assertTrue((profile_dir / "distribution.yaml").is_file())
                actual_skills = sorted(
                    path.parent.name for path in (profile_dir / "skills").glob("*/SKILL.md")
                )
                self.assertEqual(profile["capabilities"], actual_skills)
                self.assertEqual(
                    profile["content_digest"],
                    catalog.profile_content_digest(
                        profile_dir,
                        profile["name"],
                        profile["version"],
                    ),
                )

    def test_profile_filter_emits_one_stable_profile(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "catalog.py"),
                "--profile",
                "agency-backend-engineer",
                "--compact",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(
            [profile["name"] for profile in value["profiles"]],
            ["agency-backend-engineer"],
        )
        self.assertIn("api-design", value["profiles"][0]["capabilities"])
        self.assertEqual(len(value["profiles"][0]["content_digest"]), 64)

    def test_category_filter_is_exact(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "catalog.py"),
                "--category",
                "qa",
                "--compact",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        manifest = json.loads((ROOT / "agency.json").read_text(encoding="utf-8"))
        self.assertEqual(len(value["profiles"]), manifest["categories"]["qa"])
        self.assertTrue(all(profile["category"] == "qa" for profile in value["profiles"]))

    def test_unknown_profile_fails_closed(self):
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "catalog.py"),
                "--profile",
                "agency-does-not-exist",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown profile", result.stderr)

    def test_content_digest_is_deterministic_and_tracks_behavior_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            profile = Path(temporary) / "agency-example"
            skill = profile / "skills" / "review"
            references = skill / "references"
            references.mkdir(parents=True)
            (profile / "SOUL.md").write_text("professional identity\n", encoding="utf-8")
            (skill / "SKILL.md").write_text("procedure\n", encoding="utf-8")
            (references / "checklist.md").write_text("evidence\n", encoding="utf-8")
            (profile / "distribution.yaml").write_text(
                "name: agency-example\nversion: 1.2.3\ndescription: example\n",
                encoding="utf-8",
            )

            original = catalog.profile_content_digest(profile, "agency-example", "1.2.3")
            self.assertEqual(
                original,
                catalog.profile_content_digest(profile, "agency-example", "1.2.3"),
            )

            (profile / "README.md").write_text("human documentation\n", encoding="utf-8")
            (profile / "distribution.yaml").write_text(
                "name: agency-example\nversion: 1.2.3\ndescription: changed\nsource: local\n",
                encoding="utf-8",
            )
            self.assertEqual(
                original,
                catalog.profile_content_digest(profile, "agency-example", "1.2.3"),
            )

            (profile / "SOUL.md").write_text("changed professional identity\n", encoding="utf-8")
            soul_changed = catalog.profile_content_digest(profile, "agency-example", "1.2.3")
            self.assertNotEqual(original, soul_changed)

            (profile / "SOUL.md").write_text("professional identity\n", encoding="utf-8")
            (references / "checklist.md").write_text("changed evidence\n", encoding="utf-8")
            reference_changed = catalog.profile_content_digest(profile, "agency-example", "1.2.3")
            self.assertNotEqual(original, reference_changed)

            (references / "checklist.md").write_text("evidence\n", encoding="utf-8")
            (profile / "config.yaml").write_text("toolsets:\n  - kanban\n", encoding="utf-8")
            config_changed = catalog.profile_content_digest(profile, "agency-example", "1.2.3")
            self.assertNotEqual(original, config_changed)

            (profile / "config.yaml").unlink()
            (profile / ".no-bundled-skills").write_text("", encoding="utf-8")
            marker_changed = catalog.profile_content_digest(profile, "agency-example", "1.2.3")
            self.assertNotEqual(original, marker_changed)

    def test_content_digest_binds_executable_file_semantics(self):
        with tempfile.TemporaryDirectory() as temporary:
            profile = Path(temporary) / "agency-example"
            skill = profile / "skills" / "tooling"
            scripts = skill / "scripts"
            scripts.mkdir(parents=True)
            (profile / "SOUL.md").write_text("identity\n", encoding="utf-8")
            (skill / "SKILL.md").write_text("run helper\n", encoding="utf-8")
            script = scripts / "helper.sh"
            script.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            script.chmod(0o644)

            not_executable = catalog.profile_content_digest(
                profile, "agency-example", "1.0.0"
            )
            script.chmod(0o755)
            executable = catalog.profile_content_digest(profile, "agency-example", "1.0.0")
            self.assertNotEqual(not_executable, executable)

    def test_content_digest_binds_name_and_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            profile = Path(temporary) / "agency-example"
            skill = profile / "skills" / "review"
            skill.mkdir(parents=True)
            (profile / "SOUL.md").write_text("identity\n", encoding="utf-8")
            (skill / "SKILL.md").write_text("procedure\n", encoding="utf-8")

            baseline = catalog.profile_content_digest(profile, "agency-example", "1.0.0")
            self.assertNotEqual(
                baseline,
                catalog.profile_content_digest(profile, "agency-other", "1.0.0"),
            )
            self.assertNotEqual(
                baseline,
                catalog.profile_content_digest(profile, "agency-example", "1.0.1"),
            )

    def test_content_digest_rejects_symlinks_in_behavior_content(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            profile = root / "agency-example"
            skill = profile / "skills" / "review"
            skill.mkdir(parents=True)
            (profile / "SOUL.md").write_text("identity\n", encoding="utf-8")
            (skill / "SKILL.md").write_text("procedure\n", encoding="utf-8")
            outside = root / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            (skill / "reference.md").symlink_to(outside)

            with self.assertRaisesRegex(ValueError, "does not permit symlinks"):
                catalog.profile_content_digest(profile, "agency-example", "1.0.0")

    def test_distribution_identity_guard_fails_closed_on_drift(self):
        matching = {
            "name": "agency-example",
            "version": "1.0.0",
            "description": "example",
        }
        catalog._validate_distribution_identity(matching, "agency-example", "1.0.0")

        for drifted in (
            {**matching, "name": "agency-other"},
            {**matching, "version": "9.9.9"},
        ):
            with self.subTest(drifted=drifted):
                with self.assertRaisesRegex(ValueError, "does not match Agency catalog"):
                    catalog._validate_distribution_identity(
                        drifted, "agency-example", "1.0.0"
                    )


if __name__ == "__main__":
    unittest.main()
