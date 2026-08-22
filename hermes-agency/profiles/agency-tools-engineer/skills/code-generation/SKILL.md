---
name: code-generation
description: Build maintainable code generators with explicit source schemas, deterministic output, minimal generated surface, safe overwrite rules, versioning, validation, and a migration path for generated consumers.
---
# Code Generation

Use when repeated boilerplate or schema-driven artifacts can be generated more reliably than hand-maintained copies.

## Procedure
1. Define the authoritative input model/schema and the output contract. Generate only information that can be derived reliably from the source of truth.
2. Decide whether generated files are committed, ephemeral build output, or created once and then owned manually. Make that lifecycle obvious in headers/docs/tool behavior.
3. Keep generated output minimal, readable, formatted, and idiomatic enough that failures can be inspected. Avoid generating large abstraction layers when a runtime library or shared component would evolve more safely.
4. Make generation deterministic for the same inputs/tool version, controlling ordering, timestamps, random identifiers, locale, and environment influence where they would create meaningless diffs.
5. Define overwrite behavior. Never silently destroy user-owned edits; separate protected generated regions, regenerate whole owned files, or fail with guidance according to the lifecycle model.
6. Validate inputs before writing and generate into temporary/staged output where practical so partial failure cannot leave a half-updated tree.
7. Version the generator and input schema when consumers depend on output shape. Define migrations for breaking changes rather than assuming every project can simply regenerate.
8. Add golden/fixture tests for representative inputs plus invalid, empty, unusual identifiers, ordering, and compatibility cases. Compare semantics rather than brittle formatting where possible.
9. Verify generated output builds/tests/lints using the normal consumer toolchain, not only that the generator itself exits successfully.
10. Document how to invoke, update, troubleshoot, and tell generated ownership from hand-written code.

## Decision rules
- Generate repeated facts; do not generate business logic that developers need to understand and evolve independently without a compelling reason.
- Deterministic output keeps diffs reviewable and caches trustworthy.
- A generator is a maintained product; copied generated code still needs an upgrade story if its source contract evolves.
- Never bake local machine paths, credentials, or Fleet node identities into generated output unless they are explicitly supplied runtime configuration and truly belong there.

## Quality gate
The generator is ready when source-of-truth ownership is explicit, repeated runs are deterministic and safe, user edits cannot be silently destroyed, version/migration behavior is defined, representative generated output passes its real toolchain, and another developer can regenerate or upgrade without private knowledge.