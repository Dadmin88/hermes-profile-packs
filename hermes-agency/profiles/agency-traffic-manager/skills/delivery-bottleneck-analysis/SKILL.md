---
name: delivery-bottleneck-analysis
description: Diagnose persistent delivery bottlenecks from queue age, WIP, handoffs, dependencies, rework, specialist scarcity, approvals, and flow evidence before moving work or adding capacity.
---
# Delivery Bottleneck Analysis

Use when work repeatedly accumulates, misses expectations, or stalls at one stage, role, decision, or handoff.

## Procedure
1. Define the affected workstream and measure where age, backlog, blocked time, or missed commitments actually accumulate.
2. Map the flow from intake to completion and identify queues, handoffs, approvals, specialist roles, dependencies, and rework loops.
3. Distinguish temporary spikes from structural constraints using data across a representative period.
4. Check whether the apparent bottleneck is caused upstream by poor intake, oversized work, missing decisions, defects, or batching.
5. Identify the limiting resource or policy and estimate how it constrains throughput or lead time.
6. Compare interventions such as reducing WIP, improving input quality, changing sequencing, removing approval friction, cross-training, automation, or adding specialist capacity.
7. Avoid optimizing one stage in a way that simply moves the queue downstream.
8. Implement the smallest promising intervention and measure whether the bottleneck and end-to-end flow actually improve.

## Decision rules
- The busiest role is not always the bottleneck.
- Adding more work to a constrained system increases WIP, not throughput.
- Machine/resource bottlenecks belong to Fleet/Infrastructure when evidence shows runtime capacity is the constraint.
- Fix flow causes before institutionalizing manual expediting.

## Quality gate
The analysis is complete when the actual constraint is evidence-backed, upstream and downstream effects are understood, the proposed intervention targets that constraint, and improvement will be judged by end-to-end flow rather than local activity.