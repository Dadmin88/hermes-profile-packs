---
name: capacity-model
description: Build a system-level capacity model that connects workload demand to bottlenecks across services, nodes, queues, storage, network, shared dependencies, redundancy, and placement constraints.
---
# Capacity Model

Use when a distributed or multi-service architecture needs quantitative reasoning about scale, bottlenecks, headroom, or resource placement.

## Procedure
1. Define the workload dimensions that drive the system: active users, requests, jobs, agents, objects, bytes, event rate, model invocations, concurrency, or another meaningful demand unit.
2. Map each unit of demand through the topology and identify resource consumption or amplification at every major boundary, including fan-out, retries, replication, indexing, background work, and shared services.
3. Use measured service/resource data where available. Separate observed coefficients from estimates and label confidence on uncertain assumptions.
4. Identify the constraining resource for each scale regime: CPU, memory, GPU/accelerator, disk capacity/I/O, network, connections, queue throughput, database locks, provider quotas, control-plane rate, or human operation as relevant.
5. Model peak/burst behavior and queueing, not only average throughput. Include how long bursts can be buffered and the latency or failure consequence of backlog growth.
6. Include redundancy and failure headroom. Capacity required to survive designed node/zone/service loss is different from capacity when everything is healthy.
7. Include placement constraints and heterogeneity. For Fleet-managed nodes, distinguish hard capability requirements from live free capacity so Fleet can match profiles/tasks to eligible nodes.
8. Define scaling thresholds, provisioning latency, maximum practical scale, and the next architectural breakpoint where simply adding instances stops helping.
9. Validate the model with load tests, production telemetry, or representative benchmarks and recalibrate when observed behavior diverges.
10. Present assumptions, formulas, bottlenecks, headroom, and sensitivity so another engineer can update the model rather than treating one forecast number as truth.

## Decision rules
- System capacity is constrained by the tightest shared bottleneck, not by the sum of advertised machine resources.
- Retry and fan-out amplification belong in the model because failure can increase load.
- Heterogeneous nodes require capability-aware capacity accounting rather than one generic “worker slot.”
- Prefer ranges and sensitivity analysis when inputs are uncertain.

## Quality gate
The model is useful when demand maps quantitatively through the topology, bottlenecks and amplification are visible, failure headroom and placement constraints are included, scaling limits are explicit, and measurements can confirm or revise the assumptions.