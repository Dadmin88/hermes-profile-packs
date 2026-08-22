---
name: readiness-check
description: Assess launch readiness across product behavior, quality, operations, support, communications, dependencies, legal or compliance, analytics, rollback, and owner sign-off using evidence rather than optimistic status.
---
# Launch Readiness Check

Use when a feature, product, program, or release is approaching a public or operational go-live decision.

## Procedure
1. Define launch scope, audience, date or window, environments, rollout method, and the outcomes that must be true at go-live.
2. Identify readiness domains relevant to the launch: product, engineering, QA, security, accessibility, compliance, data, infrastructure, support, documentation, marketing, sales, partners, analytics, and operations.
3. For each domain, require an owner, status, evidence, blocking criteria, and known residual risk rather than a vague green or red label.
4. Verify critical user journeys, monitoring, support escalation, documentation, communications, analytics, and dependencies in the actual launch configuration.
5. Confirm rollout, rollback or forward-recovery, incident ownership, and decision authority for pausing or reversing launch.
6. Review unresolved issues by severity, likelihood, workaround, audience exposure, and ability to correct after launch.
7. Distinguish blockers, accepted risks, and post-launch follow-ups explicitly.
8. Record the final go, no-go, or conditional decision with evidence and owners for remaining actions.

## Decision rules
- A calendar date is not evidence of readiness.
- Every readiness item needs an owner and proof proportional to its risk.
- Non-blocking follow-ups should not be disguised as completed work.
- The person coordinating launch should not unilaterally waive risks owned by another authority.

## Quality gate
The launch is ready when critical domains have current evidence, blockers are resolved or explicitly accepted by the correct authority, rollout and recovery are executable, support and monitoring can detect problems, and the go-live decision is traceable rather than ceremonial.