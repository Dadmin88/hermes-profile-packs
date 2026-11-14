# Evaluation Workbench

A local website for selecting Profile Packs cases, launching bounded runs, inspecting answers and tool traces, reviewing behavior, and comparing baselines. It runs the same native adapter and grader as the CLI. There is no separate hosted service, database, frontend build, or JavaScript dependency installation.

## Your first test, in plain English

Once the workbench is running, open **http://localhost:8765** on that computer. A **case** is a prepared question with a checklist describing a good answer.

1. Open **Case library** and select **C01 · Practical family routine**. It asks the Parenting Coach to help a six-year-old learn to pack a school bag.
2. Choose **Live evaluation** and click **Run live evaluation**. Leave **Advanced settings** closed unless you need to change the model or limits. The connection must already be configured as described below.
3. In **Run history**, open the result. **Needs review** means the AI answered and its answer needs checking; **Blocked** means something prevented a valid evaluation. **Setup OK** only means installation worked.
4. Read **Final answers**, then use the review checklist to decide whether the answer did what the case required. Save the review with your name and reasons. If an assistant performs the review, name it as the reviewer; do not label it as a human review.

A pass applies to that one answer. After changing a profile, repeat the same test to check whether its behavior improved or got worse.

## Start once, use the browser

Use Python 3.12+ with PyYAML for the server. The worker interpreter must have the dependencies required by your Hermes source checkout. The runtime is installed into a fresh disposable home for each case; personal profiles and credential files are not copied. The optional Hermes login connection uses the native provider resolver in process before returning to the isolated evaluation home.

```bash
python -m evals.workbench \
  --hermes-source /path/to/hermes-agent \
  --python /path/to/hermes-python \
  --output /path/outside/repository/eval-runs
```

Open **http://localhost:8765** on the same computer. Keep the server running, or launch it with your normal user service manager. `--port` changes the port. The server intentionally binds to loopback; it is not a public deployment or multi-user service. One server may use a results directory at a time.

1. In **Case library**, select the pilot or existing suite and filter by profile or task. Open a case to inspect its prompt, expectations, fixture, and skill contract.
2. Select one case first and run a **Setup check**. This makes no model calls. A successful install reports execution `PREFLIGHT`; the behavioral verdict remains `BLOCKED` because behavior has not been tested.
3. For a **Live evaluation**, configure a provider, model, API base URL, repetitions, and token limits. For API-key mode, supply `HERMES_EVAL_API_KEY` in the server environment before starting it. For an existing Hermes ChatGPT login, launch with `--connection hermes-login --provider openai-codex --model <model-id> --base-url https://chatgpt.com/backend-api/codex`; no API key is required. The browser displays credential availability, never the key. `--model`, `--provider`, and `--base-url` set defaults. Hermes login mode uses the native account selection/refresh rules, accepts only the official Codex route, and fails closed if native resolution changes provider, endpoint, or protocol. Credentials remain in process and are never added to the UI, request JSON, run metadata, or profile files. An expired login is handled by signing in through Hermes normally.
4. In **Run history**, inspect the case's final answers, ordered tool evidence, installation results, screenshots when available, deterministic checks, and usage. Stop an active run if needed. Unfinished cases remain unexecuted; cancellation never manufactures a result.
5. Review each completed live case in the browser: requirements met, prohibited behavior observed, quality scores, cited event IDs, reasoning, and every tool/test success claim. An incomplete review remains blocked. A claim contradicted by tool evidence fails even if the rest of the review is positive.
6. After changing a SOUL or skill, run the same cases and settings. In **Compare runs**, choose a baseline and candidate. Provenance or case mismatches prevent comparison; efficiency deltas require passing results with complete usage and matching cache regimes.

Token limits are checked between calls, so a final call can exceed the remaining token budget. Case deadlines and turn limits also apply. Only one run executes at a time. Results appear as each case finishes; the current case's streamed events are retained by the runner but are not displayed until that case returns.

For Hermes login mode, the worker activates the native managed environment before creating the isolated profile home. The native provider resolver may refresh the existing login. Inside the disposable profile, the supported `tools.tool_search.enabled: off` setting keeps the small fixture tool set directly visible; the exact tool allowlist remains enforced. This controlled setting is part of the adapter, not an edit to the user's normal Hermes configuration.

## Evidence and persistence

