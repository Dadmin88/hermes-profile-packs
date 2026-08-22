---
name: audio-implementation-plan
description: Plan how music, ambience, effects, dialogue, UI cues, spatialization, states, priorities, and runtime controls integrate with product or game behavior.
---
# Audio Implementation Plan

Use when audio direction must be translated into concrete runtime triggers, states, routing, and asset requirements.

## Procedure
1. Map user or game states and events that need audio feedback, including entry, exit, interruption, failure, success, transitions, and repeated actions.
2. Classify each sound by function: informational, emotional, spatial, diegetic, UI, dialogue, ambience, music, or accessibility support as relevant.
3. Define trigger ownership and state logic so audio is driven by authoritative product or game events rather than fragile visual timing.
4. Specify concurrency, priority, cooldown, randomization, variation, looping, fades, ducking, and interruption behavior for repeated or competing sounds.
5. Define spatialization, attenuation, listener behavior, zones, occlusion, or 2D mix rules where applicable.
6. Define buses or groups, loudness targets, dynamic range, and user controls such as master, music, effects, dialogue, and mute behavior.
7. List required assets, variants, metadata, and fallback behavior for missing or late-loaded content.
8. Validate the plan against runtime and performance constraints and hand implementation ownership to the appropriate engineer or technical audio pipeline.

## Decision rules
- Audio should respond to authoritative state, not scrape UI visuals or animation timing when a real event exists.
- Not every event deserves a sound; avoid cue saturation.
- Repeated sounds need explicit variation and concurrency policy to prevent fatigue.
- User volume and mute preferences are part of the contract.

## Quality gate
The plan is implementation-ready when every material cue has a trigger or state owner, concurrency and transition behavior are explicit, spatial, mix, and user-control rules are defined, asset requirements are known, and engineers can wire audio without inventing product behavior.