---
name: integration-plan
description: Plan how independently owned engineering changes will combine into one working system, including interface readiness, merge order, data/schema compatibility, feature exposure, test environments, and rollback checkpoints.
---
# Integration Plan

Use when multiple engineering specialties or components must land separately but succeed together.

## Procedure
1. Identify the integrated outcome and enumerate every component, service, client, schema, migration, job, configuration, generated artifact, and external dependency that participates in it.
2. Define the interfaces between independently owned pieces before parallel work relies on them. Record request/response, data, event, state, error, version, or ownership contracts at the level implementers need.
3. Identify compatibility windows: old producer/new consumer, new producer/old consumer, existing persisted data, rolling deployment, feature-flag states, and partial rollout conditions that may exist during integration.
4. Decide integration order from those constraints rather than from who finishes first. Introduce additive or backward-compatible enabling changes before consumers when possible; schedule coordinated cutovers only when compatibility cannot reasonably be preserved.
5. Define how unfinished pieces remain safe: feature flags, disabled routes, dormant schema, adapters, dual-read/write, shadow traffic, test-only wiring, or another bounded mechanism. Avoid long-lived temporary architecture without a removal plan.
6. Specify shared integration environments, fixtures, seed data, external sandboxes, credentials, and configuration necessary to exercise the assembled flow. Identify what cannot be proven locally.
7. Map validation at each checkpoint: component tests before handoff, contract tests at interfaces, integration tests after wiring, end-to-end proof for the critical flow, and independent review/security/performance validation where risk warrants it.
8. Define merge/rebase ownership and how concurrent changes avoid stomping the same files or generated outputs. Route source-control mechanics to `agency-git-steward` when they become material.
9. Define rollback or forward-fix boundaries for consequential integration steps, especially migrations, externally visible contracts, irreversible side effects, or distributed deployments.
10. Track integration findings separately from component completion. A component can be done while the integrated system remains unproven.

## Decision rules
- Integration risk lives at boundaries and sequencing, not only inside components.
- Prefer compatibility over synchronized flag days when the cost is reasonable.
- Do not use feature flags as permanent architecture or as a substitute for clear contracts.
- Integration ownership belongs with Technical Lead; durable boundary redesign belongs with Software Architect.

## Quality gate
The integration plan is ready when every independently owned piece has a stable contract and integration point, mixed-version and migration states are understood, merge/deployment order is explicit, validation can prove the assembled outcome, and rollback or containment exists for the steps with meaningful blast radius.