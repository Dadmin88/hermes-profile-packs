---
name: incident-analysis
description: Analyze a security incident from detection through containment, evidence preservation, scope, timeline, root cause, credential and data impact, remediation, validation, and durable prevention.
---
# Incident Analysis

Use when a compromise, suspicious access, credential exposure, malicious dependency, data disclosure, privilege abuse, or other security event needs structured technical investigation.

## Procedure
1. Establish the incident owner, current severity, affected environment, known facts, unknowns, and immediate safety constraints. Separate verified evidence from hypotheses from the first note onward.
2. Contain active harm without destroying evidence needed to understand scope. Actions may include disabling exposed credentials, isolating a service or workload, blocking a malicious path, or pausing a vulnerable integration while preserving relevant logs and artifacts.
3. Preserve evidence with timestamps and provenance: logs, alerts, cloud/audit events, authentication events, affected binaries or packages, configuration, relevant snapshots, hashes, deployment/version identifiers, and copies of volatile data when appropriate and authorized.
4. Build a timeline from the earliest known precursor through detection, attacker or failure actions, defender actions, containment, and recovery. Normalize time zones and distinguish event time from ingestion/report time.
5. Determine entry vector and first unauthorized capability gained. Then trace privilege changes, lateral movement, persistence, credential access, data access/exfiltration, destructive actions, and affected downstream systems based on evidence rather than assumptions.
6. Scope affected identities, tenants, records, hosts, workloads, repositories, credentials, dependencies, and time windows. Revisit scope as new evidence appears; do not freeze the original alert's boundaries if the incident expanded beyond them.
7. Identify root cause and contributing controls: the technical defect or compromise path, why preventive controls did not stop it, why detective controls did or did not surface it quickly, and which operational assumptions amplified impact.
8. Remediate in dependency order. Revoke/rotate compromised credentials, remove persistence, patch or remove the vulnerable component, repair authorization or configuration, restore trusted artifacts/data, and validate that recovery does not reintroduce the cause.
9. Verify containment and recovery using independent evidence: clean authentication/activity patterns, expected deployment hashes/versions, closed exploit path, rotated credentials, corrected controls, and monitoring for recurrence.
10. Produce an incident record with timeline, impact, evidence, root cause, containment, remediation, remaining uncertainty, follow-up owners, and prevention/detection improvements. Keep sensitive investigative material appropriately restricted.

## Decision rules
- Containment and evidence preservation must be balanced deliberately; neither "keep everything running" nor "wipe it immediately" is a universal answer.
- Rotate or revoke exposed credentials before spending time hiding them from source history or screenshots.
- Do not overstate attribution. Explain what the evidence proves about actions and access separately from who you think performed them.
- A post-incident review should improve systems and controls, not become a blame document.
- Legal, privacy, regulatory, customer-notification, or law-enforcement decisions belong with the appropriate organizational authority; provide technical evidence without inventing those obligations.

## Quality gate
The analysis is complete when active harm is contained, evidence and timeline support the scoped impact and root cause, compromised trust has been re-established rather than assumed, remediation is independently validated, uncertainty is explicit, and prevention/detection follow-ups have owners.