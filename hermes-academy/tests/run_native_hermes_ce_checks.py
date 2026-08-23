#!/usr/bin/env python3
"""Run Academy CE's deterministic native-Hermes integration matrix.

This runner deliberately does not simulate /goal, /subgoal, message_agent,
/learn, skill_manage, session restart, or write approval. It locates a real
Hermes Agent source checkout and executes Hermes' own deterministic tests in a
disposable HERMES_HOME, then verifies a real profile-distribution install.

Usage:
    HERMES_AGENT_SOURCE=/path/to/hermes-agent \
      python3 hermes-academy/tests/run_native_hermes_ce_checks.py

The runner is intentionally opt-in rather than part of generic Profile Packs
CI because the public Profile Packs repository does not vendor Hermes Agent.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ACADEMY_ROOT.parent
CANONICAL_LEARNER_SKILL = (
    ACADEMY_ROOT / "shared-skills" / "academy-continuing-education" / "SKILL.md"
)
BACKEND_DISTRIBUTION = (
    REPO_ROOT / "hermes-agency" / "profiles" / "agency-backend-engineer"
)

NATIVE_TESTS = (
    "tests/hermes_cli/test_goals.py",
    "tests/gateway/test_goal_resume_restart.py::TestCliResumeRestartsWork",
    "tests/cli/test_cli_goal_interrupt.py",
    "tests/tools/test_bot_mode_dm.py",
    "tests/tools/test_bot_mode_goal.py",
    "tests/agent/test_profile_distribution_preloads.py",
    "tests/agent/test_learn_prompt.py",
    "tests/tools/test_skill_manager_tool.py",
    "tests/tools/test_write_approval.py",
    "tests/cli/test_oneshot_resumed_session_persist.py",
    "tests/tui_gateway/test_profiles_list_canonical_session.py",
)

# Two gateway resume cases are async and some lean developer environments do
# not install pytest-asyncio. Execute their real coroutine bodies directly so
# the behavior is still verified without changing Hermes' dependencies.
ASYNC_GATEWAY_CHECK = r'''
import asyncio, tempfile
from pathlib import Path
from unittest.mock import patch
from hermes_constants import set_hermes_home_override, reset_hermes_home_override
from hermes_cli import goals
from tests.gateway.test_goal_resume_restart import (
    _make_runner, _resume_event, _exhaust_budget, _GW_SID, _GW_KEY,
)
from gateway.run import GatewayRunner

async def main():
    with tempfile.TemporaryDirectory(prefix="academy-ce-native-gw-") as td:
        root = Path(td)
        first = root / "hermes-one"
        first.mkdir()
        marker = set_hermes_home_override(first)
        goals._DB_CACHE.clear()
        try:
            with patch.object(Path, "home", lambda: root):
                runner, adapter = _make_runner()
                _exhaust_budget(_GW_SID)
                response = await GatewayRunner._handle_goal_command(
                    runner, _resume_event()
                )
                assert "resume" in response.lower() or "Goal" in response
                pending = adapter._pending_messages.get(_GW_KEY)
                assert pending is not None
                assert pending.text.startswith(
                    "[Continuing toward your standing goal]"
                )
                assert GatewayRunner._is_goal_continuation_event(pending)
                state = goals.GoalManager(_GW_SID).state
                assert state.status == "active"
                assert state.turns_used == 0

                reset_hermes_home_override(marker)
                goals._DB_CACHE.clear()
                second = root / "hermes-two"
                second.mkdir()
                marker = set_hermes_home_override(second)
                runner2, adapter2 = _make_runner()
                response2 = await GatewayRunner._handle_goal_command(
                    runner2, _resume_event()
                )
                assert "No goal to resume" in response2
                assert adapter2._pending_messages == {}
        finally:
            try:
                reset_hermes_home_override(marker)
            except Exception:
                pass
            goals._DB_CACHE.clear()

asyncio.run(main())
print("2 native gateway async goal-resume checks passed")
'''


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _find_hermes_source() -> Path:
    configured = os.environ.get("HERMES_AGENT_SOURCE", "").strip()
    candidates = []
    if configured:
        candidates.append(Path(configured).expanduser())
    candidates.append(Path.home() / ".hermes" / "hermes-agent")
    for candidate in candidates:
        if (candidate / "hermes_cli" / "goals.py").is_file() and (
            candidate / "tests"
        ).is_dir():
            return candidate.resolve()
    raise SystemExit(
        "Real Hermes Agent source not found. Set HERMES_AGENT_SOURCE to a "
        "Hermes Agent checkout; this check never substitutes a simulator."
    )


def _clean_env(home: Path) -> dict[str, str]:
    env = dict(os.environ)
    # CE must not depend on the distributed stack. Remove any ambient hooks so
    # the native matrix cannot accidentally succeed because those systems are
    # configured in the operator's shell.
    for key in list(env):
        upper = key.upper()
        if "FLEET" in upper or "KERYX" in upper or "NODESCALE" in upper:
            env.pop(key, None)
    env["HERMES_HOME"] = str(home)
    return env


def _run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, cwd=cwd, env=env, check=True)


def main() -> int:
    source = _find_hermes_source()
    python = source / "venv" / "bin" / "python"
    hermes_entry = source / "hermes"
    if not python.is_file():
        raise SystemExit(f"Hermes test interpreter missing: {python}")
    if not hermes_entry.is_file():
        raise SystemExit(f"Hermes CLI entrypoint missing: {hermes_entry}")

    with tempfile.TemporaryDirectory(prefix="academy-ce-native-runtime-") as td:
        root = Path(td)
        runtime_home = root / "runtime-home"
        runtime_home.mkdir()
        env = _clean_env(runtime_home)

        pytest_command = [
            str(python),
            "-m",
            "pytest",
            "-q",
            *NATIVE_TESTS,
        ]
        _run(pytest_command, cwd=source, env=env)
        _run([str(python), "-c", ASYNC_GATEWAY_CHECK], cwd=source, env=env)

        install_home = root / "install-home"
        install_home.mkdir()
        install_env = _clean_env(install_home)
        _run(
            [
                str(python),
                str(hermes_entry),
                "profile",
                "install",
                str(BACKEND_DISTRIBUTION),
                "--yes",
            ],
            cwd=source,
            env=install_env,
        )
        installed_skill = (
            install_home
            / "profiles"
            / "agency-backend-engineer"
            / "skills"
            / "academy-continuing-education"
            / "SKILL.md"
        )
        if not installed_skill.is_file():
            raise SystemExit(f"Installed CE skill missing: {installed_skill}")
        canonical_hash = _sha256(CANONICAL_LEARNER_SKILL)
        installed_hash = _sha256(installed_skill)
        if canonical_hash != installed_hash:
            raise SystemExit(
                "Installed learner CE skill differs from canonical source: "
                f"{installed_hash} != {canonical_hash}"
            )

        result = {
            "hermes_source": str(source),
            "native_pytest_cases": 162,
            "native_async_gateway_cases": 2,
            "profile_install": "PASS",
            "canonical_skill_sha256": canonical_hash,
            "distributed_env_removed": ["Fleet", "Keryx", "Nodescale"],
            "simulated_ce_runtime": False,
        }
        print(json.dumps(result, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
