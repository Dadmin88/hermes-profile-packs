---
name: supabase-postgres-best-practices
description: Review PostgreSQL schema changes, migrations, access boundaries, transactions, query plans, and indexes for a full-stack feature.
version: 1.1.1
author: Supabase
license: MIT
---

# Supabase Postgres best practices

Apply the relevant PostgreSQL rules whenever a feature changes schemas, migrations, transaction boundaries, queries, or permissions. These rules apply to PostgreSQL regardless of hosting provider.

1. Identify the PostgreSQL version, project migration runner, target role, table size, and how old and new app versions overlap during rollout. Use the project's disposable database and representative synthetic fixtures.
2. Inspect existing data and dependencies before adding constraints or indexes. Plan locks, backfill batches, retries, compatibility and a recovery path. Verify both fresh install and upgrade from the previous schema.
3. Exercise reads and writes as the app's database role. Where row-level security applies, verify both access and denial across users or tenants. Use the project's established, trusted identity binding. A client-writable session setting alone cannot establish identity.
4. Keep transactions short and use consistent lock order. Verify concurrent requests, uniqueness, and repeat submissions at the boundary that owns the invariant.
5. Compare plans before and after index or query changes using representative data. Start with plain `EXPLAIN`. Use `EXPLAIN (ANALYZE, BUFFERS)` only where actually executing the statement is acceptable. Run application and migration checks against the approved dev/test target. Record the plan, fixtures, and any production rollout steps needing separate authorization.

## Reference rules

- [Constraints](references/schema-constraints.md), [data types](references/schema-data-types.md), and [foreign key indexes](references/schema-foreign-key-indexes.md).
- [Short transactions](references/lock-short-transactions.md), [consistent lock ordering](references/lock-deadlock-prevention.md), and [atomic upserts](references/data-upsert.md).
- [Cursor pagination](references/data-pagination.md), [composite indexes](references/query-composite-indexes.md), and [query plans](references/monitor-explain-analyze.md).

SQL examples explain patterns. Adapt names and types to the project. Keep the migration runner in charge of migration history and scope all SQL to the identified test database.
