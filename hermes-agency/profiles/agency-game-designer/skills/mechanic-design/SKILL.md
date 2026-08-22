---
name: mechanic-design
description: Design a discrete game mechanic from player intent, inputs, rules, state, feedback, constraints, mastery, edge cases, and interaction with the core loop.
---
# Mechanic Design

Use when creating or revising one player-facing action or rule set such as movement, crafting, stealth, dialogue, building, combat input, or interaction.

## Procedure
1. Define the intended player experience and the decisions or skill the mechanic should create.
2. Specify inputs, preconditions, state transitions, outputs, costs, cooldowns, constraints, failure, and cancellation behavior.
3. Define immediate feedback through visuals, audio, haptics, UI, animation, or world response appropriate to the mechanic.
4. Map how the mechanic combines with existing systems and identify emergent interactions or conflicts.
5. Define mastery depth: what beginners understand quickly, what experienced players can optimize, and what dominant exploit should not emerge.
6. Prototype the smallest playable version that can test the central design hypothesis before content or polish multiplies cost.
7. Test edge conditions such as repeated input, interruption, resource boundaries, multiplayer or AI interaction, and unusual state combinations.
8. Iterate from observed player behavior and remove rules that add complexity without meaningful decisions.

## Decision rules
- A mechanic should create an understandable action or decision, not merely another meter.
- Depth can come from interactions between simple rules.
- Feedback is part of the mechanic contract.
- Do not protect complexity that playtests show players neither notice nor use.

## Quality gate
The mechanic is ready when its rules and feedback are understandable, it creates the intended decisions, edge and interaction states are defined, mastery has room without one obvious dominant exploit, and playtest evidence supports the central design hypothesis.