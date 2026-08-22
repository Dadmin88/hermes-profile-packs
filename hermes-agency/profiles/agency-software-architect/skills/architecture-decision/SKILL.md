---
name: architecture-decision
description: Make and document a consequential software architecture decision using constraints, alternatives, tradeoffs, boundaries, failure modes, migration, and validation.
---
# Architecture Decision

Use when a decision affects multiple components, durable interfaces, dependency direction, protocol, persistence strategy, or future change cost.

## Procedure
1. State the problem and forces: product needs, constraints, scale, reliability, security, team/runtime realities, and existing architecture.
2. Identify the decision boundary and what is deliberately not being decided.
3. Generate credible alternatives, including preserving the current design where applicable.
4. Compare alternatives on the forces that matter rather than generic pros/cons.
5. Define the chosen boundaries, interfaces, data/control flow, ownership, and failure behavior.
6. Plan migration and compatibility if existing callers/data are affected.
7. Record consequences, risks, and conditions that would justify revisiting the decision.
8. Validate risky assumptions with a spike, benchmark, prototype, or primary documentation where useful.

## Quality gate
An architecture decision must make downstream implementation clearer and acknowledge the costs it introduces.