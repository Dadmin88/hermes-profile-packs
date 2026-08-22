---
name: load-testing
description: Design and run load tests that represent real demand, concurrency, data, arrival patterns, bottlenecks, saturation, recovery, and service objectives without turning a synthetic benchmark into a production claim.
---
# Load Testing

Use when validating throughput, latency, scaling, overload behavior, or capacity under concurrent/large workloads.

## Procedure
1. Define the questions the test must answer: capacity limit, target traffic, burst behavior, scaling response, queue behavior, dependency pressure, or regression comparison.
2. Model realistic workload mix, request/job distribution, data sizes, think time, concurrency/arrival rate, session behavior, hot keys/entities, and read/write ratios instead of one repeated trivial request.
3. Choose a representative environment and document differences from production in topology, hardware, data, dependencies, quotas, caches, and network path.
4. Establish a low-load functional baseline before increasing traffic so correctness defects are not mistaken for load effects.
5. Ramp demand deliberately, hold steady long enough to observe saturation/recovery, and include credible bursts when the real workload has them.
6. Measure end-to-end latency distributions, success/error rate, throughput, queue/backlog, resource saturation, dependency behavior, retries, timeouts, and scaling events together.
7. Identify the first bottleneck and the system behavior beyond it: graceful queuing/shedding, increasing tail latency, cascading retries, resource exhaustion, or correctness failure.
8. Avoid overwhelming external third-party systems without explicit permission; stub or sandbox them when the test question does not require their real capacity.
9. After changes, repeat the same controlled test and compare results. Keep test code/data/version and environment configuration traceable.
10. Run recovery observation after load drops or failures end to ensure queues, memory, connections, and autoscaling return to healthy state.

## Decision rules
- Closed-loop concurrency and open-loop arrival-rate tests answer different questions; choose the model that matches real demand.
- Average latency hides overload and tail behavior; use distributions/percentiles appropriate to the objective.
- A test environment smaller than production can still reveal bottlenecks if its scaling relationship is understood, but do not extrapolate blindly.
- Fleet-wide tests should include placement/capacity behavior only when Fleet itself is part of the system under test.

## Quality gate
The load test is valid when workload and environment assumptions are documented, functional correctness is maintained, demand is controlled and reproducible, saturation and recovery are observed across end-to-end and resource signals, the first bottleneck is supported by evidence, and conclusions stay within what the test actually measured.