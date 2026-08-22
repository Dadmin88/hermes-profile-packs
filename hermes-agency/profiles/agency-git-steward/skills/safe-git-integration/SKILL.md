---
name: safe-git-integration
description: Integrate reviewed work into Git safely using exact repository state, scoped staging, coherent commits, branch hygiene, conflict discipline, and remote verification.
---
# Safe Git Integration

Use for staging, committing, rebasing, merging, cherry-picking, pull requests, or release checkpoints.

## Procedure
1. Inspect branch, HEAD, remotes, worktrees, status, staged state, and divergence before changing Git state.
2. Preserve unrelated work. Never stage by broad pattern when the requested change can be scoped to known paths.
3. Review the exact diff being committed and verify generated/vendor changes are intentional.
4. Create coherent commits whose message describes the resulting change, not the editing process.
5. Before rebasing/merging/cherry-picking, identify local modifications and conflict risk; use a recoverable strategy.
6. Resolve conflicts by understanding both sides, then rerun relevant validation.
7. After push/merge, verify the remote branch or PR points at the intended commit and report exact identifiers when useful.

## Quality gate
A Git operation is complete only when repository state is understood and no unrelated work was silently lost, staged, or overwritten.