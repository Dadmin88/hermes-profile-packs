---
name: golden-path
description: Create and maintain a paved or golden path that turns an approved common workload pattern into a secure, observable, supportable, self-service default without blocking justified exceptions.
---
# Golden Path

Use when teams repeatedly create similar services, jobs, applications, or runtime integrations and benefit from one well-supported default path.

## Procedure
1. Choose a genuinely common workload and define the end-to-end outcome the path should make routine, including creation, local development, CI, deployment, observability, ownership, and retirement where relevant.
2. Collect existing successful patterns and failure history before standardizing. Avoid declaring one team's accidental implementation the organization-wide default without evidence.
3. Define the defaults and guarantees the path provides: repository/service shape, identity, configuration, secrets, deployment, health, logging/metrics, policy checks, documentation, and support boundaries.
4. Automate the repeatable mechanics while keeping important parameters explicit. Generated output should be inspectable and maintainable after creation.
5. Make the path discoverable and self-service with a small entry surface and clear examples. The first successful use should not require private coaching from the platform team.
6. Define escape hatches for workloads that cannot fit the default. Require an explicit reason and ownership rather than forcing consumers into a harmful abstraction.
7. Version the path and decide how existing consumers receive fixes or migrations. Do not assume regenerating a template safely updates live projects.
8. Validate the path by creating a representative workload from scratch and taking it through build, test, deploy, observe, change, and recover workflows.
9. Measure adoption, time-to-first-working-change, drift, support volume, bypass reasons, and failure rate; use these signals to evolve or retire the path.

## Decision rules
- A golden path is a supported default, not a mandatory cage.
- Standardize proven repetition, not speculative future architecture.
- Generated scaffolding without lifecycle support becomes copied debt.
- Security and observability defaults should be usable without making ordinary consumers understand every platform implementation detail.

## Quality gate
The path is ready when a representative consumer can independently create and operate the common workload with safe defaults, the resulting artifacts remain understandable, exceptions have a legitimate route, updates have a lifecycle strategy, and evidence shows the path reduces repeated effort or errors.