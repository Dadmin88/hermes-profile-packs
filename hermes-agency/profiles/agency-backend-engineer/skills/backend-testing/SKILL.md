---
name: backend-testing
description: Build backend tests at the right layer to prove domain behavior, API contracts, persistence interactions, authorization, and important failure paths without brittle implementation coupling.
---
# Backend Testing

Use when implementing or changing server-side behavior and the work needs evidence that the backend contract remains correct.

## Procedure
1. Read the project's test conventions and run the relevant existing tests first when practical so pre-existing failures are not mistaken for regressions.
2. List the behaviors the change can affect: domain invariants, API responses, persistence, transactions, authorization, retries, external integrations, migrations, and failure handling.
3. Choose the cheapest test layer that proves each behavior:
   - unit tests for isolated deterministic domain logic;
   - integration tests for persistence, transactions, framework wiring, and service boundaries;
   - contract tests for interfaces depended on by another component or service;
   - end-to-end tests only when confidence depends on the assembled system.
4. Prefer testing through stable public behavior rather than private method calls, incidental SQL shape, logging text, or other implementation details unless those details are themselves the contract.
5. Use realistic infrastructure where semantics matter. A mock database cannot prove transaction, constraint, query, or migration behavior; a mock HTTP client cannot prove an actual wire contract. Use fakes or mocks when they deliberately isolate a dependency and the missing realism is not what the test is meant to prove.
6. Cover the important negative paths: invalid input, unauthenticated and unauthorized access, missing resources, conflicts, dependency failures, retries, partial failure, and boundary values relevant to the change.
7. Make fixtures deterministic, minimal, and independent. Control time, randomness, identifiers, network access, and global state where they otherwise make tests flaky.
8. Add a regression test for a bug before or with the fix whenever the failure can be reproduced automatically.
9. Run focused tests during development, then the broader relevant suite before completion. Record the exact validation commands and any intentionally untested risk in the handoff.
10. Use coverage reports to locate unexercised risk, not as an arbitrary percentage target. A high number does not compensate for missing assertions or missing failure cases.

## Decision rules
- A test should fail for a meaningful contract violation and stay green through safe refactoring.
- Do not replace a valuable integration test with mocks merely because the real dependency is inconvenient to set up.
- Do not create an expensive end-to-end test when a smaller layer proves the same behavior more reliably.
- QA owns independent product validation; backend tests are the engineer's executable evidence for the implementation contract.

## Quality gate
Testing is sufficient when the changed behavior and its material failure modes are proven at appropriate layers, tests are deterministic and maintainable, the relevant suite passes, and remaining untested risk is explicit.