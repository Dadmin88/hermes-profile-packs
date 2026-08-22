---
name: data-pipeline-design
description: Design or implement a data pipeline with source contracts, schema, transformations, quality checks, idempotency, lineage, backfills, and operational recovery.
---
# Data Pipeline Design

Use for ingestion, ETL/ELT, event pipelines, analytical datasets, or recurring data transformations.

## Procedure
1. Define source ownership, extraction method, freshness, volume, schema, and reliability expectations.
2. Establish the target data contract and transformation rules with explicit types and keys.
3. Design incremental processing, idempotency, deduplication, late-arriving data, and schema evolution.
4. Add quality checks for completeness, uniqueness, validity, referential integrity, and business invariants as appropriate.
5. Plan backfills and reprocessing so historical correction is possible.
6. Preserve lineage and metadata needed to trace a bad output to source inputs and code/version.
7. Add observability for freshness, failures, volume anomalies, and quality regressions.

## Quality gate
A pipeline is production-ready when it can be rerun and recovered without silently duplicating, dropping, or corrupting data.