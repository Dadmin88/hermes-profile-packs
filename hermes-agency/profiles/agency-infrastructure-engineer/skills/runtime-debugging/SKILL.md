---
name: runtime-debugging
description: Diagnose infrastructure/runtime failures by tracing evidence across process, container, host, network, storage, resource pressure, configuration, dependency, and deployment layers.
---
# Runtime Debugging

Use when an application or worker is unhealthy but the failing runtime or infrastructure layer is not yet known.

## Procedure
1. Capture the symptom and scope precisely: affected service/profile, node or environment, first occurrence, deployment revision, user-visible impact, frequency, and whether the problem follows workload, node, or time.
2. Establish current health and recent change before restarting anything. Preserve logs, events, metrics, process state, resource pressure, and identifiers that may disappear after recovery actions.
3. Trace the runtime stack from the workload outward: application process, supervisor/container, host kernel/resources, filesystem/storage, network/DNS/TLS, service discovery/load balancing, and external dependencies.
4. Check resource exhaustion and limits explicitly: memory pressure/OOM, CPU throttling, disk space/inodes/I/O, file descriptors, process/thread limits, sockets/connections, quotas, and queue saturation as relevant.
5. Compare failing and healthy instances or nodes when possible. Differences in config, revision, runtime version, permissions, network path, mounted state, clock, or resource pressure often narrow the fault quickly.
6. Form a hypothesis that predicts observable evidence and test the narrowest layer first. Avoid changing multiple infrastructure variables simultaneously.
7. Distinguish a workaround from a root-cause repair. Restarting or moving a workload may restore service while leaving the defect unexplained; capture that distinction.
8. Apply the smallest safe correction at the owning layer and preserve rollback/recovery options.
9. Reproduce or validate the original path after the fix, then check restart/redeploy behavior and adjacent nodes or instances for the same condition.
10. Record root cause, triggering conditions, evidence, remediation, monitoring or guardrail changes, and whether another specialty owns the underlying defect.

## Decision rules
- Do not reboot first and investigate later when evidence can be collected safely.
- Application errors can be infrastructure symptoms, and infrastructure alarms can be consequences of application behavior; follow evidence across the boundary.
- If Fleet moves a failed task/profile to another node, treat successful relocation as availability recovery, not proof the original node is healthy.
- Escalate software defects to the implementation owner with the runtime evidence intact.

## Quality gate
The incident is understood when evidence identifies the failing layer and triggering condition, the correction addresses that cause or a deliberate containment is recorded, service behavior is revalidated, recurrence detection or prevention is improved, and any node returned to service has actually passed health checks.