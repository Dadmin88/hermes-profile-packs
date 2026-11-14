"""CLI: list, run/preflight, review, compare. No live calls from default CI."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time

from evals.core import (ROOT, GRADER_VERSION, compare_runs, digest, git_revision, grade,
                        load_cases, profile_path, public_request, review_template, tree_hashes, usage_total)


def manifest(args, root):
    settings = {"model": args.model, "provider": args.provider, "base_url": args.base_url,
                "max_output_tokens": args.max_output_tokens, "connection": getattr(args, "connection", "api-key"),
                "hermes_source": str(Path(args.hermes_source).resolve()), "preflight": args.preflight}
    data = {"schema_version": 1, "pack_commit": git_revision(root), "runtime_commit": git_revision(Path(args.hermes_source)),
            "model": args.model, "provider": args.provider, "base_url": args.base_url,
            "settings_hash": digest({k: v for k, v in settings.items() if k not in {"hermes_source", "preflight"}}),
            "adapter_version": digest({k: v for k, v in tree_hashes(root / "evals").items()
                                       if not k.startswith("web/") and k != "workbench.py"}), "grader_version": GRADER_VERSION,
            "browser_version": None, "preflight": args.preflight,
            "limitations": ["Controlled fixture tools; no real delivery or production execution.",
                            "Native skill preprocessing disabled; no shell or script execution.",
                            "Semantic results require evidence-bound manual review.",
                            "Continuity prerequisites are retained but deferred."]}
    return settings, data


def execute(request, python, root, timeout):
    # Minimal environment prevents native imports from inheriting live profile/account settings.
    env = {k: os.environ[k] for k in ("PATH", "LANG", "LC_ALL", "SSL_CERT_FILE", "SSL_CERT_DIR", "PLAYWRIGHT_BROWSERS_PATH", "HERMES_EVAL_CHROMIUM") if k in os.environ}
    if "HERMES_EVAL_API_KEY" in os.environ:
        env["HERMES_EVAL_API_KEY"] = os.environ["HERMES_EVAL_API_KEY"]
    if request.get("settings", {}).get("connection") == "hermes-login":
        env["HERMES_EVAL_LOGIN_HOME"] = str(Path.home())
    env["PYTHONPATH"] = str(root)
    env["PYTHONUNBUFFERED"] = "1"
    # start_new_session lets a timeout stop the worker and any browser subprocesses.
    with tempfile.TemporaryDirectory(prefix="profile-eval-parent-") as tmp:
        env.update(HOME=tmp, HERMES_HOME=str(Path(tmp) / ".hermes"))
        command = [python, "-m", "evals.native_worker"]
        if request.get("settings", {}).get("connection") == "hermes-login" and not request["settings"].get("preflight"):
            # Let native PM activate its installed dependencies before creating the isolated
            # profile home. A -c entry survives native interpreter relaunch without losing
            # this repository's package path. No bootstrap flags or checks are bypassed.
            env.update(HOME=env["HERMES_EVAL_LOGIN_HOME"],
                       HERMES_HOME=str(Path(env["HERMES_EVAL_LOGIN_HOME"]) / ".hermes"))
            source = str(Path(request["settings"]["hermes_source"]).resolve())
            entry = (f"import sys, runpy; sys.path.insert(0, {source!r}); "
                     f"import hermes_bootstrap; sys.path.insert(0, {str(root)!r}); "
                     "runpy.run_module('evals.native_worker', run_name='__main__')")
            command = [python, "-c", entry]
        process = subprocess.Popen(command, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=tmp,
                                   env=env, start_new_session=True)
        timed_out = False
        previous = signal.getsignal(signal.SIGTERM)
        def terminate(signum, frame):
            raise KeyboardInterrupt("Run cancelled")
        signal.signal(signal.SIGTERM, terminate)
        try:
            try:
                out, err = process.communicate(json.dumps(request), timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(process.pid, signal.SIGKILL)
                out, err = process.communicate()
            except BaseException:
                if process.poll() is None:
                    os.killpg(process.pid, signal.SIGKILL)
                process.communicate()
                raise
        finally:
            signal.signal(signal.SIGTERM, previous)
    events, result = [], None
    for line in out.splitlines():
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(item, dict) and "event" in item:
            events.append(item["event"])
        if isinstance(item, dict) and "result" in item:
            result = item["result"]
    if result is None:
        result = {"mode": "native", "execution_status": "BLOCKED", "events": events,
                  "finals": [e["text"] for e in events if e["type"] == "final"], "artifact_checks": {},
                  "reason": "Worker timed out" if timed_out else "Worker failed before result; " + err[-2000:]}
        if timed_out and any(e["type"] == "model_usage" for e in events):
            result["execution_status"] = "FAIL"
    return result


def atomic_json(path, value):
    # Readers always see a complete snapshot, including while the workbench polls.
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, indent=2) + "\n")
    temp.replace(path)


def write_report(run, output):
    output.mkdir(parents=True, exist_ok=True)
    atomic_json(output / "results.json", run)
    counts = {s: sum(r["grade"]["status"] == s for r in run["results"]) for s in ("PASS", "FAIL", "BLOCKED", "NOT RUN")}
    lines = ["# Profile evaluation results", "", "Behavioral verdicts require observed native execution and semantic review.", "",
             "Counts: " + ", ".join(f"{k}={v}" for k, v in counts.items()), "",
             "| Case | Repeat | Status | Efficiency | Reason |", "| --- | --- | --- | --- | --- |"]
    for r in run["results"]:
        reason = "; ".join(r["grade"]["failures"] + r["grade"]["blocked"])
        lines.append(f"| {r['case_id']} | {r['repetition']} | {r['grade']['status']} | {r['grade']['efficiency_status']} | {reason.replace('|', '/').replace(chr(10), ' ')} |")
    (output / "report.md").write_text("\n".join(lines) + "\n")


def outside_repo(output, root):
    if output.resolve().is_relative_to(root.resolve()):
        raise ValueError("Evaluation output must be outside the repository (runtime transcripts are not distributions)")


def run_command(args):
    root = args.root.resolve()
    outside_repo(args.output, root)
    cases = load_cases(root, args.suite)
    if args.case:
        ids = set(args.case)
        known = {c["id"] for c in cases}
        if ids - known:
            raise ValueError(f"Unknown case IDs: {sorted(ids - known)}")
        cases = [c for c in cases if c["id"] in ids]
    settings, meta = manifest(args, root)
    results, templates = [], []
    spent, attempts = 0, 0
    for c in cases:
        for repeat in range(args.repeat):
            if c.get("unsupported_reason"):
                evidence = {"mode": "native", "execution_status": "BLOCKED", "reason": c["unsupported_reason"], "events": [], "finals": []}
            elif not args.preflight and (spent >= args.max_total_tokens or attempts >= args.limit):
                evidence = {"mode": "native", "execution_status": "NOT RUN", "reason": "Run token/case budget exhausted", "events": [], "finals": []}
            else:
                request = public_request(c, profile_path(root, c["profile"]), settings)
                request["settings"] = dict(settings, token_budget_remaining=max(1, args.max_total_tokens-spent))
                evidence = execute(request, args.python, root, c["limits"]["max_seconds"] + 30)
                attempts += 1
            record = {**evidence, "case_id": c["id"], "profile": c["profile"], "case_hash": c["case_hash"],
                      "repetition": repeat, "profile_hash": digest(tree_hashes(profile_path(root, c["profile"])))}
            record["evidence_hash"] = digest(evidence)
            record["usage"] = usage_total(record.get("events", []))
            if record.get("execution_status") != "COMPLETE":
                record["usage"]["complete"] = False
            spent += sum((e.get("input_tokens") or 0) + (e.get("output_tokens") or 0)
                         for e in record.get("events", []) if e["type"] == "model_usage")
            # Missing usage prevents further spend: unknown does not mean free.
            if not args.preflight and record.get("execution_status") == "COMPLETE" and not record["usage"]["complete"]:
                spent = args.max_total_tokens
            record["grade"] = grade(c, record)
            results.append(record)
            templates.append(review_template(c, record))
            if record.get("browser_version"):
                meta["browser_version"] = record["browser_version"]
            print(f"{c['id']} [{repeat}]: {record['grade']['status']} — {record.get('reason', '')}", flush=True)
            write_report({"manifest": meta, "results": results}, args.output)
    (args.output / "review-template.json").write_text(json.dumps(templates, indent=2) + "\n")
    return 1 if any(r["grade"]["status"] == "FAIL" for r in results) else 2 if any(r["grade"]["status"] != "PASS" for r in results) else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    ls = sub.add_parser("list"); ls.add_argument("--suite", choices=["pilot", "existing", "all"], default="pilot")
    run = sub.add_parser("run")
    run.add_argument("--suite", choices=["pilot", "existing", "all"], default="pilot")
    run.add_argument("--case", action="append")
    run.add_argument("--hermes-source", required=True)
    run.add_argument("--python", default=sys.executable)
    run.add_argument("--preflight", action="store_true")
    run.add_argument("--connection", choices=["api-key", "hermes-login"], default="api-key")
    run.add_argument("--model", default="")
    run.add_argument("--provider", default="openai")
    run.add_argument("--base-url", default="")
    run.add_argument("--max-output-tokens", type=int, default=2048)
    run.add_argument("--max-total-tokens", type=int, default=60000)
    run.add_argument("--limit", type=int, default=18)
    run.add_argument("--repeat", type=int, default=1)
    run.add_argument("--output", type=Path, required=True)
    review = sub.add_parser("review")
    review.add_argument("results", type=Path); review.add_argument("reviews", type=Path)
    review.add_argument("--output", type=Path, required=True)
    comp = sub.add_parser("compare")
    comp.add_argument("baseline", type=Path); comp.add_argument("candidate", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            cases = load_cases(args.root, args.suite)
            print(json.dumps([{"id": c["id"], "profile": c["profile"], "title": c["title"],
                               "deferred": bool(c.get("unsupported_reason"))} for c in cases], indent=2))
            return 0
        if args.command == "run":
            if min(args.repeat, args.limit, args.max_output_tokens, args.max_total_tokens) < 1:
                raise ValueError("Budgets and repetition count must be positive")
            return run_command(args)
        if args.command == "compare":
            result = compare_runs(json.loads(args.baseline.read_text()), json.loads(args.candidate.read_text()))
            print(json.dumps(result, indent=2))
            return 0 if result["status"] == "NO_REGRESSION" else 2
        outside_repo(args.output, args.root)
        run = json.loads(args.results.read_text())
        reviews = json.loads(args.reviews.read_text())
        # Include both canonical and pilot IDs when grading a run of either suite.
        cases = {c["id"]: c for suite in ["existing", "pilot"] for c in load_cases(args.root, suite)}
        lookup = {(r["case_id"], r["evidence_hash"]): r for r in reviews}
        for record in run["results"]:
            c = cases[record["case_id"]]
            if c["case_hash"] != record["case_hash"]:
                raise ValueError("Case changed since execution; use the original checkout")
            # Verify result bytes before accepting a semantic review.
            evidence = {k: v for k, v in record.items() if k not in {"case_id", "profile", "case_hash", "repetition", "profile_hash", "evidence_hash", "usage", "grade"}}
            if digest(evidence) != record["evidence_hash"]:
                raise ValueError("Evidence was altered after execution")
            record["grade"] = grade(c, record, lookup.get((record["case_id"], record["evidence_hash"])))
        write_report(run, args.output)
        return 0 if all(r["grade"]["status"] == "PASS" for r in run["results"]) else 2
    except (ValueError, KeyError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
