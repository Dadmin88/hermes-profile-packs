---
name: deployment-topology
description: Design how distributed components may be placed and rolled out across failure domains, networks, state, trust boundaries, heterogeneous nodes, and upgrade cohorts without confusing architecture with live scheduler state.
---
# Deployment Topology

Use when services, workers, control planes, or stateful components can run across multiple hosts, nodes, zones, regions, or device classes.

## Procedure
1. Start from the logical topology and identify which components have placement-sensitive behavior: latency, hardware/runtime requirements, data locality, identity/trust, network reachability, storage attachment, failure isolation, or licensing constraints.
2. Define eligible placement domains and hard constraints separately from preferences. Examples include architecture/OS, accelerator availability, minimum resources, trusted network membership, locality, or anti-affinity.
3. Identify components that may be freely replicated/moved versus those with state ownership, singleton/leader semantics, attached storage, or external identity that makes relocation consequential.
4. Define anti-affinity and redundancy so replicas intended to survive a failure are not accidentally concentrated in the same host/site/provider failure domain.
5. Model communication cost and reachability between placements. Cross-zone/region/device traffic may alter latency, bandwidth, security, or dependency assumptions.
6. Define rollout cohorts and mixed-version compatibility. Decide whether upgrades proceed by node, service, zone, ring, canary group, or another boundary and what versions may coexist.
7. Define drain, handoff, shutdown, and rescheduling behavior for maintenance or failure, including in-flight work and state reconciliation.
8. For Fleet-controlled Hermes nodes, publish profile/workload requirements and topology constraints while keeping live `profile -> nodes` presence and final placement decisions in Fleet's runtime registry.
9. Define observability that can relate logical component identity, version, node identity, and current placement during diagnosis without treating historical placement as static architecture.
10. Validate topology assumptions with a representative failover, relocation, or rolling upgrade across at least one real failure/placement boundary when practical.

## Decision rules
- Architecture defines where a component is allowed or preferred to run; orchestration decides where it runs now.
- Replicas on one host are not host-failure redundancy.
- Stateful relocation requires ownership/data semantics, not just starting another process.
- Heterogeneous fleets should advertise capabilities and constraints rather than pretending every node is interchangeable.

## Quality gate
The deployment topology is ready when eligibility and preference constraints are explicit, redundancy spans the intended failure domains, stateful versus movable components are distinguished, rollout/drain/reschedule behavior is defined, live placement remains an orchestration concern, and relocation or upgrade behavior has been validated against realistic boundaries.