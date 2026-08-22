---
name: systems-design
description: Design a multi-service or distributed system around responsibilities, protocols, topology, identity, consistency, failure, capacity, observability, and evolution.
---
# Systems Design

Use for architectures that span services, machines, networks, queues, distributed state, or operational domains.

## Procedure
1. Define system outcomes, environment, actors, scale, latency, availability, durability, and security constraints.
2. Partition responsibilities and state ownership before selecting technologies.
3. Define protocols, addressing/discovery, identity, authorization, message/data contracts, and versioning.
4. Choose consistency and coordination semantics explicitly; identify what happens during partition, retry, duplicate delivery, and partial failure.
5. Model capacity, backpressure, resource limits, queues, overload behavior, and recovery.
6. Design observability around boundaries and end-to-end flows.
7. Define deployment/evolution strategy so nodes or services can change without requiring impossible lockstep upgrades where practical.
8. Test the hardest failure and scaling assumptions with prototypes or evidence.

## Quality gate
The design should explain how the system behaves when parts fail, not only when every component is healthy.