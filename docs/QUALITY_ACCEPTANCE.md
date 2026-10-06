# Quality acceptance record

Execution checkpoint: 2026-10-06. Content implementation and independent reviews complete; live acceptance and upstream integration BLOCKED.

## Revisions and scope

- Source baseline: `3821183d2b7d5af3cd18bc1c7c4da58ad9bb784e`; branch `feat/profile-quality-20261006`.
- Catalog baseline: `b10eeae1a8f0413760b05d928234e0c08eec3f32`; four Council entries only, with existing scoped MIT grant. See `CATALOG_MAPPING.md`.
- Candidate versions: root pack 0.4.1; Council and Academy distributions 0.2.1; profiles 0.1.1; catalog entries 1.0.1 and workflow skills 0.1.1.
- All 51 personalities and 204 owned skills reviewed. Council dispositions and Academy domain coverage are recorded under `quality/`. Academy adds 29 domain teaching kits and Dean examples.
- Canonical installed Hermes: v0.21.5+5397.g105e876; commit `105e8765863f23f837b19433c648de1208415f2f`; Python 3.14.7. Existing model/provider: `gpt-5.6-luna` / `openai-codex`.

## Verified evidence

| Check | Result | Scope and limitation |
|---|---|---|
| Source validate.py, README counts, diff whitespace | PASS | Existing identities, roster, jobs and canonical shared content preserved |
| Source unittest suites | 256 run: 255 passed, 1 skipped | Root 20, Council 3, Academy 201, Agency 32; native-runtime skip is not PASS |
| Independent specification and quality reviews | PASS | Included domain examples, answer keys and corrected learner-facing fixtures |
| Source native distribution installs | 51 PASS | Canonical Python 3.14.7; SOUL and 308 owned skill payload files match source; 29 teaching references preserved; isolated roots removed |
| Native memory and workspace lifecycle | PASS | Direct native API add/reload/replace/remove and file write/read/correct/delete; does not prove model approval or continuity cases |
| Catalog focused runner | 41 passed | scripts/run_tests.sh: bot_catalog and bot_starter_workflows; isolated task environment |
| Catalog extraction | PASS, 16 entries | Includes unchanged community entries; only four Council bots edited |
| Catalog native profile installs | 4 PASS | Actual fork installer, isolated Python 3.11 environment; SOUL plus five bundle files each match; no copied credentials, routines paused, no cron jobs |
| Native Continuing Education preflight | BLOCKED, exit 2 | Installed target lacks required native test/bridge files; two preflight regression tests PASS |

Catalog installation on the installed canonical 3.14 environment is separately BLOCKED by missing PyYAML for the unmerged fork. The four successful fork installations do not establish deployment or Bot Chat UI acceptance.

## Behavioral cases and result rules

175 synthetic cases are prepared: Council 82, continuity 7, Academy STEM 46, Academy humanities 40. Their live status remains NOT RUN. Fixtures contain user messages, expected/prohibited behavior and relevant skills; evaluator answer keys are withheld from learner prompts. Continuity save/correct/restart must execute in order.

Every behavioral result must record profile, case ID, source/catalog, exact content revision, runtime/model, observed response/tool actions and verdict. Static review and direct storage API proofs do not count as model behavior. Synthetic starters and source/catalog C02/C04/C07 parity still require actual responses. Canonical Bot Chat delivery also remains unverified.

## Remaining gates and exact resume order

1. Restore availability of the existing model/provider. The canonical credential resolver reported an existing 429/quota cooldown before inference; the last probe reported a 13:38 UTC reset on 2026-10-06. No model response, tool calls or token usage were produced. No provider, model or authentication was changed.
2. Run bounded incoming Council C01–C08 and catalog starter probes, then source/catalog parity. Run the remaining Council domain/boundary cases, continuity lifecycle and Academy teaching/routing cases. Fix failures and rerun only affected cases.
3. Verify native CE on a Hermes revision implementing goal interruption, bot goal mode, distribution preloads and resumed-session persistence. Current missing files: tests/cli/test_cli_goal_interrupt.py, tests/tools/test_bot_mode_goal.py, tests/agent/test_profile_distribution_preloads.py, tests/cli/test_oneshot_resumed_session_persist.py. Do not weaken the preflight to simulate support.
4. Rebase Council adaptations when the catalog foundation or community batch advances, rerun focused tests/extraction and obtain actual deployed Bot Chat acceptance.
5. Establish the Academy catalog roster, integration revision and explicit licensing scope before creating its catalog entries. The Council MIT grant does not cover Academy.
6. Maintainers review and merge only after applicable gates pass. This checkpoint is not a full-plan completion or release certification.
