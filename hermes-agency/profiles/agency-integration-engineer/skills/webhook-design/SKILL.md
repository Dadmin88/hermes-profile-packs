---
name: webhook-design
description: Design inbound or outbound webhooks with authenticated origin, stable event contracts, fast acknowledgement, duplicate/reorder handling, retries, idempotent processing, observability, and replay recovery.
---
# Webhook Design

Use when one system asynchronously notifies another about events over HTTP or a similar push callback.

## Procedure
1. Define event ownership and semantics: event type, stable event ID, resource/tenant identity, occurrence time, schema/version, ordering guarantees, and whether payload is snapshot, delta, or reference requiring a follow-up fetch.
2. For inbound webhooks, authenticate origin using the provider's supported signature/mTLS/token mechanism and validate against the exact raw/body representation the scheme requires before trusting the payload.
3. Apply timestamp/replay-window checks when the signature protocol supports them, while keeping legitimate provider retries possible.
4. Return acknowledgement quickly after durable acceptance when processing may be slow. Do not hold the provider request open for unrelated downstream work if a queue/durable inbox is appropriate.
5. Assume duplicate delivery unless the provider explicitly proves otherwise. Deduplicate using stable event/business identifiers and make downstream effects idempotent.
6. Do not assume global order. Use event versions/sequence numbers or fetch authoritative current state when correctness depends on ordering and the provider supplies such mechanisms.
7. For outbound webhooks, define retryable status/network failures, bounded backoff, delivery timeout, signing/secret rotation, endpoint disablement, and dead-letter/manual replay policy.
8. Protect tenant/resource boundaries. A validly signed event still needs schema validation and correct mapping to the authorized internal tenant/resource.
9. Record delivery/receipt state, attempts, result, provider/request IDs, event ID/type, and non-sensitive diagnostics so a specific event can be traced or replayed.
10. Test valid, invalid signature, expired/replayed, duplicate, out-of-order, malformed, slow, failing endpoint, retry exhaustion, and manual replay behavior.

## Decision rules
- Webhooks are at-least-once, unordered inputs unless a stronger provider contract is explicitly documented and tested.
- Signature verification must follow the provider protocol exactly; do not invent ad hoc hashing.
- HTTP 2xx should mean the event reached the durability/acceptance boundary promised to the sender, not necessarily that every downstream side effect finished.
- Replays should preserve idempotency and audit history rather than masquerade as brand-new events.

## Quality gate
The webhook path is ready when origin and tenant mapping are validated, events have stable contracts/identity, durable acceptance is clear, duplicates and reordering cannot corrupt state, retries/replay are bounded and observable, and fault tests demonstrate recovery from real delivery behavior.