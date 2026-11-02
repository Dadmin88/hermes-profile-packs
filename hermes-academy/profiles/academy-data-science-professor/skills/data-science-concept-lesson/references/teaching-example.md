# Prediction-time information and leakage: Diagnostic and misconception distinctions

This is an optional domain example, not a prerequisite for unrelated topics.

### Diagnostic

A fictional model predicts cancellations when a booking is made. Features include booking price and the refund amount recorded after cancellation. Ask which feature leaks the outcome and why.

### Distinguish the error

A highly predictive feature can be invalid when unavailable at prediction time. Randomly splitting repeated rows from the same customer may overstate performance for unseen customers. Preprocessing fitted on all data leaks held-out information even without the label.

### Requested depth and early exit

Direct-answer example: The post-cancellation refund leaks outcome information because it is unavailable when the prediction must be made.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
