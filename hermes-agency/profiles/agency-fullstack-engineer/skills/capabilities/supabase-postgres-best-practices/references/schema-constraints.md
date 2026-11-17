---
title: Add Constraints Safely in Migrations
impact: HIGH
impactDescription: Prevents migration failures and enables idempotent schema changes
tags: constraints, migrations, schema, alter-table
---

## Add Constraints Safely in Migrations

PostgreSQL does not support `ADD CONSTRAINT IF NOT EXISTS`. Migrations using this syntax will fail.

**Incorrect (causes syntax error):**

```sql
-- ERROR: syntax error at or near "not" (SQLSTATE 42601)
alter table public.profiles
add constraint if not exists profiles_birthchart_id_unique unique (birthchart_id);
```

**Correct (idempotent constraint creation):**

```sql
-- Use DO block to check before adding
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conname = 'profiles_birthchart_id_unique'
    and conrelid = 'public.profiles'::regclass
  ) then
    alter table public.profiles
    add constraint profiles_birthchart_id_unique unique (birthchart_id);
  end if;
end $$;
```

Use the migration runner's normal serialization and version checks. An existing name does not prove the constraint has the expected definition. Inspect `pg_get_constraintdef` on the correct relation and compare it before treating a migration as satisfied.

Reference: [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
