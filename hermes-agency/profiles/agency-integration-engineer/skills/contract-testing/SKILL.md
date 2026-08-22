---
name: contract-testing
description: Test an integration boundary against explicit request, response, event, schema, error, authentication, pagination, and compatibility contracts without confusing mocks with provider truth.
---
# Integration Contract Testing

Use when two independently owned systems must evolve without silently breaking their shared interface.

## Procedure
1. Define the contract surface being protected: operations/events, schemas, required/optional fields, identifiers, types, units, auth context, errors, pagination, ordering, retries, and side effects as relevant.
2. Identify the authoritative contract source: provider specification, OpenAPI/GraphQL/IDL/schema, consumer expectations, recorded fixtures, or a jointly versioned interface.
3. Build focused contract cases for common success, empty/optional data, validation/auth errors, pagination boundaries, rate limits, conflict/retry states, and provider-specific edge behavior.
4. Validate both syntax and semantics. A response that decodes successfully may still violate units, identifiers, default behavior, enum meaning, or state transitions expected by the consumer.
5. Use generated/mocked provider behavior only for deterministic local coverage. Keep at least one validation path against a real sandbox/test provider or current authoritative fixtures when practical so mocks do not become the only source of truth.
6. For consumer-driven contracts, ensure they represent supported provider behavior rather than requiring every accidental consumer assumption forever.
7. Version fixtures/schemas and record the provider/API revision they represent. Refresh them deliberately when provider behavior changes.
8. Test compatibility across the actual rollout window, including old/new client or provider representations when mixed versions or replayed events can coexist.
9. Make failures explain which contract dimension changed and preserve provider correlation/fixture identifiers needed to investigate.
10. Run contract tests at a cadence appropriate to provider change risk, especially before upgrading SDK/API versions or after provider deprecation notices.

## Decision rules
- Mocks can prove consumer handling of a contract but cannot prove the external provider still honors it.
- Do not snapshot enormous payloads when a smaller explicit assertion better captures the contract.
- Provider quirks that matter to correctness should be encoded deliberately, not left as tribal knowledge.
- Contract tests complement end-to-end testing; they do not replace product-level validation of the assembled workflow.

## Quality gate
Contract coverage is adequate when the meaningful integration surface is explicit, important success/error/compatibility cases are executable, mocks/fixtures are tied to authoritative behavior, mixed-version assumptions are tested, and a provider or client change that violates a relied-on contract produces a precise failure before production surprises consumers.