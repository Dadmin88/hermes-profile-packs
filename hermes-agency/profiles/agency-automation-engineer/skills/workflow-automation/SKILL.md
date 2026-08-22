---
name: workflow-automation
description: Implement multi-step workflow automation with explicit state, prerequisites, branching, side-effect boundaries, checkpoints, resumability, approvals, cancellation, and final reconciliation.
---
# Workflow Automation

Use when a recurring process spans several steps or systems and needs more structure than a single script or job.

## Procedure
1. Define the workflow outcome, trigger, actor/tenant, input contract, owner, and the authoritative state that determines whether the workflow is complete.
2. Map steps, prerequisites, branches, side effects, external dependencies, human decisions, and terminal states before writing orchestration logic.
3. Represent workflow state explicitly enough to distinguish not-started, running, waiting, blocked, succeeded, failed, cancelled, and partially completed conditions relevant to the process.
4. Give each side-effecting step an idempotency/reconciliation strategy and stable operation identity so retries or resume do not duplicate work.
5. Persist checkpoints at boundaries where process/node failure must be recoverable. Do not rely on one long-lived in-memory call stack for durable business workflows.
6. Define timeout and waiting behavior for asynchronous dependencies or human approvals, including escalation and cancellation where required.
7. Bound parallelism and fan-out so one workflow cannot exhaust shared resources or overwhelm dependencies.
8. Preserve causality: workflow ID, step/attempt ID, inputs/version, result, timestamps, and external correlation identifiers should be traceable through the run.
9. Define final reconciliation for mixed outcomes. If one step succeeds and a later step fails, state whether the process retries, compensates, waits for operator action, or completes in a partial accepted state.
10. Test restart/resume, duplicate trigger, branch conditions, dependency timeout, partial failure, cancellation, and replay in addition to the happy path.

## Decision rules
- Durable workflows need durable state; process memory is not a workflow database.
- Compensation is a domain decision, not an automatic inverse of every side effect.
- Avoid a workflow engine abstraction when a small idempotent script genuinely solves the process reliably.
- Fleet may move/resume execution on another node, so workflow state and operation identity must not depend on one machine's local memory.

## Quality gate
The workflow is ready when state and ownership are explicit, process interruption can resume safely, side effects cannot silently duplicate, waiting/approval/cancellation behavior is defined, partial outcomes reconcile predictably, and tests cover the failure transitions most likely to strand work.