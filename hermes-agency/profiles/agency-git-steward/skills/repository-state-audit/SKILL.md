---
name: repository-state-audit
description: Audit exact Git and contribution state across branch, HEAD, index, working tree, remotes, divergence, worktrees, reachable commits, and relevant PR relationships before consequential source-control operations.
---
# Repository State Audit

Use before merges, rebases, resets, releases, history rewrites, cleanup, contribution triage, handoff, or whenever the repository's true state must be known precisely.

## Procedure
1. Identify repository root and active worktree. Record current branch or detached HEAD, exact commit SHA, and whether a rebase, merge, cherry-pick, bisect, or other operation is in progress.
2. Inspect working tree and index separately: staged changes, unstaged changes, relevant untracked/ignored files, conflicts, intent-to-add, deletions, renames, and submodule state where used.
3. Inspect branch upstream/tracking configuration and remotes. Confirm which remote and branch are authoritative for the intended operation rather than assuming `origin/main`.
4. Refresh remote refs when current remote state is necessary and network policy allows it, then record ahead/behind/divergence and merge-base relationships relevant to the task.
5. Inspect linked worktrees and branches checked out elsewhere so cleanup, branch movement, or history rewriting does not collide with active work on another path, process, or agent.
6. Identify commits or changes at risk of becoming unreachable before reset, delete, squash, or rewrite. Preserve a named reference or exact SHA when recovery would otherwise depend on reflog luck.
7. Inspect stash state if relevant, but do not assume stashes contain only the current task or are safe to apply/drop blindly.
8. For release/checkpoint work, verify the exact tree/content being claimed: commit tree, tags, branch pointers, submodule revisions, generated artifacts, and remote parity at the required assurance level.
9. When the audit concerns contribution or PR triage, inspect relevant open/merged PRs and issues for the same reported bug, subsystem, or change. Identify duplicate, sibling, stacked, superseding, or already-landed relationships before treating each contribution as independent.
10. If several contributions share the same underlying fix, report the cluster and contributor provenance so the review owner can decide whether to consolidate, preserve separate changes, or close duplicates. Do not perform forge writes as part of the read-only audit unless separately authorized.
11. Report the state compactly with exact identifiers and hazards: uncommitted work, divergence, stale remote knowledge, operation in progress, unexpected worktree, missing upstream, at-risk commits, or contribution relationships that change the next action.

## Decision rules
- Working tree, index, commit, branch ref, remote ref, and PR state are distinct; never conflate them.
- `git status` alone does not prove remote divergence, worktree ownership, exact tree identity, or contribution relationships.
- Similar PR titles do not prove duplicate fixes; compare the actual premise, subsystem, and diff.
- Preserve authorship/credit when contribution work is later consolidated.
- An untracked file can be valuable work; “not in Git” does not mean disposable.

## Quality gate
The audit is complete when current commit/branch, staged and unstaged work, untracked/conflicted state, remote/upstream relationship, relevant worktrees, at-risk commits, and any material PR/issue relationships are known well enough that the next source-control or contribution decision proceeds from evidence rather than assumed repository state.