# Bounded Contract Review Reference

## Probe matrix

Use only the probes authorized by the task:

| Invariant | Probe | Expected |
|---|---|---|
| Unicode boundary | JSON escaped lone surrogate; direct surrogate in text/value/key | domain-specific error |
| Revision parity | 40 and 64 lowercase hex; 39/41/63/65; uppercase; non-string | only 40/64 accepted |
| Constructor boundary | wrong scalar type in each public constructor | domain error, never leaked built-in exception |
| Immutability | mutate source list/mapping/nested list after construction | value and hash unchanged |
| Iterable policy | string, mapping, set, custom iterable where list/tuple is required | rejected, or deterministic only if contract says so |
| Canonical identity | reordered keys; serialize/parse round-trip | equal canonical bytes/hash |
| Runtime neutrality | inspect imports, consumers, constructor side effects | no backend/host/node/persistence behavior |

## Failure classification

- **Blocker:** accepted invalid value, leaked exception outside the domain error, mutable state affecting identity, nondeterministic canonical identity, or runtime coupling that violates the contract.
- **Non-blocking gap:** missing regression coverage where implementation is otherwise demonstrably correct.
- **Out of scope:** unrelated consumers or broad suite failures not caused by the bounded diff.

## Reproduction pattern

1. Read the exact diff and changed tests.
2. Use a small probe helper that reports `domain error`, unexpected exception class, or accepted value.
3. Probe each direct constructor independently before composing the parent object.
4. Round-trip one valid object through canonical serialization and compare hashes.
5. Probe mutable and unordered collection inputs separately; do not infer their behavior from type annotations.
6. Report one smallest fix per blocker with path and line range.

## Known pitfall

`list(value)` is not an exact list/tuple validator. It accepts strings, mappings, sets, and arbitrary iterables. When list/tuple semantics are required, guard the type first, then copy to a tuple. This simultaneously closes accidental acceptance, unordered hash drift, and many non-domain exception paths.