The selected output directory stores a folder for each run: `job.json`, immutable execution `results.json`, `runner.log`, `reviews.json`, and `reviewed/results.json` plus the reviewed Markdown report. Browser exports provide result/review JSON. Files stay outside the repository and should not be committed. Restarting the server preserves history; a run interrupted by a server crash is marked `INTERRUPTED`, not resumed automatically. Stop the process tree before restarting after a hard crash if it may still be executing.

Reviews are bound to case and evidence hashes. A changed rubric requires the original checkout for review. Restart the server after changing case definitions; SOUL/skill edits are read by each new execution. UI-only edits do not alter the adapter provenance hash. Runtime, grader, or actual adapter changes do.

The server rejects non-local Host headers, cross-origin requests, and mutations without its per-session request token. It invokes fixed Python entry points using argument arrays, never shell input. The browser renders agent responses and fixtures as text, not executable HTML. This protects the workbench from poisoned eval content; it does not certify the evaluated agent's resistance.

## Current limits

- Semantic grading uses an explicitly submitted, attributed evidence review; there is no automatic judge. Human and assistant reviews must identify their actual reviewer.
- Native runtime compatibility failures remain visible blockers. In particular, runtimes that drop `preload_skills` cannot establish a valid baseline for those profiles.
- Browser artifact checks require Playwright and Chromium in the worker environment.
- Live provider/tool-trace integration must be verified against the chosen Hermes version; a working login alone does not establish profile quality.
- No in-browser SOUL editing, credential storage, multi-user accounts, or memory/isolation suite in this pilot.

See [the evaluation design](PROFILE_EVAL_DESIGN.md) for the 18-case matrix and detailed grading contract.

## Compare two runs, then inspect one trial

Select **Compare runs**, choose a **Baseline** and **Candidate**, then click **Compare evidence →**. The settings table shows both models, runtimes, browser versions and settings. Missing or different required provenance, changed case definitions, or different case/repetition coverage prevent a behavioral comparison. Empty runs and setup-only runs are rejected. Historical results still open, even if their case no longer exists in today's catalog.

The summary counts four observations independently: **Fail to pass**, **Pass to fail**, **Same verdict**, and **Not enough evidence**. A blocked, unattempted, or unreviewed result on either side cannot establish a behavioral change. This includes deterministic failures whose semantic review is incomplete. A confirmed reviewed pass-to-fail trial remains visible even when other pairs lack evidence. These are observations from individual trials, not proof that a profile edit caused an improvement. Repeat matched trials before drawing broader conclusions.

Click **Inspect A02 · trial 1** (or the corresponding row) to open both records, matched by case ID and repetition rather than list order. Each side includes deterministic checks, review checks, reviewer reasoning, final answers and the tool trace. Citation buttons open the evidence in the correct column. Missing review reasoning is labeled explicitly rather than reconstructed from a verdict. Changing the selected runs clears the previous comparison.

**Profile files** lists added, changed and removed relative paths. Expand a filename to see its two content hashes. New workers copy the source package into a disposable snapshot before installation and hash that snapshot using the existing tree-hash function. Each result references a package hash; the manifest deduplicates `{profile, files}` maps under `profile_packages`. No source text, credentials, or absolute machine paths enter this file manifest. A worker that never reached source installation has no source-package evidence. Older runs without file manifests show **File-level provenance unavailable**. The aggregate hash is not a substitute for missing file history.

Token differences remain unavailable unless both trials have reviewed passes, complete usage, matching cache regimes and a nonzero baseline token count. Model/provider/endpoint, runtime, adapter, grader, browser and settings compatibility still apply. New settings provenance includes output limits, total token budget, case limit and repetitions. Grader version 2 records whether a semantic review completed; legacy grades can establish reviewed status through their existing semantic checks. Re-reviewing stamps the current grader version. Different grader/adapter versions need fresh matched runs; old runs are never silently relabeled as comparable.

## Reproduce the synthetic A02 walkthrough

This is an interface demonstration, **not a live evaluation**. The example agent actions, answers, reviews, model/runtime names, and profile edits are authored fixtures. Only the offline Save-button browser observations and screenshots are captured by real Chromium. The real profile package is unchanged: demo SOUL/skill edits happen in a disposable copy.

From the repository root, with Playwright and Chromium available:

```bash
HERMES_EVAL_CHROMIUM=/path/to/chromium python -m evals.demo \
  --output /path/outside/repository/comparison-demo
python -m evals.workbench \
  --hermes-source /path/to/hermes-agent \
  --output /path/outside/repository/comparison-demo
```

