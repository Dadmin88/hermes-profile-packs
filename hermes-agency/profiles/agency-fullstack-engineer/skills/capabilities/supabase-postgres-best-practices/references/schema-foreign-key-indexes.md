---
title: Index Foreign Key Columns
impact: HIGH
impactDescription: 10-100x faster JOINs and CASCADE operations
tags: foreign-key, indexes, joins, schema
---

## Index Foreign Key Columns

Postgres does not automatically index foreign key columns. Missing indexes cause slow JOINs and CASCADE operations.

**Incorrect (unindexed foreign key):**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- No index on customer_id!
-- Lookups and cascading deletes may scan this table
select * from orders where customer_id = 123;  -- Seq Scan
delete from customers where id = 123;          -- Locks table, scans all orders
```

**Correct (indexed foreign key):**

```sql
create table orders (
  id bigint generated always as identity primary key,
  customer_id bigint references customers(id) on delete cascade,
  total numeric(10,2)
);

-- Add an index when the actual lookup or referential checks warrant it
create index orders_customer_id_idx on orders (customer_id);

-- Now JOINs and cascades are fast
select * from orders where customer_id = 123;  -- Index Scan
delete from customers where id = 123;          -- Uses index, fast cascade
```

Check existing indexes first, including the leading columns of composite indexes.

Reference: [Foreign Keys](https://www.postgresql.org/docs/current/ddl-constraints.html#DDL-CONSTRAINTS-FK)
