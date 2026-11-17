---
name: pixel-frame-animation
description: Animate pixel sprites with key poses, fixed registration, directional tags, millisecond timing, loop checks, and frame-by-frame cleanup.
---
# Pixel Frame Animation

1. Define each state, facing, tag, loop policy, and timing target. Record the registration point and any deliberate root motion. Preserve an approved neutral pose as the identity anchor.
2. Block key poses before in-betweens. For locomotion, plan contact, passing, and recovery poses. For a small gesture, isolate the moving cel or layer while holding stable landmarks. Preserve asymmetric equipment and silhouettes when considering a mirrored direction.
3. Use onion skin or compare adjacent frames at the same coordinates. Check planted feet, shoulder and joint continuity, accessory continuity, and edge cleanup. Use per-frame durations where a hold or impact needs more time. Record durations in milliseconds for handoff. When calling the editor, convert to seconds for Aseprite or a multiplier of the base frame period for Pixelorama. Reserve GIF for visual review.
4. Play the loop at actual timing and 1× scale. Inspect the last-to-first transition, direction order, popping, clipping, and drifting anchors. Review any intentional squash or displacement against the brief.
5. Save the editable source with named layers and state tags. Hand off frame order, durations, loop policy, facing labels, and origin through `pixel-asset-export`. If the bridge lacks timing or tags, finish them in the editor or report the gap.

**Quality gate** — Motion reads in playback and frame inspection confirms stable registration, consistent identity, and the expected frame order and timing.
