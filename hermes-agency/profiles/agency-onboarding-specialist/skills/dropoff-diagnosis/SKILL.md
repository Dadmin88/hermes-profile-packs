---
name: dropoff-diagnosis
description: Diagnose onboarding dropoff by locating the first meaningful friction point and distinguishing comprehension, motivation, trust, technical failure, prerequisite, latency, and audience-fit causes using quantitative and qualitative evidence.
---
# Dropoff Diagnosis

Use when users abandon or stall during onboarding and the team needs to understand why before redesigning the flow.

## Procedure
1. Define the affected segment, onboarding revision, time window, and exact step or outcome considered abandonment or stall.
2. Build the funnel from authoritative events and verify instrumentation before interpreting a step as problematic.
3. Segment dropoff by device, platform, acquisition source, role, plan, geography, account type, and other plausible dimensions without fishing for arbitrary differences.
4. Inspect errors, latency, validation failures, permission denials, dependency failures, and data prerequisites around the dropoff point.
5. Review session evidence, support contacts, user interviews, usability tests, or recordings where available to distinguish inability, confusion, low motivation, or low perceived value.
6. Trace the first meaningful divergence from successful users rather than assuming the screen where they leave caused the problem.
7. Rank root-cause hypotheses by evidence, user impact, frequency, and confidence.
8. Recommend the smallest experiment or design change that can test the leading cause and define the metric expected to move.

## Decision rules
- A high-exit screen may be the consequence of friction introduced earlier.
- Instrumentation gaps are a diagnosis problem, not evidence that the user behaved normally.
- Some abandonment reflects poor audience fit rather than onboarding design.
- Do not remove necessary trust or safety steps solely because they add friction.

## Quality gate
The diagnosis is ready when the dropoff is measured from trustworthy events, successful and unsuccessful paths are compared, technical and behavioral causes are separated, leading hypotheses are evidence-ranked, and the proposed next change can confirm or falsify the suspected cause.