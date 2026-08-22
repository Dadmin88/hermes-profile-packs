---
name: cross-functional-checklist
description: Build a launch checklist that coordinates cross-functional dependencies, evidence, owners, timing, sequencing, and handoffs without turning every launch into the same template.
---
# Cross-Functional Launch Checklist

Use when a launch spans several specialties and omitted coordination work is a realistic failure mode.

## Procedure
1. Start from launch scope, audience, channels, rollout, dependencies, and risks; generate checklist items from the actual launch rather than a universal giant template.
2. Group items by outcome or domain and assign one owner, due point, evidence requirement, and dependency where relevant.
3. Include product or engineering, QA, infrastructure, security, data, support, docs, legal or compliance, marketing, sales, partners, and analytics only when those functions are actually implicated.
4. Sequence prerequisites before dependent actions such as documentation, enablement, announcements, data migration, feature activation, or partner coordination.
5. Distinguish pre-launch blockers, launch-window actions, post-launch validation, and later follow-up.
6. Link to durable artifacts or evidence instead of pasting transient status into the checklist.
7. Review incomplete and at-risk items on a cadence proportional to launch urgency and route blockers to the correct owner.
8. Archive or summarize the final checklist as launch evidence and capture recurring omissions for future templates.

## Decision rules
- Checklists should reduce omission risk, not create work with no launch relevance.
- One owner per item is clearer than shared accountability.
- Completion means the evidence exists, not that somebody clicked a box.
- Do not encode node placement or live Fleet state in static Agency checklists; reference runtime evidence instead.

## Quality gate
The checklist is useful when every launch-critical cross-functional action has one owner and proof, sequencing and dependencies are explicit, blockers are distinguishable from post-launch work, and the team can run the launch without reconstructing obligations from chat history.