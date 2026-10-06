---
name: architecture-reading
description: Teach learners to read and critique a systems architecture by tracing requests, state, dependencies, trust boundaries, failure domains, and scaling assumptions.
---
# Architecture Reading

Trace one representative request or workflow end to end. Mark where state lives, where network hops occur, what can fail independently, and which component owns each guarantee.

Ask what happens under latency, restart, partial outage, retry, and load growth.

## Teaching example

When teaching retries, durable state, and duplicate effects, use [the domain example](references/teaching-example.md) for worked reasoning. Read it only when relevant. Match requested depth: answer directly when asked, use already-supplied work to skip mastered steps, and keep a learner’s unaided transfer attempt free of the instructor key. Preserve this skill’s scope and safety boundaries for other topics.
