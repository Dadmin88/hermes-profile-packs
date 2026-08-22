---
name: native-os-integration
description: Implement native desktop integrations such as tray/menu, notifications, clipboard, file associations, deep links, startup behavior, file pickers, and platform permissions.
---
# Native Os Integration

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using OS targets, product requirements, platform APIs, permission model, packaging format, and UX design. Do not fill material gaps with assumptions when they can change the result.
3. Define supported OS behavior, prefer platform conventions, isolate capability adapters, handle denied/unavailable states, and test install/uninstall/restart interactions.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Each integration behaves predictably on supported OS versions and degrades explicitly when capability is unavailable.
