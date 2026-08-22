---
name: capacity-planning
description: Plan operational team or process capacity from demand, service expectations, work mix, variability, constraints, and recovery margin without confusing organizational capacity with Fleet node scheduling.
---
# Operational Capacity Planning

Use when recurring operational demand must be matched to people, process, vendor, or service capacity over a planning horizon.

## Procedure
1. Define the demand units, service expectations, planning horizon, and work categories whose effort or bottlenecks differ materially.
2. Measure recent arrival rate, seasonality, backlog, completion rate, lead time, rework, escalation, and exceptional load where data exists.
3. Estimate effective capacity after meetings, maintenance, leave, interrupts, training, and specialized-skill constraints rather than using nominal headcount alone.
4. Identify bottleneck roles, approvals, vendors, tools, or process stages that limit throughput before adding generalized capacity.
5. Model expected demand plus reasonable variability and recovery margin for incidents or backlog spikes.
6. Compare options such as reprioritization, process improvement, automation, cross-training, vendor support, staffing, or service-level changes.
7. Make the chosen capacity assumptions and tradeoffs explicit and define leading indicators that show the model is failing.
8. Reforecast when demand mix, service expectations, or constraints change materially.

## Decision rules
- Utilization near 100% leaves no recovery room for variable work.
- Headcount is not interchangeable when specialist capability is the bottleneck.
- This skill plans operational/team capacity; Fleet owns live compute/node capacity and placement.
- Do not hide backlog growth by redefining completion.

## Quality gate
The plan is credible when demand, effective capacity, bottlenecks, variability, recovery margin, and assumptions are explicit; proposed changes address the actual constraint; and leading indicators show when capacity must be revisited.