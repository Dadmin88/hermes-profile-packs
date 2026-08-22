---
name: rebase-conflict-resolution
description: Rebase or resolve Git conflicts by preserving both sides' intended behavior, understanding commit context, validating the resolved result, and keeping a recoverable path throughout the operation.
---
# Rebase and Conflict Resolution

Use when replaying commits onto a new base or resolving merge/rebase/cherry-pick conflicts between independently changed lines or files.

## Procedure
1. Inspect repository status, current branch/HEAD, operation state, remotes, worktrees, and uncommitted changes before starting or continuing. Create a recoverable checkpoint or stop if local state could be lost.
2. Understand the purpose of the commits being replayed and the relevant changes on the new base. Read commit messages/diffs and adjacent code rather than treating conflict markers as the entire context.
3. For each conflict, identify the behavior each side intended and whether the new base already supersedes, renames, moves, or restructures part of the older change.
4. Resolve semantically. Do not automatically choose “ours,” “theirs,” or both text blocks when that would duplicate behavior, reintroduce removed code, or discard a required change.
5. Check non-conflicting nearby changes too. Git can merge text cleanly while producing a semantic conflict through changed types, APIs, imports, assumptions, generated files, or migration order.
6. Stage only resolved paths after reviewing their diff. Continue the rebase/cherry-pick/merge one step at a time and inspect any subsequent conflict in its new parent context.
7. If the resolution becomes uncertain or the operation is based on the wrong assumptions, abort back to the recoverable starting state rather than pushing through blindly.
8. After the operation, compare the resulting commits/diff to the intended change and new base. Run relevant tests/builds/static checks and inspect generated/migration behavior where conflicts touched them.
9. Verify branch divergence and remote state before pushing. Use force-with-lease rather than unconditional force only when history rewriting is authorized and the remote branch must be updated.

## Decision rules
- Conflict resolution is behavior integration, not marker deletion.
- Clean textual merge does not guarantee semantic compatibility.
- Preserve authors' intended outcomes where they remain valid, but the newer accepted architecture/API may require adapting older code rather than preserving old syntax.
- Never force-push shared or protected history without explicit authority and a verified remote expectation.

## Quality gate
The operation is complete when the replayed history expresses the intended behavior on the new base, semantic as well as textual conflicts have been checked, validation passes for affected areas, a recoverable path existed throughout, and any rewritten remote update is authorized and verified.