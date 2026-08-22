---
name: fault-tolerance
description: Design and test fault tolerance by defining expected faults, containment boundaries, detection, failover, retry/replay semantics, state reconciliation, and safe recovery after partial failure.
---
# Fault Tolerance

Use when a system must continue useful work or recover predictably despite component, node, dependency, or communication failures.

## Procedure
1. Enumerate faults within scope: process crash, node loss, dependency timeout, partition, stale membership, storage unavailability, corrupted/invalid data, queue outage, credential expiry, overload, or operator error as relevant.
2. Define the desired response for each fault: mask transparently, fail over, retry, degrade, queue, reject, isolate, require operator intervention, or stop safely.
3. Establish containment boundaries so one faulty component cannot consume unbounded resources, spread corrupted state, or cascade through unrelated workloads.
4. Define failure detection and its uncertainty. Health checks, leases, heartbeats, timeouts, and suspicion windows can produce false positives or stale views; state what actions are safe under uncertainty.
5. Make retry/replay and failover semantics compatible with side effects. Use idempotency, fencing, version checks, reconciliation, or compensation where duplicate/late execution can occur.
6. Protect state during failover. Define ownership transfer, leader/primary transitions, split-brain prevention, stale writers, and what data may be lost or require reconciliation.
7. Bound recovery work. Thundering-herd reconnects, mass retries, cache refill, or task rescheduling should not turn one failure into sustained overload.
8. Define return-to-service criteria for recovered nodes/components and how stale local state is refreshed before they receive normal work.
9. Test faults intentionally in representative environments and verify both service behavior and operational visibility, including repeated or combined failures that are plausible.
10. Record residual faults the design does not tolerate and the operator response required when they occur.

## Decision rules
- Failover without fencing or state ownership can create a second writer instead of recovery.
- Health detection is not perfect truth; pair detection thresholds with actions safe for that confidence level.
- Tolerance should match consequence and probability; not every component needs seamless redundancy.
- In Fleet, rescheduling a task after node loss must respect the task's side-effect/idempotency semantics and the profile readiness of the replacement node.

## Quality gate
Fault tolerance is credible when expected faults have explicit containment and response, duplicate/late execution cannot silently corrupt state, failover preserves ownership guarantees, recovery work is bounded, recovered components meet return-to-service criteria, and fault tests demonstrate the intended behavior.