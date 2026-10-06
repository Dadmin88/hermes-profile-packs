# Loop invariants and boundary cases: Diagnostic and misconception distinctions

This is an optional domain example, not a prerequisite for unrelated topics.

### Diagnostic

Show language-neutral pseudocode: total ← 0; for each x in [2, −1, 4]: total ← total + x; return total. Ask the returned value and the empty-list result.

### Distinguish the error

Returning only 4 confuses assignment with accumulation; returning the count confuses values with loop iterations. Correct states with 2−1 = 2 is arithmetic. Initializing from the first element without a stated precondition misses the empty input.

### Requested depth and early exit

Direct-answer example: The pseudocode returns 5; it returns 0 for an empty list.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
