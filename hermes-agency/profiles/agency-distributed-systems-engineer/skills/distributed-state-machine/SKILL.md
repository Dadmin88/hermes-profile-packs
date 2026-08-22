---
name: distributed-state-machine
description: Implement a distributed state machine with explicit commands, invariants, authority, transitions, persistence, replay, and recovery semantics.
---
# Distributed State Machine

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using protocol contract, state invariants, durable records, concurrency model, and failure scenarios. Do not fill material gaps with assumptions when they can change the result.
3. Translate architectural guarantees into state transitions, define duplicate/out-of-order behavior, make persistence boundaries explicit, and prove restart/replay correctness.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
All accepted event orders preserve invariants and recovery produces the same authoritative state.
