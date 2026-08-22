---
name: reliability-design
description: Design system reliability from user-critical outcomes through service objectives, dependency budgets, redundancy, graceful degradation, recovery, observability, and operational ownership.
---
# Reliability Design

Use when architecture must meet explicit availability, durability, latency, or continuity expectations across multiple components.

## Procedure
1. Define critical user/system journeys and the consequence of failure. Establish measurable service objectives or equivalent reliability expectations for those outcomes.
2. Map each journey through its dependencies and identify which components are required synchronously, asynchronously, or only for optional capability.
3. Allocate reliability expectations across dependencies without assuming the end-to-end system can be more available than every hard dependency indefinitely.
4. Remove unnecessary single points of failure and shared failure domains where the objective justifies redundancy. Define quorum/replication/failover semantics rather than counting replicas alone.
5. Design timeouts, retries, circuit breaking, backpressure, load shedding, queue bounds, and degraded modes as a coordinated policy. Retries must not amplify overload.
6. Define data durability and recovery separately from request availability. State what may be lost, delayed, replayed, or reconstructed after failure.
7. Plan maintenance and deployment behavior so routine change does not consume the entire reliability margin.
8. Define observability around the user-critical outcomes and error budget or reliability margin, plus dependency symptoms needed to diagnose violations.
9. Define ownership and response for objective breaches, dependency degradation, capacity exhaustion, and repeated near misses.
10. Validate the design with representative dependency failures, node loss, overload, restart, and recovery tests before relying on redundancy claims.

## Decision rules
- Reliability is an end-to-end outcome, not the number of replicas.
- Redundancy inside one shared failure domain may not improve the failure scenario that matters.
- Graceful degradation should preserve the most important outcome rather than keep every feature partially alive.
- In Fleet systems, routing around an unhealthy node improves service availability only if node health, profile readiness, task semantics, and retry/idempotency are correctly integrated.

## Quality gate
The reliability design is ready when critical outcomes have explicit objectives, dependency and failure-domain contributions are understood, overload/retry/degradation policies cooperate, durability and recovery are defined, observability exposes objective violations, and failure tests demonstrate the intended behavior.