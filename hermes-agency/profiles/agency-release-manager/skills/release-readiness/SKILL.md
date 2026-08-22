---
name: release-readiness
description: Assess whether a release is ready to ship using evidence from scope, testing, security, operations, documentation, rollback, and stakeholder approvals.
---
# Release Readiness

Use before a production release or other consequential delivery checkpoint.

## Procedure
1. Establish the exact release candidate: version, commit, build, artifacts, and included scope.
2. Confirm acceptance criteria and required approvals for the release class.
3. Gather evidence from implementation review, QA, security, migrations, compatibility, documentation, and operational readiness as applicable.
4. Verify deployment steps, configuration changes, data migrations, observability, and rollback or recovery path.
5. Classify remaining issues by release impact. Separate known accepted risk from unresolved uncertainty.
6. Confirm communication, release notes, ownership during rollout, and post-release validation.
7. Produce a go, no-go, or conditional-go recommendation with explicit reasons.

## Quality gate
Never call a release ready because work is 'finished.' Readiness requires an identifiable candidate, passed gates, understood residual risk, and a credible recovery path.