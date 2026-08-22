---
name: sprite-production
description: Produce sprites and sprite sheets with clear silhouettes, consistent scale, animation-ready registration, clean transparency, sampling discipline, and runtime validation.
---
# Sprite Production

Use when creating 2D game, UI, icon, or animated sprite assets.

## Procedure
1. Confirm target resolution, display scale, camera or UI context, art direction, animation needs, and import constraints.
2. Establish silhouette, value grouping, palette, and scale relative to neighboring sprites before polishing interior detail.
3. Maintain consistent pivot or origin, baseline, bounds, and padding so static and animated frames register correctly.
4. Handle transparency, edge pixels, premultiplication or bleeding, and atlas padding according to the target renderer.
5. For pixel art, preserve intentional pixel scale and sampling rules; for vector or raster hybrids, validate rasterization at actual display sizes.
6. Build animation frames around readable poses and timing, checking loops and transitions in motion rather than frame-by-frame only.
7. Pack atlases or sheets according to runtime requirements and confirm cropping, rotation, or trimming do not break pivots or effects.
8. Validate the imported sprite in the actual engine or UI with target scaling, filtering, lighting, tinting, and neighboring content.

## Decision rules
- Readability at target size matters more than detail visible only in the source file.
- Do not let automatic atlas trimming silently change gameplay or UI alignment.
- Pixel-art sampling and vector scaling are different production problems; use the appropriate discipline.
- Animation quality must be judged in motion.

## Quality gate
Sprite production is complete when silhouettes and scale are coherent, pivots and bounds remain stable, transparency and sampling are clean, animation reads in motion, atlas and import behavior are correct, and the asset survives real runtime presentation.