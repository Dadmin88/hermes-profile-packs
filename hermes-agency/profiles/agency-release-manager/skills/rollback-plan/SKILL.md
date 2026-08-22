---
name: rollback-plan
description: Design a release rollback or forward-recovery plan from failure modes, state changes, data compatibility, trigger conditions, authority, execution steps, and validation evidence.
---
# Rollback Plan

Use before a release where failed deployment or behavior could require fast, controlled recovery.

## Procedure
1. Identify the release changes that can fail: binaries, configuration, schema/data, dependencies, feature flags, infrastructure, caches, or external integrations.
2. Determine which changes are safely reversible and which require forward recovery because rollback could lose or corrupt state.
3. Define trigger conditions for rollback/recovery using observable health, error, integrity, latency, or business-impact signals.
4. Record the exact prior artifact/configuration/state required for rollback and confirm it is actually available.
5. Sequence rollback steps including traffic, compatibility, migrations, workers, caches, and dependent services where relevant.
6. Assign authority to initiate recovery and owners for technical execution, communication, and validation.
7. Define how to verify restored service and data integrity, not merely successful deployment commands.
8. Rehearse or dry-run high-risk recovery paths when practical and update the plan from evidence.

## Decision rules
- Rollback is not always safer than forward repair.
- Schema/data compatibility determines whether old code can safely return.
- Do not wait for an incident to discover the previous artifact was not retained.
- Recovery criteria should be observable before the release starts.

## Quality gate
The plan is credible when reversal versus forward recovery is explicit for each consequential state change, trigger signals and authority are known, required artifacts exist, execution is ordered, and validation proves service and data integrity after recovery.