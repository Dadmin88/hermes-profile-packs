---
name: intake-triage
description: Triage incoming work by clarifying requested outcome, source, urgency, authority, duplication, prerequisites, owner, and acceptance evidence before it enters active queues.
---
# Intake Triage

Use when requests arrive from users, stakeholders, incidents, ideas, support, projects, or automated sources and need disciplined admission into Agency work.

## Procedure
1. Capture the requested outcome, requester/source, affected product or system, time sensitivity, and why the work matters.
2. Check for duplicates, already-active work, existing decisions, known incidents, or a source-of-truth task/spec before creating a new assignment.
3. Determine whether the request is actionable, requires clarification, belongs to another workflow, or should be rejected/deferred.
4. Identify the professional role that owns the primary decision or deliverable and any required collaborating/review roles.
5. Record prerequisites, dependencies, artifacts, constraints, and acceptance evidence needed for clean execution.
6. Classify urgency from consequence and deadline rather than requester intensity.
7. Admit work with a clear owner and queue/priority state; preserve deferred/rejected rationale when it may matter later.
8. For distributed execution, pass the selected profile identity to Fleet rather than binding intake to a particular machine.

## Decision rules
- Intake is a quality gate, not a paperwork tax.
- Do not create duplicate tasks when existing work already owns the outcome.
- Ambiguity that changes ownership or acceptance should be resolved before routing.
- Machine location is not part of Agency intake unless the task itself has an explicit environment constraint.

## Quality gate
An admitted request is ready when outcome, owner, urgency, prerequisites, dependencies, constraints, and completion evidence are clear enough to route without reconstructing the request, and duplicates or non-actionable work have been handled deliberately.