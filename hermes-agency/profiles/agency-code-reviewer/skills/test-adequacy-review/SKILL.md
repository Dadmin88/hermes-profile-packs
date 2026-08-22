---
name: test-adequacy-review
description: Review whether tests provide meaningful evidence for the changed contract, important failures, boundaries, concurrency, integration behavior, and regression risk without rewarding brittle or superficial coverage.
---
# Test Adequacy Review

Use when reviewing a change whose correctness claim depends partly on automated tests.

## Procedure
1. Map the changed behavior and preserved contracts to test evidence. Ask what could be wrong even if every added test passes.
2. Check that each material behavior is tested at the layer capable of proving it: pure logic at unit level, real persistence/protocol/framework semantics at integration level, consumer contracts at contract level, and assembled critical flows at end-to-end level when necessary.
3. Review assertions for meaning. Tests should verify the outcome, invariant, error, side effect, state transition, or contract that matters rather than merely executing lines or snapshotting large structures without focused expectations.
4. Review negative and boundary coverage: invalid input, empty/maximum values, missing resources, unauthorized access, conflicts, dependency failure, retries, cancellation, duplicate operations, time boundaries, and other cases implicated by the change.
5. Review stateful and concurrent behavior where relevant. Tests should exercise transaction boundaries, stale updates, duplicate delivery, race conditions, idempotency, replay, or ordering when those are part of the risk.
6. Check mocks and fakes. A mock is acceptable when the test intentionally isolates a dependency; it is inadequate when the behavior being claimed depends on the real database, browser, network contract, parser, queue, filesystem, or framework semantics that the mock replaces.
7. Review regression linkage. Bug fixes should normally include a test that would fail for the original defect when the failure is automatable and stable.
8. Review determinism and isolation. Flag tests that depend on sleep timing, order, global mutable state, external mutable services, shared fixtures, local timezone/locale, or random behavior without control.
9. Use coverage data only as a clue to untested code paths. Do not treat a percentage threshold as proof that important behavior is covered.
10. Distinguish missing test evidence from a proven implementation defect. A reviewer may block for absent evidence when the untested risk is material, but should state exactly what claim remains unproven.

## Decision rules
- More tests are not automatically better; each test should buy confidence in a meaningful risk.
- A test that duplicates implementation details can make safe refactoring harder while missing the real contract.
- End-to-end tests are valuable for assembled behavior and expensive as a universal substitute for smaller tests.
- Test quality includes failure clarity: when a test breaks, the assertion should help identify which contract failed.

## Quality gate
The review is complete when material changed and preserved contracts are mapped to appropriate evidence, important negative and stateful risks are covered, mocks do not erase the behavior being claimed, tests are deterministic enough to trust, and any blocking evidence gap is precise.