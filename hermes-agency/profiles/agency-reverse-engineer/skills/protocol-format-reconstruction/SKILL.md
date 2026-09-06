---
name: protocol-format-reconstruction
description: Infer and validate an undocumented protocol or file format from authorized samples, captures, and implementation evidence.
---
# Protocol and Format Reconstruction

Use when interoperability, migration, analysis, or documentation requires an evidence-backed specification for an undocumented message protocol or data format.

## Procedure

1. Define the authorized interoperability question, protocol or format boundary, versions, producers, consumers, and representative operations or sample classes.
2. Preserve original captures and samples with identifiers and hashes. Record how each was produced, including input, software version, environment, ordering, and transport framing when known.
3. Normalize presentation without destroying evidence. Separate transport framing, record boundaries, headers, payloads, checksums, compression, encryption, and encoding layers.
4. Compare controlled sample pairs that vary one semantic field at a time. Infer candidate field offsets, lengths, types, byte order, optionality, enumeration values, dependencies, and state transitions.
5. Cross-check candidates against implementation evidence such as parsers, serializers, constants, error paths, traces, or known standards. Label direct observation, inference, and speculation distinctly.
6. Test the model with withheld samples. Where authorized and safe, build a minimal parser, serializer, or replay harness that rejects malformed data and does not contact production systems by default.
7. Document framing, grammar or schema, field semantics, state machine, error behavior, version negotiation, integrity checks, examples, and unresolved fields.
8. Hand implementation of a production adapter to `agency-integration-engineer`; hand security-impact review to `agency-security-reviewer` rather than expanding reconstruction into either role.

## Quality gate

The recovered specification must explain representative and withheld evidence, preserve version and uncertainty notes, and include reproducible examples or a bounded validation harness. A field name inferred from one sample or a successful replay without semantic validation is not sufficient proof.