---
name: email-experiment
description: Design and evaluate email experiments on message, timing, sequence, audience, or call to action using stable assignment, delivered-population awareness, downstream outcomes, and negative-signal guardrails.
---
# Email Experiment

Use when an email decision can be learned through controlled variation rather than comparing unrelated campaign sends.

## Procedure
1. State the hypothesis, target audience, treatment, primary downstream outcome, and guardrail metrics before launch.
2. Randomize or otherwise assign at the appropriate unit and keep treatment stable across repeated messages when journey consistency matters.
3. Define whether analysis uses assigned, sent, delivered, or opened populations and understand the bias each denominator can introduce.
4. Change one coherent dimension at a time when the goal is to identify cause: subject, body, CTA, timing, frequency, sequence, or audience logic.
5. Instrument product conversion or desired behavior rather than treating opens and clicks as the final outcome when stronger signals exist.
6. Monitor complaints, unsubscribes, bounces, support, and longer-term engagement so a short-term lift does not hide audience harm.
7. Account for time zone, send-time, provider, device, segment, and campaign interference where they can confound the result.
8. Record exact variants, assignment, dates, eligibility, results, uncertainty, and the resulting decision.

## Decision rules
- Open metrics can be noisy or privacy-distorted and should not automatically be the primary outcome.
- Do not compare separate historical sends as if they were randomized experiments.
- Guardrail audience trust and deliverability while optimizing conversion.
- Repeated experiment exposure may require user-level assignment rather than message-level randomness.

## Quality gate
The experiment is ready when assignment and denominators are clear, the treatment is reproducible, downstream and negative outcomes are measured, confounders are understood, and the final decision follows evidence stronger than open-rate movement alone.