---
name: infrastructure-design
description: Design runtime infrastructure around service requirements, failure domains, identity, networking, storage, capacity, operability, reproducibility, and controlled evolution.
---
# Infrastructure Design

Use when defining or materially reshaping the runtime substrate for applications, services, data, or distributed workers.

## Procedure
1. Start from workload requirements: availability, latency, throughput, durability, security, locality, compliance, operational ownership, and expected growth.
2. Map the current environment and constraints before choosing new infrastructure. Identify compute, network, storage, identity, DNS, secrets, observability, deployment, and external-service dependencies.
3. Define clear failure domains and redundancy boundaries. Decide which failures may be shared and which resources must not fail together.
4. Separate stateless execution, durable state, caches, queues, and control-plane state so their lifecycle and recovery requirements are explicit.
5. Define identity and trust boundaries for users, services, nodes, automation, and administrative access. Hand security-policy decisions to `agency-security-engineer` when they exceed infrastructure implementation authority.
6. Design network paths, ingress/egress, name resolution, service discovery, encryption boundaries, and access controls from the actual traffic flows rather than from a generic diagram.
7. Model capacity and overload behavior. Include headroom, burst characteristics, scaling limits, quotas, backpressure, and what degrades first when demand exceeds supply.
8. Prefer reproducible declarative configuration and immutable or rebuildable components where practical. Make intentional mutable state and manual recovery points obvious.
9. Plan rollout, migration, rollback or forward recovery, monitoring, and validation before changing live infrastructure.
10. Validate risky assumptions with primary documentation, prototypes, failure tests, or measurements appropriate to the environment.

## Decision rules
- Infrastructure design should expose useful health and capacity signals to orchestration without embedding placement policy into the workload package.
- Do not centralize unrelated failure domains merely for administrative convenience.
- Avoid introducing a managed service, cluster, or control plane unless its operational value exceeds the complexity it adds.
- Design for the real workload and credible growth, not hypothetical internet scale.

## Quality gate
The design is ready when workload requirements map to explicit runtime components and failure domains, identity/network/storage/capacity behavior is understandable, infrastructure can be reproduced and operated, rollout and recovery are credible, and the hardest assumptions have evidence behind them.