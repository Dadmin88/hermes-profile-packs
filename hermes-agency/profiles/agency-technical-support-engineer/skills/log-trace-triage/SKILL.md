---
name: log-trace-triage
description: Turn noisy logs and traces into a precise failure timeline by correlating identifiers, requests, retries, dependencies, resource state, and user-visible outcomes.
---
# Log Trace Triage

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using logs, traces, request IDs, deploy history, host/service metrics, and customer timestamps. Do not fill material gaps with assumptions when they can change the result.
3. Define time window and correlation keys, normalize clocks, identify first error versus downstream noise, reconstruct causal chain, and preserve representative evidence.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
The timeline identifies the earliest actionable divergence and distinguishes cause from cascade.
