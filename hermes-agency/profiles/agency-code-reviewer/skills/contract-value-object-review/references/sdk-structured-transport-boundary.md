# Structured SDK transport-boundary review

Use this reference when a compatibility API evolves from a scalar text argument to a structured message/part representation.

## Review matrix

| Input path | Expected wire result | Required checks |
|---|---|---|
| legacy `message_text="hello"` | one `text/plain` part with exact text | keyword compatibility and no behavior regression |
| mapping text part | one `text/plain` part | nonempty text, exact media type, metadata preservation |
| typed `Message` + typed `Part` text | same as mapping text | do not discard typed fields during normalization |
| mapping binary part | one raw-bytes part with caller media type | preserve NUL/0xff, exact bytes, metadata, non-`text/plain` media type |
| typed `Message` + typed `Part` binary | same as mapping binary | preserve `raw`, `media_type`, and metadata |
| empty/missing parts | reject | stable domain `ValueError`, no daemon call |
| multiple parts | reject when contract says one part | stable domain `ValueError`, no daemon call |
| text and raw together | reject | stable ambiguity error, no daemon call |
| raw with missing or `text/plain` media type | reject | binary scope cannot be inferred safely |
| malformed field types | reject before coercion/protobuf assignment | no silent `str(...)`; no leaked `AttributeError`/protobuf `TypeError` |

## Boundary probes

1. Exercise each public input shape independently and inspect the constructed protobuf request, not only the returned task handle.
2. Use binary fixtures containing `b"\\x00\\xff"` and assert byte-for-byte equality.
3. Use typed model objects as well as dictionaries; helpers written for legacy dictionaries often accidentally erase `raw`, `media_type`, or metadata from typed objects.
4. Probe empty values separately from absent values. Truthiness-based conversion (`value or default`) can turn an invalid empty binary payload into an apparently text-shaped part.
5. Pass wrong types for text, raw bytes, media type, metadata, and parts. Validation should happen at the SDK boundary with the documented exception class.
6. Confirm compatibility and identity invariants: legacy callers still work, structured and legacy representations are mutually exclusive when required, and caller-selected task IDs/idempotency keys reach the envelope unchanged.

## Review finding pattern

Report a blocker only when a reachable public input produces data loss, ambiguous wire semantics, an exception outside the API contract, or a compatibility break. Cite the final implementation line and give the smallest fix (usually preserving typed fields in normalization or adding type guards before coercion).
