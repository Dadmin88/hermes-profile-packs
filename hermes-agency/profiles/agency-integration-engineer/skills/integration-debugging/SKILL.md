---
name: integration-debugging
description: Diagnose cross-system integration failures by reconstructing one operation across internal mapping, authentication, network, provider request/response, retries, asynchronous callbacks, persisted state, and reconciliation.
---
# Integration Debugging

Use when an external integration fails, disagrees with local state, behaves intermittently, or produces an unexplained partial outcome.

## Procedure
1. Capture one failing business operation with exact time, internal operation/request ID, provider correlation IDs, account/tenant context, code/config/provider API revision, and expected versus actual result.
2. Trace the operation end to end: internal trigger, data mapping, auth context, outbound request or inbound event, network/provider result, retries, persistence, asynchronous webhook/event, and final application state.
3. Redact secrets/sensitive values while preserving structural evidence such as status codes, field presence, timestamps, identifiers, headers/metadata safe to log, and provider error codes.
4. Determine the first divergence: wrong local mapping, invalid credential/scope/config, network/TLS/DNS issue, provider validation/error, rate limit, timeout/uncertain result, stale provider state, dropped/duplicate callback, retry bug, or downstream local processing failure.
5. Compare with a successful operation under similar conditions and with current provider documentation/status where provider behavior or availability may have changed.
6. Check local and provider clocks/time zones, pagination/cursor state, idempotency keys, webhook delivery attempts, event ordering/version, and retries when symptoms are intermittent or duplicate/missing.
7. Form one evidence-backed hypothesis and reproduce it with a sandbox, fixture, replay, or controlled request without causing duplicate production side effects.
8. Fix the owning boundary, then add a regression contract/integration test or replay fixture for the observed failure class.
9. Reconcile any operations left in uncertain/partial state before declaring the bug fixed.
10. Record root cause, provider behavior relied on, exact repair, affected operations requiring cleanup, and monitoring needed to detect recurrence.

## Decision rules
- The provider error may be a symptom of bad local mapping, and a local error may be a consequence of provider behavior; trace the complete operation.
- Do not “just retry” an uncertain side effect until idempotency/reconciliation is understood.
- Provider status pages and docs are useful evidence but do not replace the trace of the affected request/event.
- If failure is primarily Fleet/Keryx transport between Hermes nodes rather than the external provider boundary, hand off the trace to the distributed runtime owner.

## Quality gate
The investigation is complete when one failing operation is traceable across every integration boundary, the first divergence and owning layer are supported by evidence, uncertain state has been reconciled, the fix is covered by executable evidence, and provider-specific assumptions are documented for future diagnosis.