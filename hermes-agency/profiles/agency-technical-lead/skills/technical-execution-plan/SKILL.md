---
name: technical-execution-plan
description: Convert approved product scope and architecture into a coordinated technical execution plan across engineering specialties.
---
# Technical Execution Plan

Use when a change spans multiple engineering domains or requires careful integration sequencing.

## Procedure
1. Confirm product acceptance criteria and any architecture decisions already made.
2. Identify the components, interfaces, data changes, migrations, and operational surfaces affected.
3. Assign implementation ownership by engineering specialty. Keep architecture, security, and quality gates independent where appropriate.
4. Define interface contracts and integration points before parallel implementation begins.
5. Identify technical dependencies, migration order, compatibility constraints, and rollback concerns.
6. Define the validation strategy: unit/integration/E2E tests, builds, performance checks, observability, or manual proof as appropriate.
7. Sequence the work to minimize integration risk while preserving useful parallelism.
8. Resolve local implementation tradeoffs; escalate only decisions that cross product, architecture, security, or operational authority.

## Quality gate
The plan is ready when engineers can work independently without inventing conflicting interfaces, and the integration/validation path is explicit before implementation starts.