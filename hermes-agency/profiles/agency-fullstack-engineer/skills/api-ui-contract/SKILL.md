---
name: api-ui-contract
description: Define and implement the contract between a user-facing interface and its backend API so user states, server semantics, validation, authorization, concurrency, and compatibility remain coherent across both sides.
---
# API to UI Contract

Use when one bounded feature spans frontend and backend and the two layers need a clear shared behavior contract.

## Procedure
1. Start from the product flow and list every user-visible state/action the backend must support: load, empty, success, validation, permission, conflict, slow/pending, retry/recovery, and destructive confirmation where relevant.
2. Define backend operations around domain/user intent and map their inputs/outputs/errors to those UI states without leaking raw persistence or provider structures into components.
3. Specify field types, identifiers, optional/null behavior, enums/states, units, ordering, pagination, and timestamps clearly enough that both sides make the same assumptions.
4. Keep validation ownership explicit: client validation improves feedback, while server-side validation/authorization/domain invariants remain authoritative.
5. Define concurrency and stale-data behavior for edits, optimistic changes, duplicate submissions, conflicts, refresh, cancellation, and out-of-order responses where relevant.
6. Separate authentication state, authorization failures, missing resources, validation problems, conflicts, dependency failures, and unexpected server failures so the UI can respond appropriately.
7. Define compatibility when frontend/backend versions may roll independently or clients can remain cached. Avoid changes that require impossible lockstep deployment without an explicit plan.
8. Encode the contract using the project's normal schemas/types/fixtures and add tests on both client handling and server behavior for the most important states.
9. Validate the complete flow against the real assembled frontend/backend, including at least one negative/conflict/failure path.

## Decision rules
- The API is not merely a database-shaped transport for the UI.
- Frontend state should reflect server truth without duplicating server authorization/business invariants as authority.
- If the contract becomes a shared public/cross-team interface, involve `agency-software-architect` or the owning Backend/Frontend specialists rather than making a local full-stack decision silently.
- Provider or Fleet node details should remain behind backend/runtime boundaries unless the product explicitly exposes them.

## Quality gate
The contract is ready when every important UI state maps to explicit server behavior, types/errors/concurrency are understood on both sides, authorization and business invariants remain server-enforced, compatibility is workable, and client/server plus assembled-flow tests prove the shared semantics.