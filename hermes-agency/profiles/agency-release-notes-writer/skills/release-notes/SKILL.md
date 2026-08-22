---
name: release-notes
description: Turn verified shipped changes into concise release notes organized around user impact, upgrade implications, fixes, and compatibility concerns.
---
# Release Notes

Use when a version, deployment, or public release needs an accurate change summary.

## Procedure
1. Identify the exact release candidate and authoritative list of included changes.
2. Group changes by user impact rather than commit order.
3. Explain what changed, who it affects, and any action users must take.
4. Call out breaking changes, migrations, deprecations, security-sensitive fixes, and known limitations clearly.
5. Remove internal implementation detail unless it helps users operate or upgrade safely.
6. Verify version numbers, links, commands, feature availability, and dates.

## Quality gate
Every claimed change must actually be in the release. A reader should know what matters without reading Git history.