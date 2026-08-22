---
name: flaky-test-diagnosis
description: Diagnose and eliminate flaky automated tests by classifying nondeterminism across timing, shared state, environment, ordering, network, resources, and assertions.
---
# Flaky Test Diagnosis

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using CI history, retry patterns, traces, screenshots, logs, resource pressure, timing, and seed/order data. Do not fill material gaps with assumptions when they can change the result.
3. Reproduce statistically, preserve repeated-run artifacts, locate the first nondeterministic divergence, fix the underlying synchronization/state flaw, and prove stability.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
The test is stable under repeated and parallel execution without masking failure through blind retries.
