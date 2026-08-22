---
name: schema-evolution
description: Evolve analytical or pipeline data schemas without silently breaking producers, consumers, historical data, lineage, or mixed-version processing.
---
# Schema Evolution

Use when source, event, warehouse, lake, or pipeline data contracts change over time.

## Procedure
1. Identify schema ownership, producers, consumers, storage formats, historical partitions, generated models, and compatibility expectations before changing fields.
2. Compare the old and proposed contract across names, types, nullability, defaults, units, enums, identifiers, nested structures, and semantic meaning.
3. Prefer additive compatible change when it preserves the intended semantics, but verify consumers can tolerate unknown fields, new enum values, nulls, or changed sparsity.
4. Define the mixed-version window: old producers with new consumers, new producers with old consumers, replayed historical data, and partially migrated partitions.
5. Version the contract or metadata when consumers need an explicit compatibility boundary. Do not use version numbers as a substitute for migration behavior.
6. Plan transformations for historical data separately from live ingestion. Decide whether old data is interpreted in place, lazily adapted, or physically backfilled.
7. Update validation, catalogs, lineage, tests, documentation, and downstream models together with the schema.
8. Add compatibility tests or representative fixtures that exercise old/new records across the consumers most likely to break.
9. Monitor post-change parse failures, null/default changes, volume shifts, and downstream quality metrics for evidence of semantic breakage.

## Decision rules
- Type compatibility does not guarantee semantic compatibility.
- Historical/replayed data remains part of the contract unless explicitly retired.
- Avoid destructive field reuse; a field name with new meaning is usually a new contract.
- Database physical-schema decisions belong to `agency-database-engineer` when the primary concern is engine/storage behavior rather than data-pipeline contracts.

## Quality gate
Evolution is ready when producers and consumers have a defined compatibility path, historical data remains interpretable or has a migration plan, validation and lineage reflect the new contract, representative mixed-version cases pass, and post-change signals can detect silent semantic regressions.