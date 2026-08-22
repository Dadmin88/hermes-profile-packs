---
name: test-harness-design
description: Design an automated test harness with stable boundaries, fixtures, observability, and failure diagnostics appropriate to the product architecture.
---
# Test Harness Design

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using system contracts, test strategy, runtime dependencies, environment constraints, and current failure pain. Do not fill material gaps with assumptions when they can change the result.
3. Choose test layers from risk, isolate external dependencies deliberately, provide deterministic setup/teardown, and make failures explain themselves.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
The harness is repeatable, debuggable, and cheaper to maintain than duplicated ad-hoc test code.
