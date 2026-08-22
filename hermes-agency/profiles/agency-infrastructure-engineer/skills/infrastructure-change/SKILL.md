---
name: infrastructure-change
description: Plan and execute an infrastructure change with current-state discovery, blast-radius control, reproducibility, observability, validation, and recovery.
---
# Infrastructure Change

Use for cloud, host, networking, container, service, DNS, storage, or infrastructure-as-code changes.

## Procedure
1. Inspect the real current state, configuration source, dependencies, ownership, and environment before proposing changes.
2. Define desired state and the exact operational problem being solved.
3. Identify blast radius, privileges, network paths, data durability, capacity, and external dependencies.
4. Prefer declarative/reproducible changes when infrastructure is managed as code; avoid manual drift.
5. Stage or sequence high-risk changes so health can be checked before expanding impact.
6. Preserve access and recovery paths for changes affecting networking, authentication, or host management.
7. Validate service health, logs/metrics, connectivity, persistence, and restart behavior after change.
8. Record rollback or forward-recovery steps and the resulting state.

## Quality gate
Infrastructure is not done because a command returned zero. The intended service behavior must be verified from the outside.