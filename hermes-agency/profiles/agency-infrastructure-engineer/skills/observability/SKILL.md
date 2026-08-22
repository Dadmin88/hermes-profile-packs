---
name: observability
description: Design infrastructure observability that answers operational questions across compute, network, storage, runtime, dependencies, saturation, failures, and recovery without collecting noise for its own sake.
---
# Infrastructure Observability

Use when infrastructure health, performance, failure, or capacity cannot be understood reliably from existing telemetry.

## Procedure
1. List the operational questions responders must answer: is the service reachable, what failed, where is the bottleneck, what changed, what is saturated, and what user-visible behavior is affected?
2. Map the runtime path across hosts, containers or processes, network, DNS, load balancing, storage, queues, and critical external dependencies.
3. Choose signals that represent behavior and resource pressure: availability, latency, errors, throughput, queue age/depth, CPU, memory, disk, I/O, network, connection pools, file descriptors, and other workload-specific saturation indicators.
4. Preserve correlation across boundaries using timestamps, request/job identifiers, node or instance identity, deployment revision, and other stable dimensions that help trace one event through the system.
5. Define logs as structured diagnostic evidence rather than a transcript of everything. Keep secrets, credentials, and unnecessary sensitive data out of telemetry.
6. Build dashboards around decisions and failure modes, not around whatever metrics happen to exist. Separate service-level outcomes from lower-level resource signals.
7. Alert on actionable symptoms or leading indicators with clear ownership and enough context to start diagnosis. Avoid alerts that fire continuously without a response action.
8. Define retention, cardinality, sampling, cost, and access controls so telemetry remains usable at scale.
9. Test observability during representative failures and deployments. Confirm responders can locate the failing layer without privileged guesswork.

## Decision rules
- Telemetry is valuable when it reduces uncertainty during operation, capacity planning, or incident response.
- Infrastructure metrics do not replace application-level outcome signals, and application metrics do not replace host/network/storage evidence.
- Prefer a smaller set of trustworthy correlated signals over large dashboards of unowned data.
- When a Fleet manages nodes, expose node health and resource signals in a machine-consumable form but leave scheduling decisions to Fleet.

## Quality gate
Observability is sufficient when responders can connect user-visible symptoms to the responsible infrastructure layer, identify saturation and recent change, trace important flows, act on alerts, and do so without leaking sensitive information or depending on one operator's memory.