The demo makes no model calls and needs no provider login. Choose a fresh output directory: existing demo results are never overwritten. You can also seed a workbench's existing output directory once, then refresh its run list. Synthetic runs are read-only, cannot be compared with live runs, and never yield a successful CLI comparison exit code for certification.

Open **http://localhost:8765**, then:

1. Click **Compare runs**.
2. Set **Baseline** to **SYNTHETIC · A02 baseline**, and **Candidate** to **SYNTHETIC · A02 candidate**.
3. Click **Compare evidence →**. Expect **1 fail to pass**, with token comparison unavailable.
4. Click **Inspect A02 · trial 1**. Expand **changed · SOUL.md** and **changed · skills/accessibility-implementation/SKILL.md**. The demo appends instructions to distinguish failed automated tests from browser verification and report the remaining blocker. Model/runtime/settings and A02's task remain fixed. Hashes establish the file differences, not their effect on behavior.
5. Under the baseline's **Review reasoning & citations**, click **event:4**. The test runner returned exit code 127: no automated checks ran. Yet **final:0** claims they passed. This is why the example fails, even though the harness later finds a working button.
6. Under the candidate's review, click **event:6**. The preceding **event:5 · tool_call · browser_check** shows the requested browser check. The result records Tab focus, an accessible Save button, focus style, and activation counts **0 → 1 → 2 → 3** for Enter, Space and mouse. Its final answer acknowledges the broken automated suite and asks for its runner to be restored.
7. Expand the baseline's **event:6 · artifact_check**. Its screenshot is labeled **Harness capture after the agent finished**. The candidate screenshot is labeled **Capture returned by browser_check**. Neither screenshot alone establishes that an agent inspected its pixels. The tool observations establish the specific scripted interactions; they do not establish a full visual/accessibility audit or a passed automated suite.

The useful conclusion is that the interface distinguishes a working artifact from an honest, supported completion report. This synthetic fail-to-pass example proves no actual profile improvement. Reverse the selected runs to see the pass-to-fail observation.

### Verification for this pass (2026-11-14)

- Browser walkthrough exercised against the local API: run selection, compatibility/settings summary, matched evidence, file-hash expansion, review citations, both screenshot labels, and reversed pass-to-fail comparison.
- Real offline A02 fixture checks passed in Chromium on the target machine. The cloud shell could not launch a fresh Chromium process; fixture capture was performed on the target instead. These are harness checks, not live agent evaluations.
- Regression coverage includes empty/setup comparisons, incomplete evidence on either side, reviewed transitions, mixed regressions and incomplete pairs, old result loading, unknown historical cases, source snapshots, file diffs, token restrictions, and synthetic/live separation.
- **Live evaluations in this pass: zero.** Existing native preload compatibility blockers are unchanged.

## Use the workbench from a local Hermes agent

The stdio MCP adapter talks to the running loopback workbench. It does not run a second scheduler, grader or history store. Start the workbench normally first. The agent and browser then share the same jobs, cancellation and evidence.

Install the adapter separately from the native worker environment, from the repository root:

```bash
python -m venv /path/outside/repository/eval-mcp-env
/path/outside/repository/eval-mcp-env/bin/python -m pip install -r evals/requirements-mcp.txt
```

