---
name: dashboard-spec
description: Specify an analytics dashboard around decisions, metric definitions, dimensions, freshness, ownership, thresholds, drilldowns, data quality, and interpretation rather than filling a screen with available charts.
---
# Analytics Dashboard Specification

Use when recurring marketing or product decisions need a durable shared measurement surface.

## Procedure
1. Define the dashboard audience and the decisions or monitoring questions it must support.
2. Select the smallest set of metrics needed and document exact definitions, numerators, denominators, units, source systems, and owners.
3. Define dimensions, filters, date behavior, cohort or attribution rules, and comparison periods needed for interpretation.
4. Specify freshness, expected latency, backfill behavior, and how incomplete or delayed data is shown.
5. Choose visual forms according to the question: trend, composition, funnel, distribution, cohort, table, or alert rather than defaulting every metric to a card.
6. Define thresholds or alerts only where an owner has a known response.
7. Provide drilldown paths or links from summary signals to enough detail for diagnosis.
8. Include data-quality indicators and annotations for material launches, outages, tracking changes, or methodology revisions.

## Decision rules
- A dashboard should support a recurring decision or operational question.
- Metric definitions are part of the product, not hidden analyst knowledge.
- More charts can reduce clarity.
- Never show stale or partial data as if it were complete current truth.

## Quality gate
The specification is ready when every metric and dimension is reproducible, freshness and data quality are visible, visualizations answer concrete questions, diagnostic paths and ownership exist, and a new reader can interpret the dashboard without oral folklore.