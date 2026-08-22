---
name: upgrade-summary
description: Summarize an upgrade for existing users through benefits, changed behavior, prerequisites, compatibility, migration effort, validation, rollback or recovery, and post-upgrade differences.
---
# Upgrade Summary

Use when existing users need a concise decision and preparation guide for moving to a new version.

## Procedure
1. Define the from-version or supported range, target version, audience, and exact release artifacts in scope.
2. Summarize the most important reasons to upgrade in user or operator terms rather than listing every included change.
3. Identify prerequisites such as runtime, operating system, dependency, storage, database, configuration, license, or account requirements.
4. Call out breaking changes, removed behavior, deprecations, changed defaults, migrations, and compatibility constraints that affect preparation.
5. Estimate migration complexity by scenario and link exact step-by-step guides rather than hiding required work behind a generic upgrade command.
6. Define backup, validation, rollback or forward-recovery, and post-upgrade health checks appropriate to the system.
7. Note known issues or reasons a user may reasonably delay the upgrade.
8. Verify version numbers, commands, compatibility, links, and migration outcomes against the actual released build.

## Decision rules
- An upgrade summary helps users decide and prepare; it does not replace detailed migration instructions.
- Do not hide breaking changes behind release benefits.
- Version and compatibility claims must be checked against the release.
- State when rollback is not safely supported.

## Quality gate
The summary is ready when existing users can decide whether to upgrade, understand prerequisites and disruption, locate required migration steps, know how to validate and recover, and trust that all claims correspond to the released versions.