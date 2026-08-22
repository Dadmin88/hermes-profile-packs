---
name: external-api-integration
description: Integrate an external API through authoritative contract discovery, typed mapping, authentication, pagination, limits, compatibility, resilient client behavior, and provider-isolated application boundaries.
---
# External API Integration

Use when application behavior depends on calling a third-party or separately owned HTTP/RPC/GraphQL API.

## Procedure
1. Read the provider's current authoritative documentation and pin the API/version or compatibility assumptions the integration relies on. Record deprecation/lifecycle information when the provider publishes it.
2. Define the internal operation the application needs before mirroring provider resources. Keep provider-specific fields and error quirks behind a clear adapter boundary where practical.
3. Implement authentication/authorization using the provider's supported mechanism and minimum required scopes/permissions. Resolve credentials through approved secret/identity systems, never source code or URLs.
4. Validate and normalize request/response data: identifiers, types, optional/null fields, enum expansion, units, timestamps/timezones, pagination, ordering, and partial results.
5. Define timeout, cancellation, connection behavior, rate-limit handling, pagination termination, and retry semantics based on provider guarantees and operation idempotency.
6. Classify provider failures into actionable internal categories while retaining provider request IDs/status/details needed for diagnosis without exposing secrets or sensitive payloads.
7. Handle compatibility/deprecation deliberately. Encapsulate provider version differences and add monitoring for warnings or behaviors that signal upcoming migration.
8. Add observability for call volume, latency, errors, rate-limit pressure, retries, and provider correlation identifiers.
9. Test against sandbox/test endpoints when trustworthy and supplement with contract fixtures for important success, pagination, auth, rate-limit, malformed, and error responses.
10. Define degraded behavior for provider unavailability: queue, retry later, cached/read-only mode, explicit user failure, or another product-approved response.

## Decision rules
- Provider SDKs reduce boilerplate but do not remove the need to understand the wire/business contract.
- Remote responses are untrusted data even from reputable providers.
- Do not leak provider schemas throughout the product when an adapter can protect the internal contract.
- Verify changing provider facts from current official documentation at implementation/review time.

## Quality gate
The integration is ready when the current provider contract is understood and versioned, credentials/scopes are appropriate, data is validated and mapped cleanly, limits/retries/failures are explicit, provider-specific behavior is contained, telemetry supports diagnosis, and representative provider failure/deprecation scenarios have a defined response.