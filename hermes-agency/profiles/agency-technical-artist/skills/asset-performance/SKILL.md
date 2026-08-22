---
name: asset-performance
description: Profile and optimize art-asset runtime cost across geometry, materials, textures, animation, VFX, draw calls, overdraw, memory, streaming, and scene density without sacrificing visible intent blindly.
---
# Asset Performance

Use when art content is suspected of causing runtime performance or memory pressure.

## Procedure
1. Profile representative scenes and target hardware to identify the asset class and cost actually responsible.
2. Break cost into geometry or vertices, materials or draw calls, texture memory or bandwidth, transparency or overdraw, shader complexity, skinning or morphs, particles or VFX, animation, collision, and streaming as relevant.
3. Trace expensive content back to source or import settings so changes can be made at the right layer.
4. Prioritize optimizations by measured savings and perceptual or gameplay impact.
5. Choose LOD, atlas or material consolidation, texture resizing or compression, shader simplification, particle limits, skinning reduction, instancing, culling, or streaming changes according to the bottleneck.
6. Coordinate with artists to preserve silhouette, material identity, animation deformation, and art direction where users actually notice them.
7. Re-profile under the same workload and compare before and after metrics plus visual regressions.
8. Document budgets and recurring failure patterns so future assets can avoid the same cost.

## Decision rules
- Art optimization starts from measured runtime cost.
- Optimize the expensive dimension, not the easiest attribute to count.
- Technical Artist bridges art intent and engine cost; neither side should be ignored.
- One powerful workstation is not representative of all Fleet or target devices.

## Quality gate
The optimization is complete when the targeted asset cost is measurably reduced in representative scenes, visible or artistic loss is within the accepted threshold, import and source changes are reproducible, and useful budget guidance is captured for future production.