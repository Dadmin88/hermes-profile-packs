---
name: cohort-analysis
description: Analyze behavior over time by cohort using consistent entry events, maturity windows, retention or value measures, and segment context so lifecycle patterns are not distorted by mixing users at different ages.
---
# Cohort Analysis

Use when marketing or product performance changes with time since acquisition, activation, purchase, or another defining event.

## Procedure
1. Define the cohort entry event, calendar granularity, population rules, observation window, and outcome being measured.
2. Verify each subject belongs to the intended cohort once unless repeat-event cohorts are explicitly part of the design.
3. Compare equal maturity windows so recent cohorts are not penalized for outcomes they have not had time to reach.
4. Measure retention, repeat action, revenue, conversion, expansion, or another relevant outcome by age since cohort entry.
5. Segment by source, campaign, audience, plan, product revision, geography, or other plausible factors while watching sample size.
6. Mark major launches, pricing changes, seasonality, outages, or acquisition-mix shifts that can explain cohort differences.
7. Distinguish composition change from behavior change; a better cohort may simply contain different customers.
8. Translate durable patterns into hypotheses about acquisition quality, onboarding, retention, or product value and define follow-up analysis.

## Decision rules
- Compare cohorts at equal maturity.
- Cohort definition should match the business question, not whatever date is easiest to query.
- Calendar effects and lifecycle-age effects are different phenomena.
- Small segmented cohorts should not carry precise claims.

## Quality gate
The analysis is ready when cohort entry and maturity are consistent, lifecycle outcomes are comparable over time, composition and calendar changes are visible, uncertainty is proportional to sample size, and findings connect to specific acquisition or retention decisions.