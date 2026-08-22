---
name: warehouse-modeling
description: Model analytical warehouse data around business grain, dimensions, facts, history, keys, measures, semantic consistency, performance, and consumer-ready contracts.
---
# Warehouse Modeling

Use when raw or staged data must become durable analytical models for reporting, metrics, exploration, or downstream data products.

## Procedure
1. Start from business questions and define the grain of each model in one precise sentence before selecting columns or joins.
2. Identify facts/events, dimensions/entities, measures, descriptive attributes, and relationships. Keep each fact at a consistent grain to avoid accidental double counting.
3. Define keys deliberately: source/natural identifiers, warehouse surrogate keys where useful, uniqueness, late-arriving references, and how unknown/missing dimension values are represented.
4. Decide how history is modeled for mutable dimensions and facts. Preserve only the history consumers need and make valid-time/recorded-time semantics explicit when temporal analysis matters.
5. Define measures and units with aggregation behavior. Distinguish additive, semi-additive, non-additive, derived, and snapshot metrics so consumers do not sum values incorrectly.
6. Centralize important business definitions in reusable semantic models rather than allowing every dashboard/query to reinterpret the same concept independently.
7. Design incremental loading, partitioning/clustering/indexing, and materialization based on actual engine/query patterns without sacrificing correctness for premature optimization.
8. Add tests for grain uniqueness, referential relationships, accepted values, nullability, metric invariants, and reconciliation against authoritative sources.
9. Document lineage and ownership from source through transformations to exposed models/metrics, including freshness and known limitations.
10. Validate representative consumer queries for both correctness and acceptable performance before declaring the model production-ready.

## Decision rules
- Grain is the primary contract; ambiguous grain creates misleading metrics.
- Do not denormalize merely because “warehouses should be star schemas”; choose structures that fit the engine and consumer workload while preserving semantic clarity.
- Metric definitions should have one authoritative semantic home even if physically materialized in several places.
- Warehouse models serve analytical consumers; transactional schema design remains `agency-database-engineer` territory.

## Quality gate
The model is ready when grain, keys, history, measures, and semantic definitions are explicit, reconciliation and data-quality tests pass, lineage/ownership are visible, representative queries return correct results without accidental duplication, and consumers can use the model without recreating business logic privately.