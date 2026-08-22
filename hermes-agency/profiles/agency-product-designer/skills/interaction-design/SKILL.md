---
name: interaction-design
description: Design interaction behavior for a product feature by mapping user intent, controls, feedback, navigation, direct manipulation, interruptions, errors, and platform conventions into a coherent usable flow.
---
# Interaction Design

Use when a product requirement is defined but the detailed user interaction and behavioral model still need to be designed.

## Procedure
1. Start from the user goal, context, constraints, and product acceptance criteria. Identify what the user knows, wants to do, and needs to understand at each point in the flow.
2. Map actions and responses: what controls are available, what each action changes, what feedback appears immediately, what requires confirmation, and what remains reversible.
3. Prefer familiar platform and product conventions where they fit. Introduce novel interaction only when it materially improves the user outcome and the learning cost is justified.
4. Define selection, editing, navigation, drag/direct-manipulation, keyboard, touch/pointer, and gesture behavior as relevant. Ensure equivalent access for users who cannot use the primary input mode.
5. Design system feedback around latency and uncertainty: pending states, progress, optimistic behavior, success, partial success, failure, retry, cancellation, and reconnect/recovery.
6. Decide how destructive, irreversible, expensive, or privacy-sensitive actions are confirmed and whether undo is a better safety mechanism than modal confirmation.
7. Handle interruptions and re-entry. Specify what happens when users navigate away, refresh/restart, lose connectivity, switch devices/windows, or return to partially completed work when the workflow supports persistence.
8. Keep focus, reading order, announcements, and keyboard operation in the interaction model from the beginning. Coordinate deeper accessibility review where the pattern is custom or high impact.
9. Prototype high-risk transitions or novel controls at the minimum fidelity needed to evaluate comprehension and usability before polishing visuals.
10. Document interaction rules, states, and unresolved product decisions for implementation handoff without prescribing frontend code structure.

## Decision rules
- Interaction design answers how the product behaves for the user, not how the implementation is structured.
- Prefer undo/recovery over confirmation fatigue when the operation is safely reversible.
- Loading and error behavior are part of the interaction, not engineering leftovers.
- Do not hide essential actions behind hover-only, gesture-only, or pointer-only affordances.
- Use user research for uncertain behavior rather than arguing from taste.

## Quality gate
Interaction design is ready when primary and alternate actions are understandable, feedback and recovery behavior are defined, the flow works across relevant input modes, high-risk assumptions have been prototyped or validated, and engineering can implement the behavior without inventing missing interaction rules.