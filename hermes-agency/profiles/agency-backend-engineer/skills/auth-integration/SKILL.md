---
name: auth-integration
description: Integrate an accepted authentication and authorization design into backend services without weakening trust boundaries, credential handling, or access-control guarantees.
---
# Auth Integration

Use when implementing login/session/token handling, protecting backend operations, or connecting an existing identity provider or authorization model to application code.

## Procedure
1. Identify the accepted identity source, trust boundary, credential or session format, protected resources, and authorization policy before writing middleware or route checks.
2. Keep authentication and authorization separate: first establish who the caller is, then decide whether that identity may perform the requested action on the specific resource.
3. Validate credentials according to the chosen protocol and library. For signed tokens, verify the required signature and claims such as issuer, audience, expiry, and intended token type. For server sessions, validate the session identifier and server-side state. Do not invent cryptography.
4. Derive permissions from trusted server-side policy and authoritative data. Never grant access from client-supplied roles, hidden UI state, or an unverified claim merely because it is present.
5. Apply authorization at every backend operation that needs it, including resource ownership, tenant boundaries, administrative actions, background entry points, and indirect object access.
6. Handle credential lifecycle deliberately: creation, renewal, revocation, logout, account disablement, key rotation, and stale sessions or tokens. Do not place bearer credentials in URLs, logs, analytics, or error messages.
7. Protect browser session flows against the threats relevant to the chosen mechanism, including secure cookie attributes and CSRF defenses when cookies carry ambient authority.
8. Return stable, non-sensitive failure responses and record security-relevant events without logging passwords, raw tokens, session secrets, or unnecessary personal data.
9. Test missing, malformed, expired, revoked, cross-user, cross-tenant, underprivileged, and privileged cases in addition to the happy path.
10. If the work changes the trust model, credential scheme, cryptographic choices, or authorization policy, obtain review from `agency-security-engineer` rather than making that policy decision inside the integration task.

## Decision rules
- Prefer mature framework or provider primitives over custom authentication protocols.
- Least privilege applies to users, services, jobs, API keys, and administrative paths.
- A frontend access check improves UX; it is never the backend security boundary.
- Generic auth guidance does not override provider or framework documentation for protocol details.

## Quality gate
The integration is done when identity is established from a trusted source, authorization is enforced server-side at the relevant resource boundary, credential lifecycle and failure behavior are deliberate, sensitive material is not exposed, and negative tests prove access is denied when it should be.