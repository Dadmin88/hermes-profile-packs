---
name: retry-idempotency
description: Design integration retries and idempotency so timeouts, duplicate delivery, uncertain outcomes, rate limits, and replay cannot silently duplicate or lose external side effects.
---
# Retry and Idempotency

Use when an integration can be retried by clients, queues, providers, schedulers, webhooks, or operators after partial or uncertain failure.

## Procedure
1. Classify each operation as read-only, naturally idempotent, conditionally idempotent, or side-effecting/non-idempotent before adding automatic retries.
2. Identify uncertain outcomes: a timeout or disconnect may occur after the remote system accepted the request but before the caller received the response.
3. Use the provider's supported idempotency key/request identity when available and define the key around the business operation so retries/replays of the same intent converge on one effect.
4. When the provider lacks idempotency support, design an internal operation record, reconciliation check, unique business identifier, or compensation strategy appropriate to the external effect.
5. Classify failures into retryable transient conditions, throttling/rate limits, concurrency/conflict states, authorization/configuration failures, validation/business failures, and unknown outcomes.
6. Retry only safe/retryable classes using bounded attempts, backoff, jitter, and provider retry guidance. Respect server-supplied retry windows or rate-limit resets where applicable.
7. Persist enough attempt/result state to resume after process/node failure without losing whether an external effect may already have occurred.
8. Define reconciliation for operations that remain uncertain after retries: query remote state, await a webhook/event, compare a provider operation ID, or route to manual review.
9. Bound queues and retry storms so provider degradation does not amplify traffic or starve healthy work.
10. Test duplicate requests, timeout-after-acceptance, rate-limit responses, permanent errors, process restart, replay, and retry exhaustion against fixtures or provider sandboxes.

## Decision rules
- “Retry on any exception” is unsafe for side effects.
- An idempotency key should represent one business intent, not merely one network attempt.
- Exactly-once effects require an end-to-end guarantee; design for duplicate/uncertain execution unless every boundary proves otherwise.
- Keryx/Fleet may retry transport or placement after node failure; integration task semantics must still remain safe when work is resumed elsewhere.

## Quality gate
The integration is reliable when retryable versus permanent failures are explicit, duplicate/uncertain execution converges safely, attempt state survives interruption, retry amplification is bounded, unresolved outcomes have a reconciliation path, and fault tests prove repeated delivery cannot silently duplicate consequential effects.