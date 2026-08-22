---
name: failure-debugging
description: Diagnose backend failures systematically from reproducible symptom through evidence, hypothesis, root cause, minimal fix, regression proof, and production-relevant verification.
---
# Failure Debugging

Use for incorrect responses, crashes, failed jobs, data inconsistencies, timeouts, dependency errors, flaky backend behavior, or regressions with an unknown cause.

## Procedure
1. Capture the symptom precisely: expected behavior, actual behavior, exact error, inputs, environment, version or commit, timing, and reproduction steps. Determine whether the failure is deterministic, intermittent, load-dependent, data-dependent, or environment-specific.
2. Establish blast radius and urgency. Identify which callers, tenants, data, jobs, or environments are affected and whether continuing execution can cause further harm.
3. Reproduce the smallest faithful failure you can. Preserve a real failing example before changing code.
4. Trace the execution path end to end: request or job entry, authorization, domain logic, persistence, external dependencies, asynchronous boundaries, and response. Correlate logs, traces, metrics, database state, and recent changes instead of relying on one signal.
5. Form an explicit hypothesis that predicts observable evidence. Gather or add the minimum instrumentation needed to confirm or falsify it. Prefer narrowing the fault over changing several plausible causes at once.
6. Distinguish root cause from downstream symptoms. Check boundaries where bad state could first have been introduced, including invalid assumptions about data, concurrency, retries, time, ordering, configuration, and dependency behavior.
7. Implement the smallest cohesive fix that restores the intended invariant or contract. Avoid unrelated cleanup while the failure is under investigation unless it is required to make the fix safe.
8. Add a regression test or reproducible automated check that fails for the original defect and passes with the fix whenever feasible.
9. Re-run the original reproduction, targeted tests, and the broader relevant suite. Verify important side effects such as persisted state, retries, emitted events, or dependent calls, not only the final response.
10. If evidence points primarily to database internals, infrastructure, networking, security policy, or an external integration, hand off the evidence to the owning specialist instead of guessing outside the Backend Engineer's lane.

## Decision rules
- Do not shotgun speculative fixes. Change a hypothesis only after evidence changes.
- Error messages are evidence, not always the root cause.
- Recent code changes are useful suspects, not proof of causality.
- A disappearing symptom is not enough; explain why the fix addresses the cause and how regression is prevented.

## Quality gate
The investigation is complete when the failure is explained by evidence, the fix addresses the root cause, the original reproduction and relevant tests pass, material side effects are verified, and any remaining uncertainty is explicit.