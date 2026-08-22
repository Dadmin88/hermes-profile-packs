---
name: automation-design
description: Design a reliable automation from trigger through validation, idempotency, side effects, retries, observability, failure handling, and human escalation.
---
# Automation Design

Use when turning a recurring manual process into a script, workflow, bot, or event-driven automation.

## Procedure
1. Define the trigger, inputs, desired outcome, owner, and frequency/volume.
2. Map side effects and identify which operations must be idempotent or deduplicated.
3. Validate inputs before destructive or external actions.
4. Design retries only for retryable failures and add backoff/limits where repeated attempts can amplify harm.
5. Preserve state or checkpoints needed for recovery without creating hidden partial success.
6. Emit logs/metrics sufficient to answer what ran, what changed, and why it failed.
7. Define human escalation for ambiguity, authorization, or repeated failure.
8. Test normal execution, duplicates, partial failure, restart, and unavailable dependencies.

## Quality gate
A good automation is safe to run twice, diagnosable when it fails, and explicit about the cases that still require a human.