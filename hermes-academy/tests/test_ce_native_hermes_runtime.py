"""Opt-in native Hermes Agent integration gate for Academy CE.

Generic Profile Packs CI does not vendor Hermes Agent, so this test is skipped
unless HERMES_AGENT_SOURCE is explicitly provided. Release/preflight gates on a
Hermes development machine must set that variable and execute this test.
"""
from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path

RUNNER = Path(__file__).with_name("run_native_hermes_ce_checks.py")


class NativeHermesRuntimeIntegrationTest(unittest.TestCase):
    @unittest.skipUnless(
        os.environ.get("HERMES_AGENT_SOURCE"),
        "set HERMES_AGENT_SOURCE to execute the real Hermes runtime matrix",
    )
    def test_real_hermes_runtime_matrix(self):
        self.assertTrue(RUNNER.is_file())
        subprocess.run(
            [sys.executable, str(RUNNER)],
            check=True,
            env=dict(os.environ),
        )


if __name__ == "__main__":
    unittest.main()
