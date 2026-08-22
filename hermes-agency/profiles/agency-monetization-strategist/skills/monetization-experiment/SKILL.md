---
name: monetization-experiment
description: Design and evaluate a commercial experiment for pricing, packaging, value metrics, offers, or upgrade paths using an explicit hypothesis, measurable outcomes, guardrails, segmentation, and reproducible evidence.
---
# Monetization Experiment

Use when a monetization decision can be tested with observed customer behavior rather than settled by opinion alone.

## Procedure
1. State the hypothesis, target segment, decision it should inform, and the customer behavior expected to change.
2. Define the intervention precisely: price, package, value metric, trial, limit, offer, upgrade path, or another controlled change.
3. Choose primary and guardrail metrics that capture both business outcome and customer experience, such as conversion, expansion, retention, support burden, refund rate, or usage as relevant.
4. Identify confounders such as seasonality, acquisition channel, sales assistance, existing contracts, promotions, geography, or customer maturity.
5. Select an assignment, rollout, or cohort design that can produce interpretable evidence while respecting existing customer commitments.
6. Define sample, duration, stopping criteria, rollback conditions, and the minimum effect that would matter to the decision.
7. Instrument exposure and outcome so each participant or account can be traced to the correct experiment state without collecting unnecessary sensitive data.
8. Analyze effects by relevant segment and distinguish short-term conversion gains from downstream retention, margin, support, or usage effects.
9. Record the exact configuration, dates, exclusions, results, uncertainty, and recommendation so future pricing work can build on evidence rather than memory.

## Decision rules
- An experiment should answer one meaningful monetization question, not test several unrelated changes at once.
- Conversion alone is not sufficient when the treatment can change retention, margin, usage, or support burden.
- Respect contracts, disclosure requirements, and established customer commitments.
- A neutral result can still be useful when the design rules out effects large enough to matter.

## Quality gate
The experiment is decision-ready when the hypothesis and treatment are explicit, assignment and instrumentation support interpretation, customer and business guardrails are protected, segment and downstream effects are considered, and the recommendation reflects the strength and uncertainty of the evidence.