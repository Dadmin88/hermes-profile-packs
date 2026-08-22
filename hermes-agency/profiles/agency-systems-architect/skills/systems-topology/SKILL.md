---
name: systems-topology
description: Model a system's logical and physical topology across services, nodes, networks, state, control planes, trust boundaries, failure domains, dependencies, and communication paths.
---
# Systems Topology

Use when a multi-service or multi-node system needs an accurate map before architecture, reliability, security, migration, or capacity decisions can be made.

## Procedure
1. Define the system boundary and the user/system outcomes it exists to provide. Mark external actors and dependencies explicitly.
2. Inventory runtime components and responsibilities: services, workers, data stores, queues, gateways, control planes, node agents, schedulers/orchestrators, caches, observability, and external systems as relevant.
3. Map state ownership and persistence separately from compute placement. Identify authoritative stores, replicated/cached state, ephemeral state, and control-plane state.
4. Map communication paths with protocol, direction, identity, discovery/addressing, authentication, authorization, encryption boundary, and expected latency/availability needs.
5. Mark trust boundaries, administrative boundaries, tenancy boundaries, and credentials or authority that cross them.
6. Mark physical/logical failure domains: process, host, node, rack/site/zone/region, provider, network, storage, shared dependency, and control-plane concentration as applicable.
7. Distinguish desired topology from live placement. In Fleet-managed systems, Fleet's registry owns current node/workload presence while the architecture documents allowed roles, constraints, and relationships.
8. Record scale and cardinality where topology changes behavior, such as N nodes, many tenants, leader/follower sets, sharded partitions, or fan-out relationships.
9. Validate the topology against deployment/configuration/runtime evidence rather than relying only on outdated diagrams.

## Decision rules
- A topology diagram is useful only if its boundaries and arrows have defined semantics.
- Do not mix “where a component may run” with “where it happens to run right now.”
- Shared dependencies belong in the topology because they create shared failure domains.
- State/control-plane components deserve explicit treatment even when they are small in code size.

## Quality gate
The topology is ready when components, state, communication, trust, failure domains, and external dependencies are explicit; live placement is distinguished from architectural constraints; and another specialist can use the model to reason about failure, capacity, security, or evolution without discovering major hidden components.