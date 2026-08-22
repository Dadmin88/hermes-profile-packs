---
name: migration-design
description: Design safe architectural migrations across data, interfaces, components, deployments, and consumers using compatibility stages, observability, rollback or forward recovery, and explicit completion criteria.
---
# Migration Design

Use when changing durable architecture while existing data, callers, deployments, or users must continue working through the transition.

## Procedure
1. Define the current state, target state, and reason for migration. Identify every durable artifact or consumer that spans the transition: data, APIs, events, files, caches, jobs, configuration, clients, services, and operational procedures.
2. Identify incompatibilities between old and new states and the deployment combinations that can exist in reality. Include rolling deployments, offline clients/workers, replayed events, old persisted records, and partial completion.
3. Prefer staged compatibility when practical: introduce additive support, deploy compatible readers, migrate/backfill state, switch writers/traffic, observe, then remove old paths only after evidence shows they are unused.
4. For data migrations, define invariants, backfill strategy, batching, concurrency with live writes, validation, retry/restart semantics, and how failures are detected without corrupting or silently skipping records.
5. For interface migrations, define version/feature negotiation, adapters or shims, deprecation signals, consumer migration order, and the condition that permits deleting compatibility code.
6. Define source of truth during each stage. Dual-read/write designs require explicit conflict and reconciliation rules; avoid indefinite periods where nobody knows which representation is authoritative.
7. Plan observability around migration progress and correctness: counts, mismatches, error rates, old-path usage, queue/backlog age, performance impact, and other signals that prove whether a stage is safe to advance.
8. Define recovery. Use rollback where the previous state can actually be restored safely; otherwise define forward-fix or restore-from-backup/replay procedures for irreversible transformations.
9. Keep the migration bounded. Give temporary adapters, flags, duplicate fields, and compatibility code owners plus removal criteria so the transition does not become permanent architecture.
10. Validate the migration in a representative environment and with production-shaped data/traffic when risk warrants it before executing irreversible stages.

## Decision rules
- A migration plan must cover mixed states, not only the beginning and end diagrams.
- Rollback is not real if data or external side effects become incompatible with the old version.
- Prefer additive staged change over synchronized cutover when the compatibility cost is reasonable.
- Temporary complexity is acceptable when it buys safe transition, but it needs an exit condition.
- Operational execution belongs to the implementing/operations roles; Software Architect owns the durable transition design and compatibility model.

## Quality gate
The migration design is ready when current/target states and intermediate combinations are explicit, data and interface compatibility are preserved or deliberately coordinated, progress/correctness are observable, recovery matches what is actually reversible, temporary mechanisms have removal criteria, and the migration can finish without leaving two permanent architectures.