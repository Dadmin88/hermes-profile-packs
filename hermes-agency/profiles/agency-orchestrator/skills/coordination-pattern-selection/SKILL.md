---
name: coordination-pattern-selection
description: Decide whether a goal should stay with one specialist, use a paired execution/review pattern, or be decomposed across a larger team before creating coordination overhead.
---
# Coordination Pattern Selection

Use this before decomposing a goal merely because several profiles are available.

## Procedure

1. Restate the observable outcome and identify the specialty that owns the primary decision or deliverable.
2. Count the genuinely distinct domains involved. Do not count different file types or task steps as separate specialties unless they require different professional judgment.
3. Choose **solo ownership** when one specialist can complete the work coherently and validate it appropriately.
4. Choose a **pair** when another specialist adds one distinct dependency, materially different expertise, or independent review. If correctness is the reason for adding someone, prefer a reviewer over a second author.
5. Choose a **multi-specialist team** only when there are several clean work packages that can be independently owned and validated, or several independent gates are justified by risk.
6. For every proposed split, state the seam in one sentence: what the upstream package produces and what the downstream/parallel owner consumes.
7. Reject a split when ownership overlaps, the seam is unclear, context-transfer cost dominates, or synthesis would recreate the original task in one place anyway.
8. Parallelize only work that does not depend on unfinished outputs from another package and whose parallel execution can shorten the real critical path.
9. Define one synthesis owner. Synthesis reconciles specialist outputs; it does not erase disagreement, uncertainty, or failed validation.
10. Record durable commitments in the normal work system. Use chat/group rooms for deliberation, not as the sole system of record.

## Pattern guide

- **Solo**: one domain, coherent implementation, low coordination value.
- **Pair**: implementation + review, two clean domains, or one expert second opinion.
- **Team**: several distinct packages with explicit dependencies, or high-risk work requiring multiple independent gates.

## Quality gate

The coordination pattern is ready when every added profile has a unique reason to participate, each work package has one owner and checkable output, dependencies are explicit, and removing any participant would remove real expertise, review, or useful parallelism rather than merely reducing activity.
