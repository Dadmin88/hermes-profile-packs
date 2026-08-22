---
name: authorization-review
description: Review authorization for complete server-side enforcement of roles, permissions, ownership, tenant boundaries, object access, privileged actions, and policy changes.
---
# Authorization Review

Use when reviewing access-control policy, protected operations, multi-tenant behavior, administrative functions, resource ownership, or changes that affect who may do what.

## Procedure
1. Build an actor-action-resource matrix from actual product behavior. Include ordinary users, privileged roles, service identities, background workers, support/admin paths, anonymous callers, and disabled or partially provisioned identities where relevant.
2. Identify the authoritative policy source and every enforcement point. Authorization must be enforced at trusted server or service boundaries, not inferred from hidden UI, route visibility, client state, or caller-supplied role fields.
3. Review object-level access. For every identifier, nested resource, batch operation, export, search, file, attachment, and indirect reference, verify the caller is allowed to access that specific object rather than merely the endpoint type.
4. Review tenant and organizational boundaries end to end. Query filters, caches, background jobs, event consumers, bulk operations, analytics/export paths, and administrative tools must preserve the same isolation guarantees as direct reads and writes.
5. Review role and permission composition. Look for unintended privilege inheritance, wildcard permissions, inconsistent policy precedence, stale privileges after role changes, default-allow behavior, and paths that skip the central policy layer.
6. Review privileged and sensitive operations for stronger requirements where appropriate: reauthentication, dual control, step-up authentication, explicit scope, audit logging, or narrower service credentials.
7. Check confused-deputy and service-to-service cases. A trusted service acting on behalf of a user must not silently convert the user's limited authority into the service's broader authority.
8. Review creation and mutation paths for ownership assignment, mass assignment, parent-child relationship changes, invitation/transfer flows, and privilege-bearing fields that a caller should not be able to set directly.
9. Test negative cases systematically: cross-user, cross-role, cross-tenant, guessed identifiers, nested resources, batch access, stale sessions after permission changes, disabled accounts, service credentials, and administrative boundaries.
10. Record policy gaps separately from implementation bugs. If the desired authorization rule itself is ambiguous, escalate the policy decision rather than inventing one during review.

## Decision rules
- Default deny is safer than relying on every new code path to remember an allowlist exception.
- Authentication success does not imply authorization to the requested resource.
- Filtering results after an over-broad query is not equivalent to enforcing access at the data/service boundary when sensitive data can already leak through side effects, counts, logs, or errors.
- Authorization policy should have one clear source of truth even when enforcement occurs at multiple layers.

## Quality gate
The review is complete when actor/action/resource policy is explicit, every meaningful entry point enforces it at a trusted boundary, object and tenant isolation survive indirect paths, privilege changes take effect predictably, negative tests prove denials, and unresolved policy decisions have named owners.