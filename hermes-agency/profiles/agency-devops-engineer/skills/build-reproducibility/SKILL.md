---
name: build-reproducibility
description: Make builds traceable and reproducible by controlling inputs, dependency resolution, toolchains, generated state, environment influence, artifact identity, and verification across clean builders.
---
# Build Reproducibility

Use when the same source can produce inconsistent artifacts, releases cannot be traced confidently, or builds depend on undeclared machine state.

## Procedure
1. Enumerate all build inputs: source revision, dependency manifests/locks, toolchain/runtime versions, build configuration, generated sources, assets, environment variables, external downloads, timestamps, locale/timezone, and platform architecture as relevant.
2. Pin or constrain dependency and toolchain resolution to the level required by the project's release guarantees. Record intentional floating inputs rather than hiding them.
3. Remove undeclared local-machine dependencies. A clean builder should not need developer caches, global packages, home-directory files, private paths, or manually prepared generated output unless those inputs are explicitly supplied.
4. Treat code generation and vendoring as controlled inputs. Define whether generated artifacts are committed or deterministically produced and validate they match their source definitions.
5. Isolate secrets from build content unless an artifact genuinely requires signing or another controlled release operation. Secrets should not change ordinary artifact bytes accidentally.
6. Normalize nondeterministic metadata where practical when bit-for-bit reproduction matters; otherwise define the artifact properties that must match and why.
7. Build the same revision from at least one clean/independent environment and compare artifact digest, package contents, dependency inventory, or another strong identity check.
8. Attach provenance to releases: source revision, builder/toolchain, build configuration, artifact digest, and relevant dependency metadata.
9. Investigate cache use separately from reproducibility. Caches may accelerate builds but must not become required hidden inputs or allow stale artifacts to bypass invalidation.
10. Re-check reproducibility when toolchains, base images, dependency managers, generators, or build infrastructure change.

## Decision rules
- A build that succeeds twice on one developer machine is not proof of reproducibility.
- Lockfiles help only when the entire dependency/toolchain resolution path respects them.
- Do not require bit-for-bit identity when it adds large complexity without supporting a real supply-chain or release need; define the needed guarantee explicitly.
- Fleet may choose the build node, but the artifact should not depend on which eligible node performed the build unless architecture/platform is an intentional input.

## Quality gate
The build is reproducible enough when declared inputs can recreate the intended artifact on a clean compatible builder, hidden host state is absent, cache behavior cannot silently change correctness, release artifacts carry traceable identity/provenance, and the chosen reproducibility guarantee has been verified rather than assumed.