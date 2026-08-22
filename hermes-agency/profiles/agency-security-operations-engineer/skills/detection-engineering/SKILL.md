---
name: detection-engineering
description: Create and tune a security detection from a concrete threat/abuse hypothesis through telemetry requirements, logic, testing, severity, suppression, and response playbook.
---
# Detection Engineering

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using threat model, logs/events, identity/assets, baseline behavior, incident history, and response capability. Do not fill material gaps with assumptions when they can change the result.
3. Define behavior to detect and benign lookalikes, verify telemetry fidelity, implement query/rule, replay known positive/negative cases, tune noise, and attach actionable context.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
The detection catches representative malicious behavior with tolerable false positives and tells responders what to do next.
