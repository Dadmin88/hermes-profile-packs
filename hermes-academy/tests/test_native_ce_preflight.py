"""Verify the native CE runner blocks unsupported source trees before execution."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "native_ce_runner", Path(__file__).with_name("run_native_hermes_ce_checks.py")
)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class NativeCePreflightTests(unittest.TestCase):
    def test_all_declared_files_present_passes_preflight(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td)
            for relative in {
                target.split("::", 1)[0] for target in runner.NATIVE_TESTS
            } | {runner.ASYNC_GATEWAY_TEST_FILE}:
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            self.assertEqual(runner._missing_required_native_test_files(source), [])

    def test_missing_file_blocks_before_subprocess(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td)
            missing = runner.NATIVE_TESTS[0].split("::", 1)[0]
            for target in runner.NATIVE_TESTS[1:]:
                path = source / target.split("::", 1)[0]
                path.parent.mkdir(parents=True, exist_ok=True)
                path.touch()
            output = io.StringIO()
            with patch.object(runner, "_find_hermes_source", return_value=source), \
                    patch.object(runner.subprocess, "run") as run, \
                    contextlib.redirect_stdout(output):
                self.assertEqual(runner.main(), 2)
            run.assert_not_called()
            result = json.loads(output.getvalue())
            self.assertEqual(result["status"], "BLOCKED")
            self.assertEqual(result["missing_required_test_files"], [missing])
            self.assertFalse(result["native_matrix_executed"])


if __name__ == "__main__":
    unittest.main()
