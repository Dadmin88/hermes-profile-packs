---
name: internal-platform-design
description: Design an internal platform around repeated consumer needs, explicit service boundaries, self-service contracts, tenancy, policy, lifecycle, reliability, and sustainable ownership.
---
# Internal Platform Design

Use when multiple teams or workloads repeatedly solve the same infrastructure/runtime problem and a shared platform may reduce their cognitive and operational load.

## Procedure
1. Identify concrete consumers, repeated jobs-to-be-done, current pain, and evidence that centralization will remove more complexity than it creates.
2. Separate the platform's responsibility from product/application responsibility. Define what the platform guarantees and what remains owned by consumers.
3. Design a stable self-service contract through APIs, CLI, configuration, templates, portals, or another interface appropriate to the workflow.
4. Define identity, tenancy/isolation, permissions, quotas, secrets, network boundaries, data ownership, lifecycle, and deletion behavior.
5. Provide a paved path for common use while preserving explicit escape hatches for valid exceptions. Avoid a platform that requires tickets for routine operations.
6. Define versioning and compatibility so platform evolution does not force impossible lockstep migrations across consumers.
7. Design reliability and failure behavior for both the platform control surface and the workloads it manages. Avoid making the platform an unnecessary single point of failure.
8. Include observability, support boundaries, operational ownership, documentation, and migration/onboarding as first-class parts of the design.
9. Prototype the highest-risk consumer workflow before broad platform investment and measure whether it actually reduces time, errors, or cognitive load.

## Decision rules
- Do not build a platform for a hypothetical future customer base.
- A shared abstraction is valuable only when consumers can rely on its contract without learning all hidden implementation details.
- Platform policy should be enforceable and inspectable, not tribal knowledge.
- Fleet placement/routing is a Fleet capability; a platform may expose compatible interfaces or runtime services without duplicating Fleet's control plane.

## Quality gate
The platform design is ready when real consumers and recurring needs justify it, responsibility and contracts are explicit, routine operations are self-service, tenancy/reliability/lifecycle are defined, evolution is possible without constant breakage, and a representative workflow demonstrates reduced consumer complexity.