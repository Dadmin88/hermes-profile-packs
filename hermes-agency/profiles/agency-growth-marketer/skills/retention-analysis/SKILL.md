---
name: retention-analysis
description: Analyze retention from a meaningful cohort and repeated-value definition, separating lifecycle, segment, acquisition quality, product change, seasonality, and resurrection effects.
---
# Retention Analysis

Use when growth depends on whether users or accounts continue receiving value after acquisition or activation.

## Procedure
1. Define cohort entry, retained behavior, observation interval, maturity window, and whether retention is user, account, revenue, or another unit.
2. Choose a retained action that represents meaningful repeated value rather than any login or background event.
3. Build cohort curves using equal maturity and distinguish classic, rolling, return, or revenue retention according to the business question.
4. Segment by acquisition source, activation path, use case, plan, team size, geography, or product revision where plausible differences exist.
5. Identify early drop, long-term plateau, resurrection, expansion, and churn timing separately.
6. Mark product changes, seasonality, outages, pricing, or acquisition-mix shifts that could explain curve movement.
7. Compare retained and churned cohorts for behavioral differences while avoiding causal claims from correlation alone.
8. Translate patterns into product or growth hypotheses and prioritize interventions around durable value rather than notification volume.

## Decision rules
- Retention requires a meaningful return behavior.
- Compare equal-age cohorts.
- Acquisition quality and product retention are intertwined; segment them before blaming one layer.
- Resurrection is useful but should not be confused with continuous retention.

## Quality gate
The analysis is ready when the retention definition matches real value, cohort age and segmentation are correct, lifecycle patterns and external changes are visible, churn correlates are separated from causal claims, and findings produce testable hypotheses about durable customer value.