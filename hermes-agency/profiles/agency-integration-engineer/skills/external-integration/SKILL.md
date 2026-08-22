---
name: external-integration
description: Implement a robust external-system integration with contract discovery, authentication, mapping, idempotency, rate limits, retries, observability, and failure isolation.
---
# External Integration

Use for third-party APIs, webhooks, queues, identity providers, payment/data providers, or system-to-system connectors.

## Procedure
1. Read authoritative provider documentation and confirm version, auth model, scopes, limits, and lifecycle behavior.
2. Define the internal/external contract mapping, including identifiers, types, timezones, pagination, and optional fields.
3. Treat remote input as untrusted and validate signatures/authentication for inbound events where supported.
4. Design idempotency and deduplication for retried requests or duplicate webhooks.
5. Handle rate limits, timeouts, retryable vs permanent errors, partial failure, and provider downtime.
6. Keep provider-specific semantics behind a clear adapter boundary when practical.
7. Add observability that can trace a failed operation without logging secrets or sensitive payloads unnecessarily.
8. Test against sandbox/fixtures and important error responses.

## Quality gate
The integration must remain understandable and recoverable when the remote system is slow, duplicated, inconsistent, or unavailable.