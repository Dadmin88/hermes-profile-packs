---
name: desktop-update-runtime-debugging
description: Design update/rollback behavior and diagnose failures that occur only in installed/packaged desktop builds.
---
# Desktop Update Runtime Debugging

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using current/target versions, package format, updater state, local data schema, logs, OS environment, and signatures. Do not fill material gaps with assumptions when they can change the result.
3. Model version transitions and state compatibility, stage updates safely, capture startup/update logs, compare dev versus package environment, inspect resource/native paths, and prove rollback/recovery.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
A failed update cannot strand the application and packaged-only failures have a reproducible root cause or bounded recovery.
