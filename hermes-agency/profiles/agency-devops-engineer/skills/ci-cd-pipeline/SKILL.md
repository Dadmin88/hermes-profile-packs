---
name: ci-cd-pipeline
description: Design or improve CI/CD so changes are reproducibly built, tested, secured, promoted, deployed, observed, and recoverable.
---
# CI/CD Pipeline

Use when creating or changing build, test, artifact, promotion, or deployment automation.

## Procedure
1. Define the source event, supported branches/tags, artifact, environments, and release policy.
2. Make builds deterministic enough to identify exactly what source produced an artifact.
3. Order fast feedback before expensive jobs while preserving required quality/security gates.
4. Keep secrets scoped to the smallest jobs/environments and avoid exposing them to untrusted code.
5. Promote immutable artifacts rather than rebuilding differently for each environment when practical.
6. Design deployment strategy, health validation, concurrency controls, and rollback/recovery.
7. Cache carefully: optimize time without allowing stale or untrusted state to bypass correctness.
8. Emit useful job/deployment evidence for failures and releases.

## Quality gate
The pipeline must make the safe path the normal path and allow a failed release to be diagnosed and recovered without guesswork.