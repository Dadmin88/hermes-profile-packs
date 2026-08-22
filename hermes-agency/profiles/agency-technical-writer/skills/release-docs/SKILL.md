---
name: release-docs
description: Coordinate the technical documentation required for a release by identifying changed behavior, affected pages, new reference, migration, configuration, examples, troubleshooting, and versioned notices tied to the released state.
---
# Release Documentation

Use when a software release changes enough behavior that existing documentation must be updated as part of shipping.

## Procedure
1. Define the exact release range and gather user-visible, operator-visible, API, configuration, dependency, and compatibility changes from authoritative artifacts.
2. Map each change to existing documentation that becomes incomplete, wrong, or ambiguous and identify genuinely new pages required.
3. Prioritize breaking changes, migrations, new setup, changed defaults, removed behavior, new interfaces, and operational procedures before low-impact wording updates.
4. Update conceptual, tutorial, how-to, reference, troubleshooting, and example content according to the information need rather than duplicating release notes everywhere.
5. Add version or applicability notes where multiple supported releases differ and avoid silently rewriting history in docs intended for older versions.
6. Verify commands, screenshots, configuration, links, API examples, and migration steps against the release candidate or final build.
7. Coordinate publication timing so docs match actual availability and links are live when users encounter the release.
8. Record deferred documentation gaps explicitly and assign an owner rather than treating them as invisible post-release cleanup.

## Decision rules
- Documentation change is part of the release when users need it to adopt or operate the release safely.
- Release notes summarize change; durable docs teach the resulting product.
- Do not update version-sensitive claims from roadmap intent.
- Preserve old-version docs when they remain supported.

## Quality gate
Release documentation is ready when every material changed behavior has the right durable documentation update, breaking and migration paths are verified, version applicability is clear, publication matches real availability, and any remaining gap is visible and owned.