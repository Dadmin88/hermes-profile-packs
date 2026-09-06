---
name: dynamic-behavior-analysis
description: Test bounded hypotheses about an authorized software artifact through controlled execution, tracing, and instrumentation.
---
# Dynamic Behavior Analysis

Use only when static evidence cannot answer the authorized question and an appropriately isolated execution environment is available.

## Procedure

1. Restate the exact hypothesis, expected observable, permitted inputs, prohibited effects, stop conditions, and evidence needed. Avoid exploratory execution without a bounded question.
2. Verify containment before launch: disposable snapshot or reset path, no real credentials or personal data, least privilege, restricted or simulated network access, controlled shared folders, and resource/time limits.
3. Capture a clean baseline of processes, files, configuration, services, network state, and other observables relevant to the hypothesis.
4. Instrument the smallest useful surface—such as process creation, filesystem changes, IPC, library calls, memory state, or network messages—without weakening containment.
5. Execute one controlled input or state change at a time. Timestamp and retain the input, environment, trace, output, exit state, and resulting artifact changes.
6. Compare the result with the baseline and static model. Repeat only when needed to distinguish deterministic behavior, environmental dependence, timing effects, or competing hypotheses.
7. Reset the environment between materially different experiments. Do not allow unknown samples to reach production systems, unrestricted networks, real accounts, or unrelated devices.
8. Report confirmed behavior, negative results, environmental assumptions, reproducibility steps, confidence, and remaining unknowns. Preserve raw traces separately from interpretation.

## Quality gate

Dynamic evidence is acceptable only when containment was verified, the experiment addressed a stated hypothesis, inputs and environment were recorded, effects remained within authorization, and another analyst can reproduce the observation without using real credentials or production access.