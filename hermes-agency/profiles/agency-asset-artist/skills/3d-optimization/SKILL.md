---
name: 3d-optimization
description: Optimize 3D assets for runtime while preserving silhouette and material intent through geometry, LOD, UV, draw-call, skinning, collision, and import decisions.
---
# 3D Asset Optimization

Use when a 3D asset needs to meet runtime performance budgets without visibly damaging the approved look.

## Procedure
1. Measure the asset in target scenes first: triangle or vertex count, materials, draw calls, texture memory, skinning, overdraw, collision, and observed performance where available.
2. Identify the visual features that must survive optimization: silhouette, deformation, close-up detail, material breaks, and gameplay-relevant geometry.
3. Remove or simplify geometry that does not contribute at target viewing distance while preserving topology needed for shading and deformation.
4. Design LODs or distance variants around perceptual change and transition behavior rather than arbitrary percentage reductions.
5. Reduce unnecessary material slots and unique texture sets when batching or atlasing can preserve the art direction.
6. Review UVs, normals, tangents, smoothing, lightmap data, vertex attributes, and skin weights after topology changes.
7. Use simplified collision or physics meshes appropriate to gameplay rather than rendering geometry by default.
8. Validate import settings and runtime appearance across representative distances, animation, lighting, and target hardware.

## Decision rules
- Optimize measured bottlenecks and budget pressure, not polygon count as a vanity metric.
- Silhouette and deformation usually deserve more geometry than hidden flat surfaces.
- Fewer materials can matter more than fewer triangles depending on the renderer and scene.
- Collision complexity should follow gameplay need, not visual mesh fidelity.

## Quality gate
The asset is optimized when it meets its runtime budget under representative conditions, perceptually important form and deformation are preserved, LOD, import, and collision behavior are stable, and the optimization has measurable benefit without visible regressions beyond the accepted threshold.