"""One native Hermes process per case. stdin contains only agent-visible inputs.

Run with an interpreter that already supports the selected Hermes source tree.
No credentials are copied from installed profiles. Explicit API configuration only.
"""
from __future__ import annotations

import hashlib
import inspect
import json
import os
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch

from evals.core import digest, tree_hashes
from evals.fixture_tools import FixtureTools, browser_observations


class EvaluationStop(BaseException):
    """Escape native callback error suppression without starting another provider call."""


def main():
    request = json.load(sys.stdin)
    settings = request["settings"]
    started = time.monotonic()
    events, finals = [], []
    output = {"mode": "native", "execution_status": "BLOCKED", "events": events, "finals": finals,
              "artifact_checks": {}, "reason": "Native worker did not complete"}
    def emit(kind, **data):
        event = {"id": f"event:{len(events)}", "type": kind, **data}
        events.append(event)
        # Stream evidence to the controller so timeouts retain partial traces.
        print(json.dumps({"event": event}), file=sys.__stdout__, flush=True)
    try:
        with tempfile.TemporaryDirectory(prefix="hermes-profile-eval-") as tmp:
            lab = Path(tmp)
            home, workspace = lab / "home", lab / "workspace"
            home.mkdir(); workspace.mkdir()
            os.environ.update(HOME=str(home), HERMES_HOME=str(home / ".hermes"), TMPDIR=str(lab),
                              XDG_CONFIG_HOME=str(home / "config"), XDG_DATA_HOME=str(home / "data"),
                              XDG_CACHE_HOME=str(home / "cache"))
            os.environ.pop("HERMES_PROFILE", None)
            source = Path(settings["hermes_source"]).resolve()
            sys.path.insert(0, str(source))
            os.chdir(workspace)
            import yaml
            from hermes_cli.profile_distribution import install_distribution
            profile_source = Path(request["profile_source"])
            manifest = yaml.safe_load((profile_source / "distribution.yaml").read_text())
            plan = install_distribution(str(profile_source), create_alias=False)
            target = plan.target_dir.resolve()
            if not target.is_relative_to(home):
                raise RuntimeError("Installer target escaped disposable home")
            installed = yaml.safe_load((target / "distribution.yaml").read_text())
            if installed.get("preload_skills", []) != manifest.get("preload_skills", []):
                raise RuntimeError("Native installer does not preserve distribution preload_skills; no compatibility shim applied")
            os.environ["HERMES_HOME"] = str(target)
            from tools.skills_sync import sync_skills
            sync_skills(quiet=True)
            # Full profile payload readback, including markers and referenced skill files.
            payload = tree_hashes(profile_source)
            for name, value in payload.items():
                if name == "distribution.yaml":
                    continue  # installer stamps provenance
                if not (target / name).is_file() or hashlib.sha256((target / name).read_bytes()).hexdigest() != value:
                    raise RuntimeError(f"Native install readback mismatch: {name}")
            os.environ["HERMES_HOME"] = str(target)
            os.environ["HERMES_PROFILE"] = request["profile"]
            output["installed_hash"] = digest(payload)
            output["installed_skills_hash"] = digest(tree_hashes(target / "skills"))
            emit("installed", profile=request["profile"], content_hash=output["installed_hash"])
            for name, content in request["fixture"].get("workspace_files", {}).items():
                from evals.core import within
                path = within(workspace, name)
                path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)
            if settings.get("preflight"):
                output.update(execution_status="PREFLIGHT", reason="Native installation/readback only; no model call")
            else:
                if not settings.get("model") or not settings.get("base_url") or not os.getenv("HERMES_EVAL_API_KEY"):
                    raise RuntimeError("Live evaluation requires explicit model, base URL and HERMES_EVAL_API_KEY")
                cfg_path = target / "config.yaml"
                cfg = yaml.safe_load(cfg_path.read_text()) if cfg_path.exists() else {}
                cfg = cfg or {}
                if any(v.get("enabled", True) for v in (cfg.get("mcp_servers") or {}).values()):
                    raise RuntimeError("Active MCP integrations unsupported in isolated pilot")
                # Do not let runtime imports load a project .env or installed account resolver.
                from hermes_cli import env_loader
                with patch.object(env_loader, "load_hermes_dotenv", return_value=[]):
                    from run_agent import AIAgent
                    from tools.registry import registry
                    from tools import skills_tool
                    from agent import turn_usage
                    from agent import turn_response_check
                    from agent.usage_pricing import normalize_usage
                    required = {"load_soul_identity", "tool_complete_callback", "skip_memory", "skip_background_review"}
                    if not required <= set(inspect.signature(AIAgent).parameters):
                        raise RuntimeError("Unsupported native AIAgent API")
                    fixture_tools = FixtureTools(request, workspace, emit)
                    for schema in fixture_tools.schemas():
                        name = schema["name"]
                        registry.register(name=name, toolset="profile_eval", schema=schema,
                                          handler=lambda args, _name=name, **kw: fixture_tools.call(_name, args))
                    # Native skill functions retained; preprocessing is disabled so skill reads cannot execute shell snippets.
                    def view(args, **kw):
                        result = skills_tool.skill_view(args["name"], file_path=args.get("file_path"), preprocess=False)
                        parsed = json.loads(result)
                        emit("tool_result", tool="skill_view", args=args, result=parsed)
                        rel = parsed.get("path", "")
                        path = (target / "skills" / rel).resolve()
                        if parsed.get("success") and path.is_relative_to(target / "skills") and path.is_file():
                            content = parsed.get("content")
                            if content == path.read_text():
                                emit("skill_loaded", source_path=str(
                                     Path(f"hermes-{request['profile'].split('-')[0]}/profiles") / request["profile"] / "skills" / rel),
                                     content_hash=hashlib.sha256(content.encode()).hexdigest(), verified=True, preloaded=False)
                        return result
                    registry.register(name="skill_view", toolset="profile_eval", schema=skills_tool.SKILL_VIEW_SCHEMA, handler=view, override=True)
                    registry.register(name="skills_list", toolset="profile_eval", schema=skills_tool.SKILLS_LIST_SCHEMA,
                                      handler=lambda args, **kw: skills_tool.skills_list(category=args.get("category")), override=True)
                    from tools.skills_tool import clear_skills_cache
                    clear_skills_cache()
                    model_steps = 0
                    def bound_step(*args):
                        nonlocal model_steps
                        model_steps += 1
                        if model_steps > request["limits"]["max_model_turns"]:
                            output.update(execution_status="FAIL", reason="Case model-turn limit exceeded")
                            raise EvaluationStop(output["reason"])
                    agent = AIAgent(model=settings["model"], provider=settings["provider"], base_url=settings["base_url"],
                                    api_key=os.environ["HERMES_EVAL_API_KEY"], enabled_toolsets=["profile_eval"],
                                    max_iterations=request["limits"]["max_model_turns"], max_tokens=settings["max_output_tokens"],
                                    quiet_mode=True, save_trajectories=False, load_soul_identity=True,
                                    skip_memory=True, skip_background_review=True, cwd=str(workspace),
                                    run_budget_seconds=request["limits"]["max_seconds"], fallback_model=None,
                                    step_callback=bound_step)
                    allowed = {s["name"] for s in fixture_tools.schemas()} | {"skills_list", "skill_view"}
                    if agent.valid_tool_names != allowed:
                        raise RuntimeError(f"Unexpected native tool surface: {sorted(agent.valid_tool_names ^ allowed)}")
                    prompt = agent._build_system_prompt()
                    soul = (target / "SOUL.md").read_text().strip()
                    if soul not in prompt:
                        raise RuntimeError("Native prompt did not include complete installed SOUL")
                    # Fail closed if any declared preload is not observable in the actual prompt.
                    for name in manifest.get("preload_skills", []):
                        matches = [p for p in (target / "skills").rglob("SKILL.md") if p.parent.name == name]
                        if len(matches) != 1 or matches[0].read_text().strip() not in prompt:
                            raise RuntimeError(f"Native preload injection unverified: {name}")
                        p = matches[0]
                        emit("skill_loaded", source_path=str(Path(f"hermes-{request['profile'].split('-')[0]}/profiles") /
                             request["profile"] / p.relative_to(target)), content_hash=hashlib.sha256(p.read_bytes()).hexdigest(),
                             verified=True, preloaded=True)
                    emit("prompt_loaded", soul_hash=hashlib.sha256(soul.encode()).hexdigest(), prompt_hash=hashlib.sha256(prompt.encode()).hexdigest())
                    original_usage = turn_usage.record_response_usage
                    def capture_usage(agent, response, **kwargs):
                        raw = getattr(response, "usage", None)
                        if raw:
                            u = normalize_usage(raw, provider=agent.provider, api_mode=agent.api_mode)
                            emit("model_usage", input_tokens=u.prompt_tokens, output_tokens=u.output_tokens,
                                 cached_input_tokens=u.cache_read_tokens, reasoning_tokens=u.reasoning_tokens)
                        else:
                            emit("model_usage", input_tokens=None, output_tokens=None)
                        result = original_usage(agent, response, **kwargs)
                        used = sum((e.get("input_tokens") or 0) + (e.get("output_tokens") or 0)
                                   for e in events if e["type"] == "model_usage")
                        if used >= settings.get("token_budget_remaining", 60000):
                            raise EvaluationStop("Evaluation token budget exhausted; no further model call permitted")
                        return result
                    history = []
                    with patch.object(turn_usage, "record_response_usage", capture_usage), patch.object(turn_response_check, "record_response_usage", capture_usage):
                        for message in request["messages"]:
                            response = agent.run_conversation(message["content"], conversation_history=history)
                            history = response.get("messages", [])
                            final = response.get("final_response", "")
                            finals.append(final)
                            emit("final", text=final)
                            if response.get("error") or not final:
                                raise RuntimeError("Native turn failed or returned no final response")
                            if response.get("completed") is False:
                                output.update(execution_status="FAIL", reason="Native turn did not complete within its limits")
                                raise RuntimeError(output["reason"])
                    output.update(execution_status="COMPLETE", reason="")
                    if hasattr(agent, "close"):
                        agent.close()
                    if request["environment"] == "isolated-browser-workspace":
                        obs = browser_observations(workspace)
                        output["artifact_checks"] = obs["checks"]
                        output["browser_version"] = obs["observations"]["browser_version"]
                        emit("artifact_check", result=obs)
                    output["artifacts"] = {str(p.relative_to(workspace)): p.read_text() for p in workspace.rglob("*") if p.is_file()}
    except (Exception, EvaluationStop) as exc:
        if output["execution_status"] != "FAIL":
            output["execution_status"] = "BLOCKED"
        output["reason"] = f"{type(exc).__name__}: {exc}"
    output["duration_seconds"] = time.monotonic() - started
    print(json.dumps({"result": output}), file=sys.__stdout__, flush=True)


if __name__ == "__main__":
    main()
