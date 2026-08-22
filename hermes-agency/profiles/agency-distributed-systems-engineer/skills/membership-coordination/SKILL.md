---
name: membership-coordination
description: Implement node membership, discovery, leases, leadership or coordination without allowing stale identity or split authority to silently corrupt state.
---
# Membership Coordination

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using identity model, clocks/deadlines, discovery source, persisted epochs, and partition scenarios. Do not fill material gaps with assumptions when they can change the result.
3. Define identity and epoch rules, join/leave transitions, liveness evidence, fencing, and recovery from simultaneous or stale participants.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Stale or duplicate members cannot exercise authority after losing eligibility.
