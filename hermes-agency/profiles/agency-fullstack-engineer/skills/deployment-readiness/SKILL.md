---
name: deployment-readiness
description: Prepare a bounded full-stack feature for deployment by reconciling client/server artifacts, migrations, configuration, assets, compatibility, health, observability, rollback, and post-release validation.
---
# Deployment Readiness

Use when a full-stack feature is implemented and needs an engineer-level readiness check before release management or deployment automation takes over.

## Procedure
1. Identify every deliverable and runtime dependency changed by the feature: frontend bundle/assets, backend artifact, schema/data migration, configuration, feature flags, external integrations, queues/jobs, caches, and documentation as relevant.
2. Confirm build/test outputs correspond to the same reviewed source revision and no local-only/generated/uncommitted state is required for the feature to run.
3. Verify configuration and secrets are declared through supported environment/platform mechanisms with safe defaults or explicit required values; do not depend on one developer machine.
4. Review frontend/backend/API compatibility across the rollout window, including cached clients, rolling backend versions, and schema migrations when components may update at different times.
5. Sequence migrations, artifact deployment, feature enablement, background work, and cache/index changes so partially deployed states remain safe or are explicitly blocked.
6. Define health/readiness and user-visible validation that proves the feature works after deployment, plus telemetry needed to detect regression.
7. Identify rollback versus forward-recovery limits, especially after data changes or external side effects, and hand deployment strategy details to DevOps/Release roles when they own them.
8. Validate production-like build/startup, critical feature flow, static/assets, API connectivity, permissions, and background processing in the most representative available environment.
9. Record known limitations, manual steps, migration/compatibility concerns, verification commands, and any external dependency change requiring coordination.
10. Hand off exact source/artifact/migration state to the deployment/release owner rather than a vague “ready to ship” claim.

## Decision rules
- Passing unit tests does not prove the assembled production artifact can start and serve the feature.
- A feature depending on local environment state is not deployment-ready.
- Full-Stack Engineer validates feature readiness; DevOps/Release Manager own broader pipeline/release governance.
- Fleet node placement is dynamic. Declare runtime requirements if the feature genuinely has them instead of assuming the profile/service will land on one machine.

## Quality gate
The feature is ready for deployment when reviewed artifacts are reproducible, configuration and migrations are explicit, mixed-version states are safe, representative build/runtime validation passes, health/observability and recovery constraints are known, and the release owner receives exact artifacts, evidence, sequencing needs, and risks.