---
name: requirements-traceability
description: Trace business needs through product requirements, design, implementation, validation, release evidence, and change history so important intent cannot disappear between teams.
---
# Requirements Traceability

Use when a project has contractual, business-critical, regulated, or complex requirements that need end-to-end evidence.

## Procedure
1. Identify the authoritative business needs, requirements, constraints, and decision owners in scope.
2. Give each material requirement a stable identifier or otherwise durable reference that survives document reformatting.
3. Map each requirement to the product behavior, design artifact, implementation component, data or process change, and validation evidence that satisfies it.
4. Record status and gaps separately: proposed, accepted, implemented, validated, deferred, superseded, or not applicable as appropriate.
5. Trace changes in both directions so an implementation change can reveal affected requirements and a requirement change can reveal affected artifacts.
6. Distinguish derived requirements and implementation decisions from the original business requirement that motivated them.
7. Review orphaned requirements and orphaned implementation regularly; either connect them, remove them, or document why they exist.
8. Keep traceability lightweight enough to maintain and automate links where stable system identifiers are available.

## Decision rules
- Traceability should answer impact and evidence questions, not create paperwork for its own sake.
- Do not treat a link as proof that the requirement is actually satisfied.
- Preserve the distinction between business intent and one chosen implementation.
- Stable IDs are more useful than page or line references that drift constantly.

## Quality gate
Traceability is adequate when each material requirement has a known owner and status, downstream artifacts and validation can be found quickly, changes expose their impact in both directions, and missing evidence or orphaned work is visible instead of hidden.