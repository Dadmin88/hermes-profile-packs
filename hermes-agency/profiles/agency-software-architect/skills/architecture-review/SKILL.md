---
name: architecture-review
description: Review a proposed or implemented architecture against real product constraints, boundaries, dependency direction, data ownership, failure behavior, operability, security, migration, and unnecessary complexity.
---
# Architecture Review

Use when an architecture proposal, ADR, cross-component design, or major implementation needs independent architectural scrutiny before commitment or release.

## Procedure
1. Restate the actual problem, constraints, expected scale, reliability/security needs, team/runtime realities, and existing system context. Review against those forces, not against a generic ideal architecture.
2. Check component boundaries and ownership. Each major component should own coherent decisions/data and expose a contract that protects consumers from implementation details.
3. Review dependency direction and coupling: cycles, shared mutable state, shared databases, cross-layer imports, universal schemas, vendor/framework leakage, and components that must deploy/change together unexpectedly.
4. Review data/control flow end to end, including authority, consistency, caching, event ordering, retries, idempotency, and where durable state lives.
5. Review failure behavior at every boundary. Network/process boundaries introduce partial failure, timeout, retry, version mismatch, duplicate delivery, and observability requirements that local calls may not.
6. Review operability: configuration, deployment topology, health/readiness, upgrades, rollback/forward recovery, backup/restore, capacity, observability, and how an operator will diagnose the system under failure.
7. Review security and trust boundaries at the architectural level, then route detailed security validation to `agency-security-engineer` rather than substituting architecture review for security review.
8. Review migration and compatibility with current callers/data. A clean target diagram is incomplete if the system cannot reach it safely from the current state.
9. Challenge speculative complexity. Identify services, abstractions, queues, caches, plugin systems, generalized frameworks, or distributed protocols whose cost is not justified by a current constraint or credible near-term requirement.
10. Validate consequential assumptions with evidence such as benchmarks, prototypes, primary documentation, failure tests, or operational history when inspection alone is insufficient.
11. Report blocking architectural risks separately from optional improvements and state the tradeoff or consequence behind every significant finding.

## Decision rules
- Architecture exists to make change and operation safer, not to maximize component count or pattern vocabulary.
- A network boundary needs a reason beyond “scalability someday.”
- Simplicity means fewer independent concepts and failure modes, not merely fewer files.
- Do not redesign healthy unrelated architecture during review unless it materially blocks the proposed change.

## Quality gate
The review is complete when boundaries, dependencies, data ownership, failure behavior, operability, security/migration implications, and complexity are evaluated against real constraints; blockers have concrete consequences; and the design is either executable as written or has precise architectural changes required.