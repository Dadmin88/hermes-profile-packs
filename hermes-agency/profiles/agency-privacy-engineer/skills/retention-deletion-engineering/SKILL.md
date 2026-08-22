---
name: retention-deletion-engineering
description: Implement retention and deletion across primary stores, derived data, indexes, logs, queues, caches, exports, backups, and external processors with verifiable completion.
---
# Retention Deletion Engineering

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using data inventory, approved retention rules, storage topology, backup policy, vendors, and deletion requests. Do not fill material gaps with assumptions when they can change the result.
3. Translate approved retention rules into data-specific timers/events, identify exceptions, make deletion idempotent, track downstream propagation, and test restore/recovery interactions.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Deletion/expiry is measurable across every in-scope copy and backup recovery does not silently resurrect active personal data.
