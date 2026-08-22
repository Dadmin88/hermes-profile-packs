---
name: acceptance-criteria
description: Define acceptance criteria as observable product behavior, states, permissions, boundaries, errors, and outcomes that design, engineering, and QA can interpret consistently without prescribing unnecessary implementation.
---
# Acceptance Criteria

Use when a product requirement needs a testable definition of success before implementation or validation.

## Procedure
1. Start from the user or business outcome and identify the observable behavior that proves it. Acceptance criteria should answer what must be true, not how the code must be written.
2. Cover the main success path and the material alternate states the product must handle: empty, loading, error, permission differences, limits, retries, cancellation, existing data, repeated actions, or other domain-relevant conditions.
3. State preconditions only when they change the expected behavior, such as user role, account state, feature availability, existing records, device capability, or external dependency state.
4. Make each criterion independently understandable and falsifiable. Use Given/When/Then when state transitions benefit from it, concise bullet criteria when simpler, or examples/tables when combinations are clearer. The format serves clarity, not ceremony.
5. Specify boundaries and measurable thresholds only when the threshold is a real product requirement. Avoid invented performance numbers, arbitrary field limits, or implementation constraints that have not been decided.
6. Distinguish product criteria from engineering definition-of-done activities. Code review, unit tests, deployment, or documentation may be delivery requirements, but they should not be disguised as the user's observable product outcome.
7. Include authorization and visibility behavior when different roles or owners should experience different outcomes, while leaving security enforcement design to the appropriate technical/security owner.
8. Resolve contradictions or ambiguities before implementation when they affect the product contract. If an edge case is intentionally unspecified, mark it as an open decision instead of letting different specialists guess differently.
9. Review the criteria with design/engineering/QA context where useful: design should be free to choose interaction details not fixed by product, engineering should identify feasibility constraints, and QA should be able to derive validation without reverse-engineering intent.

## Decision rules
- Acceptance criteria define success; they are not a miniature technical design.
- One user story template is optional. A clear requirement does not become invalid because it lacks “As a…”.
- Avoid criteria that merely restate the feature title or use words such as “works correctly,” “fast,” or “user-friendly” without observable meaning.
- Do not enumerate every imaginable edge case. Cover cases that materially affect the product contract and route deeper technical failure handling to engineering.

## Quality gate
Acceptance criteria are ready when the intended behavior and important alternate states are observable and falsifiable, roles and boundaries are clear, implementation freedom remains where appropriate, unresolved product decisions are explicit, and QA can validate success without inventing the requirement.