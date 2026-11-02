# Retries, durable state, and duplicate effects: Worked reasoning

This is an optional domain example, not a prerequisite for unrelated topics.

### Worked example

Trace client → service → durable store → service → client. The store commits record R; the final reply is lost. A repeat can create R2 unless the operation has a durable idempotency mechanism. In this toy model, a stable request key is atomically stored with the result; repeating the same key and payload returns that result. Key scope, expiry, mismatched payloads, and external side effects require additional design; the model grants no universal exactly-once guarantee.

### Requested depth and early exit

Direct-answer example: A timeout does not prove failure. The write may have committed, so a blind retry can duplicate its effect.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
