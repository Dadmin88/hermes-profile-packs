---
name: texture-workflow
description: Create and validate texture sets with intentional material definition, texel density, channel packing, tiling, color management, compression, and runtime context.
---
# Texture Workflow

Use when producing or revising textures for 2D or 3D production assets.

## Procedure
1. Confirm the target asset, renderer or material model, texture budget, resolution range, color-space expectations, and platform constraints.
2. Establish texel density and reuse strategy relative to neighboring assets before painting detail.
3. Build material information by physical or visual function rather than baking lighting or noise indiscriminately into every channel.
4. Keep seams, tiling, edge wear, decals, masks, and variation intentional at the viewing distances where the asset will appear.
5. Pack and name channels according to the project's material contract, preserving linear versus color data correctly.
6. Preview under representative lighting and material settings rather than judging texture maps only in the authoring tool.
7. Test compression, mip behavior, memory footprint, and alpha artifacts on the target runtime when those can affect quality.
8. Deliver source and exported textures with enough provenance and version context for another node or artist to reproduce the result.

## Decision rules
- Texture detail should support material readability at target distance, not merely look busy at 100% zoom.
- Color-space and channel semantics are part of the material contract.
- Do not bake environment-specific lighting into reusable material data unless that is an intentional style choice.
- Prefer reusable masks or tiling where they preserve quality and materially reduce memory.

## Quality gate
The texture set is done when the material reads correctly in target lighting and scale, channel semantics and color management are correct, seams, compression, and mips are acceptable, runtime cost fits the budget, and source or export artifacts are reproducible.