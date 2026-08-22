---
name: release-scope
description: Define the smallest coherent product scope for a release by protecting the intended outcome, separating must-have behavior from follow-up work, and making exclusions, dependencies, risks, and acceptance explicit.
---
# Release Scope

Use when a product initiative must be cut into a shippable release or when schedule, capacity, risk, or discovery requires deciding what belongs now versus later.

## Procedure
1. Restate the release outcome in user or business terms. Scope decisions should protect the reason for shipping rather than preserve every originally proposed feature.
2. List the capabilities and states required for that outcome to be complete enough to use safely and understand. Include permissions, failure/empty states, migration or onboarding implications, and other product behavior that would make the core capability misleading if omitted.
3. Separate must-have outcome requirements from enhancements, convenience, polish, adjacent use cases, and speculative flexibility. Do not call necessary correctness, security, accessibility, or recovery behavior “nice to have” merely because it is less visible.
4. Identify dependencies and constraints with design, engineering, security, operations, or external commitments. A small product scope that cannot be delivered independently may not be a real scope reduction.
5. Look for vertical cuts that deliver one coherent end-to-end outcome rather than horizontal cuts that leave unusable backend-only, UI-only, or half-workflow pieces unless an internal enabling release is intentionally the goal.
6. Evaluate deferred items for compatibility. Confirm the first release does not make the next likely step unnecessarily expensive through irreversible data models, contracts, or user expectations; route technical implications to the appropriate owner.
7. Define explicit non-goals and deferred behavior so teams do not silently re-add it during implementation. Record why each material cut is safe to defer and what would trigger bringing it back.
8. Align acceptance criteria to the reduced scope. Remove criteria for deferred outcomes while keeping criteria necessary to make the shipped outcome correct and understandable.
9. Check that the scope has a believable validation and release path, including critical QA/security/review needs and any operational or communication dependency.
10. If the outcome no longer provides enough value after necessary cuts, recommend changing the date/approach or not releasing rather than shipping a technically complete but product-empty fragment.

## Decision rules
- Smallest coherent beats smallest possible.
- Scope cuts should remove outcomes or variants cleanly, not hide incomplete behavior behind ambiguous requirements.
- Correctness, security, and essential accessibility are not ordinary scope knobs.
- Engineering estimates and architectural constraints come from their owning roles; Product Manager decides how those constraints change product scope.
- Explicit non-goals are part of the scope contract.

## Quality gate
Release scope is ready when the shipped outcome remains valuable and coherent, must-haves and deferrals are distinguishable, dependencies and irreversible implications are understood, acceptance criteria match the chosen cut, non-goals are explicit, and the team can explain why the release is complete without claiming deferred work is already solved.