---
name: release-checklist
description: Build and execute a release checklist from the actual release surface, required evidence, owners, dependencies, approvals, rollout steps, and recovery conditions rather than a generic template.
---
# Release Checklist

Use when coordinating a software, product, content, configuration, or operational release with multiple readiness conditions.

## Procedure
1. Define the release artifact, scope, target environments/audiences, version or revision, timing, and accountable release owner.
2. Derive checklist items from the real change: build/artifact integrity, tests, migrations, compatibility, security, accessibility, documentation, support, communications, monitoring, and approvals as relevant.
3. Assign each item an owner and evidence that proves completion; avoid checkboxes whose meaning is “someone looked at it.”
4. Identify sequencing and dependencies, especially irreversible changes, migrations, external vendors, caches, configuration, and staged rollout requirements.
5. Include pre-release health checks and the exact artifact/revision being released.
6. Define go/no-go criteria and who has authority to decide when evidence is incomplete or conditions degrade.
7. Include rollback or forward-recovery readiness and post-release validation steps.
8. Record final release state, skipped items with explicit acceptance, and links to evidence.

## Decision rules
- A reusable template is a starting point, not proof the current release is covered.
- Never mark validation complete without revision-specific evidence.
- Release scope changes require checklist review.
- High-risk exceptions need explicit authority, not an unchecked box hidden in the list.

## Quality gate
The checklist is release-ready when it covers the actual change surface, every consequential item has an owner and evidence, go/no-go and recovery are explicit, the exact artifact/revision is known, and post-release validation is part of completion.