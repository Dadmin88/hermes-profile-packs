---
name: incident-coordination
description: Coordinate an operational incident by establishing command, impact, workstreams, communication, decision cadence, evidence, and recovery ownership without replacing the technical responders.
---
# Incident Coordination

Use when an incident spans multiple responders or functions and coordination quality materially affects recovery.

## Procedure
1. Establish the incident scope, current impact, start time, affected users/services, and severity using the organization's actual criteria.
2. Name an incident coordinator and technical/domain owners; keep command and hands-on diagnosis distinct when scale warrants it.
3. Create a durable timeline and shared state for observations, decisions, actions, owners, and status.
4. Split independent workstreams such as mitigation, diagnosis, customer communication, vendor escalation, security review, or recovery validation without duplicating effort.
5. Set a communication cadence appropriate to impact and uncertainty and record what is confirmed versus suspected.
6. Protect responders from unrelated requests and route consequential changes through explicit ownership.
7. Track mitigation, service restoration, data integrity, backlog/replay, and validation separately so partial recovery is not mistaken for closure.
8. After stabilization, hand root-cause analysis and corrective actions to the appropriate owners with the incident evidence intact.

## Decision rules
- Coordination should reduce responder load, not add status bureaucracy.
- Restored availability does not automatically prove correctness or data integrity.
- Do not let incident urgency erase security or recovery boundaries unnecessarily.
- Fleet may reroute workloads during a node failure; successful failover is mitigation evidence, not root cause.

## Quality gate
The incident is coordinated effectively when ownership and workstreams are clear, current impact and evidence are visible, communications are accurate, recovery is validated, and post-incident owners receive a complete timeline and unresolved risks.