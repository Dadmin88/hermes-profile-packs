---
name: maintainability-review
description: Review implementation structure for clarity, cohesion, coupling, complexity, duplication, ownership, extension pressure, and operational readability without turning style preference into blockers.
---
# Maintainability Review

Use when a change is functionally plausible but needs independent judgment about whether future engineers can safely understand, modify, debug, and extend it.

## Procedure
1. Understand the required behavior and constraints before judging structure. Complexity that directly represents a complex domain may be justified; accidental complexity is the target.
2. Check cohesion: each module, type, function, component, or service should have a comprehensible responsibility. Flag abstractions that mix unrelated policy, I/O, formatting, persistence, transport, and orchestration without a reason.
3. Check coupling: identify knowledge that leaks across boundaries, duplicated protocol/domain rules, global state, hidden ordering dependencies, temporal coupling, and changes that require editing many unrelated places to preserve one concept.
4. Review names and control flow for truthful readability. A maintainer should be able to identify inputs, state transitions, failure paths, side effects, and ownership without mentally executing unnecessary indirection.
5. Review duplication by meaning, not line similarity. Duplicate business rules or compatibility logic are dangerous; a few repeated straightforward lines may be clearer than a premature generic abstraction.
6. Review abstraction fit. Challenge wrappers that only rename an underlying API, inheritance or generic layers with one speculative consumer, configuration systems for fixed behavior, and helper layers that make debugging harder without protecting a real boundary.
7. Review error and observability paths. Failures should retain enough context to diagnose the responsible operation without leaking secrets or forcing maintainers to infer which branch ran.
8. Review lifecycle and extension pressure. Ask how the code will handle the next likely requirement, schema change, variant, or failure mode without predicting an imaginary platform years ahead.
9. Review comments and documentation for durable intent: explain non-obvious constraints, compatibility reasons, invariants, and tradeoffs rather than narrating obvious syntax or leaving implementation diaries.
10. Separate blockers from improvement suggestions. Block only when maintainability creates material correctness, regression, security, operability, or near-term change risk.

## Decision rules
- Readability and simplicity are engineering properties, not excuses to enforce personal formatting taste.
- Do not require a design pattern because it has a name.
- Prefer one obvious path over several flexible mechanisms when the flexibility has no demonstrated consumer.
- Refactoring unrelated code during feature review increases risk; recommend it separately unless it is necessary to make the change safe.
- The best abstraction protects a real concept or boundary and reduces future reasoning, not merely line count.

## Quality gate
The review is complete when material cohesion, coupling, complexity, duplication, abstraction, and diagnosability risks have been evaluated against the real requirements, blockers have concrete consequences, and style-only preferences are not disguised as correctness findings.