---
name: policy-control-mapping
description: Map an identified policy or requirement set to concrete system/process controls, owners, evidence, exceptions, and verification status.
---
# Policy Control Mapping

Use when a written requirement set needs to be translated into observable controls and review evidence.

## Procedure
1. Identify the authoritative requirement document, version, scope, definitions, and applicable sections before building the mapping.
2. Split relevant statements into atomic obligations or control objectives and retain source section identifiers for traceability.
3. For each obligation, identify the system, process, artifact, or workflow in scope and the role that owns implementation or operation.
4. Describe the actual control mechanism in concrete terms, such as configuration, access rule, approval step, review, retention process, logging, monitoring, or documented workflow.
5. Define the evidence that would demonstrate the control exists and, when needed, operates as described: configuration snapshots, code, logs, approvals, tickets, test results, sampled records, or other artifacts.
6. Mark each item from evidence as implemented, partial, absent, not applicable to the documented scope, inherited/shared, or requiring clarification.
7. Record approved exceptions with rationale, scope, compensating control, owner, and review/expiry information when the governing process provides for exceptions.
8. Identify shared controls and reusable evidence so one mechanism is not needlessly reimplemented or reviewed multiple times.
9. Validate representative controls in operation when the requirement expects recurring behavior rather than a one-time configuration.
10. Update the mapping when the requirement source, system, ownership, or control implementation changes.

## Decision rules
- Requirement text states what is expected; the mapping records how the scoped system demonstrates it.
- Documentation that a process exists is different from evidence that the process actually operated.
- Do not mark an item not applicable without an explicit scope-based rationale.
- Where interpretation exceeds the reviewer's authority, record the ambiguity and route it to the appropriate policy or legal owner instead of inventing an answer.

## Quality gate
The mapping is ready when each scoped obligation traces to a source section, control implementation and ownership are explicit, required evidence is identified, status follows evidence rather than assertion, exceptions are visible, and another reviewer can move from requirement to control proof without reconstructing the analysis.