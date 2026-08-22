---
name: deployment-automation
description: Automate deployment from an immutable release artifact through environment targeting, concurrency control, health validation, progressive rollout, failure handling, and auditable completion.
---
# Deployment Automation

Use when manual or inconsistent release steps need to become a repeatable delivery workflow.

## Procedure
1. Define the deployable artifact, source revision, target environment, deployment unit, required approvals, and the exact post-deployment behavior that proves success.
2. Separate build from deploy when practical. Promote an identified immutable artifact rather than rebuilding source differently on each target.
3. Resolve environment-specific configuration and secrets at deployment/runtime through controlled mechanisms; never bake live credentials into artifacts or scripts.
4. Make deployment operations idempotent or safely resumable. Re-running after interruption should not duplicate irreversible side effects or leave ambiguous partial state.
5. Define concurrency and ordering: prevent conflicting deployments to the same target, coordinate migrations or dependent services, and preserve required compatibility during rolling change.
6. Choose a rollout strategy appropriate to blast radius: all-at-once only when justified, otherwise rolling, canary, blue/green, staged cohorts, or another controlled progression.
7. Automate readiness/health checks based on real service behavior and define how long the system waits before declaring failure.
8. On failure, stop expansion, preserve diagnostic evidence, and execute the approved rollback or forward-recovery path rather than improvising in the pipeline.
9. Record artifact/revision, target, actor/automation identity, timestamps, result, health evidence, and recovery action for audit and diagnosis.
10. Test the automation against a non-critical representative environment, including interrupted or failed deployment behavior, before trusting it for production.

## Decision rules
- A deployment command returning success is not release validation.
- Automate the decision boundaries and evidence, not only the shell commands.
- Infrastructure placement chosen by Fleet should be consumed as runtime target state, not hardcoded into an Agency skill or deployment artifact.
- Prefer fewer deployment mechanisms with well-understood failure behavior over one bespoke script per service.

## Quality gate
Deployment automation is ready when a known artifact can be delivered repeatably to a declared target, concurrent/partial execution is controlled, health gates determine progression, failure leaves a recoverable and diagnosable state, and the resulting release can be traced to exact source and artifact identity.