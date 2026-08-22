---
name: attribution-analysis
description: Analyze marketing attribution using explicit touchpoint scope, identity rules, conversion windows, model assumptions, incrementality limits, and cross-channel evidence without treating attributed credit as causal proof.
---
# Attribution Analysis

Use when deciding which marketing activities appear to contribute to acquisition, conversion, or revenue.

## Procedure
1. Define the conversion, population, channels, touchpoints, identity stitching, lookback window, and date range in scope.
2. Audit tracking coverage and known blind spots such as privacy restrictions, offline sales, dark social, cross-device use, or missing campaign parameters.
3. Compare multiple attribution views where useful, such as first touch, last touch, position-based, platform-reported, or modeled credit.
4. Reconcile channel totals against authoritative conversions or revenue and explain unavoidable gaps or duplicated platform claims.
5. Segment by customer type, acquisition motion, geography, device, or sales cycle when journeys differ materially.
6. Distinguish attribution from incrementality; credited touchpoints may have participated without causing the conversion.
7. Use experiments, holdouts, geo tests, or other causal evidence where spend decisions require stronger confidence.
8. Report channel contribution as a range of evidence and implications, not a single magical percentage.

## Decision rules
- Attribution models allocate credit; they do not inherently estimate causality.
- Self-reported platform attribution often overlaps across channels.
- Missing tracking should remain visible rather than being silently assigned.
- Use stronger causal methods for high-cost allocation decisions when feasible.

## Quality gate
The analysis is ready when tracking scope and blind spots are explicit, credited conversions reconcile reasonably to authoritative outcomes, model assumptions are visible, attribution is separated from causal lift, and spend recommendations match the strength of the evidence.