# Translate evidence into rules

Begin with a loop: action → state change → feedback → next decision. State the goal, pressure (or an explicitly relaxed mode), success, recovery and restart. Choose a small connected playable scope before a catalog of disconnected showcase scenes.

Every mechanic should state input, precondition, state mutation, visual/audio feedback, and rejection behavior. For example, “offer fruit” consumes exactly one fruit after a valid committed interaction, changes one identified creature's trust, plays feedback and rejects repeated input while busy. Neither animation frames nor button labels own inventory state.

## Useful invariants by mechanic family

| Family | Invariants worth testing |
|---|---|
| Racing / traversal | Ordered forward checkpoints; pickups once; collisions swept at boosted speed; landing zone agrees with visible ramp; recovery returns to valid terrain |
| Factory / puzzle / strategy | Deterministic update order; conservation; unique delivery IDs; capacity/backpressure; valid graph ports; undo restores state; a known solution actually completes |
| Exploration / collection | Stable entity identity; one journal entry per species; reachable routes; resources cannot become negative; interaction eligibility consistent with UI |
| Combat / platforming | Hit once per projectile; reload and shield costs committed once; collision matches geometry; jump endpoints reachable; death/retry clears transient events |
| Rhythm / audio-led | One master clock; input windows tested at boundaries; explicit latency assumptions; replay timing independent of render cadence |
| Social / dialogue / narrative | Explicit branching state; choices persist; impossible branches rejected; accessibility and save recovery |

These are examples, not required genres. Design additional invariants from the actual brief.

Separate simulation, rendering, UI and audio. Use a bounded fixed-step simulation where timing matters; interpolate visuals. Clear held input on blur, handle pointer-lock loss, and pause deliberately. Maintain an explicit coordinate frame for moving worlds: a train-local level and moving scenery can be simpler than rebasing every collision body.

Use stable IDs for entities, rewards and objectives; pool short-lived effects. Restart resets timers, subscriptions, state machines, particles, audio sources and input, not just the camera. Validate corrupted saves and repeat actions. Level content must define traversable connections, spawn/goal locations and interaction ranges; decorative maps should represent that same state.

A title screen, a showroom and a video player are not a game loop. A generated background is legitimate scenery when interactive elements, camera constraints and occlusion remain coherent. State exactly which parts are interactive.
