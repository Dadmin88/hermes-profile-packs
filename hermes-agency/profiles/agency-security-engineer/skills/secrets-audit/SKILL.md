---
name: secrets-audit
description: Audit source, configuration, CI, artifacts, logs, client bundles, and runtime boundaries for secret exposure, excessive credential scope, unsafe storage, and incomplete rotation.
---
# Secrets Audit

Use when reviewing credential handling, preparing a release, investigating possible exposure, or hardening how applications and automation receive secrets.

## Procedure
1. Inventory the secret classes the system uses: API keys, passwords, signing keys, private keys, database credentials, session secrets, OAuth client secrets, webhook secrets, cloud credentials, CI tokens, and equivalent privileged material.
2. Trace each secret from issuance to use: authoritative store, delivery mechanism, runtime consumer, scope, lifetime, rotation mechanism, revocation mechanism, and where copies can persist.
3. Search the relevant source tree, configuration, examples, fixtures, build outputs, container images, deployment manifests, CI logs, application logs, crash reports, caches, artifacts, generated documentation, and client bundles for accidental exposure. Do not print secret values into audit output.
4. Distinguish credentials from public identifiers and configuration so remediation is focused. When a value is uncertain, treat it conservatively until its privilege and exposure are understood.
5. Review storage and injection. Prefer the platform's established secret-management mechanism over plaintext files or baked images, and ensure production secrets do not need to exist in source-controlled examples.
6. Review privilege and lifetime. Credentials should be scoped to the operations and environments that need them, with short-lived or automatically rotated credentials preferred where the platform supports them reliably.
7. Review environment separation. Development, test, staging, CI, and production should not share powerful credentials merely for convenience, and pull-request or untrusted build contexts should not receive secrets they do not require.
8. Review logging and error paths for headers, URLs, environment dumps, command echo, exception context, request bodies, and debugging helpers that can reveal credentials indirectly.
9. If exposure is confirmed or credibly suspected, prioritize revocation/rotation and containment before cosmetic source cleanup. Determine where the exposed value was usable and for how long, then review access/audit records when available.
10. After rotation, remove unnecessary copies, repair the path that caused exposure, validate the replacement credential, and add prevention or detection appropriate to the cause.

## Decision rules
- Secret scanning finds strings; the audit must determine actual privilege, reachability, and lifecycle.
- Removing a leaked secret from the latest commit does not invalidate copies already cloned, cached, logged, or published.
- Never include raw secret values in findings, tickets, chat, examples, or test evidence.
- A credential that never expires or is shared across unrelated systems carries a larger compromise blast radius.

## Quality gate
The audit is complete when secret classes and their lifecycle are mapped, likely exposure surfaces have been checked, scope and rotation are appropriate, confirmed exposures are revoked and investigated, raw secret material is absent from findings, and the root exposure path is closed rather than merely hidden.