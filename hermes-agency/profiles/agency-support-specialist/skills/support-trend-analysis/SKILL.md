---
name: support-trend-analysis
description: Analyze support volume and case evidence to identify recurring product, documentation, reliability, onboarding, policy, or operational problems without mistaking ticket count for root cause.
---
# Support Trend Analysis

Use when recurring cases may indicate a systemic problem or when product/operations teams need evidence from support activity.

## Procedure
1. Define the decision and time window, then gather cases with enough metadata and text to distinguish issue types, affected products, segments, versions, and outcomes.
2. Normalize obvious duplicates and separate one incident generating many contacts from many independent defects.
3. Cluster by underlying user problem rather than ticket wording alone; sample cases to verify each cluster's meaning.
4. Measure volume, recurrence, severity, time-to-resolution, reopen/escalation rate, affected segment, and operational cost where useful.
5. Trace likely drivers across product defects, confusing UX, missing docs, onboarding gaps, reliability incidents, policy ambiguity, integration failures, or unsupported expectations.
6. Compare against releases, incidents, campaigns, customer growth, and seasonality before claiming a trend.
7. Pull representative evidence and quantify confidence; keep anecdotal signals distinct from repeated patterns.
8. Recommend the smallest set of owned interventions and define what subsequent support data would show improvement.

## Decision rules
- Ticket count alone is not severity or prevalence.
- One noisy customer or incident can dominate volume.
- Support can surface patterns but should not invent engineering root cause without evidence.
- Preserve user privacy when sharing examples.

## Quality gate
The analysis is useful when recurring problems are evidence-backed, duplicate/incident effects are controlled, affected populations and consequences are visible, uncertainty is stated, and each recommended intervention has an appropriate owner and measurable follow-up.