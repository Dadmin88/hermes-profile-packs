---
name: frontend-implementation
description: Implement a user-facing interface from product/design specs through state, accessibility, responsive behavior, API integration, tests, and runtime validation.
---
# Frontend Implementation

Use for web or app UI feature implementation.

## Procedure
1. Read the user flow, design states, acceptance criteria, component conventions, and API contracts.
2. Identify all meaningful states: loading, empty, populated, validation, error, success, disabled, permission, and responsive variants.
3. Implement semantic structure and accessibility alongside visuals: labels, roles, keyboard, focus, announcements, contrast-sensitive behavior, and reduced motion as relevant.
4. Keep server/client state ownership clear and handle race, retry, cancellation, and stale data where the interaction requires it.
5. Reuse design-system components when they match the semantics; do not force reuse when it changes behavior incorrectly.
6. Add tests for important interaction/state logic and validate the flow in the real rendered UI.
7. Check console/network errors, layout breakpoints, and integration failures before handoff.

## Quality gate
The implementation must work across real states and inputs, not only the happy-path screenshot.