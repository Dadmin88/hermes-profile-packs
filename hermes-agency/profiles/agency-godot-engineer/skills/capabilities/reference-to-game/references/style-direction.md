# Preserve visual identity

A palette is a system of roles, proportions and contrasts, not a handful of dominant hex values. Lock the foreground accent relative to the environment, the darkest framing value, the UI surface/ink pair, highlight warmth and the size of saturated areas. Account for lighting: a texture's albedo is not the color of a shaded screenshot.

## The style contract

- **Anchors:** source IDs and why each governs the design. Name deliberate departures.
- **Palette:** named roles, sampled location or authored origin, color, approximate coverage and contrast relationships. Preserve muted or monochrome directions when supplied.
- **Identity:** character counts, silhouette landmarks, proportions, costume blocks, facial features, persistent IDs; objects need the same care.
- **Materials and edges:** brush grain versus smooth shading, roughness versus gloss, rim width, translucency, line work, bevel and outline language.
- **Lighting:** key direction and softness, fill temperature, contact shadows, atmosphere, exposure and background separation.
- **Camera:** perspective or orthographic, subject height as a fraction of frame, horizon position, angle, follow behavior and supported gameplay views.
- **UI:** type family and weight, spacing, panel material, icon silhouettes, corner treatment, color roles, anchoring and responsive behavior.
- **Motion:** weight, anticipation, hold times, squash, trails, animation commitment and feedback hierarchy.

## First scene checkpoint

Implement a representative view with one hero subject, some environment, a real action and the real UI family. Compare at the intended viewport and matching framing. Start with silhouette/coverage and camera, then palette/light/material, then detail. A wrong field of view can masquerade as an asset problem. A tone mapper can flatten carefully sampled colors. Do not “fix” either by adding unrelated saturation.

Capture reference and implementation with readable labels. Review full-frame masses and focal crops, HUD on/off, idle/action, and the lowest supported quality setting. Record a short reason for each verdict rather than claiming a universal similarity percentage. A copied background can score well in a pixel metric while the hero, controls and world are wrong.

## Iteration discipline

Change the largest visible mismatch first, keep the same capture state, and compare again. Keep a small revision history with screenshots and source fingerprints. Treat direction consistency as an invariant as the game grows. Preserve accepted assets; a new generation is a controlled replacement, not a random improvement attempt.

Performance tradeoffs should remove distant density, reduce shadow cost or simplify hidden geometry before changing the focal silhouette, key colors or typography. A painterly reference may be better served by painted billboards with depth-aware occlusion than by an expensive but generic 3D model. A solid moving object may need actual geometry. Choose per asset.
