---
name: vertical-slice
description: Implement a bounded end-to-end feature slice across UI, API, domain logic, and persistence while preserving contracts and avoiding unnecessary cross-system redesign.
---
# Vertical Slice

Use when a cohesive feature is small enough for one engineer to own across frontend and backend boundaries.

## Procedure
1. Confirm product behavior and architecture boundaries; identify where specialist review is still required.
2. Trace the complete current path from user action to persistence/external effects and back.
3. Define the minimal interface/data changes needed to deliver one coherent outcome.
4. Implement from contract inward, keeping validation and authorization on appropriate server boundaries.
5. Preserve transactional/data consistency and handle user-visible failure/retry behavior.
6. Add tests at each layer only where they provide distinct confidence, plus an integration or E2E proof of the slice.
7. Validate the complete flow in a representative environment.

## Quality gate
Full-stack ownership is not permission to bypass architecture, security, design, or review authority. Escalate cross-cutting decisions to the relevant specialist.