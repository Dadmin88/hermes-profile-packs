---
name: state-management
description: Design and implement frontend state ownership, transitions, synchronization, persistence, and async behavior without duplicating sources of truth or creating race-prone UI logic.
---
# State Management

Use when a frontend feature introduces or changes client state, shared state, server-derived data, navigation state, forms, optimistic updates, or multi-step interaction behavior.

## Procedure
1. Inventory the state before choosing a library or pattern. Classify each value as server-derived/cache state, navigation or URL state, local interaction state, form/input state, shared application state, or persisted preference.
2. Keep each fact owned in one place. Derive values when they can be computed reliably instead of storing synchronized copies that can drift.
3. Put state as close as practical to the behavior that owns it. Lift or centralize state only when multiple consumers truly require shared ownership or coordinated transitions.
4. Define lifecycle and transitions explicitly. For workflows with mutually exclusive modes, multi-step progress, cancellation, retries, or invalid transition risk, model named states and events rather than accumulating unrelated booleans.
5. Separate remote/server state from durable client intent. Account for loading, stale data, refresh, invalidation, pagination, optimistic updates, rollback, and reconciliation with the authoritative server result.
6. Handle concurrency deliberately. Prevent stale responses, duplicate submissions, out-of-order completion, abandoned requests, and unmounted or superseded work from overwriting newer state.
7. Treat persistence as a data contract. Persist only what should survive reload/restart, version stored shapes when they may evolve, provide migration or reset behavior, and do not persist secrets merely for convenience.
8. Follow the framework and repository's established state conventions unless there is evidence they cannot represent the required behavior cleanly. Do not introduce a global store to solve a local problem.
9. Validate state transitions through realistic interactions, including refresh/navigation, rapid repeated actions, failure/retry, cancellation, optimistic rollback, and stale-data cases where applicable.

## Decision rules
- Prefer derived state over duplicated state.
- Prefer explicit transitions over combinations of flags when state complexity grows.
- A cache is not automatically the source of truth; know what system owns the authoritative value.
- Do not move server authorization or business invariants into client state. The frontend may reflect them, but the backend must enforce them.
- Optimize state subscriptions only after identifying actual re-render or responsiveness cost.

## Quality gate
State management is ready when ownership is unambiguous, important transitions are representable without contradictory states, async races are controlled, persistence is intentional, and tests prove the user-visible behavior under success, failure, and interruption.