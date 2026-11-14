# Operational pilot: a real profile-change comparison

Verified on Katana, November 14, 2026. This is a small **live** workflow demonstration, with three executions per version of C01. It is separate from the synthetic A02 examples and from setup checks. All six official behavioral verdicts remain **Needs review** for Kyle; no review was submitted and no candidate was promoted.

## Readiness

| Case | Installs with required readback | Can execute live | Evidence ready for behavioral review |
| --- | --- | --- | --- |
| C01 · Practical family routine | Yes | Yes; six completed executions | Yes; final answers, verified skill delivery, deterministic checks and complete reported usage |
| A02 · Accessibility fix with broken test runner | Blocked: declared startup skill is lost by native installer | Not ready; no live A02 call attempted in this pilot | No; only installation failure evidence |

The fresh MCP setup job was `280b1f03935b47e783b1ad97393b4216`. C01 returned `PREFLIGHT`; A02 returned `BLOCKED`, reproducing earlier setup job `5fe6c4f2767e45a8b9b769279a3ae798`. A successful setup check verifies installation, not behavior.

### A02: the exact dependency

1. `hermes-agency/profiles/agency-frontend-engineer/distribution.yaml` declares `preload_skills: [academy-continuing-education]`.
2. Native `hermes_cli/profile_distribution.py:plan_install` reads that manifest into `DistributionManifest`. At tested runtime commit `b51a30c461ee663313ce89d01947bb10b55a619c`, its `from_dict` and `to_dict` have no `preload_skills` field.
3. `_copy_dist_payload` calls `write_manifest(target, manifest)` after copying. Serializing that parsed manifest drops the declaration.
4. `evals/native_worker.py` reads back the installed manifest and compares its startup-skill list with the frozen source. The mismatch stops execution before the model call. The later check that requires actual preload content in the native system prompt also remains intact.

