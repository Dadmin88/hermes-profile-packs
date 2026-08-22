---
name: contract-value-object-review
description: "Use when reviewing bounded schema/value-object diffs."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [code-review, contracts, value-objects, immutability, canonicalization, unicode, validation]
    related_skills: [requesting-code-review, runtime-architecture-auditing, test-driven-development]
---

# Contract and Value-Object Review

## Use when

Use for bounded read-only reviews of schema/value-object changes: frozen dataclasses, DTOs, recipe/config documents, parser contracts, canonical JSON identities, hashes, revisions, and other runtime-neutral domain values. This is a class-level review skill, not a feature-specific checklist.

## Review boundary

1. Resolve the exact worktree and base revision before inspecting code.
2. Confirm the diff scope and status, including untracked files when relevant.
3. Read changed implementation and direct tests; inspect nearby consumers only to verify runtime neutrality and public-constructor reachability.
4. Do not edit files or run broad tests when the task is explicitly bounded/read-only. Use only focused tests or small direct probes authorized by the task.
5. Return either `NO BLOCKER` or blocker path/line plus the smallest viable fix. Separate non-blocking test gaps from release blockers.

## Constructor parity and error boundaries

Treat every public constructor as part of the contract, not just `from_dict`, `from_json`, or deserialization helpers.

- Enumerate direct constructors, classmethods, and public normalization entry points.
- Parser and direct-constructor validation must accept and reject the same semantic values.
- Invalid inputs must consistently raise the domain-specific error. Look for leaked `TypeError`, `UnicodeError`, `RecursionError`, `KeyError`, `AttributeError`, and `OverflowError` paths.
- Type guards should run before regex matching, `.encode()`, iteration, mapping access, or serialization.
- Do not rely on dataclass annotations as runtime validation.
- If a nested object has its own constructor contract, require the exact intended type or a clearly specified protocol rather than a lookalike that bypasses validation.

## Deep immutability

A frozen outer dataclass is not enough. Trace every nested field reachable from public constructors.

- Copy caller-owned mutable lists into tuples.
- Copy nested lists recursively into tuples.
- Copy mappings into read-only mappings and recursively normalize values.
- Validate before or during normalization so invalid mutable inputs cannot pass through coercion.
- Do not coerce arbitrary iterables unless iterable semantics are explicit. Strings and mappings may be accidentally accepted; sets and other unordered iterables can make canonical ordering and hashes nondeterministic.
- Mutate original inputs after construction and verify the value and identity remain unchanged.

## Capability-bearing value objects and side-effect boundaries

A frozen or redacted dataclass is not automatically a safe capability. Treat every direct constructor, `dataclasses.replace`, and low-level mutation path as reachable when the value controls filesystem or other irreversible side effects.

1. Put ordinary invariant checks in `__post_init__`, but also revalidate at the side-effect boundary. A caller can manufacture a frozen instance with `object.__setattr__` or `dataclasses.replace`; use-site checks must not trust that construction previously ran correctly.
2. Require exact domain types for capability-bearing values and reject arbitrary lookalike objects before attribute access. Validate every field that affects authority: source path type and root constraints, bounded destination filename grammar, identity snapshot fields, owner UID, size, and provider-neutral reference identity.
3. Derive the destination only from a fixed execution-owned root plus one freshly validated plain filename. Check that the resulting path remains directly under the root, create it with exclusive/no-follow flags, and make cleanup prove that no execution copy remains outside the owned slot.
4. Filesystem TOCTOU checks must repeat the complete source invariant at every relevant phase, not only device/inode/size identity. Recheck regular-file type, same UID, exact `0600` mode, single hard link, and size bound both before copying and after the read; reject and remove the destination copy on any mismatch. Open with `O_NOFOLLOW` and read through the source FD so the canonical source is never modified.
5. Add adversarial probes for forged exact instances, traversal-like destination names, symlink sources/targets, mode or link-count changes between checks, arbitrary objects with explosive hooks, plaintext `repr`/logging/durable-state paths, and cleanup after partial-copy failure. A normal valid capability control must still copy and then clean up successfully.

