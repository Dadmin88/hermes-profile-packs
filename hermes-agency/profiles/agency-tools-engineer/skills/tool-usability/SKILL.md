---
name: tool-usability
description: Evaluate and improve an engineering tool through real task success, discoverability, defaults, feedback, error recovery, scriptability, latency, accessibility, and support evidence.
---
# Tool Usability

Use when a developer/operator tool technically works but users make repeated mistakes, avoid it, need private coaching, or cannot recover from failures efficiently.

## Procedure
1. Define the primary users and top tasks, including frequency, consequence, environment, and whether the interface is interactive, script-driven, editor-based, API-based, or mixed.
2. Observe representative users completing real tasks. Record time, wrong turns, help lookups, failed attempts, confusing terms, manual workarounds, and places they cannot tell what the tool is doing.
3. Check discoverability: installation, entry commands/actions, contextual help, examples, autocomplete/discovery, documentation links, and naming aligned with user concepts.
4. Check defaults and required decisions. Remove questions/options that can be answered safely by context; keep destructive/scope-sensitive decisions explicit.
5. Check feedback: progress for long work, current target/context, success result, warnings, preview/diff, and enough information to know what changed.
6. Check failure recovery. Errors should identify the problem, preserve user work, distinguish retryable versus configuration/usage failures, and point to the next useful action.
7. Check composability/scriptability when required: stable structured output, stdin/stdout behavior, exit status, non-interactive mode, idempotency, and predictable configuration precedence.
8. Check performance/latency and accessibility for the interface type. Repeated small delays or inaccessible keyboard/focus behavior can make an otherwise correct tool effectively unusable.
9. Prioritize improvements by frequency and cost of failure, then retest the same tasks with users or task metrics.
10. Monitor support questions, abandonment, retries, telemetry, and bypass behavior after release to confirm the improvement changed real usage.

## Decision rules
- More options are not more power when users cannot predict their effect.
- Documentation can explain necessary complexity, but recurring mistakes in the common path are often an interface defect.
- A successful command that leaves users unsure what changed is not a good experience.
- Tool usability is evidence-driven; personal CLI/editor preferences should not become universal requirements without user/task support.

## Quality gate
The tool is usable when representative users can discover and complete core tasks without private instruction, defaults reduce unnecessary decisions, target/effect/status are clear, errors preserve work and lead to recovery, automation interfaces remain predictable, and follow-up evidence shows fewer wrong turns or support interventions.