---
name: traceability
description: Maintain requirement-level traceability from source need through decisions, product behavior, acceptance evidence, implementation references, and change history so scope and validation remain auditable.
---
# Requirement Traceability

Use when individual requirements need durable links to their origin, downstream artifacts, and proof of satisfaction.

## Procedure
1. Identify the authoritative source and assign a stable reference to each material requirement.
2. Record rationale, owner, status, dependencies, and any parent or derived requirement relationships.
3. Link each requirement to product or design decisions that define its intended behavior.
4. Link implementation or configuration artifacts only at the level useful for impact analysis and evidence; avoid brittle references to incidental internals.
5. Link validation evidence such as test cases, review findings, demonstrations, or acceptance records that prove the requirement rather than merely mention it.
6. Record supersession, scope change, deferral, or removal with the decision that authorized it.
7. Review orphaned requirements and artifacts and repair or explicitly explain missing links.
8. Use stable repository, task, document, or system identifiers so traceability survives Fleet-routed work and context changes.

## Decision rules
- A link is navigation, not proof of satisfaction.
- Traceability should survive implementation refactoring where the product requirement did not change.
- Keep source requirement, derived requirement, and implementation decision distinguishable.
- Do not maintain links that create more drift than decision value.

## Quality gate
Traceability is healthy when every material requirement has source, status, owner, downstream decision, and acceptance evidence; changes expose affected artifacts; superseded items retain history; and another specialist can follow the chain without reconstructing it from conversation logs.