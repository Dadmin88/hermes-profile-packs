---
name: background-jobs
description: Design and implement reliable background work with explicit delivery semantics, idempotency, retry policy, concurrency control, observability, and recovery behavior.
---
# Background Jobs

Use when work should execute outside the request path because it is slow, scheduled, retryable, resource-intensive, or naturally asynchronous.

## Procedure
1. Confirm that asynchronous execution is actually needed and define what the caller should observe after enqueueing: acknowledgement, job identifier, status, result, cancellation, or no follow-up contract.
2. Define the job payload as a durable contract. Include only the identifiers and immutable inputs required to reconstruct the work; avoid copying large or sensitive objects into queues without a reason.
3. State the delivery semantics the system can provide. Assume duplicate delivery is possible unless the queue and surrounding transaction prove otherwise.
4. Make the job idempotent or define an explicit deduplication strategy. Choose an idempotency key tied to the business operation, not merely to a transient queue message when retries or re-enqueueing can create new message IDs.
5. Address the database-to-queue consistency boundary. If creating domain state and enqueueing work must behave atomically, use an established transactional-outbox, durable scheduler, or equivalent project pattern instead of a fragile two-step write.
6. Classify failures before retrying. Retry transient dependency or resource failures with bounded backoff and jitter; do not repeatedly retry deterministic validation, authorization, or permanent domain failures.
7. Define maximum attempts, timeout behavior, poison/dead-letter handling, manual replay rules, and what happens after exhaustion. Replays must preserve idempotency and auditability.
8. Control concurrency where jobs contend for the same resource. Use queue partitioning, leases, locks, optimistic concurrency, or domain-level serialization only where the invariant requires it.
9. Instrument enqueue rate, start, completion, latency, retries, failures, queue age/depth, and stalled work at the level needed to diagnose production behavior. Correlate jobs with the originating request or business operation when possible.
10. Handle worker lifecycle deliberately: graceful shutdown, in-flight work, cancellation, deployment interruption, and restart recovery.
11. Test duplicate delivery, retryable and permanent failure, worker interruption, concurrency conflicts, and exhausted retries in addition to normal completion.

## Decision rules
- Never treat "fire and forget" as a reliability guarantee.
- Framework-specific queue features are implementation choices, not substitutes for defining business semantics.
- Side effects outside the primary transaction, such as email, payment, or third-party API calls, need their own idempotency or reconciliation strategy.
- If queue topology, capacity, or runtime placement is the primary problem, hand it to `agency-infrastructure-engineer` or `agency-platform-engineer` as appropriate.

## Quality gate
The job system is done when duplicate and failed execution cannot silently corrupt domain state, retry and exhaustion behavior are explicit, interrupted workers recover predictably, and operators can tell whether work is progressing or stuck.