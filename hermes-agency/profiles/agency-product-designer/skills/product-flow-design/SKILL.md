---
name: product-flow-design
description: Design an end-to-end product flow from user goal through information architecture, states, interactions, errors, accessibility, and implementation handoff.
---
# Product Flow Design

Use when a feature or workflow needs a coherent user experience before implementation.

## Procedure
1. Start from user goal, product requirements, constraints, and known research.
2. Map the end-to-end flow including entry, success, cancellation, interruption, error, empty, loading, permission, and recovery states.
3. Define information hierarchy and decision points before visual polish.
4. Choose interaction patterns that match platform conventions and existing system behavior where possible.
5. Design accessibility and responsive behavior as part of the flow, not as a final pass.
6. Validate high-risk assumptions with prototypes or user research.
7. Produce implementation-ready specifications for states, transitions, content, and edge behavior.

## Quality gate
An implementer should not need to invent missing product behavior, and a user should be able to recover from common failure states.