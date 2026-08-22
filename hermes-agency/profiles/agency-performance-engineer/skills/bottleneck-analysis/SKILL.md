---
name: bottleneck-analysis
description: Identify the system bottleneck that limits an end-to-end performance objective by connecting queueing, utilization, dependency time, contention, critical paths, and workload scaling rather than optimizing components in isolation.
---
# Bottleneck Analysis

Use when a system is slow or cannot scale and several components appear busy at once.

## Procedure
1. Define the constrained outcome and workload: end-to-end latency, throughput, frame rate, job completion, build duration, or another user/system metric.
2. Map the critical path and parallel work for one representative operation, including queues, services, databases, external dependencies, network, storage, and client/runtime work.
3. Measure time spent waiting versus executing at each boundary and correlate with resource utilization, concurrency, queue depth, lock/contention, retries, and downstream latency.
4. Increase or vary load in controlled steps to see which resource/queue reaches nonlinear degradation first. High utilization alone is not proof of the limiting resource.
5. Check serial fractions and coordination boundaries that cap speedup even when individual workers or hosts have spare capacity.
6. Separate primary bottleneck from secondary symptoms. Upstream queues, retries, CPU, or memory can rise because a downstream dependency slowed first.
7. Form a capacity/latency model explaining how the suspected bottleneck produces the observed end-to-end behavior.
8. Apply or simulate one change that should relieve that constraint and predict what will become the next limit.
9. Re-measure under the same workload. If end-to-end improvement does not match the model, revise the hypothesis rather than stacking optimizations.
10. Record the current limiting resource, operating range, evidence, next likely bottleneck, and conditions that could change the conclusion.

## Decision rules
- The bottleneck is the constraint on the goal, not simply the busiest component.
- Removing one bottleneck reveals another; optimization is iterative.
- Queue growth and tail latency often expose capacity limits before average utilization reaches an intuitive threshold.
- If the bottleneck is Fleet node scarcity or placement constraint, report the capability/capacity evidence to Fleet rather than embedding scheduling logic in the workload.

## Quality gate
Analysis is complete when the end-to-end constraint is explained by measured critical-path/resource/queue behavior, a model predicts the effect of relieving it, a controlled change validates or falsifies that model, and the next limiting factor or uncertainty is explicit.