---
name: release-observability
description: Observe software delivery from commit through build, artifact, promotion, deployment, health, rollback, and post-release behavior so release state and failures are traceable to exact revisions.
---
# Release Observability

Use when teams cannot quickly answer what version is running, whether a rollout is healthy, where a delivery failed, or which release caused a regression.

## Procedure
1. Define the release lifecycle and identifiers that connect it: source commit, build/run ID, artifact digest/version, environment, deployment/release ID, target revision, and rollout cohort or node set where relevant.
2. Emit structured events for build start/result, artifact creation, promotion, deployment start/progress/result, health gates, rollback/recovery, and final release completion.
3. Preserve correlation between pipeline events and runtime telemetry so service errors or latency can be compared against exact deployment windows and revisions.
4. Track deployment duration, queue/wait time, failure stage, retry count, rollback rate, lead time, and other delivery signals that reveal bottlenecks or instability.
5. Make current release state queryable without reading raw pipeline logs: what is intended, what is actually running, what is progressing, and what failed.
6. Separate pipeline success from runtime success. A completed deploy must still pass the health/user-behavior gates defined by the release process.
7. Alert on stuck or repeatedly failing release operations when action is required, and include enough identifiers to open the right pipeline/runtime evidence immediately.
8. Retain release evidence long enough to investigate delayed regressions and audit significant changes without keeping unrestricted secrets or sensitive logs.
9. Validate telemetry during a failed deployment and rollback so the most important recovery path is not the least observable one.

## Decision rules
- Release observability should answer “what changed?” before an incident responder searches commit history manually.
- Artifact/revision identity is more useful than mutable labels such as “latest.”
- When Fleet distributes workloads, record the rollout/revision on the selected nodes but keep Fleet's live placement registry authoritative for current location.
- Delivery metrics are diagnostic signals, not performance targets to game by removing safety gates.

## Quality gate
Release observability is ready when an operator can identify the exact source/artifact deployed, see rollout state and failure stage, correlate runtime change with release events, determine whether recovery occurred, and investigate the release without reconstructing state from scattered logs.