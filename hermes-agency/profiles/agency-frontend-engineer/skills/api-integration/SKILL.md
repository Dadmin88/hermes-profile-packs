---
name: api-integration
description: Integrate a frontend with backend or third-party APIs using explicit contracts, resilient async state, safe credential handling, cancellation, retries, and user-visible failure behavior.
---
# API Integration

Use when connecting a user-facing interface to a backend service, RPC endpoint, GraphQL API, event stream, or other remote data source.

## Procedure
1. Read the actual contract before writing client code. Confirm inputs, outputs, authentication context, authorization expectations, error semantics, pagination or streaming behavior, and compatibility constraints.
2. Keep transport concerns at a clear boundary. Parse and normalize remote responses into the frontend's domain/view model instead of spreading raw response shapes throughout components.
3. Represent meaningful request states explicitly: idle when relevant, loading, success, empty, validation failure, authorization failure, retryable dependency failure, and unrecoverable failure.
4. Protect against stale and duplicate work. Cancel or supersede obsolete requests where supported, deduplicate equivalent requests when appropriate, and prevent slower old responses from overwriting newer user intent.
5. Retry only when the operation and failure are safe to retry. Respect idempotency, server retry guidance, rate limits, and backoff. Never hide an uncertain write behind automatic retries that could duplicate side effects.
6. Handle optimistic updates as reversible hypotheses. Record enough prior state to roll back or reconcile, and replace optimistic values with the authoritative server result when it arrives.
7. Keep credentials and trust boundaries appropriate to the client. Do not embed server secrets in frontend bundles, URLs, logs, analytics, or persisted state. Use the application's accepted session/token mechanism rather than inventing one.
8. Make pagination, infinite loading, polling, subscriptions, and refresh behavior explicit. Define termination, ordering, deduplication, reconnect, and stale-data behavior when those modes are used.
9. Surface errors in language and placement appropriate to the user's action while retaining enough structured diagnostic information for development. Do not expose raw internal server errors or secrets.
10. Test representative success, empty, invalid, unauthorized, slow, cancelled, stale, retry, conflict, and dependency-failure paths at the client boundary.

## Decision rules
- The frontend adapts to an accepted API contract; it does not quietly redefine backend semantics in component code.
- Treat third-party responses as untrusted input and validate or narrow them when correctness depends on their shape.
- Prefer one shared integration boundary per capability over repeated ad hoc request logic across components.
- A loading spinner is not an integration strategy. The interaction must remain coherent under delay, failure, refresh, and interruption.

## Quality gate
The integration is ready when the client honors the real contract, async races and retries are safe, credentials are handled appropriately, user-visible states are complete, and tests prove behavior across the important network and failure conditions.