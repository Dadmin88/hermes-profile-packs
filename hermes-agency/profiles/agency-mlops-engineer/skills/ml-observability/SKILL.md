---
name: ml-observability
description: Observe ML systems across input drift, output quality proxies, latency, errors, resource use, model/version mix, evaluation regressions, and rollback signals.
---
# Ml Observability

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using serving telemetry, model metadata, evaluation baselines, feature/input statistics, privacy constraints, and user outcomes. Do not fill material gaps with assumptions when they can change the result.
3. Define model-specific operational questions, instrument requests without leaking sensitive content, compare segments/versions, detect drift, and connect alerts to action.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Operators can identify which model/version/workload changed and whether to roll back, retrain, or investigate data/application behavior.
