---
name: audience-segmentation
description: Segment release-note information by the readers whose actions or workflows differ, such as end users, administrators, developers, operators, or integrators, without duplicating the entire release for each audience.
---
# Release Notes Audience Segmentation

Use when one release affects several audiences in materially different ways.

## Procedure
1. Identify the audiences affected by the release and the decisions or actions each needs to make.
2. Classify changes by consequence: visible capability, changed workflow, configuration, API or integration, administration, operations, migration, or compatibility.
3. Put universally important changes in a shared summary and route specialist detail into clear audience sections.
4. Emphasize required action, deadline, permissions, compatibility, or operational risk only for the readers who actually need it.
5. Avoid duplicating identical prose across sections; cross-reference shared entries where detail overlaps.
6. Use vocabulary each audience understands while preserving exact technical names where they must act on configuration or interfaces.
7. Check that no high-impact change is hidden solely inside a specialist section when it also affects general users.
8. Review the final notes from each audience perspective and remove material that creates noise without changing their behavior.

## Decision rules
- Segment by different reader needs, not organizational team names alone.
- Shared summaries prevent fragmented understanding of the release.
- Technical precision and audience clarity can coexist.
- Do not force users to read developer notes to discover a breaking workflow change.

## Quality gate
Segmentation is ready when every affected audience can quickly identify what changed for them, required actions and compatibility risks are visible, shared information is not duplicated unnecessarily, and specialist detail does not bury release-wide consequences.