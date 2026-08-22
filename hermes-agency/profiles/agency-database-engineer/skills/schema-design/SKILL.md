---
name: schema-design
description: Design transactional database schemas around domain invariants, access patterns, keys, constraints, relationships, lifecycle, engine semantics, and safe evolution without cargo-cult rules.
---
# Schema Design

Use when persistent application data needs a new or materially changed relational/document/key-value representation.

## Procedure
1. Define the domain facts and invariants the database must preserve, plus the read/write/query patterns that will operate on them.
2. Choose the data model and database features based on those requirements and the engine actually in use. Do not force relational, document, or distributed patterns onto workloads that do not need them.
3. Define identifiers/keys, relationships, ownership, optionality, lifecycle, and deletion behavior. Choose key types for real interoperability, locality, generation, and scale needs rather than one universal rule.
4. Encode important invariants with database constraints or transactional operations where the engine can enforce them reliably: uniqueness, foreign/reference integrity, checks, required values, and valid state relations.
5. Normalize repeated facts enough to prevent contradictory sources of truth, then denormalize deliberately when measured read/performance/availability requirements justify the maintenance cost.
6. Model temporal data, precision, units, collation/case, time zones, JSON/blob content, and enum/state representation explicitly where mistakes would change meaning.
7. Consider concurrency and transaction boundaries during schema design. Tables/collections that must change atomically or contend heavily need an intentional consistency strategy.
8. Design indexes alongside real access patterns, but keep index selection distinct from logical schema correctness so performance tuning can evolve.
9. Plan schema evolution and compatibility before the first deployment when the data will outlive one application version.
10. Validate the design with representative records, invariant tests, expected queries, update/delete behavior, and engine-specific documentation for uncertain semantics.

## Decision rules
- Database schemas encode durable meaning; framework/ORM defaults are not the authority.
- Avoid universal prescriptions such as every ID must be a UUID or every table must have the same timestamp columns; choose what the domain and engine require.
- Constraints are valuable when they protect real invariants and are compatible with operational/migration needs.
- Analytical warehouse modeling belongs to `agency-data-engineer`; this skill owns operational/transactional persistence design.

## Quality gate
The schema is ready when durable facts and invariants have clear representation and ownership, key/relationship/lifecycle semantics are explicit, the engine can enforce the required consistency, common operations are viable, evolution is considered, and representative data plus queries validate the design without relying on ORM magic.