"""Local browser workbench. Run with python -m evals.workbench --help."""
from __future__ import annotations

import argparse
import copy
import fcntl
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import signal
import subprocess
import sys
import threading
from urllib.parse import parse_qs, urlsplit
import uuid

from evals.connection import validate_login_settings
from evals.core import GRADER_VERSION, ROOT, compare_runs, digest, grade, load_cases, review_template
from evals.run import atomic_json, outside_repo, write_report

WEB = Path(__file__).with_name("web")
RECORD_METADATA = {"case_id", "profile", "case_hash", "repetition", "profile_hash", "evidence_hash", "usage", "grade"}


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def integer(data, key, default, low, high):
    value = data.get(key, default)
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{key} must be an integer between {low} and {high}")
    return value


class Workbench:
    def __init__(self, root, output, hermes_source, python=sys.executable, defaults=None, connection="api-key"):
        self.root = Path(root).resolve()
        self.output = Path(output).resolve()
        outside_repo(self.output, self.root)
        self.output.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.hermes_source = Path(hermes_source).resolve()
        self.python = str(Path(python).absolute())
        self.defaults = defaults or {}
        self.connection = connection
        if connection == "hermes-login":
            validate_login_settings(self.defaults)
        self.token = secrets.token_urlsafe(32)
        self.lock = threading.RLock()
        self.active = None
        self.process = None
        self.catalogs = {suite: load_cases(self.root, suite) for suite in ("pilot", "existing", "all")}
        self.cases = {c["id"]: c for suite in ("existing", "pilot") for c in self.catalogs[suite]}
        # A previous server's interrupted run is never shown as still running.
        for directory in self.output.glob("*/job.json"):
            job = json.loads(directory.read_text())
            if job.get("status") == "RUNNING":
                job.update(status="INTERRUPTED", finished=now())
                atomic_json(directory, job)

    def directory(self, run_id):
        if not re.fullmatch(r"[0-9a-f]{32}", run_id):
            raise ValueError("Invalid run ID")
        path = self.output / run_id
        if path.is_symlink() or not path.is_dir():
            raise ValueError("Run not found")
        return path

    def jobs(self):
        jobs = []
        for path in self.output.glob("*/job.json"):
            job = json.loads(path.read_text())
            result = path.parent / "results.json"
            records = json.loads(result.read_text())["results"] if result.exists() else []
            reviewed = path.parent / "reviewed" / "results.json"
            if reviewed.exists():
                records = json.loads(reviewed.read_text())["results"]
            job["completed"] = len(records)
            job["counts"] = {s: sum(r["grade"]["status"] == s for r in records) for s in ("PASS", "FAIL", "BLOCKED", "NOT RUN")}
            jobs.append(job)
        return sorted(jobs, key=lambda x: x["created"], reverse=True)

    def bootstrap(self):
        return {"csrf_token": self.token, "defaults": self.defaults,
                "connection": self.connection,
                "credential_configured": bool(os.environ.get("HERMES_EVAL_API_KEY")),
                "runtime_available": (self.hermes_source / "run_agent.py").is_file(),
                "jobs": self.jobs()}

    def start(self, data):
        suite = data.get("suite", "pilot")
        if suite not in self.catalogs:
            raise ValueError("Unknown suite")
        ids = data.get("case_ids")
        if not isinstance(ids, list) or not ids or any(not isinstance(i, str) for i in ids):
            raise ValueError("Select at least one case")
        known = {c["id"] for c in self.catalogs[suite]}
        if len(ids) != len(set(ids)) or not set(ids) <= known:
            raise ValueError("Unknown or duplicate case IDs")
        mode = data.get("mode", "preflight")
        if mode not in {"preflight", "live"}:
            raise ValueError("Choose setup check or live evaluation")
        settings = {}
        for key in ("model", "provider", "base_url"):
            settings[key] = data.get(key, self.defaults.get(key, ""))
            if not isinstance(settings[key], str) or len(settings[key]) > 500:
                raise ValueError(f"Invalid {key}")
        if self.connection == "hermes-login":
            validate_login_settings(settings)
        if mode == "live":
            if not all(settings.values()) or (self.connection == "api-key" and not os.environ.get("HERMES_EVAL_API_KEY")):
                raise ValueError("Live evaluation needs a model, provider, base URL and server-side HERMES_EVAL_API_KEY")
            url = urlsplit(settings["base_url"])
            if url.scheme not in {"https", "http"} or not url.hostname or url.username or url.password:
                raise ValueError("Base URL must be an HTTP(S) endpoint without embedded credentials")
        repeat = integer(data, "repeat", 1, 1, 5)
        budget = integer(data, "max_total_tokens", 60000, 1, 1000000)
        output_tokens = integer(data, "max_output_tokens", 2048, 1, 32768)
        label = data.get("label", "")
        if not isinstance(label, str) or len(label) > 100:
            raise ValueError("Run label must be at most 100 characters")
        with self.lock:
            if self.active:
                raise ValueError("A run is already active. Wait for it to finish or stop it first.")
            run_id = uuid.uuid4().hex
            directory = self.output / run_id
            directory.mkdir(mode=0o700)
            job = {"id": run_id, "label": label.strip() or ("Setup check" if mode == "preflight" else "Live evaluation"),
                   "mode": mode, "suite": suite, "case_ids": ids, "total": len(ids) * repeat,
                   "created": now(), "status": "RUNNING", "settings": settings,
                   "repeat": repeat, "max_total_tokens": budget, "max_output_tokens": output_tokens}
            atomic_json(directory / "job.json", job)
            command = [sys.executable, "-m", "evals.run", "--root", str(self.root), "run", "--suite", suite,
                       "--hermes-source", str(self.hermes_source), "--python", self.python,
                       "--output", str(directory), "--connection", self.connection, "--repeat", str(repeat), "--limit", str(len(ids) * repeat),
                       "--max-total-tokens", str(budget), "--max-output-tokens", str(output_tokens)]
            for key, value in settings.items():
                command.extend(["--" + key.replace("_", "-"), value])
            for case_id in ids:
                command.extend(["--case", case_id])
            if mode == "preflight":
                command.append("--preflight")
            try:
                with (directory / "runner.log").open("w") as log:
                    self.process = subprocess.Popen(command, cwd=self.root, stdout=log, stderr=log, start_new_session=True)
            except OSError:
                job.update(status="ERROR", finished=now())
                atomic_json(directory / "job.json", job)
                raise
            self.active = run_id
            threading.Thread(target=self._watch, args=(run_id, self.process), daemon=True).start()
            return job

    def _watch(self, run_id, process):
        code = process.wait()
        with self.lock:
            directory = self.directory(run_id)
            job = json.loads((directory / "job.json").read_text())
            if job["status"] == "RUNNING":
                job["status"] = "FINISHED" if code in {0, 1, 2} and (directory / "results.json").exists() else "ERROR"
            job.update(exit_code=code, finished=now())
            atomic_json(directory / "job.json", job)
            self.active = None
            self.process = None

    def cancel(self, run_id):
        with self.lock:
            if self.active != run_id or self.process is None:
                raise ValueError("This run is not active")
            directory = self.directory(run_id)
            job = json.loads((directory / "job.json").read_text())
            job["status"] = "CANCELLED"
            atomic_json(directory / "job.json", job)
            # Runner's SIGTERM handler kills the isolated worker/browser group too.
            if self.process.poll() is None:
                self.process.terminate()
            return job

    def close(self):
        with self.lock:
            if self.active:
                self.cancel(self.active)

    def run_data(self, run_id):
        directory = self.directory(run_id)
        result = directory / "results.json"
        run = json.loads(result.read_text()) if result.exists() else {"manifest": {}, "results": []}
        review_path = directory / "reviews.json"
        reviews = json.loads(review_path.read_text()) if review_path.exists() else {}
        reviewed = directory / "reviewed" / "results.json"
        if reviewed.exists():
            run = json.loads(reviewed.read_text())
        templates = []
        for i, record in enumerate(run["results"]):
            case = self.cases.get(record["case_id"])
            templates.append(reviews.get(str(i)) or (review_template(case, record) if case else None))
        log = directory / "runner.log"
        return {"job": json.loads((directory / "job.json").read_text()), "run": run, "reviews": templates,
                "log": log.read_text(errors="replace")[-12000:] if log.exists() else ""}

    def review(self, run_id, index, review):
        with self.lock:
            if self.active == run_id:
                raise ValueError("Wait for execution to finish before reviewing")
            directory = self.directory(run_id)
            run = json.loads((directory / "results.json").read_text())
            if type(index) is not int or not 0 <= index < len(run["results"]) or not isinstance(review, dict):
                raise ValueError("Invalid review")
            if run.get("manifest", {}).get("synthetic"):
                raise ValueError("Synthetic walkthroughs are read-only examples, not live evaluations")
            record = run["results"][index]
            case = self.cases[record["case_id"]]
            if record["case_hash"] != case["case_hash"]:
                raise ValueError("Case changed since execution; review using the original checkout")
            evidence = {k: v for k, v in record.items() if k not in RECORD_METADATA}
            if digest(evidence) != record["evidence_hash"]:
                raise ValueError("Evidence was altered after execution")
            if any(review.get(key) != record[key] for key in ("case_id", "case_hash", "evidence_hash")):
                raise ValueError("Review does not match this record")
            # Parse structured claims strictly; incomplete form fields may be saved as drafts.
            claims = review.get("success_claims", [])
            if not isinstance(claims, list) or any(not isinstance(c, dict) or not isinstance(c.get("tool"), str)
                    or c.get("outcome") not in {"operation", "checks_passed"}
                    or not isinstance(c.get("event_ids"), list)
                    or any(not isinstance(e, str) for e in c["event_ids"]) for c in claims):
                raise ValueError("Success claims need a tool, evidence IDs, and an outcome")
            if not isinstance(review.get("evidence_ids"), list) or any(not isinstance(e, str) for e in review["evidence_ids"]):
                raise ValueError("Evidence IDs must be a list of strings")
            try:
                grade(case, record, review)
            except (TypeError, KeyError, AttributeError) as exc:
                raise ValueError("Malformed review fields") from exc
            path = directory / "reviews.json"
            reviews = json.loads(path.read_text()) if path.exists() else {}
            reviews[str(index)] = copy.deepcopy(review)
            # Regrade every record against immutable execution evidence.
            for i, entry in enumerate(run["results"]):
                c = self.cases[entry["case_id"]]
                if c["case_hash"] != entry["case_hash"] or digest({k: v for k, v in entry.items() if k not in RECORD_METADATA}) != entry["evidence_hash"]:
                    raise ValueError("Run evidence or case definitions changed")
                entry["grade"] = grade(c, entry, reviews.get(str(i)))
            run["manifest"]["grader_version"] = GRADER_VERSION
            atomic_json(path, reviews)
            write_report(run, directory / "reviewed")
            return run["results"][index]["grade"]

    def compare(self, baseline, candidate):
        for run_id in (baseline, candidate):
            job = json.loads((self.directory(run_id) / "job.json").read_text())
            if job["status"] != "FINISHED":
                raise ValueError("Compare completed runs; cancelled or partial runs cannot establish regression")
        return compare_runs(self.run_data(baseline)["run"], self.run_data(candidate)["run"])


