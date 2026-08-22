---
name: dependency-planning
description: Plan multi-profile work as an explicit dependency graph so independent tasks run in parallel, dependent work waits for real prerequisites, and handoffs preserve the evidence consumers need.
---
# Dependency Planning

Use when a goal contains multiple tasks whose order or parallelism affects correctness, speed, or rework.

## Procedure
1. List the required deliverables and the information each one consumes. A dependency exists when one task cannot be completed correctly without another task's output, decision, artifact, or validated state.
2. Distinguish hard dependencies from preferences. Do not serialize work merely because one task was imagined first; independent research, implementation, design, or review preparation should proceed in parallel when their contracts are stable.
3. Define dependency direction by artifact flow: parent/prerequisite produces something concrete that the child/consumer needs. Avoid circular dependencies by separating the underlying decision or interface that both sides are waiting on.
4. Stabilize shared interfaces before parallel implementation when conflicting assumptions would cause rework. Assign ownership of the interface or decision to the role with authority over it.
5. For Hermes Kanban work, represent real prerequisites with task links so readiness follows completion state rather than conversational memory. Use comments and attachments for the handoff evidence the dependent task needs.
6. Account for validation dependencies. A release, integration, publication, or final synthesis may depend not only on implementation completion but on independent QA, security, review, or acceptance evidence.
7. Keep dependency chains as short as the work allows. Long serial chains increase idle time and make a single blocker stall the whole goal.
8. When a prerequisite blocks, record the concrete missing condition and determine whether another independent branch can continue. Do not mark downstream work ready merely to keep agents busy.
9. Re-evaluate the graph when a task changes scope, discovers a new interface, or invalidates an assumption. Update links and owners so the board reflects reality rather than the original plan.

## Decision rules
- Parallelize independence, not uncertainty.
- A shared file is not automatically a dependency if work can be separated safely; a hidden shared contract often is.
- Completion is not a useful prerequisite unless the downstream task can identify the artifact or decision it consumes.
- Dependencies should encode correctness constraints, not organizational hierarchy.

## Quality gate
The plan is ready when hard prerequisites are explicit, independent work can proceed concurrently, shared decisions have owners, validation gates appear in the graph where needed, no circular or ceremonial dependencies remain, and each downstream task knows exactly what it consumes from its prerequisites.