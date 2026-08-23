# Academy CE Phase 12 — Deterministic Integration and Regression Suite

## Purpose

This suite validates the Academy Continuing Education (CE) flow end-to-end
using deterministic fixtures and real imports rather than mock-only tests.
It covers every regression case from the master plan.

## Test architecture

### Fixture strategy

- **Real imports**: `routing.py`, `academy.json`, and skill files are imported
  directly from the Academy source tree.
- **Temp HERMES_HOME**: Each test class creates a temporary `~/.hermes`
  directory with Academy profiles installed (real file copies), then cleans
  up in `tearDown`.
- **Deterministic CE simulator** (`CEFixture`): Records every primitive
  invocation (`goal_start`, `message_agent`, `learn`, `subgoal_create`,
  `goal_complete`, `budget_tick`) so tests assert on exact event sequences
  without depending on LLM behaviour.

### No mock-only tests

Every test either:
1. Uses real `routing.py` functions against the real manifest, or
2. Exercises the `CEFixture` simulator with real skill file I/O in a temp
   HERMES_HOME, or
3. Reads real skill content to verify contract requirements.

## Regression cases covered

| # | Case | Test class |
|---|------|------------|
| 1 | Named instructor | `NamedInstructorTest` |
| 2 | Dean route | `DeanRouteTest` |
| 3 | Existing skill extend / no duplicate | `ExistingSkillExtendTest` |
| 4 | No related skill → create | `NoRelatedSkillCreateTest` |
| 5 | Write approval | `WriteApprovalTest` |
| 6 | More practice / no early completion | `MorePracticeNoEarlyCompletionTest` |
| 7 | Instructor deficiency → subgoal | `InstructorDeficiencySubgoalTest` |
| 8 | Transfer pass | `TransferPassTest` |
| 9 | Budget exhaustion | `BudgetExhaustionTest` |
| 10 | Teacher unavailable / missing | `TeacherUnavailableTest` |
| 11 | Cancel | `CancelTest` |
| 12 | Objective change | `ObjectiveChangeTest` |
| 13 | Hermes restart | `HermesRestartTest` |
| 14 | Bot Chat resume | `BotChatResumeTest` |
| 15 | Fresh session uses learned skill | `FreshSessionUsesLearnedSkillTest` |
| 16 | Teacher unchanged | `TeacherUnchangedTest` |
| 17 | Profile Packs unchanged | `ProfilePacksUnchangedTest` |
| 18 | Fleet unavailable (no-Fleet env) | `NoFleetEnvironmentTest` |

### Additional coverage

- **End-to-end integration** (`CEFlowIntegrationTest`): Full flows with Dean
  routing, named instructor, and subgoal scenarios.
- **Determinism guarantees** (`DeterminismTest`): Routing, context
  minimization, and fixture step ordering are deterministic.
- **No parallel runtime** (`NoParallelRuntimeTest`): Both CE and teach skills
  forbid custom schedulers, databases, registries, and message buses.
- **User visibility** (`UserVisibilityTest`): Status is concise, not chatty.
- **Efficiency evidence** (`EfficiencyEvidenceTest`): CE tracks efficiency
  metrics and optimizes for capability gain per inference unit.

## No-Fleet test environment

`NoFleetEnvironmentTest` explicitly verifies:
- No Fleet plugin directory in the temp HERMES_HOME.
- No Fleet, Keryx, Nodescale, Templar, or RunAuthority artifacts anywhere.
- A complete CE flow (goal → message_agent → learn → complete) succeeds
  without any distributed dependency.
- Both CE and teach skills explicitly forbid all Fleet-related systems.
- No parallel runtime is introduced.

## Running

```bash
# From repo root
python3 -m unittest discover -s hermes-academy/tests -p 'test_*.py' -v

# Just the regression suite
python3 -m unittest hermes-academy.tests.test_ce_regression_suite -v
```

## Dependencies

- Python 3.10+ (uses `X | Y` union syntax in type hints)
- No external packages beyond stdlib
- Academy source tree must be intact (routing.py, academy.json, profiles/, shared-skills/)
