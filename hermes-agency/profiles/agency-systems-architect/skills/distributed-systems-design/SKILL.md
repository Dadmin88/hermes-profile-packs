---
name: distributed-systems-design
description: Design distributed behavior explicitly around ownership, coordination, consistency, ordering, retries, duplicate delivery, partitions, discovery, membership, and evolution rather than assuming a reliable single machine.
---
# Distributed Systems Design

Use when correctness or availability depends on communication and state across multiple processes, services, or nodes that can fail independently.

## Procedure
1. Define the operation and the state it reads or changes. Identify one authoritative owner for each invariant wherever possible before adding coordination.
2. State the failure model: crash/restart, message loss/delay/duplication/reordering, network partition, stale membership, slow nodes, dependency failure, and clock uncertainty as relevant.
3. Define consistency requirements per operation rather than declaring the entire system “strong” or “eventual.” Specify what readers may observe during concurrency and failure.
4. Define message/request delivery semantics and idempotency. Assume retries can duplicate side effects unless the end-to-end operation proves otherwise.
5. Define ordering only where the domain requires it and specify the scope of that ordering. Global order is expensive and often unnecessary.
6. Choose coordination mechanisms deliberately: single owner, optimistic concurrency, compare-and-swap, leases, consensus, partition ownership, transactional outbox, saga/compensation, or another pattern only when its guarantees match the invariant.
7. Define membership and discovery behavior, including stale records, join/leave, node identity, readiness, and what the system does when the control plane is temporarily unavailable.
8. Design backpressure and bounded work. Distributed retries, queues, and fan-out must not turn partial failure into unbounded amplification.
9. Define protocol/schema versioning so mixed versions can coexist for the rollout window or state clearly when coordinated upgrades are required.
10. Validate the hardest guarantees with fault injection, model tests, deterministic simulations, or focused prototypes where ordinary happy-path tests cannot prove them.

## Decision rules
- Network calls are not local function calls; timeout and uncertainty are part of the contract.
- “Exactly once” is an end-to-end property requiring precise proof; prefer idempotent at-least-once handling when it satisfies the domain.
- Avoid consensus or distributed locking when a simpler ownership boundary removes the coordination need.
- For Fleet/Keryx/Nodescale designs, treat node identity, live profile presence, placement, and authenticated transport as explicit distributed state/contracts rather than local assumptions.

## Quality gate
The design is ready when invariants and state ownership are explicit, failure/partition/retry behavior is defined, coordination matches the required guarantees, work remains bounded under failure, mixed-version behavior is understood, and critical distributed assumptions have evidence beyond a healthy-cluster demo.