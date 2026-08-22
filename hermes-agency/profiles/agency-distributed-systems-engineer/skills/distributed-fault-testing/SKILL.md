---
name: distributed-fault-testing
description: Prove distributed behavior with deterministic and stochastic tests for delay, loss, duplication, reorder, partition, crash, restart, and clock-sensitive edges.
---
# Distributed Fault Testing

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using protocol invariants, fault model, trace hooks, seeds, checkpoints, and expected convergence. Do not fill material gaps with assumptions when they can change the result.
3. Map guarantees to fault hypotheses, instrument state transitions, inject one bounded failure dimension at a time, then combine high-risk sequences.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Failures reproduce from captured seeds/traces and every claimed guarantee has a negative-path proof.
