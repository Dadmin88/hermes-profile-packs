---
name: process-design
description: Design or improve an operational process by mapping outcomes, actors, inputs, decisions, handoffs, controls, exceptions, evidence, and failure recovery before automating it.
---
# Process Design

Use when recurring operational work is inconsistent, slow, error-prone, opaque, or dependent on tribal knowledge.

## Procedure
1. Define the process outcome, customer or internal user, trigger, scope, and current pain with evidence.
2. Observe the current process and map actors, inputs, decisions, systems, handoffs, wait states, rework, and exceptions.
3. Distinguish required controls from historical ceremony and identify duplicate approval or data-entry steps.
4. Redesign around clear ownership, minimal handoffs, explicit decision criteria, and one authoritative state where practical.
5. Define exception paths and recovery rather than documenting only the happy path.
6. Decide what should be automated only after the desired process is coherent; do not automate waste blindly.
7. Define evidence, service expectations, metrics, and controls needed to know the process is working.
8. Pilot with representative cases, capture failure modes, and revise before broad rollout.

## Decision rules
- Optimize the outcome, not the number of steps alone.
- A process should not depend on one person's memory when the work is recurring and consequential.
- Approval steps need a real decision or control purpose.
- Automation belongs to the Automation Engineer when implementation becomes the task.

## Quality gate
The process is ready when ownership and decision criteria are explicit, normal and exception flows are understandable, unnecessary handoffs are removed, evidence and controls are defined, and the process can be followed and improved without relying on oral tradition.