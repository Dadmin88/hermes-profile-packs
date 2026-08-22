---
name: performance-investigation
description: Diagnose a performance problem using measurement, profiling, workload reproduction, bottleneck isolation, controlled changes, and regression evidence.
---
# Performance Investigation

Use for latency, throughput, CPU, memory, I/O, rendering, startup, build, or scaling problems.

## Procedure
1. Define the performance symptom and user/system impact with a measurable metric.
2. Reproduce under a representative workload and record baseline environment/configuration.
3. Measure before optimizing. Use profiling, traces, query plans, flame graphs, browser performance tools, metrics, or targeted instrumentation as appropriate.
4. Identify the dominant bottleneck and distinguish cause from correlated resource usage.
5. Change one meaningful variable at a time when validating an optimization hypothesis.
6. Measure improvement and check for shifted cost: memory, CPU, correctness, tail latency, complexity, or infrastructure spend.
7. Add a benchmark or regression guard when the performance requirement is durable.

## Quality gate
Do not optimize from intuition alone. Report before/after measurements and the conditions under which they were collected.