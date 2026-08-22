---
name: post-release-validation
description: Validate a release after deployment using revision-specific health, critical user flows, data integrity, migrations, observability, error budgets, and rollback criteria before declaring it complete.
---
# Post-Release Validation

Use immediately after a release or rollout stage to prove the intended revision is healthy in the real target environment.

## Procedure
1. Verify the exact deployed artifact/revision, configuration, migration state, and rollout scope before interpreting health signals.
2. Check service availability, error rate, latency, resource pressure, queues/backlogs, dependency health, and logs/traces relevant to the changed paths.
3. Exercise critical user or operational flows that the release affects using safe representative data.
4. Validate data integrity, schema compatibility, jobs, caches, events, and integrations when the release changes stateful behavior.
5. Compare key signals against the pre-release baseline and predefined go/no-go thresholds rather than celebrating a lack of alarms.
6. Watch for delayed failure modes long enough to cover the release's relevant asynchronous or traffic behavior.
7. Record anomalies, owner, containment, and whether they require rollback, forward recovery, or accepted follow-up.
8. Declare the release complete only after the required observation window and evidence are satisfied.

## Decision rules
- Deployment success is not release success.
- Absence of alerts is weak evidence when instrumentation does not cover the changed behavior.
- Verify the exact revision that users are receiving.
- Partial rollout validation should not be generalized to the entire fleet/audience prematurely.

## Quality gate
The release is validated when the intended revision is confirmed, critical behavior and state are healthy, changed-path telemetry remains within accepted bounds for the required observation window, and unresolved anomalies have explicit owners and recovery decisions.