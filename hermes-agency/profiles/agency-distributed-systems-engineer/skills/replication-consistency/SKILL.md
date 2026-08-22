---
name: replication-consistency
description: Implement replicated state with an explicit consistency model, conflict policy, convergence mechanism, and durability/recovery behavior.
---
# Replication Consistency

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using data model, read/write paths, topology, failure assumptions, and consistency requirements. Do not fill material gaps with assumptions when they can change the result.
3. Define authoritative writes and read guarantees, model concurrent updates, implement conflict or quorum rules, and test partition/rejoin behavior.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Observed behavior matches the documented consistency guarantee through partition, restart, and rejoin.
