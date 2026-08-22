---
name: release-quality-plan
description: Define the quality evidence required for a release by mapping changed behavior, critical journeys, risks, environments, test ownership, entry/exit criteria, known gaps, and post-release validation.
---
# Release Quality Plan

Use when a release or milestone needs an explicit quality gate rather than relying on accumulated ad hoc tests.

## Procedure
1. Define release scope, changed surfaces, critical user/system journeys, supported platforms/environments, migrations/config changes, and consequences of failure.
2. Review implementation and architecture risk assessments, known defects, incident history, dependency changes, and unresolved assumptions to build the release risk picture.
3. Map each material risk to evidence and owner: static/build checks, unit/integration/contract/E2E, exploratory, accessibility, security, performance/load, migration/rollback, operational smoke, or other validation.
4. Define environment/data requirements and what each environment can legitimately prove. Call out gaps where production-like behavior cannot be reproduced pre-release.
5. Define entry criteria for release validation so QA does not test a moving or incomplete target unknowingly.
6. Define exit criteria around evidence and residual risk rather than “all tests pass.” Include blocking defect thresholds, required independent reviews, and accepted exceptions with owners.
7. Plan regression coverage proportional to blast radius, shared surfaces, and preserved contracts, including compatibility/mixed-version states when releases roll incrementally.
8. Define post-release checks and monitoring needed to catch defects that only appear with real traffic, data, platform, or distributed placement.
9. Track evidence by exact release revision/artifact so results cannot be silently reused after meaningful code/config changes.
10. Publish a concise quality disposition: ready, ready with accepted residual risk, or not ready, including missing evidence and the owner/decision required.

## Decision rules
- Release quality is a risk decision supported by evidence, not a raw test-count or pass-rate calculation.
- Do not treat lower environments as proof of behaviors they do not reproduce.
- Quality ownership stays independent from implementation; accepting residual product/business risk belongs to the appropriate decision owner.
- In Fleet deployments, include distributed/node/placement validation only when it is material to the release, while keeping live scheduling policy Fleet-owned.

## Quality gate
The plan is complete when release risks and critical journeys are explicit, each material risk has an appropriate validation owner/evidence path, environments and revision identity are clear, exit criteria expose residual risk, and post-release verification can detect failures that pre-release testing cannot prove away.