---
name: onboarding-experiment
description: Design onboarding experiments around a specific activation hypothesis using clear treatment, assignment, funnel instrumentation, experience guardrails, and downstream retention evidence.
---
# Onboarding Experiment

Use when a proposed onboarding change can be evaluated with controlled behavioral evidence.

## Procedure
1. State the onboarding hypothesis, target segment, activation outcome, and the specific friction or opportunity the treatment addresses.
2. Change one coherent experience dimension such as sequence, guidance, defaults, setup burden, progressive disclosure, or value preview.
3. Define primary funnel and activation metrics plus guardrails for errors, support, abandonment, latency, or downstream retention.
4. Instrument exposure and each meaningful onboarding step before rollout so treatment and control paths can be reconstructed.
5. Choose assignment, sample, duration, and rollout method appropriate to traffic and risk and preserve consistent treatment within the user or account journey.
6. Check segment effects and alternate activation paths rather than optimizing only the global average.
7. Inspect qualitative behavior or feedback when metric movement reveals what changed but not why.
8. Decide whether to ship, iterate, or discard from the complete evidence and record the experiment revision and result.

## Decision rules
- Optimize for activation and durable value, not tutorial completion alone.
- Do not test several unrelated onboarding redesigns in one treatment if the goal is to learn what caused the effect.
- Guard against making the first session easier while harming later comprehension or retention.
- Preserve treatment identity across devices or Fleet-routed backend work where account-level consistency matters.

## Quality gate
The experiment is complete when the hypothesis and treatment are reproducible, exposure and funnel data are trustworthy, activation and guardrail effects are interpreted by segment, downstream consequences are considered, and the resulting product decision is documented.