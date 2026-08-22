---
name: test-case-design
description: Design high-value test cases from requirements, risks, state transitions, input partitions, boundaries, permissions, decisions, failures, and realistic user workflows.
---
# Test Case Design

Use when a feature or change needs deliberate test coverage before or alongside execution.

## Procedure
1. Extract the observable requirements, acceptance criteria, invariants, user roles, supported environments, data constraints, and known risks. Mark ambiguities that prevent a reliable expected result.
2. Model the behavior before enumerating cases. Identify inputs, states, transitions, decisions, side effects, dependencies, and outputs so tests target the system's logic rather than a list of screens.
3. Partition inputs into meaningfully different classes such as valid/invalid, empty/non-empty, authorized/unauthorized, existing/new, supported/unsupported, or other domain-specific equivalence groups.
4. Test boundaries around each meaningful constraint: minimum/maximum, just inside/outside, zero/one/many, before/at/after time thresholds, length/size limits, and transition edges where defects commonly hide.
5. Use decision tables when outcomes depend on combinations of independent conditions, and state-transition cases when behavior depends on what happened previously.
6. Include permission and ownership variations for protected behavior, especially cross-user, cross-role, and cross-tenant cases where applicable.
7. Include dependency and recovery behavior: slow response, failure, retry, duplicate request, cancellation, partial success, offline/reconnect, stale state, and other failure modes implicated by the architecture.
8. Include realistic user journeys and sequencing, not only isolated inputs. Vary order, repeat actions, navigation, refresh/restart, persistence, and re-entry when the feature maintains state.
9. Prioritize cases by risk and uniqueness. Remove redundant cases that prove the same rule unless a platform, data shape, or environment creates a distinct failure mode.
10. For every case record preconditions, action/input, expected observable result, important side effects or persisted state, cleanup, and the level/environment where the case should run.

## Decision rules
- Every test case should prove a distinct behavior, boundary, risk, or state transition.
- Pairwise or combinatorial techniques can reduce large configuration spaces, but do not omit combinations known to interact materially.
- Expected results must come from accepted requirements or authoritative behavior, not the current implementation when that implementation is what is being tested.
- Ambiguous requirements are a product/specification issue to escalate, not an invitation for QA to invent the rule.

## Quality gate
The test design is ready when important requirements and risks map to distinct cases, boundaries and state/decision logic are represented, permission and failure paths are included where relevant, redundancy is controlled, and every case has an unambiguous expected outcome and execution context.