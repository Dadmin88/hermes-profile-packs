---
name: state-completeness
description: Review a design for complete user-visible states, transitions, permissions, loading, empty data, validation, failure, interruption, concurrency, success, and recovery so implementation does not invent missing product behavior.
---
# State Completeness

Use when a design looks polished in the happy path but may omit the states users encounter in a real system.

## Procedure
1. Start from the user goal and list every step that reads remote state, accepts input, changes durable state, waits, navigates, or can be interrupted.
2. For each step, enumerate meaningful states: initial/idle, loading, populated, empty, partial, disabled, validation error, authorization/permission, conflict/stale data, dependency failure, offline/disconnected, success, cancellation, and recovery where applicable.
3. Review transitions between those states. Define what triggers the transition, what the user sees, which actions remain possible, and what state is preserved or reset.
4. Check first-use versus returning-use, fresh versus existing data, and role/permission variations that change what controls or information should appear.
5. Review repeated/rapid actions, optimistic updates, duplicate submission, stale refresh, concurrent edits, and eventual completion when the product workflow can encounter them.
6. Review interruption: route away/back, close/reopen, refresh/restart, lost connection, modal dismissal, cancellation, or resumed background operation as relevant.
7. Ensure loading/waiting states communicate whether work is still progressing and prevent or allow duplicate actions intentionally rather than by accident.
8. Ensure error states preserve useful user input/context and offer a recovery action appropriate to the failure instead of dead-ending at a generic message.
9. Check completion/empty/zero-result states for a sensible next action and confirmation that the user's intended effect actually occurred.
10. Record missing or ambiguous states as product/design decisions with owner and impact, not as instructions for engineers to guess during implementation.

## Decision rules
- A state belongs in the design when it changes what the user can perceive, decide, or do.
- Do not create decorative states for impossible conditions; ground the state map in real system/product behavior.
- Error text alone is not a recovery design.
- If backend semantics or concurrency rules are unknown, route the unresolved contract to Product/Engineering rather than inventing technical behavior in design review.

## Quality gate
The design is state-complete when critical flows cover the realistic loading, empty, error, permission, conflict, interruption, success, and recovery conditions that affect user decisions; transitions and preserved state are clear; and implementers are not forced to invent material product behavior at build time.