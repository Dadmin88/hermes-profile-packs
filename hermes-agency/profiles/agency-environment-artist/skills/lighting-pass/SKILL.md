---
name: lighting-pass
description: Create and validate an environment lighting pass for readability, mood, focal hierarchy, gameplay or navigation, material response, state variation, performance, and exposure.
---
# Environment Lighting Pass

Use when an environment or scene needs authored lighting beyond basic illumination.

## Procedure
1. Define the scene's narrative or gameplay purpose, desired mood, focal areas, traversal or readability needs, camera, and platform or runtime constraints.
2. Establish primary light direction, contrast structure, ambient or fill level, exposure, and color relationship before adding decorative lights.
3. Use lighting to guide attention and navigation while preserving believable or intentionally stylized source logic.
4. Review material response, character readability, VFX, UI overlays, and important interactables under the lighting.
5. Control shadow count or range, volumetrics, baked versus dynamic contribution, probes, reflection data, and other expensive features according to the renderer.
6. Check multiple viewpoints and movement paths, not just one beauty camera.
7. Validate alternate time, weather, or state transitions and exposure adaptation where the environment changes dynamically.
8. Profile the lighting configuration on representative target hardware and revise effects that consume budget without visible benefit.

## Decision rules
- Lighting is composition and information, not only realism.
- Decorative lights should not flatten the primary hierarchy.
- Judge performance using the actual renderer and target scene complexity.
- Gameplay readability can justify stylized departures from physically plausible lighting.

## Quality gate
The lighting pass is ready when mood and hierarchy support the scene's purpose, navigation and important elements remain readable, materials and VFX translate correctly, dynamic states are coherent, and measured runtime cost fits the target without relying on one showcase viewpoint.