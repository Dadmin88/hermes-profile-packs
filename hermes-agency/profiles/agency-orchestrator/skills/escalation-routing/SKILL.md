---
name: escalation-routing
description: Route blockers, conflicts, missing decisions, and unacceptable residual risk to the role or user with actual authority to resolve them, with a compact evidence-backed decision request.
---
# Escalation Routing

Use when a task cannot proceed correctly because a required decision, authority, resource, exception, or risk acceptance lies outside the current owner's lane.

## Procedure
1. State the blocker as a concrete unresolved condition. Separate missing information, conflicting requirements, unavailable resources, failed validation, policy decisions, and risk acceptance because they require different owners.
2. Determine who has authority over the decision, not who happens to be most senior. Product scope goes to product authority, durable architecture to architecture authority, security policy/risk to security or the authorized risk owner, engineering coordination to Technical Lead, source-control mechanics to Git Steward, and user/business choices to the user or designated decision maker.
3. Package the escalation narrowly: decision needed, why current work cannot proceed safely, relevant evidence, options already considered, tradeoffs, deadline or dependency impact, and a recommended option when the current owner has a justified recommendation.
4. Do not escalate questions that the specialist is expected to decide within its professional lane. Escalation is for authority boundaries or genuinely material uncertainty, not avoidance of judgment.
5. When multiple roles contribute evidence but only one role owns the decision, consolidate their evidence into one request rather than creating a vote.
6. For Hermes Kanban, block the affected task with the concrete reason, comment or attach the decision context, and create/route follow-up work only when another named profile must produce an artifact or decision. Keep unrelated independent tasks moving.
7. When the decision returns, record it durably with enough rationale or constraints for downstream workers, unblock the affected tasks, and update dependencies or scope if the decision changes the plan.
8. If the decision maker accepts residual risk, record exactly what was accepted and under what conditions. Do not convert risk acceptance into a claim that the underlying risk disappeared.

## Decision rules
- Escalate authority, not anxiety.
- Seniority is not a substitute for domain ownership.
- A blocked task should explain what would unblock it.
- User-facing escalation should ask the smallest decision necessary rather than dumping an internal debate.
- Never silently choose outside the Agency role's authority merely to keep the board moving.

## Quality gate
The escalation is correct when the unresolved condition and evidence are clear, the request reaches the actual decision owner, the current specialist has not abdicated an in-lane judgment, dependent work is truthfully blocked, independent work can continue, and the returned decision is preserved for downstream execution.