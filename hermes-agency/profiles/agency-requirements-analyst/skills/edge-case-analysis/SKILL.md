---
name: edge-case-analysis
description: Identify and classify requirement edge cases across boundaries, invalid or missing input, permissions, concurrency, timing, partial failure, state transitions, limits, recovery, and unusual but plausible user behavior.
---
# Edge-Case Analysis

Use when a requirement or workflow appears clear on the happy path but implementation could diverge in less common states.

## Procedure
1. State the normal flow, actors, preconditions, inputs, state, and desired outcome before looking for exceptions.
2. Vary one dimension at a time: empty, missing, duplicate, maximum or minimum, malformed, stale, delayed, reordered, repeated, cancelled, unauthorized, or conflicting input as relevant.
3. Walk state transitions before, during, and after interruption, retry, refresh, navigation, process restart, or dependency failure.
4. Check ownership and permission boundaries such as cross-user, cross-tenant, administrator, guest, expired access, or resource transfer.
5. Check timing and concurrency cases where two valid actions can collide or a response arrives after the user's intent changed.
6. Check limits, quotas, pagination, long content, localization, time zones, precision, and platform differences implicated by the product.
7. Classify each case as required behavior, invalid input to reject, accepted limitation, deferred decision, or implementation detail owned elsewhere.
8. Convert material cases into requirement clarification or acceptance evidence without inflating the spec with implausible hypotheticals.

## Decision rules
- Edge cases should be plausible enough to affect behavior or risk.
- Do not use edge-case analysis to prescribe implementation architecture.
- Invalid states still need defined user or system behavior.
- Prioritize cases that cross trust, data, money, irreversible action, or durability boundaries.

## Quality gate
The analysis is ready when important boundary and interruption states have an explicit expected outcome or owner, high-consequence cases are not left to implementation guesswork, and unlikely theoretical cases are separated from requirements that genuinely need definition.