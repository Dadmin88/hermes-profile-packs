---
name: funnel-analysis
description: Analyze a marketing or product funnel from qualified entry through successive outcomes using trustworthy event definitions, segment comparison, leakage diagnosis, and decision-relevant conversion evidence.
---
# Funnel Analysis

Use when the team needs to understand where a population advances, stalls, or exits across a sequence of measurable stages.

## Procedure
1. Define the population, time window, stage sequence, entry qualification, conversion windows, and final outcome before calculating rates.
2. Verify event or CRM definitions and deduplication so one user, account, lead, or order is not counted inconsistently across stages.
3. Report both counts and conversion rates at every stage and preserve the denominator used for each rate.
4. Segment by dimensions with plausible causal relevance such as source, audience, device, geography, plan, campaign, or cohort.
5. Identify the first meaningful divergence between strong and weak paths rather than assuming the largest percentage drop is the highest-value problem.
6. Check latency and time-to-next-stage because slow progression can matter even when eventual conversion is similar.
7. Investigate instrumentation, eligibility, capacity, and operational causes before labeling every drop a messaging problem.
8. End with prioritized hypotheses, evidence gaps, and the next measurement or experiment needed to distinguish causes.

## Decision rules
- A funnel is a model of a journey, not proof that every user follows one linear path.
- Compare like populations and consistent conversion windows.
- Large percentage drops may be normal when the stage intentionally filters low-fit traffic.
- Instrumentation failure can look exactly like customer dropoff.

## Quality gate
The analysis is ready when stages and denominators are reproducible, important segments and timing are visible, leakage is distinguished from intended qualification, leading causes are evidence-ranked, and the next decision can be made from the analysis rather than the chart alone.