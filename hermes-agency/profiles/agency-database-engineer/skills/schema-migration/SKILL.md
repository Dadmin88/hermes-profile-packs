---
name: schema-migration
description: Design and execute a database schema migration with compatibility, locking, data backfill, validation, rollback or forward recovery, and deployment sequencing.
---
# Schema Migration

Use when changing persistent database structure or data representation.

## Procedure
1. Inspect current schema, indexes, constraints, data volume/distribution, query patterns, and application compatibility.
2. Decide whether the change can be additive or requires a staged expand/migrate/contract sequence.
3. Evaluate lock duration, table rewrite, replication, storage, and performance impact for the database in use.
4. Separate schema change from data backfill when doing so reduces risk.
5. Make application versions compatible across the deployment window where rolling deploys are possible.
6. Validate counts, constraints, sampled data, and query behavior after migration.
7. Define rollback when safe, or forward-recovery steps when reversal would lose data.

## Quality gate
Never rely on a migration being 'quick' without considering real data size and engine behavior. The deployment sequence and recovery path must be explicit.