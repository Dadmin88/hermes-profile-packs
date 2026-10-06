# Retries, durable state, and duplicate effects: Graduated support

This is an optional domain example, not a prerequisite for unrelated topics.

### Graduated hints

Give only the smallest needed hint, then allow the learner to respond. Skip this ladder when a direct answer is requested.

1. Mark where the write became durable, separately from where the client received a reply.
2. What does the client actually know after the timeout?
3. What stable request identity could the service recognize atomically with the result?

### Requested depth and early exit

Direct-answer example: A timeout does not prove failure. The write may have committed, so a blind retry can duplicate its effect.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
