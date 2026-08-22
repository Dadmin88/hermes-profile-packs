---
name: delivery-semantics
description: Design and implement message delivery semantics for retries, duplicates, reordering, acknowledgement, deadlines, and uncertain outcomes.
---
# Delivery Semantics

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using transport contract, producer/consumer state, retry policy, side effects, and timeout behavior. Do not fill material gaps with assumptions when they can change the result.
3. Assign stable operation identity, define acknowledgement points, make side effects idempotent or reconcilable, and test loss/duplication/reordering.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
A caller can determine or safely reconcile the outcome after every supported transport failure.
