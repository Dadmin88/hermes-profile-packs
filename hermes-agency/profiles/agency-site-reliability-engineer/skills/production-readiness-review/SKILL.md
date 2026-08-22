---
name: production-readiness-review
description: Assess whether a service is ready for production operation using reliability, capacity, dependencies, recovery, observability, ownership, and operational evidence.
---
# Production Readiness Review

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using architecture, capacity tests, dashboards, alert rules, runbooks, dependency contracts, and rollback evidence. Do not fill material gaps with assumptions when they can change the result.
3. Build a failure-oriented readiness checklist from the actual service topology, verify runbooks and recovery paths, and block launch only on material unresolved reliability risk.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Every critical failure mode has detection, ownership, and a practiced recovery path.
