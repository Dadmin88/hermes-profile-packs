---
name: bug-reproduction
description: Reproduce a reported customer issue from exact environment, inputs, account state, sequence, and evidence so engineering receives a bounded defect instead of an anecdote.
---
# Support Bug Reproduction

Use when a support case may represent a product defect that needs engineering investigation.

## Procedure
1. Capture the reported symptom, expected behavior, user impact, timestamps, account/workspace, platform, version, and any request or error identifiers already available.
2. Separate what the customer observed from assumptions about root cause.
3. Reproduce in the safest representative environment using the smallest sequence that preserves the failure.
4. Vary one dimension at a time to isolate prerequisites such as account state, permissions, data shape, device, network, version, or feature configuration.
5. Collect relevant logs, screenshots, traces, responses, or state while minimizing sensitive customer data.
6. Determine whether the issue is reproducible, intermittent, environment-specific, already fixed, expected behavior, or still unconfirmed.
7. Write a handoff containing exact steps, expected vs actual behavior, environment, frequency, impact, evidence, and the smallest known boundary of the problem.
8. Re-test the same reproduction after a proposed fix when support is asked to validate it.

## Decision rules
- Do not diagnose from the ticket title alone.
- Never alter customer data destructively just to reproduce a defect.
- One failed reproduction does not disprove an intermittent report.
- Root-cause ownership transfers to the relevant engineering specialist once the defect is bounded.

## Quality gate
The escalation is engineering-ready when another specialist can reproduce or meaningfully investigate the issue from the packet, customer-sensitive material is minimized, observed facts are separated from inference, and impact and environment are explicit.