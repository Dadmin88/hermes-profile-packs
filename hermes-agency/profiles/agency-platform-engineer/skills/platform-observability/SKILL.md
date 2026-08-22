---
name: platform-observability
description: Make an internal platform observable from the consumer and operator perspectives by connecting platform requests, provisioning, policy, runtime health, dependencies, errors, and adoption signals.
---
# Platform Observability

Use when a shared platform must be diagnosable across both its control surface and the workloads or capabilities it provides.

## Procedure
1. Identify the platform's critical consumer journeys: provision, configure, deploy, access, update, observe, recover, and delete as relevant.
2. Define outcome signals for those journeys: success rate, latency, queue/wait time, error class, policy denial, resource readiness, and time to usable result.
3. Instrument the platform control path separately from managed workload health so an operator can distinguish “the platform cannot provision” from “the provisioned service is unhealthy.”
4. Carry stable correlation identifiers across API/CLI/UI requests, automation, queues, infrastructure actions, and resulting resources where practical.
5. Expose actionable status to consumers. Avoid a black box that reports only “failed” when the user needs to know whether input, policy, quota, dependency, or platform operation caused the failure.
6. Monitor platform dependencies, queues, controller loops, reconcile lag, capacity/quota pressure, certificate/credential lifecycle, and other mechanisms that can make desired and actual state diverge.
7. Track adoption and bypass signals alongside reliability: active consumers, successful self-service operations, support/escalation volume, abandoned workflows, and recurring manual interventions.
8. Define operator alerts and runbooks around symptoms that require action rather than every internal exception.
9. Test observability with injected or staged failures in representative platform workflows and verify consumer-facing status matches operator evidence.

## Decision rules
- Consumer-visible success is the primary platform outcome; internal controller activity is supporting evidence.
- A shared platform needs both reliability telemetry and product/adoption telemetry.
- Do not expose sensitive infrastructure details to consumers merely to make errors verbose.
- If Fleet is the placement/control plane, platform telemetry may feed Fleet health/capacity decisions but should not create a competing placement registry.

## Quality gate
Platform observability is ready when operators can trace a consumer request through the platform, consumers receive useful non-sensitive status, control-plane failures are separable from workload failures, actionable alerts exist, and adoption/support data reveals whether the platform is actually serving its users.