---
name: motion-system
description: Define reusable motion principles and patterns for hierarchy, continuity, feedback, transitions, emphasis, duration, easing, and reduced-motion alternatives.
---
# Motion System

Use when a product or brand needs coherent motion behavior across many interactions or assets.

## Procedure
1. Identify the jobs motion must perform: orientation, causality, hierarchy, feedback, state change, delight, narrative, or brand expression.
2. Define core principles such as spatial continuity, responsiveness, restraint, physicality, or stylization in observable terms.
3. Create a small duration and easing vocabulary tied to interaction scale and urgency rather than arbitrary animation presets.
4. Define recurring transition patterns for entering or exiting, expanding or collapsing, reordering, navigation, loading, success or error, and other relevant states.
5. Specify how motion should adapt or reduce for users who request reduced motion and for low-performance contexts.
6. Map patterns to design-system components or tokens or production templates where reuse adds value.
7. Test sequences in context at real interaction speed, including interruptions and rapid repeated input.
8. Document exceptions where cinematic or brand motion intentionally departs from product interaction rules.

## Decision rules
- Motion should communicate state or hierarchy before it decorates.
- Duration should follow interaction scale and responsiveness, not one global number.
- Reduced motion is an alternate communication path, not simply animation disabled everywhere.
- Interrupted animations must leave the interface or scene in a valid state.

## Quality gate
The motion system is ready when recurring interactions have coherent timing and transition logic, motion communicates causality and hierarchy, reduced-motion behavior is defined, interruptions are safe, and teams can reuse the system without flattening every motion context into one effect.