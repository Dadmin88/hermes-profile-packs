---
name: privilege-boundary-testing
description: Perform authorized defensive tests of identity, role, tenant, resource-ownership, service, node, and administrative privilege boundaries using bounded negative cases and clear evidence of allowed versus denied behavior.
---
# Privilege Boundary Testing

Use when a system has multiple privilege levels or isolation domains and needs independent validation that one identity cannot exercise another's authority.

## Procedure
1. Confirm authorized scope, test identities/tenants/resources, prohibited actions, and a safe environment or dataset before attempting cross-boundary cases.
2. Build an access matrix from the intended policy: actor/role/service identity, resource/tenant, operation, context, and expected allow/deny result.
3. Identify alternate entry paths to the same authority: UI, API, background jobs, bulk operations, exports, webhooks, internal/admin tools, direct object identifiers, and service-to-service calls as relevant.
4. Test denied cases using valid test identities and the least-destructive operation that proves the enforcement boundary. Prefer reads/no-op/dummy resources where they establish the same control.
5. Vary resource identifiers, tenant context, ownership, role transitions, stale sessions/tokens, invitation/membership state, and cached permissions when those conditions can change authorization.
6. Test privilege changes both directions: newly granted access should become available as intended, while revoked/downgraded access should stop without relying on UI disappearance alone.
7. Check service/node/background identities for broader permissions than user flows and validate that internal transport or trusted-network location does not silently bypass required authorization.
8. Capture exact identity/context, operation, resource, expected policy, observed result, and non-sensitive request/trace evidence for every confirmed failure.
9. Stop/escalate if testing risks real unrelated data, destructive administration, or systems outside scope.
10. Re-test fixes and add durable negative authorization/security regression coverage for the failed boundary.

## Decision rules
- Authentication proves identity; this assessment tests whether that identity is limited to its intended authority.
- UI hiding is not an authorization control.
- A trusted node or internal network does not automatically justify cross-tenant/resource authority unless that is the explicit architecture.
- Confirmed findings should prove an unintended boundary crossing, not merely a different error message.

## Quality gate
The assessment is complete when intended privilege boundaries are represented in an access matrix, representative alternate paths and revocation changes are tested, denied operations remain denied at the authoritative boundary, confirmed violations have bounded reproducible evidence, and fixed cases become regression coverage without exceeding authorized scope.