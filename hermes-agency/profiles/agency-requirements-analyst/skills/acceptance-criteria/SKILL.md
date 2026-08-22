---
name: acceptance-criteria
description: Turn requirements into precise, observable acceptance criteria covering success, failure, permissions, boundaries, states, and constraints without dictating unnecessary implementation details.
---
# Requirements Acceptance Criteria

Use when a requirement needs testable completion conditions before design, engineering, or QA proceeds.

## Procedure
1. Restate the user or system outcome and identify the actor, preconditions, and scope.
2. Define observable success behavior from the outside of the implementation.
3. Add failure, invalid input, permission, empty, boundary, interruption, and recovery scenarios that materially affect the requirement.
4. Include measurable non-functional constraints only when they are genuinely part of accepted product behavior.
5. Keep criteria independent of private code structure, framework choices, or one proposed technical solution unless the implementation itself is the requirement.
6. Resolve ambiguous terms such as fast, intuitive, secure, supported, recent, or large into measurable or decision-owned meaning.
7. Check criteria for contradictions, impossible combinations, and missing prerequisites.
8. Review with Product Manager, designer, engineer, or QA as appropriate so all parties interpret completion the same way.

## Decision rules
- Acceptance criteria define observable completion, not a task checklist.
- Do not encode every theoretical edge case if it does not change accepted behavior.
- Technical constraints belong in criteria only when they are product or contractual requirements.
- Ambiguous criteria create hidden scope and should be resolved before implementation where practical.

## Quality gate
Criteria are ready when another specialist can determine pass or fail from observable evidence, important alternate states are covered, vague terms have been resolved, and implementation teams retain freedom over details not owned by the requirement.