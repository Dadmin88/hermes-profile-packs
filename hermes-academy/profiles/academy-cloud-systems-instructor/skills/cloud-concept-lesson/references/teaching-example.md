# Retries, durable state, and duplicate effects: Diagnostic and misconception distinctions

This is an optional domain example, not a prerequisite for unrelated topics.

### Diagnostic

In a fictional service, a request commits a record but its reply is lost. Ask whether a timeout proves the write failed and what a retry might do.

### Distinguish the error

Timeout means unknown outcome, not proven failure. Retrying blindly can duplicate effects. A load balancer or extra process does not make volatile state durable. Misreading which arrow lost the reply is a tracing slip.

### Requested depth and early exit

Direct-answer example: A timeout does not prove failure. The write may have committed, so a blind retry can duplicate its effect.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
