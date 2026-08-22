---
name: content-lifecycle
description: Manage knowledge content from proposal through authoring, review, publication, revision, validation, archival, and removal using ownership, freshness signals, source changes, and reader evidence.
---
# Knowledge Content Lifecycle

Use when a knowledge base contains enough material that stale or orphaned content becomes a reliability risk.

## Procedure
1. Define content states and the evidence required to move between draft, reviewed, published, stale, superseded, archived, and removed as appropriate.
2. Assign one accountable owner or owning team and record source dependencies whose change may invalidate the content.
3. Set review cadence based on decay risk rather than one universal schedule; volatile operational or product content should age faster than durable concepts.
4. Trigger review from product releases, policy changes, incidents, support trends, broken links, source updates, or reader feedback where possible.
5. Validate high-risk procedures or technical instructions against the current system before renewing freshness.
6. Supersede content with redirects or replacement links when readers may still encounter old URLs or references.
7. Archive material when historical value remains and remove it when retention adds confusion without useful provenance.
8. Track lifecycle metrics such as unowned pages, stale high-traffic content, review backlog, broken links, and repeated corrections.

## Decision rules
- A review date alone is not evidence content is still correct.
- Lifecycle priority should combine decay risk and reader impact.
- Preserve historical material only when its status is unmistakable.
- Ownership must survive contributor or Fleet-node changes.

## Quality gate
The lifecycle is healthy when every important article has an owner and source context, freshness reflects real validation, changes trigger review, superseded content routes readers correctly, and stale high-impact knowledge cannot silently remain authoritative.