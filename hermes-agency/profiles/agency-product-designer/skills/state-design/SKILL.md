---
name: state-design
description: Design complete product UI states and transitions for normal, empty, loading, permission, validation, error, offline, interrupted, and recovery conditions so the experience remains coherent beyond the happy path.
---
# State Design

Use when a feature needs a complete behavioral/state specification before frontend implementation.

## Procedure
1. Identify the user-visible state dimensions that can change: data availability, request/activity status, permissions, selection, validation, connectivity, progress, account/entity status, feature availability, and other domain-specific state.
2. Model valid combinations and transitions. Avoid designing every dimension independently if combinations would create contradictory or impossible screens.
3. Define the initial state and all meaningful entry states, including returning users with existing or partial data rather than assuming every flow begins empty.
4. Define loading/pending behavior according to the operation. Preserve stable content when possible, distinguish initial load from refresh/mutation, and avoid UI that appears frozen or resets unnecessarily.
5. Design empty states around why they are empty: first use, filtered no-results, permission limitation, archived/deleted data, disconnected source, or successful completion may require different guidance.
6. Design validation and error states with clear ownership and recovery. Indicate what failed, what remains preserved, what the user can correct/retry, and whether the system is uncertain about a completed side effect.
7. Define permission and availability states without leaking inaccessible information. Make the next action clear when access can be requested or configuration changed.
8. Define interruption and recovery behavior for refresh, navigation, reconnect, restart, cancellation, timeout, stale data, or resumed async work where relevant.
9. Include success/confirmation states only when the outcome is not already self-evident from the resulting UI. Avoid transient feedback that disappears before users can understand consequential outcomes.
10. Deliver a state matrix or annotated flow showing triggers, user-visible result, available actions, transitions, and accessibility/announcement considerations for implementation.

## Decision rules
- A screenshot is one state, not a complete product design.
- Preserve user input and context through recoverable failures whenever feasible.
- Error states should not invent technical details the system cannot know.
- Similar-looking empty/error/permission states may have very different user intent and next actions.
- Product Designer defines user-visible states; Frontend Engineer owns client state implementation details.

## Quality gate
State design is ready when meaningful states and transitions are complete and non-contradictory, alternate entry/recovery conditions are covered, users retain clear next actions through failure and permission limits, and the frontend implementer does not need to invent missing user-visible behavior.