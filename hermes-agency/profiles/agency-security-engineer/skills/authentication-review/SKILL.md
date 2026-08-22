---
name: authentication-review
description: Review an authentication system or change across identity proof, credential handling, sessions or tokens, recovery, revocation, abuse resistance, logging, and negative-path validation.
---
# Authentication Review

Use when reviewing login, signup, SSO, sessions, tokens, API credentials, password reset, account recovery, MFA, or any change that establishes caller identity.

## Procedure
1. Map the complete authentication lifecycle: enrollment or credential issuance, authentication, session/token creation, renewal, privilege-sensitive reauthentication, logout/revocation, account disablement, recovery, and credential rotation.
2. Identify every credential and trust assertion involved, who issues it, where it is stored, how it is transmitted, how long it remains valid, and which component verifies it.
3. Confirm mature protocol and library primitives are used correctly rather than custom cryptography or home-grown authentication protocols. Verify protocol-critical fields and claims according to the chosen mechanism.
4. Review credential storage and transport. Passwords, bearer tokens, refresh tokens, session identifiers, private keys, recovery codes, and equivalent secrets must not leak into URLs, logs, analytics, client bundles, crash reports, or unrelated storage.
5. Review session/token lifecycle for fixation, replay, excessive lifetime, missing rotation or revocation, stale privilege after account changes, logout gaps, and inconsistent behavior across devices or services.
6. Review abuse controls around login, recovery, enrollment, MFA challenges, and credential issuance. Controls should slow or contain automated abuse without creating trivial account-lockout denial of service.
7. Review browser-specific protections where relevant, including secure cookie attributes, CSRF defenses for ambient credentials, redirect handling, and safe handling of OAuth/OIDC state and return destinations.
8. Verify account recovery does not become a weaker alternate authentication path. Sensitive changes should require appropriate proof and invalidate credentials when the threat model requires it.
9. Review security event logging and alerting. Record enough to investigate suspicious authentication activity while excluding raw credentials and unnecessary sensitive data.
10. Test missing, malformed, expired, revoked, replayed, cross-account, disabled-account, changed-privilege, recovery, and abuse-rate cases in addition to normal authentication.

## Decision rules
- Authentication proves identity; authorization must still decide access to each protected action or resource.
- Client-side checks are never the authentication enforcement boundary.
- Longer-lived credentials require stronger storage, revocation, and compromise assumptions.
- Generic guidance never overrides the security requirements of the actual protocol or identity provider.

## Quality gate
The review is complete when the identity chain and credential lifecycle are explicit, verification and revocation are enforced at trusted boundaries, recovery is not a bypass, sensitive credentials are not exposed, abuse cases are tested, and residual authentication risks have owners.