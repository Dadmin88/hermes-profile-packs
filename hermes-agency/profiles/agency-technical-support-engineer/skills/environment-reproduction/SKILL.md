---
name: environment-reproduction
description: Recreate a customer or operator environment closely enough to validate a technical failure without copying secrets or unnecessary private data.
---
# Environment Reproduction

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using versions, OS/runtime, dependencies, configuration shape, topology, sample data, and failure trigger. Do not fill material gaps with assumptions when they can change the result.
3. Capture minimal environment fingerprint, build an isolated equivalent, import sanitized fixtures, verify baseline parity, then vary one suspected condition at a time.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
The reproduction explains which environment characteristics are necessary for the failure.
