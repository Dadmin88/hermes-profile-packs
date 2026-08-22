---
name: desktop-ipc-security
description: Design and implement desktop IPC with narrow message schemas, capability boundaries, validation, authentication/context, error semantics, cancellation, and observability.
---
# Desktop Ipc Security

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using process model, trust boundaries, message schemas, permissions, threat model, and UI workflows. Do not fill material gaps with assumptions when they can change the result.
3. Inventory required privileged operations, define typed request/response/events, validate untrusted renderer input, restrict filesystem/process/network authority, and test abuse/compatibility paths.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
The UI cannot expand privilege by crafting arbitrary messages and IPC failures are diagnosable without exposing secrets.
