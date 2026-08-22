---
name: failure-mode-analysis
description: Analyze architectural failure modes by tracing what can fail at each boundary, how failures propagate, what remains available or consistent, and which controls detect, contain, recover, or deliberately accept the impact.
---
# Failure Mode Analysis

Use when designing or reviewing a system whose reliability depends on multiple components, external services, distributed communication, durable state, or consequential automation.

## Procedure
1. Map the critical user/system journeys and the components, data stores, queues, networks, external dependencies, and control planes each journey requires.
2. Enumerate realistic failure modes at every boundary: unavailable/slow dependency, timeout, partial response, malformed data, stale cache, duplicate message, lost message, reordering, retry storm, process crash, node partition, disk/resource exhaustion, corrupted state, credential/permission failure, version mismatch, and human/operator error as relevant.
3. For each failure, trace propagation. Determine which upstream/downstream components wait, retry, fail closed/open, produce partial side effects, cache bad state, or amplify load.
4. Identify the invariant that must survive the failure: no duplicate charge, no cross-tenant exposure, durable task not lost, data remains internally consistent, user receives truthful status, or another domain-specific guarantee.
5. Define detection and diagnosis. Timeouts, error classification, health signals, queue age, mismatch counters, traces, audit events, and alerts should reveal failure early enough to act without requiring guesswork.
6. Define containment: bounded retries/backoff, circuit breaking, bulkheads, concurrency limits, idempotency, transactional boundaries, degraded modes, isolation, or explicit stop behavior. Use only controls that match the failure and architecture.
7. Define recovery: automatic retry, replay, reconciliation, failover, restart, restore, manual repair, or user re-action. State whether recovery is safe after uncertain partial completion.
8. Review correlated failures and dependencies that are only apparently redundant, such as two services sharing one database, region, credential authority, DNS path, or deployment pipeline.
9. Test the highest-impact assumptions through fault injection, dependency simulation, kill/restart tests, network disruption, recovery rehearsal, or representative load when practical.
10. Record residual failure modes and the product/operational consequence that is accepted rather than pretending every failure can be eliminated.

## Decision rules
- “Retry” is not a complete failure strategy; retryability, idempotency, backoff, exhaustion, and load amplification must be understood.
- A healthy process does not imply a healthy user journey.
- Redundancy that shares the same failure domain is not meaningful redundancy for that failure.
- Design for truthful degraded behavior rather than returning success while durable work is uncertain.
- Route detailed capacity/operations/security implementation to their owning specialists after the architectural guarantees are defined.

## Quality gate
The analysis is complete when important journey-level failures and propagation paths are explicit, invariants have detection/containment/recovery strategies, correlated failure domains are considered, high-risk assumptions have evidence where practical, and accepted residual failures are visible with their consequences.