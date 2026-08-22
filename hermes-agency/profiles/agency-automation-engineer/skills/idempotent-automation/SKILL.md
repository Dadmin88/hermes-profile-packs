---
name: idempotent-automation
description: Make automation safe under duplicate triggers, retries, restarts, overlapping runs, and uncertain outcomes by defining stable operation identity, state checks, atomic effects, and reconciliation.
---
# Idempotent Automation

Use when an automation may execute the same logical intent more than once or resume after an interrupted/uncertain attempt.

## Procedure
1. Define what counts as one business/operational intent and choose a stable idempotency identity that survives transport retries, process restarts, and node relocation.
2. Inventory every side effect and classify whether repeating it is naturally safe, replace/upsert safe, conditionally safe, or consequentially duplicate.
3. Check authoritative current state before creating a new effect when a prior attempt may already have succeeded.
4. Use atomic uniqueness, compare-and-set, transaction, provider idempotency, durable operation records, or another supported mechanism to prevent concurrent duplicate ownership where needed.
5. Store result/reference state for successful operations so later duplicate attempts can return/reconcile the existing outcome instead of repeating it.
6. Handle the uncertain window where the side effect may have occurred but the automation did not record success. Define a query/reconciliation path rather than assuming failure.
7. Treat partially completed multi-step automations separately: each step needs its own safe repeat behavior and the workflow needs explicit progress state.
8. Bound concurrent runs for the same resource when idempotency alone cannot protect ordering or invariant conflicts.
9. Preserve audit evidence that distinguishes first execution, duplicate suppression, retry, reconciliation, and manual replay.
10. Test duplicate trigger, simultaneous duplicate runs, crash before/after side effect, lost acknowledgement, process restart, and replay on another eligible node.

## Decision rules
- A unique job/message ID is not enough when the same business intent can be enqueued again with a new ID.
- “Check then act” can race unless the check/action boundary is made atomic where concurrency matters.
- Suppressing duplicates is only half the problem; uncertain outcomes still require reconciliation.
- Portable automation should store durable idempotency state outside transient node-local process memory when Fleet may relocate execution.

## Quality gate
The automation is idempotent when repeated or concurrent execution of the same intent converges on one accepted outcome, uncertain attempts can be reconciled, state survives restart/relocation where required, duplicate suppression is observable, and fault tests demonstrate consequential side effects cannot silently multiply.