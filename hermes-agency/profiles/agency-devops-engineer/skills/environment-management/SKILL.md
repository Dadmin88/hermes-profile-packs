---
name: environment-management
description: Manage delivery environments through explicit configuration, controlled secrets, reproducible differences, drift detection, lifecycle policy, and parity focused on behavior rather than identical infrastructure.
---
# Environment Management

Use when development, test, staging, production, preview, or other delivery environments must remain understandable and reproducible.

## Procedure
1. Define each environment's purpose, owner, lifecycle, data sensitivity, external integrations, access policy, and which claims it is trusted to validate.
2. Separate application code/artifacts from environment configuration. Document which values legitimately differ and why instead of accumulating unexplained per-environment branches.
3. Source configuration from versioned or controlled systems where practical. Validate required values, types, and compatibility before deployment.
4. Keep secrets out of source and artifacts. Use the approved secret/identity mechanism and scope access by environment and workload.
5. Model parity by behavior and contract. Test/staging should reproduce the production characteristics needed for the risk being validated without requiring wasteful identical scale.
6. Control test data and production-data use. Prefer synthetic or sanitized data when realistic behavior can be proven without exposing sensitive records.
7. Detect and reconcile drift between declared and actual environment state. Manual emergency changes should be captured back into the source of truth or deliberately reverted.
8. Define creation, refresh, cleanup, expiration, and cost/resource policy for ephemeral environments so previews do not become abandoned permanent infrastructure.
9. Track dependency and version differences across environments that can invalidate test conclusions.
10. Periodically prove a clean environment can be recreated from documented configuration and artifacts.

## Decision rules
- Environment names do not guarantee parity; compare the behavior and dependencies that matter.
- Do not use production as the only place a deployment process is exercised.
- Avoid one-off configuration edits that bypass the declared source of truth without a reconciliation plan.
- Node-specific Fleet placement is runtime state; environment configuration should describe requirements and contracts rather than permanent node addresses.

## Quality gate
Environment management is sound when each environment has a clear purpose and lifecycle, configuration and secrets are controlled, meaningful behavioral differences are explicit, drift is detectable, sensitive data is handled intentionally, and representative environments can be recreated without undocumented manual steps.