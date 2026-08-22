---
name: oauth-integration
description: Integrate a standards-based OAuth or OpenID Connect provider using the provider-supported flow, explicit scopes, identity mapping, credential lifecycle, compatibility, and negative-path validation.
---
# OAuth Integration

Use when an application delegates sign-in, identity, or API authorization to an OAuth/OpenID Connect provider.

## Procedure
1. Define the use case first: sign-in, delegated API access, service access, device authorization, or another provider-supported workflow.
2. Verify the provider's current official documentation for supported flows, endpoints, client types, redirect rules, scopes, token/claim validation, and deprecations before implementation.
3. Configure the client using the provider's supported security profile and approved application/runtime credential handling. Public clients and confidential server-side clients have different capabilities and must be treated accordingly.
4. Request only the scopes and audience the product actually requires, and document the authority each scope introduces.
5. Use the provider/standard protections required by the selected flow and validate returned identity/authorization material with supported libraries and provider metadata rather than custom protocol logic.
6. Keep external identity separate from internal application authorization. Map stable provider identity to the correct internal account/tenant and handle re-linking or provider-side account changes deliberately.
7. Define the authorization lifecycle: initial grant, renewal, expiry, revocation/disconnect, reauthorization, account disablement, provider key/configuration changes, and user denial.
8. Handle callback and provider failures without redirect loops or ambiguous partial sign-in state. Preserve enough non-sensitive diagnostics to distinguish configuration, consent, provider, mapping, and application failures.
9. Keep provider-specific behavior behind a clear integration boundary so provider changes do not spread through unrelated application code.
10. Test the complete provider flow plus denied authorization, expired/revoked access, invalid callback state, scope changes, provider downtime, and account/tenant mapping edge cases. Request security review for changes to trust or authorization policy.

## Decision rules
- Current official provider documentation is authoritative because supported flows and provider behavior can change.
- OAuth/OpenID Connect establishes delegated identity/authority; application permissions still require server-side authorization decisions.
- Use mature protocol/provider libraries rather than inventing a custom authentication protocol.
- Provider identity fields have different stability guarantees; do not assume a display name or email is the immutable account key without provider documentation.

## Quality gate
The integration is ready when the selected provider flow matches the product use case, scopes and identity mapping are explicit, lifecycle and failure behavior are defined, provider details remain contained, current provider documentation has been verified, and end-to-end plus negative-path tests demonstrate predictable authorization behavior.