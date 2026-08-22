---
name: concurrency-consistency
description: Design and diagnose database concurrency using explicit invariants, transaction boundaries, isolation, locking or optimistic control, retries, deadlock handling, and consistency guarantees.
---
# Concurrency and Consistency

Use when concurrent requests, workers, jobs, or replicas can observe or modify the same persistent state and correctness depends on ordering or atomicity.

## Procedure
1. State the invariant that concurrency must preserve in plain language and identify which rows/documents/keys or aggregates participate.
2. Define the transaction boundary and what must be atomic. Avoid spreading one invariant across independent transactions unless compensation/reconciliation is an accepted part of the domain.
3. Understand the database engine's actual isolation and concurrency semantics, including snapshot behavior, write conflicts, gap/range locks, serializable anomalies, replica reads, or conditional writes as relevant.
4. Choose the simplest concurrency control that preserves the invariant: unique/constraint enforcement, atomic update, compare-and-swap/version column, optimistic retry, row/key lock, advisory/application lock, serializable transaction, or single-owner serialization.
5. Keep lock scope and duration bounded. Establish a consistent acquisition order when multiple resources must be locked to reduce deadlock risk.
6. Treat deadlocks/serialization failures as expected concurrency outcomes when the engine documents them that way. Retry only the full safe transaction with bounded attempts and fresh reads.
7. Account for idempotency when client/job retries can repeat a transaction after an uncertain result.
8. Distinguish primary consistency from replica/read-lag semantics. Do not promise read-your-write or uniqueness based on eventually consistent replicas unless the architecture provides it.
9. Test overlapping operations intentionally using barriers/concurrent workers rather than hoping ordinary tests produce the race. Assert the invariant and final persisted state.
10. Measure contention, lock waits, abort/retry rates, hot keys/rows, and transaction duration under realistic concurrency before scaling the pattern broadly.

## Decision rules
- Application `if` checks do not protect an invariant from concurrent writers without an atomic database guarantee.
- Stronger isolation can simplify correctness but may reduce concurrency; choose from the invariant outward.
- Locks are not inherently bad, but hidden or long-lived locks create operational risk.
- Distributed coordination outside the database belongs to Systems/Infrastructure architecture when the invariant spans multiple independent stores or services.

## Quality gate
The design is correct when the invariant and atomic boundary are explicit, the chosen engine primitive actually provides the required guarantee, retries and uncertain outcomes are safe, deadlock/contention behavior is understood, and deterministic concurrent tests demonstrate that invalid final states cannot be produced.