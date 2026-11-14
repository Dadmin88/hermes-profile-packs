# Evaluation Workbench

A local website for selecting Profile Packs cases, launching bounded runs, inspecting answers and tool traces, reviewing behavior, and comparing baselines. It runs the same native adapter and grader as the CLI. There is no separate hosted service, database, frontend build, or JavaScript dependency installation.

## Start once, use the browser

Use Python 3.12+ with PyYAML for the server. The worker interpreter must have the dependencies required by your Hermes source checkout. The runtime is installed into a fresh disposable home for each case; installed account credentials and personal profiles are not copied.

```bash
python -m evals.workbench \
  --hermes-source /path/to/hermes-agent \
  --python /path/to/hermes-python \
  --output /path/outside/repository/eval-runs
```

Open **http://localhost:8765** on the same computer. Keep the server running, or launch it with your normal user service manager. `--port` changes the port. The server intentionally binds to loopback; it is not a public deployment or multi-user service. One server may use a results directory at a time.

1. In **Case library**, select the pilot or existing suite and filter by profile or task. Open a case to inspect its prompt, expectations, fixture, and skill contract.
2. Select one case first and run a **Setup check**. This makes no model calls. A successful install reports execution `PREFLIGHT`; the behavioral verdict remains `BLOCKED` because behavior has not been tested.
3. For a **Live evaluation**, configure a provider, model, API base URL, repetitions, and token limits. Supply `HERMES_EVAL_API_KEY` in the server environment before starting it. The browser displays credential availability, never the key. `--model`, `--provider`, and `--base-url` set defaults. No automatic account fallback is used.
4. In **Run history**, inspect the case's final answers, ordered tool evidence, installation results, screenshots when available, deterministic checks, and usage. Stop an active run if needed. Unfinished cases remain unexecuted; cancellation never manufactures a result.
5. Review each completed live case in the browser: requirements met, prohibited behavior observed, quality scores, cited event IDs, reasoning, and every tool/test success claim. An incomplete review remains blocked. A claim contradicted by tool evidence fails even if the rest of the review is positive.
6. After changing a SOUL or skill, run the same cases and settings. In **Compare runs**, choose a baseline and candidate. Provenance or case mismatches prevent comparison; efficiency deltas require passing results with complete usage and matching cache regimes.

Token limits are checked between calls, so a final call can exceed the remaining token budget. Case deadlines and turn limits also apply. Only one run executes at a time. Results appear as each case finishes; the current case's streamed events are retained by the runner but are not displayed until that case returns.

## Evidence and persistence

The selected output directory stores a folder for each run: `job.json`, immutable execution `results.json`, `runner.log`, `reviews.json`, and `reviewed/results.json` plus the reviewed Markdown report. Browser exports provide result/review JSON. Files stay outside the repository and should not be committed. Restarting the server preserves history; a run interrupted by a server crash is marked `INTERRUPTED`, not resumed automatically. Stop the process tree before restarting after a hard crash if it may still be executing.

Reviews are bound to case and evidence hashes. A changed rubric requires the original checkout for review. Restart the server after changing case definitions; SOUL/skill edits are read by each new execution. UI-only edits do not alter the adapter provenance hash. Runtime, grader, or actual adapter changes do.

The server rejects non-local Host headers, cross-origin requests, and mutations without its per-session request token. It invokes fixed Python entry points using argument arrays, never shell input. The browser renders agent responses and fixtures as text, not executable HTML. This protects the workbench from poisoned eval content; it does not certify the evaluated agent's resistance.

## Current limits

- Semantic grading is human review, not an automated judge.
- Native runtime compatibility failures remain visible blockers. In particular, runtimes that drop `preload_skills` cannot establish a valid baseline for those profiles.
- Browser artifact checks require Playwright and Chromium in the worker environment.
- Live provider/tool-trace integration needs a verified run with the chosen Hermes version before behavioral scores can be trusted.
- No in-browser SOUL editing, credential storage, multi-user accounts, or memory/isolation suite in this pilot.

See [the evaluation design](PROFILE_EVAL_DESIGN.md) for the 18-case matrix and detailed grading contract.
