---
name: performance-debugging
description: Diagnose and improve frontend performance by measuring user-visible symptoms, isolating the dominant bottleneck, changing one high-impact cause at a time, and proving the improvement without regressions.
---
# Performance Debugging

Use when a frontend is slow to load, respond, render, scroll, navigate, hydrate, update, or remain stable under realistic usage.

## Procedure
1. Define the symptom in user terms before optimizing: slow initial view, delayed interaction, input lag, jank, repeated rendering, memory growth, excessive network work, or another observable problem.
2. Reproduce under representative conditions and capture a baseline. Record device class, viewport, network conditions, dataset size, route/state, build mode, and the metric or trace that demonstrates the problem.
3. Classify the dominant cost before editing code: network/waterfall latency, bundle/parse cost, main-thread JavaScript, rendering/layout/paint, state subscription or re-render churn, image/media work, memory pressure, or repeated backend requests.
4. Use the platform's measurement tools rather than intuition: browser performance/network/memory tooling, framework profilers where appropriate, bundle analysis, runtime marks, and application telemetry when available.
5. Follow the critical path. Identify the longest blocking dependency chain, biggest main-thread tasks, most expensive repeated renders, largest transfer/parse costs, or resource responsible for instability.
6. Form one testable hypothesis and make the smallest change that can prove or disprove it. Examples include parallelizing independent work, removing a request waterfall, narrowing subscriptions, deferring non-critical code, reducing shipped code, virtualizing genuinely large lists, avoiding layout thrash, or fixing repeated resource creation.
7. Treat memoization, caching, lazy loading, prefetching, and virtualization as tradeoffs, not rituals. Each can add memory, staleness, complexity, or incorrect behavior; use them when measurement shows the relevant bottleneck.
8. Re-measure using the same scenario and compare against the baseline. Check both the target metric and user-perceived behavior rather than relying on a profiler screenshot alone.
9. Verify correctness, accessibility, loading/error states, and memory behavior after optimization. Performance changes must not create stale UI, broken focus, race conditions, missing content, or excessive retained state.
10. Record the bottleneck, evidence, change, before/after result, and remaining constraints so future work does not repeat the same investigation.

## Decision rules
- Optimize the dominant measured bottleneck first.
- Development-mode behavior may differ materially from production; measure the mode that represents the problem.
- Avoid micro-optimizing fast code while a request waterfall, oversized bundle, or long task dominates the experience.
- Framework-specific performance guidance is useful only when that framework is actually in use and the recommendation survives measurement in the target application.
- Escalate system-wide budgets, backend latency, infrastructure constraints, or cross-service bottlenecks to the specialty that owns them.

## Quality gate
The performance task is complete when the original symptom is reproducible, the dominant cause is supported by evidence, the change produces a measured improvement under comparable conditions, correctness and accessibility remain intact, and remaining bottlenecks are explicit.