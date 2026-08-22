---
name: rollback-strategy
description: Design rollback and forward-recovery for releases by identifying reversible surfaces, data/schema constraints, compatibility windows, triggers, decision authority, and post-recovery validation.
---
# Rollback Strategy

Use before releases where a bad change could materially affect users, data, availability, security, or dependent systems.

## Procedure
1. Identify everything the release changes: application artifact, configuration, schema/data, infrastructure, queues/events, caches, external contracts, feature flags, and irreversible side effects.
2. Classify each surface as directly reversible, reversible only within a compatibility window, forward-recovery-only, or externally irreversible.
3. Define the last known-good artifact/configuration and prove it can still run against the state that will exist after the new release begins.
4. Design database/schema changes for the required mixed-version window when rollback is expected. Avoid destructive transformations before older code can safely be retired unless a forward-only migration is explicitly accepted.
5. Define rollback triggers from observable service/user behavior and specify who or what is authorized to make the decision.
6. Automate or document the exact recovery sequence, including traffic shift, artifact/config revert, feature disablement, queue handling, cache behavior, and any required data reconciliation.
7. Preserve diagnostic evidence before rollback when possible so service restoration does not erase the cause.
8. Define validation after recovery: user-critical flows, data integrity, background work, external integrations, and monitoring returning to expected behavior.
9. Test the rollback or recovery mechanism in a representative environment, especially when releases change stateful components.
10. Record cases where rollback is unsafe and the required forward-recovery procedure instead of presenting a false one-click promise.

## Decision rules
- Rollback is a system property, not merely deploying the previous binary.
- Data and external side effects often determine whether rollback is truly possible.
- Feature flags reduce blast radius only when both paths remain tested and operational.
- Restore service first when necessary, then preserve enough evidence and ownership to complete root-cause work.

## Quality gate
The strategy is credible when reversible and irreversible surfaces are known, the previous version is compatible with reachable state or forward recovery is explicit, triggers and authority are clear, the procedure has been exercised, and validation proves the recovered system rather than assuming the old artifact restored everything.