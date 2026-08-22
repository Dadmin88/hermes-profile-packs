---
name: desktop-app-architecture
description: Design desktop application boundaries across shell, renderer/UI, background services, local state, privileged capabilities, IPC, and crash/restart lifecycle.
---
# Desktop App Architecture

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using product flows, framework/runtime, OS targets, privilege needs, persistence, integrations, and update model. Do not fill material gaps with assumptions when they can change the result.
3. Map process and trust boundaries, assign state ownership, minimize privileged surface, define startup/shutdown/restart behavior, and document platform abstractions versus native differences.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Architecture keeps privileged operations narrow and preserves coherent behavior across restart and supported operating systems.
