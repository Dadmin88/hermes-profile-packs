---
name: operational-metrics
description: Define operational metrics that connect service outcomes, demand, flow, quality, reliability, backlog, and cost to decisions without rewarding metric gaming.
---
# Operational Metrics

Use when an operations function needs a small decision-useful measurement set rather than a dashboard full of activity counts.

## Procedure
1. Define the operational outcomes and decisions the metrics must support before choosing measures.
2. Cover the relevant dimensions: demand, throughput, lead/wait time, backlog/age, quality/rework, reliability, service attainment, escalation, and cost or capacity where useful.
3. Define numerator, denominator, inclusion/exclusion rules, time window, source, owner, and refresh cadence for each measure.
4. Pair output metrics with quality or outcome measures so faster processing cannot look successful while defects or rework rise.
5. Segment where aggregation hides meaningful differences in work type, customer impact, region, channel, or severity.
6. Establish baselines and thresholds from evidence rather than arbitrary red/yellow/green decoration.
7. Review anomalies against real cases and process changes before inferring cause.
8. Retire metrics that no longer change a decision and add new measures only when they close a specific visibility gap.

## Decision rules
- Activity is not automatically value.
- A metric without an owner or decision use becomes reporting tax.
- Avoid targets that encourage queue manipulation, case splitting, or premature closure.
- Preserve definitions over time or clearly mark breaks in comparability.

## Quality gate
The metric set is ready when every measure has an explicit definition and decision use, outcome and quality are visible alongside speed or volume, gaming incentives are considered, and operators can trace surprising numbers back to real operational evidence.