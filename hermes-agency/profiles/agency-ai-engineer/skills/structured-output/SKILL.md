---
name: structured-output
description: Design and validate model outputs as explicit machine-readable contracts with typed schemas, semantic checks, bounded recovery, versioning, and failure handling.
---
# Structured Output

Use when downstream software depends on model output having a predictable shape rather than merely readable prose.

## Procedure
1. Start from the consumer. Define exactly which fields the next system needs, their types, units, allowed values, cardinality, optionality/nullability, and the meaning of missing data.
2. Keep the schema as small as the task allows. Do not ask the model to emit fields the application can derive deterministically or metadata it does not actually consume.
3. Prefer the provider or framework's native schema-constrained output mechanism when available. Otherwise use a well-defined serialization format and strict validation; do not rely on brittle regex extraction from surrounding prose.
4. Separate syntactic validity from semantic validity. A payload can match JSON Schema while still containing impossible combinations, unsupported identifiers, inconsistent totals, fabricated evidence, or values outside business rules.
5. Encode constraints structurally when practical: enums, bounded numbers, discriminated variants, required fields, arrays with defined item types, and explicit representations for unknown/not-applicable states.
6. Decide how refusals, insufficient evidence, partial results, and tool failures are represented. Do not force a plausible-looking success object when the correct outcome is uncertainty or failure.
7. Validate every model-produced payload before trusted application code consumes it. Reject or quarantine invalid output rather than silently coercing dangerous or ambiguous values.
8. If recovery is appropriate, make it bounded and evidence-preserving. Retry with the validation failure or repair only the invalid structure; avoid unbounded loops that repeatedly spend tokens without changing the cause.
9. Version schemas when consumers can persist or depend on them. Coordinate breaking changes across prompt, validator, storage, API, tests, and downstream readers.
10. Evaluate representative edge cases including optional fields, empty collections, long text, Unicode, unknown values, conflicting evidence, refusals, truncation, schema violations, and semantically invalid but syntactically valid outputs.

## Decision rules
- Use structured output because software needs a contract, not because JSON looks more technical.
- Do not conflate schema compliance with factual correctness.
- Never execute model-produced code, SQL, shell commands, URLs, or other active content merely because it appears in a valid schema.
- Prefer explicit unknown/null/refusal states over invented data inserted to satisfy required fields.
- Keep natural-language explanation outside the contract unless a field genuinely needs it.

## Quality gate
The structured-output path is ready when the schema matches the real consumer contract, every payload is validated before use, semantic invariants are checked where required, failure and uncertainty have valid representations, recovery is bounded, and tests cover both malformed and deceptively well-formed bad outputs.