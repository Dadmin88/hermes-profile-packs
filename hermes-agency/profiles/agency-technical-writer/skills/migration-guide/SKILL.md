---
name: migration-guide
description: Write a technical migration guide from a known old state to a supported new state with compatibility, prerequisites, staged changes, data or configuration transformation, verification, mixed-version behavior, and recovery.
---
# Migration Guide

Use when users or operators must change code, configuration, data, deployment, or workflow to adopt a new version or architecture.

## Procedure
1. Define supported source versions or states, target state, audience, scope, and authoritative release or schema revisions.
2. Explain why migration is required and summarize externally visible changes before giving steps.
3. List prerequisites, backups, maintenance windows, capacity, dependency versions, and compatibility conditions that must be satisfied first.
4. Break the migration into reversible or independently verifiable stages where practical, especially for data and rolling deployments.
5. Provide exact transformation steps for code, configuration, data, interfaces, or infrastructure with before-and-after examples.
6. Describe mixed-version behavior, deprecation windows, downtime, irreversible steps, and how to resume after partial completion.
7. Add verification after each critical stage and a final end-to-end proof of the target behavior.
8. Define rollback where safe or forward-recovery where reversing would risk data or state loss, then validate the guide on a representative migration.

## Decision rules
- Migration documentation must start from a specified old state.
- Do not promise rollback when the transformation is not safely reversible.
- Verification belongs throughout the procedure, not only at the end.
- Exact version and compatibility claims require current release evidence.

## Quality gate
The guide is ready when a supported source state can reach the target through verified steps, prerequisites and mixed-version constraints are explicit, irreversible actions are visible, each stage can be checked, and recovery behavior is documented honestly.