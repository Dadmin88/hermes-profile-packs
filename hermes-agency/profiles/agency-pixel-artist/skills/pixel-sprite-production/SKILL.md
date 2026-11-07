---
name: pixel-sprite-production
description: Design and edit native-resolution pixel sprites, icons, character poses, and props with consistent palettes, silhouettes, perspective, and transparent edges.
---
# Pixel Sprite Production

1. Read the brief and inspect one neighboring asset at 1×. Record canvas bounds, subject height, facing, baseline or origin, camera projection, outline policy, light direction, and palette. For a revision, preserve the existing grid and work on a duplicate unless the brief authorizes overwriting.
2. Block the silhouette with a few large shapes. Test against representative game backgrounds and next to a known-size object. Keep the darkest and lightest accents where they clarify the focal point.
3. Assign a small value ramp to each key material and reuse shared colors. Place purposeful pixel clusters before individual pixels. Check diagonal stair steps, corner thickness, and negative space. Use dithering, isolated pixels, and partial alpha only when intentional and consistent with the style.
4. Build on named layers where they improve editability. Inspect project dimensions, active layer, and frame before drawing. Batch pixel placement and review a preview after each meaningful pass. Use a known-good first pose as the reference for additional facings.
5. Inspect at 1× and integer zoom. Check the silhouette, scale, palette exceptions, stray pixels, transparency, and any clipping or unwanted smoothing. Save an editable source and send it through `pixel-asset-export` when delivery is requested.

**Quality gate** — A sprite reads at target scale, uses deliberate clusters and edges, and registers against its neighbors on the agreed pixel grid.
