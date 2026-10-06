# Prediction-time information and leakage: Transfer and feedback

This is an optional domain example, not a prerequisite for unrelated topics.

### Transfer task

A toy model predicts course completion at enrollment using final grade and prior course count. A held-out set has 80 completions and 20 noncompletions. Ask which feature to exclude and the always-complete baseline’s accuracy and noncompletion recall.

### Instructor key — withhold during an unaided attempt

Exclude final grade. Always-complete accuracy is 80%; noncompletion recall is 0%. Prior course count is eligible only if known at enrollment and validly sourced.

### Feedback

Explain leakage by timeline, not merely “bad feature.” If the feature decision is right but metric arithmetic is wrong, correct the denominator. Keep claimed performance limited to the supplied toy set.

### Requested depth and early exit

Direct-answer example: The post-cancellation refund leaks outcome information because it is unavailable when the prediction must be made.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
