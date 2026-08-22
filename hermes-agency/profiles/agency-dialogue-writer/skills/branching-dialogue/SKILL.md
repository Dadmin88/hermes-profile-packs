---
name: branching-dialogue
description: Design branching dialogue around player intent, character goals, state conditions, choice meaning, convergence, consequences, memory, and implementation identifiers without creating combinatorial branches that add no meaningful agency.
---
# Branching Dialogue

Use when dialogue choices or game state can change the conversation path or later outcome.

## Procedure
1. Define the conversation purpose, participating characters, starting world or quest state, and the player decisions the dialogue should support.
2. Give choices distinct intent or tradeoffs rather than several phrasings of the same answer unless tone-only choice is deliberate.
3. Define prerequisites and state checks for branches using authoritative game variables and stable identifiers.
4. Track immediate and deferred consequences, including relationship, information, quest, resource, faction, or world-state changes as relevant.
5. Re-converge branches where outcomes genuinely become equivalent while preserving remembered choices that should matter later.
6. Prevent impossible combinations by documenting mutually exclusive states, one-time lines, repeat behavior, interruption, and re-entry.
7. Review every branch for character knowledge, voice, pacing, and whether the player can understand the likely meaning of a choice without knowing hidden implementation flags.
8. Hand engineering or narrative tooling a structured graph or stable node/choice IDs and validate the implemented path with representative state combinations.

## Decision rules
- Branches should create meaningful perspective, information, consequence, or expression.
- More branches are not automatically more agency.
- State conditions belong to a durable contract, not line-number references.
- Hidden consequences can exist, but choices should not routinely mean the opposite of their readable intent.

## Quality gate
The branching dialogue is ready when choices have distinct meaning, state conditions and consequences are explicit, branch growth remains manageable, convergence preserves required memory, characters stay consistent, and implementation can test representative state combinations without guessing narrative logic.