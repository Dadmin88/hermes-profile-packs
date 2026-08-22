---
name: stacked-pr-management
description: Manage dependent pull-request stacks and multi-base ports by preserving explicit branch dependencies, update order, reviewable deltas, contributor credit, and target-branch compatibility.
---
# Stacked PR Management

Use when one PR/MR depends on another branch, or when the same logical change must be carried to more than one maintained base.

## Procedure
1. Identify every PR/MR in the stack or port set, its head/base branches, current SHAs, ownership, and why the dependency or multi-base requirement exists.
2. For dependent stacks, model the chain explicitly and update it bottom-up: stabilize the parent first, then rebase/merge each child onto the updated parent according to repository policy.
3. Keep each child PR targeted at the branch it actually depends on so reviewers see only the intended incremental delta.
4. When a parent changes, inspect each descendant diff after replay; textually clean rebases can still create semantic conflicts or duplicated fixes.
5. For multi-base maintenance, confirm which supported branches genuinely require the change and whether code can remain identical or needs documented compatibility adaptation.
6. Port from one reviewed source change where practical, preserving authorship and linking sibling PRs so the relationship is obvious.
7. Run validation appropriate to each target branch/environment; identical source does not guarantee identical behavior under different dependencies or configuration.
8. Avoid collapsing a dependency stack by merging the default branch into a leaf as a substitute for updating the real parent relationship.
9. Verify the forge still shows the intended bases, diffs, check state, and stack/port links after each push.
10. Report every PR/MR in the stack or port set with current head/base and any target-specific divergence.

## Decision rules
- Dependent PRs and multi-base ports are different problems; do not treat them as one generic branch pattern.
- Update dependencies from the bottom up.
- Repository history policy decides rebase versus merge.
- If two supposed ports intentionally differ, document why rather than claiming they are identical.

## Quality gate
The stack is healthy when dependency order and PR bases reflect reality, each review surface contains only its intended delta, descendants remain valid after parent changes, multi-base adaptations are explicit, validation is target-specific where needed, and contributor credit and cross-links survive the workflow.