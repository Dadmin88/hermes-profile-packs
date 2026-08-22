---
name: browser-api-automation
description: Implement browser and API automation that validates user-observable behavior without coupling tests to incidental implementation details.
---
# Browser Api Automation

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using user flows, API contracts, selectors/accessibility tree, state transitions, network evidence, and expected outcomes. Do not fill material gaps with assumptions when they can change the result.
3. Drive stable semantic interfaces, synchronize on meaningful state, use API setup only when it preserves the tested contract, and capture artifacts on failure.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Tests fail for real behavioral regressions rather than timing noise or cosmetic implementation changes.
