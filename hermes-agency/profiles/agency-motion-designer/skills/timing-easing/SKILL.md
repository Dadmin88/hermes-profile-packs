---
name: timing-easing
description: Design timing and easing from perceived responsiveness, distance, mass, hierarchy, urgency, continuity, and platform behavior rather than arbitrary animation constants.
---
# Timing and Easing

Use when motion feels mechanically wrong, inconsistent, sluggish, or disconnected from the intended interaction.

## Procedure
1. Identify the motion's trigger, distance or scale, visual mass, information priority, and whether the user is waiting on it.
2. Measure current duration and curve where possible and observe the actual perceptual problem at real playback speed.
3. Choose duration ranges that preserve immediate feedback for direct manipulation and allow longer transitions only when distance, narrative, or comprehension requires it.
4. Select easing based on physical or visual intent: entering, exiting, settling, continuous velocity, spring response, or deliberate linear progression.
5. Coordinate related elements with hierarchy-aware staggering only when it improves comprehension rather than adding delay.
6. Check repeated and interrupted use; an animation that feels fine once may become exhausting at high interaction frequency.
7. Validate reduced-motion and low-performance behavior.
8. Record the chosen timing as a reusable token or pattern only when the same interaction class genuinely recurs.

## Decision rules
- Timing is part of perceived performance.
- Do not use dramatic easing on frequent utility interactions.
- Staggering should clarify order, not make users wait.
- Reusable motion tokens should represent interaction classes rather than one arbitrary favorite curve.

## Quality gate
Timing is ready when the motion feels responsive and intentional at real interaction frequency, easing supports the visual cause or state change, hierarchy is clear without unnecessary delay, interruption and reduced-motion cases work, and reusable values are generalized only where evidence supports reuse.