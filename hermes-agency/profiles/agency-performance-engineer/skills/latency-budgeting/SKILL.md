---
name: latency-budgeting
description: Allocate and validate an end-to-end latency objective across serial and parallel work, network, queues, dependencies, computation, rendering, retries, and tail behavior using measured service contributions.
---
# Latency Budgeting

Use when a user/system journey has a latency target that spans multiple components or when teams need to know where optimization effort matters.

## Procedure
1. Define the end-to-end operation, start/finish boundaries, target percentile/distribution, workload, and whether the objective concerns response, first useful result, completion, frame, or another latency definition.
2. Trace the critical path and identify work that is serial, parallel, queued, cached, speculative, or asynchronous/outside the user's wait.
3. Measure current latency contribution at each major boundary under representative conditions, including client/network, gateway, services, databases, external APIs, queues, serialization, and rendering as relevant.
4. Account for tail amplification. Several dependencies with individually acceptable percentiles can produce worse end-to-end tail behavior, especially under fan-out.
5. Allocate budgets based on technical/product constraints and optimization opportunity rather than dividing the total evenly by component count.
6. Include queueing, retries, timeouts, connection/setup, cache misses, cold starts, and other paths that consume the objective under realistic failure/scale conditions.
7. Define component-level indicators/gates that reveal when one layer consumes too much of the end-to-end budget while preserving the overall user outcome as the authority.
8. Optimize or redesign the dominant serial/variable contributions first, then remeasure because improving one layer can expose another.
9. Revisit budgets when architecture, workload, geography, providers, or product expectations change; do not fossilize an early allocation as a permanent SLA.

## Decision rules
- End-to-end latency is not the sum of every component duration when work overlaps; use the actual critical path.
- Tail latency and variance often matter more than average latency for user experience and timeout policy.
- A component meeting its local budget does not excuse a missed user-level objective.
- Fleet placement can affect network/data-locality latency, but placement policy remains Fleet-owned; report measurable constraints or preferences.

## Quality gate
The latency budget is useful when the end-to-end boundary and percentile are explicit, critical-path contributions are measured, tail/queue/retry behavior is included, allocations reflect real constraints, local signals connect to the user objective, and optimization priorities follow the measured largest contributors.