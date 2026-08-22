---
name: frontend-testing
description: Build frontend tests that prove user-observable behavior, interaction states, accessibility, and integration contracts at the smallest reliable layer.
---
# Frontend Testing

Use when implementing or changing user-facing behavior and the frontend needs executable evidence that the interaction still works.

## Procedure
1. Read the project's test conventions and establish the relevant baseline before adding tests so existing failures are not mistaken for regressions.
2. List the behaviors at risk: rendering states, user input, validation, keyboard interaction, focus changes, navigation, permissions, async loading, API responses, optimistic updates, responsive behavior, and recovery from errors.
3. Choose the smallest layer that proves each behavior:
   - unit tests for pure formatting, reducers, selectors, parsers, and deterministic state logic;
   - component or integration tests for rendered interaction, forms, focus, state transitions, and client boundaries;
   - browser or end-to-end tests for critical flows whose confidence depends on routing, layout, real browser behavior, storage, or assembled services.
4. Exercise the interface the way a user does. Prefer accessible roles, labels, names, visible text, and stable public test hooks over CSS classes, component internals, DOM depth, or implementation-specific selectors.
5. Mock at meaningful boundaries. Stub network behavior when the test is about UI handling, but do not mock away the exact integration or browser behavior the test is supposed to prove.
6. Include important non-happy paths: loading, empty data, invalid input, unauthorized/forbidden responses, slow requests, request failure, retries, rapid repeated actions, cancellation, and stale/out-of-order responses where relevant.
7. Include accessibility assertions where automation can catch real regressions, and manually or browser-test keyboard/focus behavior for critical custom interactions. Automated accessibility checks do not replace an independent accessibility review.
8. Keep tests deterministic. Control time, randomness, network, viewport, locale, and persisted state when they would otherwise create flakiness.
9. Add a regression test for reproduced bugs whenever the failure can be captured reliably.
10. Run focused tests during implementation, then the broader relevant suite and a real rendered-flow check before completion. Record exact validation and any remaining manual-risk area.

## Decision rules
- Test user-observable contracts, not private component structure.
- Do not use snapshot volume as a substitute for meaningful assertions.
- Do not chase arbitrary coverage percentages. Use coverage to expose untested risk.
- A browser test is justified when browser behavior matters; it is wasteful when a smaller deterministic test proves the same contract.
- QA owns independent validation. Frontend tests are the engineer's implementation evidence, not a replacement for QA.

## Quality gate
Testing is sufficient when the changed user-visible behavior and material failure states are proven at appropriate layers, selectors and fixtures are stable, the relevant suite passes, and the critical flow has been validated in a real rendered environment.