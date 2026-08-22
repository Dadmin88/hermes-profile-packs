---
name: authorization-review
description: Independently review implemented authorization for role, ownership, tenant, service, node, and administrative boundaries by tracing authoritative policy decisions and representative denied cases.
---
# Authorization Review

Use when code or configuration changes who can read, change, execute, route, administer, or otherwise act on protected resources.

## Procedure
1. Identify actors, authentication context, resources, operations, tenants/ownership, privileged roles/services, and the intended authorization policy from requirements or architecture.
2. Locate the authoritative enforcement points in the implementation. Distinguish frontend visibility, route middleware, service policy, database filters, infrastructure policy, and downstream provider checks.
3. Trace representative allowed and denied operations end to end, including direct object/resource access and alternate interfaces that reach the same capability.
4. Check that authorization uses trusted server-side identity/context rather than client-supplied roles, tenant IDs, ownership claims, hidden form fields, or unverified metadata.
5. Review object/resource lookup order for cross-user or cross-tenant exposure and confused-deputy behavior. A valid ID should not grant authority by itself.
6. Review privileged service/background/node identities for excessive scope and whether internal network/transport trust bypasses policy unintentionally.
7. Check permission lifecycle: role/membership change, account disablement, token/session caching, revocation, and stale authorization state where relevant.
8. Review failure behavior for information leakage and consistent denial without turning response differences into unnecessary resource-existence disclosure.
9. Require or run focused negative tests for the highest-risk boundaries and verify the authoritative layer denies them, not merely the UI.
10. Report findings with violated policy/boundary, actor/resource/operation, reachable path, impact, exact evidence, and remediation owner.

## Decision rules
- Authentication establishes identity; authorization must still evaluate what that identity can do to this resource in this context.
- Internal/Fleet/Keryx transport identity does not automatically imply application-level resource authority.
- UI checks are useful UX controls but never sufficient authorization evidence for server-side capabilities.
- Security Reviewer independently evaluates the implementation; Security Engineer owns redesigning the security model when policy changes are required.

## Quality gate
The review is complete when intended policy maps to actual enforcement points, representative alternate paths and negative cases are evaluated, authority comes from trusted context, lifecycle/stale-state risks are addressed, and blocking findings identify a concrete unintended privilege or isolation failure with reproducible evidence.