---
name: build-tooling
description: Design and improve build tooling around dependency graphs, incremental correctness, caching, generated inputs, hermeticity, diagnostics, parallelism, reproducibility, and developer/CI feedback time.
---
# Build Tooling

Use when compilation, bundling, packaging, asset processing, code generation, or monorepo build workflows are slow, unreliable, opaque, or inconsistent.

## Procedure
1. Map the build graph: source inputs, generated inputs, toolchains, dependencies, targets/artifacts, platform variants, and post-processing/signing/package steps.
2. Establish the current correctness and timing baseline in local and CI contexts. Identify which targets/actions dominate critical-path time versus merely appearing frequently.
3. Define inputs/outputs precisely enough for incremental execution and caching. Hidden environment/filesystem/global-tool inputs make caches incorrect even when they make builds faster.
4. Separate build graph correctness from optimization. First ensure changes invalidate every affected artifact and do not invalidate unrelated work unnecessarily.
5. Improve parallelism only across genuinely independent actions and account for shared CPU, memory, disk, network, compiler daemon, or license constraints that can make excessive concurrency slower.
6. Design local/remote caches with stable keys, integrity checks, trust boundaries, eviction, and fallbacks. Treat untrusted build outputs as supply-chain inputs, not harmless acceleration.
7. Make toolchain/dependency versions and generated assets reproducible enough for the release requirements and compatible with `agency-devops-engineer` build provenance.
8. Provide diagnostics that reveal why a target rebuilt, cache hit/missed, dependency failed, or configuration selected a platform variant.
9. Benchmark changes on representative clean, incremental, and CI workloads; check memory/storage/network cost alongside elapsed time.
10. Add regression measurements/tests for graph correctness and the critical build path when build performance is a durable requirement.

## Decision rules
- A fast incremental build that misses a required invalidation is incorrect.
- Parallelism is bounded by the actual resource bottleneck.
- Caches must be optional accelerators, not hidden required state for correctness.
- Fleet can select an eligible build node, but build outputs should remain traceable/reproducible across compatible nodes rather than depending on one host's undeclared state.

## Quality gate
Build tooling is ready when dependency/input ownership is explicit, clean and incremental builds are correct, caching cannot serve stale/untrusted output silently, critical-path time is measured and improved where intended, diagnostics explain rebuild/cache behavior, and the same declared inputs produce the expected artifacts on a clean compatible builder.