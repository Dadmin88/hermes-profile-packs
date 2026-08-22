---
name: scene-optimization
description: Optimize environment scenes using measured visibility, geometry, materials, lighting, textures, VFX, culling, streaming, LOD, and instance behavior while preserving composition and gameplay.
---
# Environment Scene Optimization

Use when an environment scene exceeds or threatens runtime budgets.

## Procedure
1. Profile the representative scene on target hardware or a meaningful proxy and identify dominant CPU, GPU, memory, or streaming costs before editing assets.
2. Break cost down by geometry, draw calls or materials, overdraw or transparency, shadows or lighting, textures, VFX, scripts, collision, navigation, and streaming as relevant.
3. Prioritize changes with the largest measured impact and lowest visible or gameplay cost.
4. Use instancing, LOD or HLOD, occlusion or frustum culling, streaming or chunking, texture budgets, material consolidation, and baked data where supported and appropriate.
5. Optimize high-cost hero assets in context rather than uniformly degrading every asset.
6. Check sightlines and player or camera movement so culling or streaming does not create pop-in, missing geometry, or gameplay information loss.
7. Re-profile after each meaningful class of change under comparable conditions and record before and after metrics.
8. Validate the final scene visually and behaviorally, including lighting, collision, navigation, VFX, and state changes.

## Decision rules
- Optimize from measured scene cost, not folklore.
- Scene composition and visibility strategy can outperform asset-by-asset micro-optimization.
- Do not trade away gameplay readability or obvious art quality for negligible savings.
- Fleet node hardware may differ; record the measured target and do not assume one workstation's result is universal.

## Quality gate
The scene is optimized when the original bottlenecks are measurably improved, target budgets are met or remaining gaps are explicit, visual and gameplay integrity are preserved, streaming or culling remains stable in motion, and before and after evidence is reproducible.