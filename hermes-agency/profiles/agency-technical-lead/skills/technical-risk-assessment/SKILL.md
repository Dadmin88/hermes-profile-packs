---
name: technical-risk-assessment
description: Assess implementation risk across uncertainty, blast radius, compatibility, data, concurrency, dependencies, performance, security, operations, and reversibility so engineering effort follows the risks that can actually derail delivery.
---
# Technical Risk Assessment

Use before or during a consequential engineering change to identify which technical uncertainties need mitigation, sequencing, proof, or escalation.

## Procedure
1. Define the intended technical change and affected system boundaries. Risk is evaluated against a concrete implementation and environment, not a generic technology list.
2. Identify uncertainty: unfamiliar code paths, new technology, unclear requirements, unproven scale assumptions, undocumented legacy behavior, third-party dependencies, or areas where the team lacks evidence.
3. Identify blast radius: shared libraries, public interfaces, critical user flows, privileged paths, durable data, infrastructure, build/release systems, and downstream consumers that could be affected by failure.
4. Review compatibility and migration risk, including existing data, mixed versions, rollback, partial deployment, external clients, and any irreversible transformation or side effect.
5. Review correctness risks that tend to evade happy-path implementation: concurrency, retries, idempotency, ordering, time, partial failure, stale state, cache invalidation, resource exhaustion, and recovery behavior as relevant.
6. Include performance, security, and operational concerns without pretending to own their final review. Route deep domain analysis to the corresponding specialist when the risk is material.
7. Score or rank risks by consequence, plausibility, uncertainty, and reversibility using a lightweight scale appropriate to the project. Avoid decimal precision that the evidence cannot support.
8. Define a mitigation for each material risk: architecture decision, spike, prototype, contract test, migration rehearsal, feature flag, staged rollout, observability, independent review, load test, fallback, or another targeted control.
9. Convert risk into sequencing. High-uncertainty/high-cost assumptions should be tested early enough to change the plan; reversible low-impact risks can be handled later.
10. Reassess when implementation evidence changes the assumptions. Close risks with evidence, not because time passed or code was written.

## Decision rules
- Risk is not the same as difficulty. A difficult isolated algorithm may be lower delivery risk than a simple schema change with irreversible production impact.
- Prefer early evidence over large contingency buffers when the uncertainty can be tested cheaply.
- Escalate durable architecture choices to Software Architect and product tradeoffs to Product Manager rather than resolving them under the label of technical risk.
- A risk register that never changes the plan is bureaucracy, not engineering.

## Quality gate
The assessment is ready when material uncertainties and blast-radius risks are explicit, each important risk has an owner and mitigation or accepted rationale, sequencing tests the expensive assumptions early, and risks are closed only by evidence or authorized acceptance.