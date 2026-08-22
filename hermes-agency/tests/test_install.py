from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "install.py"
MANIFEST = json.loads((ROOT / "agency.json").read_text(encoding="utf-8"))


class InstallerContractTests(unittest.TestCase):
    def run_installer(self, *args: str, with_fake_hermes: bool = True):
        env = os.environ.copy()
        log_path: Path | None = None
        temp_dir: tempfile.TemporaryDirectory[str] | None = None

        if with_fake_hermes:
            temp_dir = tempfile.TemporaryDirectory()
            fake_dir = Path(temp_dir.name)
            log_path = fake_dir / "hermes-calls.jsonl"
            fake = fake_dir / "hermes"
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, pathlib, sys\n"
                "path = pathlib.Path(os.environ['HERMES_CALL_LOG'])\n"
                "with path.open('a', encoding='utf-8') as handle:\n"
                "    handle.write(json.dumps(sys.argv[1:]) + '\\n')\n",
                encoding="utf-8",
            )
            fake.chmod(0o755)
            env["PATH"] = str(fake_dir) + os.pathsep + env.get("PATH", "")
            env["HERMES_CALL_LOG"] = str(log_path)

        try:
            result = subprocess.run(
                [sys.executable, str(INSTALLER), *args],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            calls: list[list[str]] = []
            if log_path and log_path.exists():
                calls = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
            return result, calls
        finally:
            if temp_dir is not None:
                temp_dir.cleanup()

    def test_list_does_not_require_hermes(self):
        result, calls = self.run_installer("--list", with_fake_hermes=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"{MANIFEST['profile_count']} profiles", result.stdout)
        self.assertIn("agency-orchestrator", result.stdout)
        self.assertEqual(calls, [])

    def test_single_profile_installs_distribution_and_description(self):
        name = "agency-backend-engineer"
        result, calls = self.run_installer(name)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(calls), 2)

        install_call, describe_call = calls
        self.assertEqual(install_call[:2], ["profile", "install"])
        source = Path(install_call[2])
        self.assertEqual(source.resolve(), (ROOT / "profiles" / name).resolve())
        self.assertEqual(install_call[3:], ["--alias", "--yes"])
        self.assertTrue((source / "distribution.yaml").is_file())
        self.assertTrue(any((source / "skills").glob("*/SKILL.md")))

        self.assertEqual(describe_call[:3], ["profile", "describe", name])
        self.assertEqual(describe_call[3], "--text")
        self.assertTrue(describe_call[4].strip())

    def test_force_is_forwarded_to_hermes(self):
        result, calls = self.run_installer("agency-backend-engineer", "--force")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--force", calls[0])

    def test_category_installs_exact_category_roster(self):
        category = "qa"
        expected = {
            item["name"] for item in MANIFEST["profiles"] if item["category"] == category
        }
        result, calls = self.run_installer("--category", category)
        self.assertEqual(result.returncode, 0, result.stderr)
        install_calls = [call for call in calls if call[:2] == ["profile", "install"]]
        describe_calls = [call for call in calls if call[:2] == ["profile", "describe"]]
        installed = {Path(call[2]).name for call in install_calls}
        described = {call[2] for call in describe_calls}
        self.assertEqual(installed, expected)
        self.assertEqual(described, expected)
        self.assertEqual(len(calls), len(expected) * 2)

    def test_unknown_profile_is_rejected_before_hermes_invocation(self):
        result, calls = self.run_installer("agency-does-not-exist")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown profile", result.stderr)
        self.assertEqual(calls, [])

    def test_explicit_profiles_and_category_are_mutually_exclusive(self):
        result, calls = self.run_installer(
            "agency-backend-engineer", "--category", "engineering"
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("explicit profiles or --category", result.stderr)
        self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
