# Loop invariants and boundary cases: Worked reasoning

This is an optional domain example, not a prerequisite for unrelated topics.

### Worked example

Start total at 0. After processing 2, −1, 4, the successive totals are 2, 1, 5. Invariant: after each iteration, total equals the sum of the values processed so far. An empty list returns 0 because there are no iterations. This linear scan uses Θ(n) time and Θ(1) auxiliary storage under a unit-cost arithmetic model.

### Requested depth and early exit

Direct-answer example: The pseudocode returns 5; it returns 0 for an empty list.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
