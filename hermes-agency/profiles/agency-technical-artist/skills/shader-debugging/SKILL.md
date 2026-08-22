---
name: shader-debugging
description: Diagnose shader and material failures using reproduction, render-state inspection, inputs, spaces, precision, variants, platform differences, and frame or debugger evidence.
---
# Shader Debugging

Use when a shader renders incorrectly, inconsistently, too slowly, or only fails on certain assets or platforms.

## Procedure
1. Capture the failing material or shader revision, renderer, platform or GPU, scene, camera and light conditions, asset inputs, and exact visual symptom.
2. Reduce to the smallest reproducing material, mesh, texture set, pass, or feature toggle while preserving the defect.
3. Inspect shader inputs and coordinate spaces: UVs, normals or tangents, world, view or object space, color space, texture channels, vertex attributes, time, and uniform values.
4. Check render state and pipeline assumptions such as blend, depth, cull, transparency order, shadow pass, keywords or variants, instancing, batching, and render queue.
5. Use engine frame capture, shader debugger, generated shader code, or visualization outputs where available to locate the first bad stage.
6. Check precision, NaN or Inf, division or normalization, derivative, mip or LOD, and platform-specific limits when the defect is hardware-dependent.
7. Fix the owning layer rather than adding compensating constants that only hide one asset or camera condition.
8. Re-test on representative assets, lighting, distances, variants, and target platforms; record performance impact if the fix changes shader cost.

## Decision rules
- Visual artifacts are evidence; identify the pipeline stage that first becomes wrong.
- Do not assume the shader code is at fault when mesh attributes or import settings are wrong.
- Platform-specific precision and compiler behavior should be verified on target hardware.
- A fix that materially raises shader cost needs performance review.

## Quality gate
The shader issue is resolved when the root cause is demonstrated, the corrected output is stable across relevant variants, assets, and platforms, render-state and input assumptions are explicit, and no material performance regression is hidden.