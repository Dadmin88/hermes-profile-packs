---
name: experiment-analysis
description: Analyze a marketing or product experiment from assignment integrity, exposure, primary and guardrail metrics, uncertainty, segment effects, novelty, duration, and business relevance.
---
# Experiment Analysis

Use when an A/B, holdout, geo, cohort, or rollout experiment has completed or reached a planned decision point.

## Procedure
1. Verify the hypothesis, treatment, assignment unit, eligibility, exposure logging, sample, dates, and stopping rules before reading outcomes.
2. Check allocation balance, sample-ratio anomalies, cross-treatment contamination, missing exposure, and instrumentation changes.
3. Analyze the predeclared primary metric and guardrails using the intended statistical or decision framework.
4. Report absolute effect, relative effect, uncertainty, and business significance instead of only a significance label.
5. Inspect relevant segments cautiously, distinguishing preplanned heterogeneity from post-hoc pattern hunting.
6. Check time trends, novelty, seasonality, and delayed effects when the treatment can change behavior after the immediate session.
7. Reconcile any movement in downstream quality, retention, revenue, support, or cost metrics that alters the apparent win.
8. Recommend ship, iterate, continue, or stop and preserve the exact experiment configuration and result for future reference.

## Decision rules
- A statistically detectable effect can still be too small to matter.
- A neutral result is informative when the experiment had enough sensitivity for the decision threshold.
- Post-hoc segments are hypotheses unless independently confirmed.
- Do not rewrite the success metric after seeing the data.

## Quality gate
The analysis is ready when experiment integrity is established, effect size and uncertainty are visible, guardrails and downstream effects are considered, exploratory findings are labeled, and the decision follows the evidence and original hypothesis.