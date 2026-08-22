---
name: changelog-curation
description: Curate repository and product changes into a user-meaningful changelog by selecting externally relevant behavior, grouping related changes, verifying versions and scope, and excluding internal noise.
---
# Changelog Curation

Use when commit, PR, issue, or release history must become a coherent record of product change.

## Procedure
1. Define the release range, product or package, target audience, and authoritative source revisions.
2. Gather merged changes, release commits, issues, migrations, configuration changes, deprecations, and fixes from the actual release range.
3. Classify each change by user or operator consequence rather than commit type alone.
4. Group related implementation work into one meaningful entry and omit refactors, test-only changes, and internal chores with no relevant external effect.
5. Verify feature names, defaults, availability, affected platforms, versions, and links against the released state.
6. Highlight breaking changes, required action, security fixes, known limitations, and migration dependencies separately from routine improvements.
7. Preserve credit or issue/PR references when useful without turning the changelog into a raw commit dump.
8. Review for missing high-impact changes by comparing final release behavior and migration notes with the curated list.

## Decision rules
- A changelog explains changed behavior, not development activity.
- Several commits can represent one user-facing change.
- Internal cleanup should not crowd out meaningful release information.
- Source range and version must be exact.

## Quality gate
The changelog is ready when entries correspond to actual released behavior, implementation noise is removed, breaking or action-required changes are prominent, versions and links are verified, and important release effects cannot be discovered only by reading Git history.