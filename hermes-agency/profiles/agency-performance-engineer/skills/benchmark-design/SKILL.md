---
name: benchmark-design
description: Design trustworthy performance benchmarks with a precise question, representative workload, controlled environment, warmup and sampling discipline, statistical comparison, correctness checks, and regression thresholds.
---
# Benchmark Design

Use when performance changes need repeatable evidence rather than one-off timing or anecdotal profiling.

## Procedure
1. Define the performance question and metric: operation latency, throughput, allocations, startup/build time, frame time, memory, CPU, I/O, or another property tied to a real requirement.
2. Choose representative inputs and workload sizes, including multiple scale points when complexity or data distribution can change behavior.
3. Keep correctness assertions in or beside the benchmark so an optimization cannot “win” by doing less work or returning a different result.
4. Control the environment variables that materially affect results: build mode, runtime/compiler version, hardware, power state, background load, CPU affinity when justified, dataset/cache state, network/dependencies, and configuration.
5. Define warmup and steady-state behavior appropriate to JIT, caches, connection pools, filesystem/page cache, shaders, or other runtime mechanisms. Measure cold behavior separately when it is itself the target.
6. Run enough samples/iterations to characterize variance without pretending highly correlated micro-iterations are independent evidence.
7. Record distributions and uncertainty appropriate to the benchmark rather than comparing a single minimum or average blindly.
8. Compare candidates under the same conditions and vary order or isolate runs when thermal/cache/history effects could bias results.
9. Set regression thresholds based on meaningful user/system impact and normal benchmark noise, not an arbitrary zero-tolerance percentage.
10. Store benchmark code, inputs, environment metadata, and result format so another engineer or CI system can reproduce the comparison.

## Decision rules
- Microbenchmarks prove microbehavior; do not generalize them to end-to-end system performance without a model connecting the two.
- A benchmark that is too noisy to distinguish the claimed improvement needs better design before stronger conclusions.
- Production telemetry can validate external relevance, while controlled benchmarks isolate causes; they complement each other.
- When hardware heterogeneity matters in Fleet, benchmark per relevant capability class instead of mixing incomparable nodes into one score.

## Quality gate
The benchmark is trustworthy when it answers a precise performance question, executes correct representative work, controls or records material environmental factors, captures enough samples to interpret variance, compares candidates fairly, and can be rerun by another engineer to reproduce the claimed result.