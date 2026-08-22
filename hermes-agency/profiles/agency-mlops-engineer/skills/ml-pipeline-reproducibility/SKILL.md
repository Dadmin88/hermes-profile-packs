---
name: ml-pipeline-reproducibility
description: Build a reproducible ML pipeline that pins code, data, environment, configuration, seeds, metrics, and model artifacts from training through evaluation.
---
# Ml Pipeline Reproducibility

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using dataset revisions, code SHA, environment, configs, seeds, hardware/runtime, and evaluation suite. Do not fill material gaps with assumptions when they can change the result.
3. Assign immutable run identity, capture data/version lineage, isolate environment, record hyperparameters and metrics, persist artifacts, and reproduce from clean state.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
A second clean run can recreate the model/evaluation result within documented nondeterminism bounds.
