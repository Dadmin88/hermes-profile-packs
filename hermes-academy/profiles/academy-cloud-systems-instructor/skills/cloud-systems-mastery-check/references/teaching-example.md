# Retries, durable state, and duplicate effects: Transfer and feedback

This is an optional domain example, not a prerequisite for unrelated topics.

### Transfer task

A fictional job queue redelivers a message after a worker crashes following commit. Ask what durable evidence prevents applying the same local database change twice and what extra issue appears if the job sends an external message.

### Instructor key — withhold during an unaided attempt

A processed-message key/check and local effect in one atomic transaction can deduplicate that local effect. An external send is outside that transaction and needs a separately reasoned coordination or deduplication contract.

### Feedback

Credit correct request tracing. Repair unknown-versus-failed inference before discussing retries. Do not label local deduplication as universal exactly-once processing.

### Requested depth and early exit

Direct-answer example: A timeout does not prove failure. The write may have committed, so a blind retry can duplicate its effect.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
