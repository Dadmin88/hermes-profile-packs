---
name: offline-sync
description: Implement offline-first or offline-tolerant mobile state with local persistence, pending operations, conflict policy, retry, connectivity changes, and reconciliation.
---
# Offline Sync

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using data model, API semantics, connectivity expectations, conflict rules, local storage, and user workflows. Do not fill material gaps with assumptions when they can change the result.
3. Define authoritative state and offline scope, persist durable operation identity, queue safe mutations, reconcile conflicts, surface sync state, and test airplane/restart/reconnect sequences.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Repeated reconnect/retry cannot duplicate side effects and users can understand unsynced/conflicted state.