The upstream default-branch [manifest implementation](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/profile_distribution.py), inspected on November 14, still lacks the field (file blob `3569d5c9ff03e1ca4d6c386885b41085d18e0941`). [Upstream PR #93520](https://github.com/NousResearch/hermes-agent/pull/93520) implements manifest round-tripping and automatic prompt loading, but was **open and unmerged**, with head `8e6e86d69bec24cfbe83dd6a5c2a1f8e9fb2fdc9` and a merge conflict reported by GitHub. A CLI `-s` preload or session metadata change is not a replacement for preserving the distribution contract.

No runtime patch, manifest removal or manual prompt injection was applied. Before enabling A02, verify a supported upstream implementation in an isolated runtime: installation round-trip, actual startup prompt inclusion, disabled/missing-skill behavior and non-executing automatic preloads. Then rerun setup and a fresh live baseline. C01's success does not establish A02 readiness.

## What changed, and what stayed fixed

The first C01 baseline already gave a practical skill-building answer. Its five numbered steps mixed parent preparation with child actions. The experiment asked whether a narrower instruction could make a simple routine easier to scan without dropping adult support or review after real use.

Only `hermes-council/profiles/council-parenting-coach/skills/family-routines/SKILL.md` changed. The disposable candidate appended:

```markdown
## Small routine requests

When the user asks for a simple routine, give one predictable cue and at most three child-facing steps. Keep adult support and a review after real use explicit in brief notes outside those steps. Offer a fuller plan only when the user's situation calls for it; avoid turning a small routine into a long checklist for the parent.
```

The source skill's SHA-256 changed from `80d761e5cd8f517403212954262b1f42a53324009c895e67193358e4c27eff9f` to `db8745f24d2eda48cd995874bb89e442ee1d0ce793a7f9d3686597c7d97b6246`. The comparison API identified exactly this file, with eight package files unchanged, for every matched pair. The original was restored after the candidate trials; the candidate bytes and patch remain outside the repository with the experiment evidence. No installed everyday profile was edited.

Matched conditions:

- Model `gpt-6.1-sol`, provider `openai-codex`, existing Hermes login connection and configured endpoint.
- Runtime `b51a30c461ee663313ce89d01947bb10b55a619c`, grader `2`, adapter hash `2729d694fdf712c48bd4d730325fac90b0e00c3af6e7258d8a982e694d51f849`.
- C01 case hash `4a1afb1dc03f4fa40d90f3e2b584e876b5e46dad6d1d37c948215c16ee14e68c`, same task, native tool allowlist and case deadlines.
- Each run: 60,000 reported-token budget; 2,048 output tokens per call. The initial pair used one repetition per run; the confirmation pair used two per run. Compare within these two pairs, since their repetition/coverage settings differ.
- No workbench or runner code changed between executions. Normal model variation remains; this was not a seeded experiment.

The order was initial baseline, initial candidate, two candidate confirmations, then two baseline confirmations. This small, grouped sample is not a randomized quality study. Cache usage was observed, not forced to match.

## Open the real evidence

These links work on the machine running the loopback workbench. All six records are native live executions, not synthetic results.

| Run | ID | Browser |
| --- | --- | --- |
| First baseline | `0f87aec16b074864afd45ef23537daf3` | [C01 trial 1](http://localhost:8765/#run=0f87aec16b074864afd45ef23537daf3&case=C01&repetition=0) |
| First candidate | `57effa6e9888451cbc66b997acea855e` | [C01 trial 1](http://localhost:8765/#run=57effa6e9888451cbc66b997acea855e&case=C01&repetition=0) |
| Baseline confirmations | `c98bdcc9520246c5ac979021d1ff62c8` | [Trial 1](http://localhost:8765/#run=c98bdcc9520246c5ac979021d1ff62c8&case=C01&repetition=0) · [Trial 2](http://localhost:8765/#run=c98bdcc9520246c5ac979021d1ff62c8&case=C01&repetition=1) |
| Candidate confirmations | `762c9da9d72e40edb3ee2cb22247ae85` | [Trial 1](http://localhost:8765/#run=762c9da9d72e40edb3ee2cb22247ae85&case=C01&repetition=0) · [Trial 2](http://localhost:8765/#run=762c9da9d72e40edb3ee2cb22247ae85&case=C01&repetition=1) |

Open the workbench with `xdg-open http://localhost:8765`. Click **Compare runs**, select **LIVE · C01 baseline · trial 1** and **LIVE · C01 candidate · trial 1**, click **Compare evidence →**, then **Inspect C01 · trial 1**. Expand the changed skill file. Read both final answers and the following events:

- First baseline: `event:5` contains the successful native `skill_view` response with the original family-routines content. `event:7` verifies its source/hash, and `event:8` verifies age-appropriate-expectations.
- First candidate: `event:7` contains the successful native `skill_view` response including the added instruction. `event:8` verifies the candidate skill hash; `event:6` verifies age-appropriate-expectations.
- Each record's `final:0` is the actual answer. Source/prompt events establish profile installation and loading; they do not establish that the advice worked for a family.

Both agents described an age-appropriate routine with a predictable cue, visual reminder, adult support and a later review. The baseline used five numbered steps; the first candidate separated three child actions from notes for the adult. Neither created a file, sent a message, ran a browser check or claimed that a real family tried the routine. C01 has no screenshot evidence to inspect.

For the confirmation comparison, select the two **2 confirmation trials** runs instead. Required skill evidence is available in each record:

| Version / repetition | family-routines verified event | age-appropriate-expectations verified event | Answer |
| --- | --- | --- | --- |
| Baseline confirmation 0 | `event:6` | `event:9` | `final:0` |
| Baseline confirmation 1 | `event:6` | `event:8` | `final:0` |
| Candidate confirmation 0 | `event:8` | `event:7` | `final:0` |
| Candidate confirmation 1 | `event:7` | `event:8` | `final:0` |

Every execution completed, delivered the required skill before the final answer, and recorded provider usage. Baseline numbered-step counts were 5, 4, 4; candidate child-step counts were 3, 3, 3. Those are observations from these answers, not proof of a reliable quality improvement or a better outcome for children. The baseline was already useful; the candidate still needs review for unnecessary assumptions and loss of useful detail.

### Token observations, not an efficiency verdict

| Trial | Baseline input / output | Candidate input / output | Baseline / candidate model calls | Cached input matched? |
| --- | --- | --- | --- | --- |
| Initial | 8,597 / 328 | 8,669 / 270 | 2 / 2 | Yes: 3,840 each |
| Confirmation 0 | 12,846 / 287 | 8,651 / 259 | 3 / 2 | No: 0 / 3,840 |
| Confirmation 1 | 8,579 / 331 | 8,651 / 261 | 2 / 2 | No: 0 / 3,840 |

Reported total across the six executions: 57,729 input-plus-output tokens in 13 model calls. The first candidate's shorter output did not reduce its total tokens. These are provider-reported usage observations, not prices or a billing guarantee. The workbench correctly withholds token ratios: no reviewed passes exist, and confirmation cache regimes differ.

Both comparisons return `INCOMPLETE`, with matching provenance and the intended file change. Here that means **human review is outstanding**, not that execution failed. No PASS/FAIL transition, regression certification or efficiency win has been declared. Kyle can review each record in Run history; after evidence-bound reviews are saved, Compare Runs will use those official verdicts.

## Repeat the workflow through Hermes

In a new session with the configured `katana` profile:

> Use the eval workbench MCP to evaluate the three-child-step change to Parenting Coach's family-routines skill from the operational pilot guide. Work only in the isolated eval checkout. Run a baseline first, then change that one file; keep model, runtime, case and budgets matched. Start with one C01 pair and add two trials per version if it works, with at most 60,000 tokens per run. Inspect the evidence, give me both comparisons and browser links, restore the original file, and leave the verdict and promotion to me.

Operator sequence:

1. Use `eval_inspect_case`, `eval_list_runs` and a setup check to verify the rubric, current job state and readiness. Check the configured runtime revision and keep the evaluation checkout separate from installed everyday profiles.
2. Start the baseline with `eval_start_live_run`, explicitly specifying the budget. Save its ID immediately and poll `eval_run_status`. If the start response is lost, inspect history before retrying.
3. Use `eval_inspect_trial` and `eval_get_evidence` to inspect answers, skill delivery and failures. Do not infer a behavioral failure from a pending review.
4. Prepare the candidate using ordinary local file tools in the isolated evaluation checkout, while idle. Preserve original bytes and verify only the intended profile file changed. MCP deliberately accepts no arbitrary filesystem or endpoint override. Each worker freezes and hashes the source it actually installs.
5. Run the candidate through MCP with matched settings, then call `eval_compare_runs`. Inspect file changes and compatibility before drawing conclusions. Use `repeat: 2` for both confirmation runs, or matched individual runs; never mix coverage in a comparison.
6. Restore the original bytes with a guard against unexpected concurrent edits. Keep the candidate patch and runtime evidence outside the repository. Return observations and cited event IDs without calling `eval_submit_review` when Kyle reserves the verdict.

This pilot exposed no workbench-code gap preventing that workflow. The existing MCP, native runner, comparison API and review contract were sufficient. The changes shipped in this slice are the operational guide and updated readiness documentation, not a new execution layer.

## Validation and remaining limits

The AGENTS.md validator and all four test suites passed: 337 passed, 2 environment-gated skips. Katana's installed flow was exercised with actual stdio MCP clients for setup, live starts, status, trial inspection, individual evidence retrieval and comparison. No synthetic run was used as live acceptance. The six real answers remain stored in the same browser history, with review submission disabled.

Remaining work: Kyle's semantic review; supported upstream preload handling before A02; broader neighboring/negative cases before promoting the skill change; and more independent matched trials before claiming a reliable effect. This slice does not test real family outcomes, unrestricted agent tools, memory isolation, visual inspection or a whole-profile regression suite.
