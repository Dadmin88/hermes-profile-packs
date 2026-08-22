---
name: exploratory-testing
description: Execute a focused exploratory test session that probes real user behavior, edge cases, state transitions, and unexpected interactions.
---
# Exploratory Testing

Use when behavior needs human-style probing beyond scripted assertions.

## Procedure
1. Define a short test charter: feature, risk, user goal, and timebox.
2. Establish the expected happy path and known constraints.
3. Explore boundaries: empty/large/invalid inputs, retries, interruption, navigation changes, persistence, permissions, concurrency, slow/failing dependencies, and device/layout differences where relevant.
4. Vary sequence and state rather than repeating the same path.
5. Capture defects immediately with exact reproduction steps, environment, evidence, expected result, and actual result.
6. Note suspicious behavior that needs follow-up separately from confirmed bugs.
7. Summarize coverage, findings, and remaining uncertainty at session end.

## Quality gate
A defect is not useful until another person can reproduce it. A clean session is not proof of absence; state what was and was not explored.