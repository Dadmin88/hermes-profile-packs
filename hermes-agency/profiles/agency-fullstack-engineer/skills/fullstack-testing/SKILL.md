---
name: fullstack-testing
description: Test a bounded full-stack feature with complementary client, server, persistence, contract, and assembled-flow evidence while avoiding duplicate brittle tests at every layer.
---
# Full-Stack Testing

Use when one engineer owns a coherent feature across frontend and backend and needs confidence that both local logic and cross-boundary behavior work.

## Procedure
1. List the feature's observable contracts: user interactions/states, API behavior, domain invariants, persistence, authorization, async/external effects, and final durable outcome.
2. Assign each risk to the smallest layer that can prove it reliably: pure unit tests, frontend component/integration tests, backend integration tests, database/provider contract tests, or assembled browser/E2E validation.
3. Avoid reproducing the same assertion at every layer. Use lower layers for precise logic/failure coverage and a small number of cross-boundary tests for wiring/contract confidence.
4. Test the API/client mapping explicitly for success, empty, validation, unauthorized/forbidden, conflict, slow/failure, and stale/retry behavior implicated by the feature.
5. Use realistic persistence/framework behavior when transaction, schema, serialization, routing, browser, or storage semantics are part of the claim.
6. Control test data, time, randomness, network, authentication/permissions, and environment so tests remain deterministic and independent.
7. Include at least one assembled critical flow from a known starting state through user action, backend effect, durable state, and returned UI/result when the feature warrants it.
8. For bug fixes, capture the original failure at the narrowest reliable layer and add cross-boundary coverage only when the defect arose from integration rather than local logic.
9. Run focused tests during implementation, then broader relevant client/server suites plus the assembled-flow proof before completion.
10. Record exact validation and remaining risk; independent QA remains separate from the engineer's implementation tests.

## Decision rules
- More layers of duplicate tests can increase maintenance without increasing confidence.
- Mock only beyond the behavior the test is intended to prove.
- A server integration test cannot prove browser behavior, and a browser test that mocks the backend cannot prove server persistence.
- Cross-node Fleet execution should be covered only when distributed execution itself is a requirement of the feature; otherwise test the feature contract independently of placement.

## Quality gate
Testing is sufficient when each material risk has evidence at an appropriate layer, client/server contracts and negative states are covered, tests remain deterministic, a critical assembled flow is proven where needed, the relevant suites pass, and independent QA receives a clear statement of what engineering evidence already exists.