---
name: memory-analysis
description: Diagnose memory growth, pressure, allocation cost, retention, leaks, cache behavior, fragmentation, and out-of-memory failures using workload reproduction and runtime-specific evidence.
---
# Memory Analysis

Use when a process, service, browser/app, game, worker, or system consumes too much memory, grows over time, pauses under allocation pressure, or is killed for memory exhaustion.

## Procedure
1. Define the symptom precisely: baseline footprint, growth rate, peak/RSS/heap/VRAM or other relevant memory, workload, time to failure, GC/pause behavior, and environment/resource limits.
2. Reproduce with a controlled workload and capture memory over time so steady high usage, workload-proportional growth, cache growth, fragmentation, and true unbounded retention can be distinguished.
3. Identify the memory domains involved: managed heap, native heap, mapped files, buffers, caches, stacks, GPU resources, shared memory, page cache, or container/cgroup accounting as relevant.
4. Use the runtime/platform's allocation profiler, heap snapshot/dump, memory map, object/reference graph, resource profiler, or equivalent evidence to find dominant allocations and retained objects/resources.
5. Compare snapshots at stable workload checkpoints. Look for types/resources whose retained count/size grows when the logical workload returns to the same state.
6. Trace ownership/lifetime: references, subscriptions/listeners, caches, queues, pools, closures, globals/singletons, unfreed native/GPU handles, scene/component lifecycle, or buffers that keep data alive.
7. Evaluate GC/allocation churn separately from leaks. High allocation rate can create latency/CPU pressure even when memory eventually returns.
8. Test one hypothesis at a time and repeat the same workload. Confirm retained/peak memory changes and check throughput/latency/correctness tradeoffs.
9. Verify long-running/steady-state behavior after the fix and under the resource limit that matters, including restart/reload/scene/navigation paths if they trigger retention.
10. Add a regression workload/measurement guard when the memory bound is a durable operational requirement.

## Decision rules
- High memory usage is not automatically a leak if it is bounded and intentionally caches useful data.
- A falling managed heap does not prove process RSS or native/GPU memory is healthy.
- Restarting a worker hides retention but does not explain it; use restart only as an explicit containment strategy.
- For Fleet-managed nodes, report actual memory requirements/pressure to capacity scheduling rather than teaching the profile to choose its own host.

## Quality gate
Analysis is complete when memory behavior is reproducible, the growing or dominant memory domain is identified with profiler/snapshot evidence, ownership/lifetime explains the retention or churn, the fix measurably changes memory under the same workload, and sustained operation remains within the required bound without unacceptable regressions.