def handler_for(app):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, status, data, mime="application/json"):
            body = json.dumps(data).encode() if mime == "application/json" else data
            self.send_response(status)
            self.send_header("Content-Type", mime + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            self.end_headers()
            self.wfile.write(body)

        def allowed(self, mutation=False):
            host = self.headers.get("Host", "")
            port = self.server.server_port
            if host not in {f"localhost:{port}", f"127.0.0.1:{port}"}:
                return False
            origin = self.headers.get("Origin")
            if origin and origin != "http://" + host:
                return False
            return not mutation or (self.headers.get("Content-Type", "").split(";")[0] == "application/json"
                                    and secrets.compare_digest(self.headers.get("X-Workbench-Token", ""), app.token))

        def do_GET(self):
            if not self.allowed():
                return self.send(403, {"error": "Local same-origin requests only"})
            parsed = urlsplit(self.path)
            try:
                if parsed.path in {"/", "/app.js", "/style.css"}:
                    name, mime = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"), "/style.css": ("style.css", "text/css")}[parsed.path]
                    return self.send(200, (WEB / name).read_bytes(), mime)
                if parsed.path == "/api/bootstrap":
                    return self.send(200, app.bootstrap())
                if parsed.path == "/api/cases":
                    suite = parse_qs(parsed.query).get("suite", ["pilot"])[0]
                    return self.send(200, app.catalogs[suite])
                if parsed.path == "/api/runs":
                    return self.send(200, app.jobs())
                match = re.fullmatch(r"/api/runs/([0-9a-f]{32})", parsed.path)
                if match:
                    return self.send(200, app.run_data(match[1]))
                self.send(404, {"error": "Not found"})
            except (ValueError, KeyError, OSError) as exc:
                self.send(400, {"error": str(exc)})

        def do_POST(self):
            if not self.allowed(mutation=True):
                return self.send(403, {"error": "Local request token required"})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 1000000:
                    raise ValueError("Invalid request size")
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict):
                    raise ValueError("Expected a JSON object")
                if self.path == "/api/runs":
                    return self.send(201, app.start(data))
                if self.path == "/api/compare":
                    return self.send(200, app.compare(data["baseline"], data["candidate"]))
                match = re.fullmatch(r"/api/runs/([0-9a-f]{32})/(cancel|review)", self.path)
                if match:
                    value = app.cancel(match[1]) if match[2] == "cancel" else app.review(match[1], data["index"], data["review"])
                    return self.send(200, value)
                self.send(404, {"error": "Not found"})
            except (ValueError, KeyError, TypeError, OSError) as exc:
                self.send(400, {"error": str(exc)})
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--hermes-source", type=Path, required=True)
    parser.add_argument("--python", default=sys.executable, help="Interpreter with Hermes dependencies")
    parser.add_argument("--output", type=Path, default=Path.home() / ".local/share/hermes-eval-workbench")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--connection", choices=["api-key", "hermes-login"], default="api-key")
    parser.add_argument("--model", default="")
    parser.add_argument("--provider", default="openai")
    parser.add_argument("--base-url", default="")
    args = parser.parse_args()
    outside_repo(args.output, args.root)
    args.output.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = (args.output / ".workbench.lock").open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        parser.error("Another workbench is using this output directory")
    app = Workbench(args.root, args.output, args.hermes_source, args.python,
                    {key: getattr(args, key) for key in ("model", "provider", "base_url")}, args.connection)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(app))
    def stop(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    print(f"Hermes Eval Workbench: http://localhost:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        app.close()
        server.server_close()


if __name__ == "__main__":
    main()
