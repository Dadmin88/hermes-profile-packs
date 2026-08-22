---
name: activation-experiment
description: Design a growth experiment intended to improve activation using one explicit behavioral hypothesis, stable exposure, product-value metrics, segment analysis, and retention guardrails.
---
# Growth Activation Experiment

Use when a growth intervention targets the transition from acquired user to experienced product value.

## Procedure
1. Define the target segment, activation event, friction or motivation hypothesis, and expected behavior change.
2. Choose a treatment that directly tests that hypothesis, such as guidance, sequence, default, reminder, invitation, template, or value preview.
3. Define primary activation and time-to-value metrics plus guardrails for error, support, retention, or unwanted behavior.
4. Establish eligibility, assignment, exposure logging, sample, duration, and minimum effect that would matter.
5. Preserve consistent treatment at the appropriate user or account level across devices and sessions.
6. Inspect funnel movement and segment effects to identify whether the change helps already-high-intent users or genuinely expands activation.
7. Check downstream retention or repeated value when the intervention could create superficial first-session completion.
8. Record exact treatment, dates, results, uncertainty, and the decision to ship, iterate, or stop.

## Decision rules
- Activation should represent experienced value, not a convenient button click.
- A growth treatment should not obscure important user choice or trust boundaries.
- Segment effects can reveal who the intervention actually helps.
- Guard against moving a metric while weakening durable product understanding.

## Quality gate
The experiment is ready when the activation definition is meaningful, assignment and exposure are reliable, downstream quality is protected, segment effects are interpretable, and the decision reflects durable value rather than a cosmetic funnel lift.