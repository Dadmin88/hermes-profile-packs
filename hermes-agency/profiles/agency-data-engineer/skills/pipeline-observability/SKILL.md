---
name: pipeline-observability
description: Observe data pipelines through freshness, completeness, volume, quality, lineage, run state, backlog, resource pressure, retries, and downstream readiness so silent data failure becomes visible.
---
# Pipeline Observability

Use when data jobs can succeed operationally while producing late, incomplete, duplicated, stale, or otherwise unusable outputs.

## Procedure
1. Define the consumer-facing data outcome: which datasets must be ready, by when, at what freshness/completeness/quality level, and which downstream decisions depend on them.
2. Track pipeline run identity, code/transformation revision, input watermark or partition range, output partitions, start/end, status, retry, and ownership.
3. Measure freshness and lag end to end, not only individual job duration. Include source lateness, queue/backlog delay, processing time, and downstream publication delay.
4. Track input/output volume, record counts, bytes, partitions, deduplication, rejection/quarantine, and quality-rule results against expected ranges.
5. Preserve lineage/correlation from bad output to source batch/partition and transformation revision so diagnosis does not require reconstructing the pipeline manually.
6. Observe backlogs, queue age, scheduler delay, worker/resource pressure, rate limits, and dependency health that can cause gradual data lateness before a hard failure.
7. Alert on actionable consumer-impacting conditions such as missed freshness objectives, repeated partition failure, stalled watermarks, major volume anomalies, or quality regressions.
8. Make retry/reprocessing visible as separate states. A green final run should not hide repeated churn, duplicate cost, or partitions still missing.
9. Build status views around datasets/data products and their dependencies, not only around scheduler job names.
10. Exercise telemetry with staged late data, bad records, failed partitions, backlog, and rerun behavior to prove the signals distinguish them.

## Decision rules
- Job success is not the same as data readiness.
- Freshness, quality, and completeness are first-class reliability signals for data products.
- Avoid high-cardinality telemetry that cannot be queried economically; retain detailed run metadata in an appropriate store instead.
- Pipeline observability should reveal enough evidence for Data Engineer diagnosis while infrastructure-level resource faults may be handed to `agency-infrastructure-engineer`.

## Quality gate
Observability is sufficient when consumers and operators can tell which data is ready or stale, trace anomalies to exact source/run/revision, see backlog and retry behavior, act on meaningful alerts, and distinguish scheduler success from actual data-product health.