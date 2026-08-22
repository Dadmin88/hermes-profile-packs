---
name: backup-recovery
description: Design and prove database backup recovery around consistency, recovery point/time objectives, encryption, retention, corruption/deletion scenarios, point-in-time recovery, and tested restoration.
---
# Database Backup and Recovery

Use when persistent database state must be recoverable after data loss, corruption, operator error, infrastructure failure, or compromise.

## Procedure
1. Define which database/data is protected, its durability criticality, and the required recovery point and recovery time objectives.
2. Identify failure scenarios: accidental deletion, bad migration, logical corruption, storage loss, database/cluster loss, credential/control-plane loss, ransomware/compromise, and region/site loss as relevant.
3. Choose backup mechanisms supported by the engine that can produce a transactionally consistent recoverable state: physical snapshots/backups, logical dumps, log/WAL/binlog archiving, replicas, or combinations appropriate to the objective.
4. Keep recoverable copies isolated from the failure domain and credentials that can destroy the primary. Define encryption, key recovery, retention, immutability/deletion protection, and access auditing where needed.
5. For point-in-time recovery, ensure the base backup plus required transaction logs are complete and retention covers the intended window.
6. Document exact restore prerequisites: engine/version compatibility, extensions/plugins, configuration, keys, storage, network, users/roles, and application sequencing.
7. Perform restoration into an isolated environment. Verify the database starts cleanly, schemas/constraints exist, representative records and counts reconcile, application queries work, and the restored point matches the claimed objective.
8. Measure actual restore duration and identify bottlenecks such as download, decompression, replay, index rebuild, replica catch-up, or application reconciliation.
9. Test targeted recovery for common operator mistakes separately from full disaster recovery when a narrower restore can reduce impact.
10. Record backup health and restore evidence continuously enough that a successful scheduled backup job is not mistaken for proven recoverability.

## Decision rules
- Replication is not a backup against logical deletion/corruption when the bad change replicates.
- Backups without restore tests are unverified.
- Recovery credentials/keys are part of the backup system and need their own recoverability.
- Database recovery feeds broader disaster recovery, but `agency-infrastructure-engineer` owns rebuilding surrounding runtime infrastructure.

## Quality gate
Recovery is credible when backup artifacts and transaction history cover the stated objective, copies survive the modeled failure domain, required keys/config are recoverable, an isolated restore has been completed and reconciled, actual RPO/RTO evidence is known, and failures in the backup process are observable and owned.