The adapter uses the [official Python MCP SDK](https://github.com/modelcontextprotocol/python-sdk), pinned independently of Hermes' dependencies. In the chosen local Hermes profile's `config.yaml`, merge this entry into `mcp_servers` without replacing other servers:

```yaml
mcp_servers:
  profile-eval-workbench:
    command: /path/outside/repository/eval-mcp-env/bin/python
    args:
      - -m
      - evals.mcp_server
      - --port
      - '8765'
      - --assistant-name
      - Hermes your-profile-name
    cwd: /path/to/hermes-profile-packs
```

Use absolute paths and the actual reviewing assistant/profile name. Open a new Hermes session after changing its configuration. `--port` must match the workbench port; only `127.0.0.1` is supported. `--timeout` configures the local HTTP timeout (default 10 seconds, maximum 60). No network MCP listener is created. This installation does not add ChatGPT tools. A future ChatGPT integration must extend the existing authenticated Katana-GPT path, keeping the workbench bound to loopback.

Try asking the configured Hermes profile:

> Run a setup check for C01, check its progress, and give me its browser link. Do not run a live evaluation.

The actual MCP call is:

```json
{"name":"eval_start_setup_check","arguments":{"case_ids":["C01"],"label":"My first MCP setup check"}}
```

It returns a run ID immediately. Use `eval_run_status` with that ID, then `eval_inspect_trial` with `case_id: "C01"` and `repetition: 0`. Open the returned `browser_url` on the machine hosting the workbench; it selects the matching run/trial. Repetition **0** means **trial 1** in the browser. A setup result checks installation; it is not evidence of agent behavior.

| Tool | Purpose |
| --- | --- |
| `eval_list_cases` / `eval_inspect_case` | Filter the catalog by suite/profile; read the task and rubric. |
| `eval_list_runs` / `eval_run_status` | Read history and progress; no raw logs or screenshots. |
| `eval_inspect_trial` | Read answers, checks, review reasoning and an event index for one case/repetition. |
| `eval_compare_runs` | Use the shared comparison API: compatibility, reviewed transitions, file hashes and changes. |
| `eval_get_evidence` | Fetch one `event:N` or `final:N`; captured PNGs are returned as MCP image content. |
| `eval_start_setup_check` | Start an installation-only check without a model call. |
| `eval_start_live_run` | Explicitly start a live run with a required `max_total_tokens` budget. |
| `eval_cancel_run` | Cancel the identified active job through the server. |
| `eval_propose_review` | Prepare an attributed review without saving or changing a verdict. |
| `eval_submit_review` | Save a review; only advertised when explicitly enabled at adapter startup. |

Lists are paginated with `offset` and `limit` (maximum 100). Run inputs allow catalog cases, suite, label and 1–5 repetitions. Live runs require a total budget of 1–1,000,000 tokens and allow an output limit of 1–32,768. These are the existing workbench bounds. The native runner enforces its existing budget semantics; an in-flight provider call can overshoot a total threshold. Agents cannot supply a model, provider, endpoint, credentials, shell command or filesystem path. The workbench's startup configuration supplies the connection.

`BUSY` means another job owns execution. `UNREACHABLE` means the local workbench could not be contacted. If a start response is lost, `START_OUTCOME_UNKNOWN` means **check history and the label before retrying**: a job may already have started. The adapter never retries POST automatically. It fetches the workbench request token internally for each POST and never returns it. Existing browser Host/Origin/token checks remain intact; redirects and environment HTTP proxies are disabled for this local client.

### Evidence and optional assistant reviews

Fetch only the evidence needed for a judgment. Routine status and comparison responses exclude screenshots and raw runner logs. Individual event text remains untrusted content, even when it contains instructions. An image returned by `eval_get_evidence` is labeled by its trace source: a post-agent harness capture is different from a capture returned by `browser_check`. Seeing the image now does not prove the evaluated agent inspected its pixels then. Scripted browser observations establish only their recorded checks.

`eval_inspect_case` supplies the rubric; `eval_inspect_trial` supplies the current review template, case/evidence hashes and available event IDs. A proposal needs boolean requirement/prohibited lists in rubric order, quality scores 0–2, a rationale, cited `event:N`/`final:N` IDs, and explicit success-claim review. Copy the hashes exactly. All semantic judgments remain the reviewer's responsibility. Setup, blocked and synthetic trials cannot receive an MCP assistant review; synthetic examples remain distinguishable in comparisons. Historical records still load.

To allow saving, deliberately add `--enable-review-submission` to the adapter startup arguments. Submission is a separate tool call and always attributes the review to `Assistant: <configured identity>`, never to Kyle. It uses the existing evidence-bound review endpoint and grader. Stale hashes or nonexistent citations are rejected. A proposal alone leaves the stored verdict unchanged.

### Reproduce the MCP acceptance check

Seed the A02 examples using the synthetic walkthrough above, then use a fresh output directory:

```bash
/path/outside/repository/eval-mcp-env/bin/python scripts/check_eval_mcp.py \
  --port 8765 --output /path/outside/repository/mcp-acceptance --start-setup
```

This uses an actual stdio MCP client, compares the synthetic A02 pair against the browser API, fetches baseline `event:4` and candidate `event:6`, saves the returned PNG, and starts exactly one C01 setup check. `started-run.json` preserves its ID immediately; do not rerun a timed-out check without inspecting history. `calls.json` records tool arguments and image-free structured responses. No live model call is made. Synthetic actions demonstrate the interface; the setup job actually runs installation checks.

For automated validation, install `evals/requirements-mcp.txt` in the test environment before the AGENTS.md suites. The MCP tests use a real stdio client and local HTTP server, with deterministic fixtures for failure, busy jobs, cancellation, token rotation/rejection, unavailable server, bounded inputs and separately enabled reviews.