## Controlled Unicode and canonical UTF-8

Find every `.encode("utf-8")`, `json.dumps(..., ensure_ascii=False)`, and canonicalization boundary. Lone surrogates and malformed Unicode must produce the public domain error, not leaked `UnicodeEncodeError`. Apply the same policy to ordinary text, extension values, extension keys, repository/identifier fields, and nested values reaching canonicalization. Preserve exception causes only as implementation detail.

## Revision and digest parity

Compare parser and constructor paths side by side. A Git object ID supporting SHA-1 and SHA-256 is exactly 40 or 64 lowercase hexadecimal characters: no prefixes, whitespace, uppercase, or other lengths. Enforce identical grammar at `from_dict` and direct-constructor boundaries. Validate digest strings by exact type, grammar, and length before regex operations or hashing.

## Canonical hash stability and runtime neutrality

Canonical identity must depend only on semantic content. Use deterministic key ordering and compact serialization; exclude floating point or define an explicit cross-runtime representation. Normalize tuple/mapping values into one JSON-compatible form before hashing. Round-trip through canonical serialization, reorder input object keys, and mutate caller inputs after construction; hashes should remain stable. Reject unordered inputs unless deterministic ordering is explicitly part of the contract.

Inspect imports and consumers for runtime neutrality: logical contracts must not select a node/backend/scheduler, include host paths or execution plans, persist runtime state, or trigger side effects merely by construction or canonicalization.

## SDK transport-adapter boundaries

When a public SDK accepts both legacy convenience values and structured message objects, review the conversion boundary as part of the contract—not merely the protobuf wrapper.

- Trace every supported input shape (for example, mapping-shaped messages and typed `Message`/`Part` objects) into the wire message. Assert that text, raw bytes, media type, and metadata survive each path; a text-only compatibility helper must not silently discard structured fields.
- Validate after normalization at one canonical boundary, but preserve enough source information to distinguish text from binary. Enforce the stated cardinality and ambiguity rules there (for example, exactly one part; nonempty `text/plain` text or raw bytes with a non-text media type).
- Type-check user-controlled fields before `str(...)`, `.get(...)`, iteration, or protobuf assignment. Do not silently stringify invalid text/media values or let protobuf `TypeError`/`AttributeError` escape when the SDK promises a domain-level validation error. Defaults must be presence-aware: do not use truthiness fallbacks such as `value or b""`, `value or "text/plain"`, or `value or {}` before validation, because explicit falsey values (`False`, `0`, `""`, `[]`) are malformed inputs, not missing fields.
- Test both typed and mapping inputs, including binary/NUL/0xff payloads, metadata, empty/missing fields, explicit falsey field values, text+raw ambiguity, wrong media types, multiple parts, and malformed field types. Verify the daemon request fields/bytes, not only the high-level return value.
- Check backward compatibility at the public call boundary: legacy keyword arguments remain valid, structured and legacy representations are mutually exclusive when required, and caller-selected task/idempotency identities are unchanged.

For a compact structured-message adapter checklist and reproduction matrix, see `references/sdk-structured-transport-boundary.md`.

## Focused verification and reporting

Use the compact matrix in `references/bounded-contract-review.md`. Prefer focused tests and direct probes over broad suites. Record actual outputs and limitations; never claim a test ran when setup prevented it.

Report:

- **Blocker:** `path:line` — concise violated invariant.
- **Smallest fix:** one minimal implementation change.
- **Verification:** focused tests/probes actually run.
- If clear, say `NO BLOCKER` and list concise validation notes.

A frequent blocker is `list(value)` used to freeze a collection. If the contract requires list/tuple semantics, add an exact type guard, then normalize to a tuple. This prevents accidental strings/mappings/sets, nondeterministic hashes, and leaked errors.

See `references/bounded-contract-review.md` for reusable probes, failure classifications, and review transcript patterns.
