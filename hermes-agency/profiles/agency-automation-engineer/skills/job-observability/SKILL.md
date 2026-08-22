---
name: job-observability
description: Observe automated jobs through trigger, logical operation identity, queue/wait time, attempts, execution, side effects, checkpoints, failures, completion, and stale/stuck detection.
---
# Job Observability

Use when scheduled, queued, event-triggered, or background automation needs to be diagnosable and operable at scale.

## Procedure
1. Define the logical job/operation identity separately from individual attempts so retries, node relocation, and replay can be correlated to one intent.
2. Record trigger/source, tenant/resource scope, workflow/job type, revision/config version, enqueue/start/end time, executing node/worker when relevant, attempt count, and final state.
3. Measure queue/wait age, runtime, completion/failure rate, retry rate, backlog/depth, concurrency, and resource/dependency pressure that can explain delayed work.
4. Emit structured lifecycle events for accepted, claimed/started, checkpointed, retried, blocked/waiting, succeeded, failed, cancelled, expired, and reconciled states that exist in the automation.
5. Correlate external side effects using safe provider/request IDs without logging credentials or unnecessary sensitive payloads.
6. Detect stale/stuck work using explicit heartbeats, leases, deadlines, or progress checkpoints appropriate to the job model rather than one universal timeout.
7. Distinguish retry churn from healthy throughput. A job eventually succeeding after many attempts may still indicate a degraded dependency or broken policy.
8. Alert on actionable conditions: missed schedules/objectives, old queue age, repeated failure, retry exhaustion, stalled checkpoints, or systematic duplicate suppression/reconciliation anomalies.
9. Provide a queryable history that supports replay/recovery decisions and can answer what ran, what changed, which side effects occurred, and why the job ended in its current state.
10. Test telemetry during crash/restart, duplicate trigger, retry, stale worker, relocation to another Fleet node, partial side effect, and final reconciliation.

## Decision rules
- Attempt logs alone are not job history; preserve the logical operation across attempts.
- Metrics show population health while event/run records explain individual failures; use both where the scale warrants it.
- Do not mark a job successful merely because its process exited zero if its intended side effect or durable outcome is unverified.
- Fleet may own node/task placement, but automation telemetry should carry node/attempt identity so relocation and correlated node failures are diagnosable.

## Quality gate
Job observability is sufficient when operators can follow one logical job across triggers, attempts, nodes, checkpoints, and side effects; population-level backlog/failure health is visible; stuck work is detectable; alerts are actionable; and replay/recovery decisions can be made from recorded evidence.