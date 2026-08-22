---
name: retry-design
description: Design retries around failure classification, safe repetition, bounded attempts, backoff and jitter, deadlines, capacity, circuit breaking, reconciliation, and escalation instead of retrying every error blindly.
---
# Retry Design

Use when automation depends on operations that can fail transiently and repeated attempts may restore progress.

## Procedure
1. Classify failure modes for each operation: validation/business, authorization/configuration, conflict/concurrency, rate limit, transient dependency/network, timeout/unknown outcome, resource saturation, and permanent failure as relevant.
2. Confirm repetition is safe before retrying. Read-only or idempotent operations differ from consequential side effects with uncertain completion.
3. Define the retry budget: maximum attempts or elapsed time, per-attempt timeout, overall deadline, and which errors reset or consume the budget.
4. Use backoff and jitter appropriate to the dependency and provider/server guidance so many workers do not synchronize into a retry storm.
5. Respect explicit rate-limit/retry-after signals and combine them with local concurrency controls or admission limits when the caller itself is contributing pressure.
6. Stop retrying when failure becomes deterministic, authorization/configuration must change, the deadline/user intent expires, or continued attempts would amplify harm.
7. Define behavior after exhaustion: durable failure state, dead-letter/quarantine, delayed reschedule, alternate dependency, operator escalation, or product-visible failure.
8. Preserve attempt history, operation identity, error class, timing, and final outcome for diagnosis without flooding logs with identical stack traces.
9. For uncertain side effects, reconcile remote/current state before another attempt when the operation could already have succeeded.
10. Test transient recovery, permanent failure, rate limiting, timeout-after-success/unknown outcome, process restart, exhaustion, and fleet-wide correlated dependency failure.

## Decision rules
- Retry is a reliability tool and a load generator; design both effects.
- Exponential backoff without a maximum/deadline can still produce endless stuck work.
- Circuit breaking or admission control may be more appropriate than retry when a dependency is broadly unhealthy.
- Fleet rescheduling after node failure should not reset the logical retry/idempotency budget for the same operation automatically.

## Quality gate
Retry behavior is ready when errors are classified, only safe/transient cases repeat, attempts and time are bounded, backoff avoids synchronized amplification, unknown outcomes reconcile, exhaustion has an owned terminal path, and correlated-failure tests show the automation does not turn an outage into a retry storm.