---
name: modular-kit
description: Design a reusable environment kit with coherent dimensions, pivots, snapping, variation, material strategy, seams, collision, LOD, and composition flexibility.
---
# Modular Environment Kit

Use when building reusable architectural or environmental assets for many scenes or world sections.

## Procedure
1. Define the environment language, gameplay or camera scale, grid or dimensional logic, target platforms, and expected assembly workflows.
2. Identify the smallest useful set of structural modules and variants needed to produce meaningful composition diversity.
3. Standardize dimensions, pivots or origins, snapping surfaces, wall or floor thicknesses, and connection rules so modules assemble predictably.
4. Plan material reuse, trim sheets, tiling textures, decals, vertex blends, or other variation systems to control memory and repetition.
5. Test seams, lighting continuity, collision, navigation, occlusion, and LOD behavior at common module junctions.
6. Build representative compositions early to expose missing corner, transition, cap, damage, or elevation pieces.
7. Add variation through props, material masks, decals, and alternate modules without exploding the core kit count.
8. Document naming, export, and import conventions and test the kit in the actual engine or editor on a fresh scene.

## Decision rules
- A modular kit should maximize useful composition space, not module count.
- Grid consistency matters only where the composition workflow depends on it.
- Variation systems should fight repetition without destroying art-direction coherence.
- Test junctions and transitions early; they reveal kit flaws faster than isolated hero pieces.

## Quality gate
The kit is ready when creators can assemble varied environments quickly, modules connect without recurring seam, scale, or pivot issues, materials and runtime cost are controlled, key transitions exist, and the kit has been proven in real engine compositions rather than only in an asset browser.