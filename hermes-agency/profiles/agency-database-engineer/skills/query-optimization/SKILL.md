---
name: query-optimization
description: Optimize database queries by reproducing the workload, measuring latency and resource cost, reading the actual execution plan, fixing access strategy or data shape, and proving improvement without semantic regression.
---
# Query Optimization

Use when database operations are slow, resource-heavy, unstable at scale, or responsible for application latency.

## Procedure
1. Capture the exact query/operation, parameters or selectivity pattern, dataset size/distribution, database version/configuration, concurrency level, and observed latency/resource symptom.
2. Verify the query returns the intended semantics before optimizing it. A fast wrong query is not an improvement.
3. Obtain the engine's actual or representative execution plan and runtime statistics using the supported analysis tooling. Identify scans, joins, sorts, spills, lookups, row-estimate errors, lock waits, network/remote work, and repeated operations as relevant.
4. Compare estimated versus actual cardinalities when available. Bad statistics or skew can be the root cause even when indexes exist.
5. Determine the dominant cost: data read volume, poor access path, missing/nonselective index, join shape, repeated N+1 calls, sort/group aggregation, function/expression preventing index use, lock contention, network round trips, or another measured bottleneck.
6. Change one primary cause at a time: rewrite access pattern, batch requests, adjust query shape, add/alter index, precompute/materialize, partition, update statistics, or change schema only when evidence justifies the cost.
7. Measure the candidate using representative parameters including common, selective, unselective, empty, and worst credible cases. Watch both latency and resource consumption.
8. Evaluate write/storage/maintenance side effects of the optimization, especially new indexes/materializations or denormalization.
9. Test correctness and transaction/isolation behavior after the change, then compare before/after plans and metrics under comparable conditions.
10. Record the workload, evidence, chosen fix, measured gain, tradeoffs, and conditions under which the plan may regress as data distribution grows.

## Decision rules
- Do not add an index merely because a column appears in a filter; inspect selectivity and plan behavior.
- Avoid `SELECT *` only when excess data transfer/materialization is a real problem; it is not a universal performance law.
- Query plans are engine- and data-dependent; verify advice against the actual database/version.
- Application-level N+1 behavior may require Backend Engineer changes even if every individual query is fast.

## Quality gate
Optimization is complete when the real slow workload is reproduced, the dominant cost is supported by plan/runtime evidence, the change preserves semantics, improvement is measured across representative parameters, new write/storage/operational costs are understood, and future regression conditions are documented.