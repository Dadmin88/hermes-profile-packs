---
name: activation-analysis
description: Analyze onboarding activation by identifying the earliest behaviors that predict durable value, measuring time and path to those behaviors, and separating correlation from useful product signals.
---
# Activation Analysis

Use when onboarding performance needs to be understood beyond signup completion or tutorial progress.

## Procedure
1. Define the target user or account segment and the durable product outcome activation is expected to predict.
2. Inventory candidate early behaviors such as setup completion, first successful task, collaboration, data import, repeated use, or another value-realization event.
3. Compare retention, expansion, or repeated-value behavior across cohorts that do and do not reach each candidate event.
4. Measure time-to-event, number of steps, abandonment points, prerequisite states, and alternate successful paths.
5. Control interpretation for obvious confounders such as customer maturity, acquisition source, plan, team size, or assisted onboarding.
6. Choose an activation definition that is observable, meaningful, early enough to guide onboarding, and not trivially gameable.
7. Segment the funnel before aggregating because different user types may reach value through different paths.
8. Translate findings into hypotheses for onboarding design or experiments rather than treating correlation as causal proof.

## Decision rules
- Signup is an account event, not automatically activation.
- Activation should represent experienced value or a strong leading indicator of it.
- The most correlated event may simply identify already-high-intent users; investigate causality before optimizing blindly.
- Different segments can have different valid activation paths.

## Quality gate
The analysis is ready when the activation definition connects plausibly to durable value, cohort and timing evidence support it, segment differences and confounders are visible, alternate paths are understood, and recommended changes are framed as testable product hypotheses.