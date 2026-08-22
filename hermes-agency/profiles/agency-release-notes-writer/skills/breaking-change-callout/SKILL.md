---
name: breaking-change-callout
description: Document a breaking or behaviorally incompatible release change with affected users, old and new behavior, required migration, deadlines, mixed-version implications, recovery, and exact references.
---
# Breaking Change Callout

Use when a release removes, renames, changes, or invalidates behavior that existing consumers may rely on.

## Procedure
1. Identify the exact interface, workflow, configuration, data, API, file format, command, default, or behavior that becomes incompatible.
2. State who is affected and the versions, environments, plans, platforms, or usage patterns that determine exposure.
3. Describe old behavior and new behavior concretely, including semantic differences that may not be obvious from renamed fields or commands.
4. Give the required migration sequence with exact replacement, configuration, code, or user action and link deeper migration material where needed.
5. State deprecation and removal dates, grace periods, compatibility windows, and whether mixed versions can coexist.
6. Explain failure symptoms users may see if they do not migrate and how to verify successful migration.
7. Include rollback or recovery expectations where the release supports them and call out irreversible data changes clearly.
8. Verify the callout against the released implementation and migration tests rather than roadmap intent.

## Decision rules
- Breaking change means consumer-observable incompatibility, not merely a large code diff.
- Put required action before implementation rationale.
- Dates and version boundaries must be exact and current.
- Do not label a migration easy unless the documented path has been proven.

## Quality gate
The callout is ready when affected consumers can identify exposure, understand old versus new behavior, execute and verify migration, know the relevant deadline and mixed-version limits, and recognize failure or recovery paths without reading the source diff.