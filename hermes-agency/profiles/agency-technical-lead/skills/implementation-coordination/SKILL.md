---
name: implementation-coordination
description: Coordinate parallel engineering implementation by keeping ownership, contracts, dependencies, integration state, blockers, and validation evidence aligned without taking over specialists' work.
---
# Implementation Coordination

Use when several engineers or engineering profiles are implementing parts of the same accepted technical plan.

## Procedure
1. Establish one accountable owner for each implementation surface and make shared contracts explicit before work diverges.
2. Confirm each owner has the accepted product scope, architecture decisions, interface definitions, repository constraints, and validation expectations needed to work independently.
3. Track technical dependencies separately from organizational sequence. Keep independent work parallel and make prerequisite artifacts or decisions concrete.
4. Watch shared files, schemas, generated artifacts, migrations, configuration, and cross-cutting helpers for collision risk. Adjust ownership or sequencing before concurrent changes overwrite one another.
5. Resolve local implementation tradeoffs that cross specialist boundaries while preserving decisions owned by Product Manager, Software Architect, Security, or other authorities.
6. Keep integration state truthful: distinguish implemented, locally validated, integrated, independently reviewed, and release-ready work rather than collapsing them into one notion of done.
7. When a specialist blocks, identify the exact missing contract, decision, environment, dependency, or evidence. Route only that blocker to the owner capable of resolving it and keep unrelated work moving.
8. Require handoffs to include changed artifacts, interfaces, migrations, exact validation, known risks, and anything the next owner must preserve.
9. Coordinate rework from review, QA, security, or integration findings back to the implementation owner, then ensure the affected validation is repeated.
10. Before declaring engineering complete, confirm every planned component is integrated and the validation path defined in the execution plan has actually produced evidence.

## Decision rules
- Coordination is not implementation ownership. Specialists remain accountable for their work.
- Do not centralize every technical decision in the lead; resolve only cross-cutting tradeoffs or conflicts that need shared direction.
- Status is useful only when it describes verifiable state and next dependency.
- Parallelism is valuable when contracts are stable enough to prevent avoidable rework.

## Quality gate
Coordination is complete when engineering ownership and contracts remain clear, blockers are routed precisely, concurrent work integrates without hidden assumptions, review findings return to the right owners, and the assembled implementation has the required validation evidence.