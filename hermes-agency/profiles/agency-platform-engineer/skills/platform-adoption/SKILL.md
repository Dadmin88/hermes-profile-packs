---
name: platform-adoption
description: Drive and evaluate internal platform adoption through consumer segmentation, migration paths, enablement, incentives, feedback, support data, and evidence that the platform produces better outcomes than existing alternatives.
---
# Platform Adoption

Use when a platform capability exists but teams are not consistently using it, are bypassing it, or need to migrate from fragmented legacy paths.

## Procedure
1. Segment consumers by workload, maturity, constraints, current solution, and migration difficulty. Do not treat all non-adoption as resistance to change.
2. Establish the current baseline: who uses the platform, which journeys succeed, time/cost saved, support burden, reliability, and common bypass or abandonment reasons.
3. Interview and observe representative adopters and non-adopters. Identify missing capability, poor UX, trust/reliability issues, migration cost, documentation gaps, policy friction, or legitimate incompatibility.
4. Define the target adoption outcome and why it matters. Prefer outcomes such as safer releases, faster setup, lower support load, or more reliable operations over a vanity percentage alone.
5. Remove product/platform blockers before relying on mandates. Improve self-service, defaults, documentation, migration tooling, examples, error messages, and support paths based on evidence.
6. Provide an incremental migration path where possible. Avoid forcing consumers to rewrite unrelated systems simply to receive one platform capability.
7. Communicate the contract and benefits accurately, including escape hatches and unsupported cases. Enable champions without making success depend on tribal knowledge.
8. Instrument the adoption funnel: discovery, first successful use, repeat use, migration completion, failure, support escalation, and abandonment.
9. Review bypasses and exceptions periodically. Convert repeated valid exceptions into supported patterns or explicitly preserve them outside the platform.
10. Retire legacy paths only after the replacement is proven, migration is feasible, ownership is clear, and remaining consumers have an explicit plan.

## Decision rules
- Adoption is earned through usefulness and reliability; mandate is not evidence of product quality.
- A consumer staying on a legacy path may reveal a missing requirement rather than poor behavior.
- Measure successful outcomes, not installs or generated repositories alone.
- Platform adoption work should reduce long-term operational variants, not create parallel permanent paths accidentally.

## Quality gate
The adoption effort is working when representative consumers can migrate and succeed without bespoke intervention, measured outcomes improve, recurring bypass causes are understood and acted on, support burden trends appropriately, and legacy retirement decisions are backed by real readiness rather than schedule pressure.