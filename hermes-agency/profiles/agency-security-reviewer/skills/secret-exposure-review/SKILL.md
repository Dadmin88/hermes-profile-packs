---
name: secret-exposure-review
description: Review code, configuration, logs, artifacts, builds, tests, documentation, telemetry, and runtime boundaries for accidental exposure of credentials, tokens, keys, connection material, or other secrets.
---
# Secret Exposure Review

Use when a change touches authentication material, configuration, logging, deployment, build artifacts, integrations, support tooling, or any path that could reveal sensitive credentials.

## Procedure
1. Identify the secret types and where they are expected to originate, be stored, injected, used, rotated, and destroyed. Distinguish secrets from ordinary identifiers/configuration.
2. Inspect changed source/configuration and relevant generated/vendor files for embedded credentials, example values that are actually live, private keys, tokens, passwords, connection strings, or sensitive recovery material.
3. Trace runtime injection and propagation through environment/config stores, process arguments, files, containers, network requests, child processes, tools/plugins, and external integrations as relevant.
4. Review logs, errors, tracing, metrics labels, analytics, crash reports, support exports, debugging output, and screenshots for raw or partially exposed secret material.
5. Review build and distribution artifacts: bundles, source maps, images, archives, package metadata, generated configs, caches, CI artifacts, and mobile/web client output that may contain server-side secrets.
6. Review repository/history and test fixtures when the change suggests a secret may already have been committed. Treat removal from the current file as separate from revocation/rotation and history exposure response.
7. Check least exposure: only components that need a credential should receive it, with the narrowest supported scope and lifetime appropriate to the architecture.
8. Verify redaction/masking preserves diagnostic usefulness without allowing reconstruction of the full credential from repeated fields or correlated logs.
9. If a real credential exposure is confirmed, stop unnecessary handling, preserve minimal evidence, route rotation/revocation/incident actions to the security/operator owner, and avoid copying the secret into the finding.
10. Add preventive checks appropriate to the failure class, such as repository secret scanning, structured logging filters, build assertions, or configuration validation, then re-test the exposed path.

## Decision rules
- Never include a live secret in a review report merely to prove it exists; identify location/type and use redacted evidence.
- Deleting an exposed credential from source does not revoke it.
- Client-side/browser/mobile code and distributed artifacts must be assumed inspectable by recipients.
- Agency profiles must not contain local credentials; Fleet/Keryx/Nodescale runtime credentials belong to their managed runtime/security boundaries, not profile packages.

## Quality gate
The review is complete when secret lifecycle and propagation are traced, source/log/artifact/client exposure paths are checked, confirmed exposures use non-sensitive evidence and trigger ownership for rotation/response, least exposure is verified, and preventive controls are added or recommended for the exact failure path.