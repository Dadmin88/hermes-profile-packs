---
name: codebase-scoping
description: Scope an engineering change in an unfamiliar or evolving codebase by tracing entry points, ownership, callers, data flow, tests, configuration, generated artifacts, and adjacent contracts before assigning implementation work.
---
# Codebase Scoping

Use when the team needs to determine where a requested change actually belongs and which engineering areas it will affect before implementation begins.

## Procedure
1. Read repository instructions, architecture/development documentation, manifests, and the existing implementation around the requested behavior before proposing changes.
2. Locate the user/system entry point and trace the current behavior through the smallest useful path: UI/API/command/event entry, application/domain logic, persistence or external integration, and returned/observable result.
3. Identify ownership boundaries and neighboring implementations. Note which profile specialties own the relevant frontend, backend, data, infrastructure, AI, game/engine, integration, or tooling work.
4. Search for callers, shared types, schemas, events, configuration keys, feature flags, generated code, migrations, tests, and documentation tied to the behavior. A file that contains the obvious function may not represent the full change surface.
5. Inspect existing tests and fixtures to understand expected behavior and project conventions. Treat them as evidence of current contracts, not infallible specifications when they conflict with accepted product decisions.
6. Identify external and runtime dependencies: services, databases, queues, identity providers, filesystem state, environment variables, CI/build steps, deployment assumptions, or platform-specific behavior that affect implementation or validation.
7. Separate confirmed change surface from uncertain areas requiring a spike or specialist input. Do not inflate scope simply because a directory is nearby or a dependency exists transitively.
8. Produce a scope map with likely files/components, interfaces that may change, data/migration implications, owners, test targets, and major unknowns. Avoid promising exact line edits before the implementation evidence supports them.
9. Use the scope to divide engineering ownership and integration points. Escalate durable boundary changes to Software Architect and product ambiguity to Product Manager.

## Decision rules
- Trace behavior before counting files.
- Search for consumers and contracts, not only definitions.
- Repository conventions beat generic framework habits unless the task intentionally changes those conventions.
- Scoping is complete enough when specialists can start safely; it does not require reading the entire repository.
- Do not turn exploratory notes into permanent architecture claims without verification.

## Quality gate
Scoping is ready when the current behavior and entry-to-outcome path are understood, meaningful callers/contracts/data/configuration/tests are identified, ownership and integration surfaces are explicit, unknowns are separated from facts, and the implementation team can begin without discovering a completely different change boundary immediately.