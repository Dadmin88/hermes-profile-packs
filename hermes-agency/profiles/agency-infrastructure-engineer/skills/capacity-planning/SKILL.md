---
name: capacity-planning
description: Plan infrastructure capacity from measured demand, resource bottlenecks, growth, failure headroom, burst behavior, scaling latency, quotas, and overload policy.
---
# Capacity Planning

Use when deciding how much compute, memory, storage, network, concurrency, or other runtime capacity a workload needs now and under credible growth or failure scenarios.

## Procedure
1. Define the workload unit and service objective: requests, jobs, sessions, agents, data volume, throughput, latency, or another quantity that maps demand to resource use.
2. Establish a measured baseline under representative load. Record resource consumption, utilization distribution, queueing, latency, errors, and the first resource that saturates.
3. Separate steady demand, predictable peaks, burst traffic, batch work, and background load. Use percentiles or distributions when averages hide the real peak.
4. Model growth using explicit assumptions and a time horizon. Keep business-growth assumptions separate from technical resource-per-unit measurements so either can be revised.
5. Include failure headroom. Determine whether remaining capacity can serve the required load when an instance, node, zone, dependency, or other designed failure domain is unavailable.
6. Include scaling latency and constraints: startup/provisioning time, image/model/data warmup, connection limits, quotas, storage expansion, scheduler or placement delay, and maximum practical parallelism.
7. Define overload behavior before capacity is exhausted: admission control, queue limits, backpressure, degraded features, priority classes, rate limits, shedding, or delayed work as appropriate.
8. Set capacity thresholds and forecasting signals that trigger review or scaling before emergency saturation.
9. Revalidate after architecture, workload mix, software efficiency, pricing, or failure assumptions change materially.

## Decision rules
- Capacity plans are measured models, not fixed hardware shopping lists.
- Headroom should correspond to real burst and failure requirements rather than a ritual percentage.
- Scaling is not instantaneous; provisioning and warmup time are part of capacity.
- Under Fleet, publish trustworthy live capacity/pressure signals and hard constraints; Fleet owns which node receives a profile or task.

## Quality gate
The plan is ready when demand maps to measured resource use, credible peaks and failures fit within explicit headroom or degradation policy, scaling constraints are included, overload behavior is defined, and the assumptions can be updated from new measurements.