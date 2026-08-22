---
name: interaction-animation
description: Design interaction animation that communicates cause, state, hierarchy, and continuity while remaining responsive, interruptible, accessible, and implementable.
---
# Interaction Animation

Use when a UI or interactive object needs motion tied directly to user input or system state.

## Procedure
1. Define the before and after states, trigger, user intent, and information the motion must communicate.
2. Choose the minimum animated properties needed to make the relationship or state change understandable.
3. Set duration and easing based on distance, scale, urgency, and input cadence so the interaction feels responsive.
4. Maintain spatial continuity for moved, transformed, expanded, dismissed, or replaced elements where continuity helps orientation.
5. Design interruption, reversal, repeated input, loading delay, and cancellation behavior rather than assuming animations always finish.
6. Check layout, focus, hit targets, scrolling, and input availability during the transition so motion does not block interaction incorrectly.
7. Provide a reduced-motion behavior that preserves essential state communication.
8. Prototype and validate in the actual interaction context with realistic device or performance conditions.

## Decision rules
- Animation should never make a fast action feel slower merely to show itself off.
- Motion is not the only channel for communicating important state.
- Design interrupted states explicitly.
- Prefer properties the target platform can render smoothly when the visual result is equivalent.

## Quality gate
The interaction animation is ready when the state change remains clear and responsive, interruption and reversal are safe, focus, input, and layout stay correct, reduced-motion behavior preserves meaning, and implementation can reproduce the timing and intent on target devices.