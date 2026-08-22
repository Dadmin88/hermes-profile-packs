---
name: revenue-handoff-automation
description: Design reliable automation for marketing-sales-CS handoffs with eligibility rules, enrichment, routing, SLA timers, deduplication, retries, and exception queues.
---
# Revenue Handoff Automation

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using lifecycle rules, CRM/marketing/support APIs, identity keys, ownership map, and SLA expectations. Do not fill material gaps with assumptions when they can change the result.
3. Define authoritative trigger and owner, validate required fields, make assignment idempotent, capture reason codes, expose stuck states, and preserve manual escalation.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Each eligible record reaches one accountable owner once, and failures remain visible/recoverable.
