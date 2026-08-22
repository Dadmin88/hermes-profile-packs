---
name: capacity-balancing
description: Balance incoming professional work across Agency owners and queues using current commitments, specialist scarcity, urgency, WIP, and service expectations without performing Fleet compute scheduling.
---
# Capacity Balancing

Use when work demand exceeds or unevenly loads the available professional team and sequencing or reassignment is needed.

## Procedure
1. Establish current queued and active work by owner/profile, deadlines, priority, blocked state, and meaningful effort or complexity signals.
2. Separate capacity that is genuinely interchangeable from work requiring a specific specialty, authority, customer context, or continuity.
3. Identify overloaded queues from aging, WIP, missed service expectations, or upcoming commitments rather than headcount alone.
4. Reprioritize, defer, split, or reassign work where another qualified owner can take it without losing critical context or decision authority.
5. Protect high-value focused work from constant interruption and maintain room for urgent incidents or unplanned demand.
6. Surface persistent specialist bottlenecks that require cross-training, process change, automation, staffing, or altered service expectations.
7. Preserve task ownership and handoff context when work moves between profiles or teams.
8. Let Fleet independently choose eligible nodes and runtime capacity after the professional profile has been selected.

## Decision rules
- Professional capacity and compute capacity are separate layers.
- Do not treat every profile as interchangeable simply because another agent is idle.
- Excessive reassignment can cost more than temporary queue imbalance.
- Capacity decisions should protect outcome quality as well as response time.

## Quality gate
Capacity is balanced when urgent and high-value work has appropriate professional ownership, overloaded queues and scarcity are visible, reassignment preserves context and authority, WIP remains manageable, and node-level compute scheduling is left to Fleet.