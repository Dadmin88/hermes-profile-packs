---
name: consent-preference-engineering
description: Design and validate consent or preference controls with explicit purpose, state, provenance, propagation, revocation, and downstream enforcement.
---
# Consent Preference Engineering

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using approved requirements, user flows, data processors, preference store, event systems, and downstream jobs. Do not fill material gaps with assumptions when they can change the result.
3. Model states and jurisdiction/policy inputs supplied by owners, persist authoritative choice with evidence, propagate changes, enforce before processing, and test revocation/recovery.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
User choices are enforceable end to end and stale downstream state cannot silently continue disallowed processing.
