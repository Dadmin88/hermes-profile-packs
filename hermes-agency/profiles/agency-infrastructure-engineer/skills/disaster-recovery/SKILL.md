---
name: disaster-recovery
description: Design and validate disaster recovery around business recovery objectives, durable data, dependency restoration, rebuildability, access, runbooks, and tested recovery evidence.
---
# Disaster Recovery

Use when infrastructure or data must be recoverable after destructive failure, region/site loss, operator error, corruption, compromise, or prolonged dependency outage.

## Procedure
1. Define the protected services/data and the business consequence of losing each. Set explicit recovery time and recovery point objectives where they are meaningful.
2. Enumerate disaster scenarios that exceed ordinary high availability: full environment loss, storage corruption, accidental deletion, credential/control-plane loss, dependency outage, and compromise as relevant.
3. Inventory every prerequisite needed to recover: source/configuration, artifacts/images, infrastructure definitions, secrets/keys, DNS, identity, data backups, external accounts, licenses, and human access.
4. Design backup and replication around the recovery objective. Separate backup copies from the failure domain they protect and define retention, immutability or deletion protection when justified.
5. Define restoration order and dependency graph. Restore control/identity/network/data/service layers in an order that can actually produce a working system.
6. Plan bootstrap access for the case where normal identity, DNS, or management systems are themselves unavailable, without creating an ungoverned permanent bypass.
7. Write a runbook with decision points, exact evidence to verify each stage, ownership, communications, and criteria for failback or continued operation in recovery mode.
8. Test restoration, not only backup creation. Run tabletop exercises for broad scenarios and periodic technical recovery drills for the systems whose objectives matter.
9. Measure actual recovery time, recovered data point, missing prerequisites, manual steps, and defects found during drills; feed them back into design.
10. Revisit the plan after topology, data stores, identity, deployment, external dependencies, or business recovery requirements change.

## Decision rules
- Replication is not automatically a backup; corruption and deletion can replicate too.
- A backup that has never been restored is an unverified hypothesis.
- Recovery documentation must remain available when the primary environment is not.
- High availability handles expected component failure; disaster recovery covers loss beyond the normal availability design.

## Quality gate
Recovery is credible when required data and infrastructure can be reconstructed from failure-isolated sources, dependencies and access paths are accounted for, a documented restoration sequence exists, drills demonstrate the stated objectives or expose quantified gaps, and ownership for closing those gaps is explicit.