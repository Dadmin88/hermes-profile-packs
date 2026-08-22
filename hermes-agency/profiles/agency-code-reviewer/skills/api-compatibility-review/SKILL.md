---
name: api-compatibility-review
description: Review public or cross-component interface changes for consumer breakage across syntax, semantics, errors, defaults, ordering, timing, schemas, deprecation, and migration behavior.
---
# API Compatibility Review

Use when a change modifies an API, RPC, event, schema, file format, CLI contract, library interface, component contract, or other surface consumed outside the implementation unit.

## Procedure
1. Identify the real consumers and the contract they observe, including undocumented behavior that existing callers may rely on. Distinguish public/external consumers from coordinated internal consumers, but do not assume internal means safely breakable.
2. Compare before and after at the wire or caller boundary: operation names, parameters, field names/types, requiredness, nullability, enums, defaults, validation, response shape, errors, ordering, pagination, identifiers, side effects, and protocol semantics.
3. Look for semantic breaks hidden behind type-compatible changes: changed units, timezone, sorting, interpretation of empty/null, retry semantics, permission behavior, idempotency, consistency guarantees, precision, case sensitivity, or default scope.
4. Review additive changes critically. New enum variants, response fields, events, redirects, warnings, or larger payloads can break exhaustive consumers, strict decoders, caches, signatures, size assumptions, or UI layout even when old fields remain.
5. Review removals and renames for deprecation path, migration documentation, version negotiation, compatibility shims, and how long mixed consumer versions can coexist.
6. Review event/schema evolution for producers and consumers deployed at different times. Confirm old consumers can tolerate new producers and new consumers can handle old data when rolling deployment or replay makes that possible.
7. Review error compatibility. Changing status codes, error types/codes, retryability, or whether an operation partially succeeds can be as breaking as changing the success payload.
8. Check generated clients, SDKs, schemas, examples, contract fixtures, and documentation that represent the interface. A source-level change may require regenerating or publishing dependent artifacts.
9. Require contract or consumer tests for material compatibility claims. Test representative old callers/data against the new implementation when feasible rather than relying on inspection alone.
10. Report each break with affected consumer, observed contract, migration consequence, and the least risky path forward.

## Decision rules
- Compatibility is defined by consumer-observable behavior, not by whether the compiler accepts the new code.
- "Additive" is a hypothesis to verify, not an automatic guarantee.
- Versioning is not a substitute for a migration strategy; too many live versions create their own operational cost.
- If all consumers are changed atomically under one deployment boundary, a deliberate break may be acceptable, but that coordination must be real and verified.

## Quality gate
The review is complete when actual consumers and observable contracts are mapped, syntactic and semantic differences are evaluated, mixed-version and error behavior are considered, migration/deprecation is explicit for intentional breaks, and compatibility claims are backed by executable or consumer-level evidence.