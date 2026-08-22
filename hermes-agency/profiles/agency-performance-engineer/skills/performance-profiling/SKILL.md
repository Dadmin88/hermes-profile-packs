---
name: performance-profiling
description: Profile system performance using representative workloads, time/resource attribution, traces, profilers, query plans, and repeatable evidence to locate where execution cost actually accumulates.
---
# Performance Profiling

Use when a measured performance symptom exists but the expensive code, query, resource, or boundary is not yet known.

## Procedure
1. Define the target metric and scenario before profiling: latency percentile, throughput, startup time, frame time, CPU, I/O, allocations, or another measurable outcome.
2. Reproduce under a representative workload and environment. Record build mode, dataset size, concurrency, hardware/runtime, configuration, and warm/cold state that materially affect results.
3. Choose the profiler or trace closest to the suspected layer: CPU sampling/instrumentation, allocation/memory profiler, database plan, browser/runtime trace, I/O/network trace, application spans, or engine-specific profiler.
4. Capture enough duration/samples to represent the problem without averaging away bursts or spending most time in profiler overhead.
5. Attribute cost by call path/boundary, not just by function names. Look for hot paths, repeated work, waits, lock/contention, I/O, serialization, garbage collection, context switching, and dependency time as relevant.
6. Compare failing/slow traces with a healthy baseline or alternate workload to isolate what changes with the symptom.
7. Form a specific hypothesis about the dominant cost and design the smallest experiment that can change that cost without altering several layers at once.
8. Re-profile after the change using the same scenario and compare both the target metric and where cost moved.
9. Preserve representative profiles/traces or a summarized result with exact conditions so future regressions can be compared rather than rediscovered.

## Decision rules
- A hot function is not automatically the best optimization target if it is required useful work or outside the critical path.
- Profiler overhead and development/debug builds can distort results; measure the mode relevant to the problem.
- Optimize the dominant end-to-end cost, not the most visually dramatic chart segment.
- Infrastructure or database bottlenecks should be handed to their owning specialist when the profiling evidence crosses that boundary.

## Quality gate
Profiling is complete when the symptom is reproducible, cost is attributed to a specific path or resource with representative evidence, an optimization hypothesis follows from that evidence, and re-profiling demonstrates whether the cost was reduced or merely shifted.