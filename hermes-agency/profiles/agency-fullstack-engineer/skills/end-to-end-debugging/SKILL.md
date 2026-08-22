---
name: end-to-end-debugging
description: Diagnose a full-stack defect by following one user operation across rendered UI, client state, network contract, backend logic, persistence, async work, and returned state until the first divergence is identified.
---
# End-to-End Debugging

Use when a feature fails across frontend/backend boundaries and the owning layer is not yet clear.

## Procedure
1. Capture the user-visible reproduction with exact inputs, account/role, environment, client/build revision, backend revision, data preconditions, and expected versus actual behavior.
2. Observe the rendered/client state at the failure point: UI state, console/runtime errors, route/navigation, local/persisted state, and the exact user action that triggered the operation.
3. Trace the network boundary: request method/operation, URL or RPC, payload, auth context, timing, response/status/error, retries, cancellation, and whether a newer request superseded it.
4. Correlate the request with backend logs/traces and follow validation, authorization, domain logic, database/external calls, async jobs/events, and response construction.
5. Inspect persisted state and side effects directly enough to determine whether the server changed data correctly even if the UI is stale or failed to render the result.
6. Locate the first meaningful divergence from intended behavior rather than fixing the final visible symptom. Classify it as client state/rendering, contract/mapping, backend logic, persistence/concurrency, external dependency, async delivery, or deployment/configuration.
7. Compare a successful operation or previous version when available and form one falsifiable hypothesis.
8. Implement the fix at the owning layer, then add the smallest regression tests that prove both that layer and the cross-boundary behavior at risk.
9. Re-run the original user flow in the assembled environment and verify durable side effects plus resulting UI state, not merely an individual API response.
10. Hand off to a narrower specialist when the trace shows the primary defect is outside full-stack implementation authority, preserving all correlation evidence.

## Decision rules
- A visible frontend error can originate from backend/data failure, and a backend 200 can still produce a broken user experience; trace the whole path.
- Do not change frontend and backend simultaneously until evidence requires both.
- Reproducing through direct database/API shortcuts can isolate layers but does not replace final validation through the user flow.
- Fleet/Keryx execution location is part of runtime evidence when relevant, but the full-stack fix should not hardcode around a particular node.

## Quality gate
The defect is resolved when the first divergence is supported by cross-layer evidence, the fix is made in the responsible layer, persisted and user-visible outcomes both validate correctly, regression coverage protects the relevant boundary, and the original assembled flow succeeds under the documented conditions.