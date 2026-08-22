---
name: procedural-tools
description: Design procedural art tools that encode repeatable artistic constraints while exposing useful controls, deterministic generation, editable outputs, performance limits, and safe artist override.
---
# Procedural Art Tools

Use when artists repeatedly build variations or environments through a workflow that benefits from controlled generation.

## Procedure
1. Observe the manual workflow and identify repeated decisions that can be automated without erasing important artistic judgment.
2. Define inputs, constraints, deterministic seed or state, outputs, editable boundaries, and the artist decisions that must remain exposed.
3. Prototype the smallest generator that proves the workflow before building a general node graph, plugin, or system.
4. Make generated output inspectable and editable where production needs manual art direction after generation.
5. Bound complexity and resource use so a parameter cannot accidentally create unmanageable geometry, textures, instances, or build times.
6. Provide predictable naming, grouping, metadata, and regeneration behavior so generated assets can move through export and build pipelines.
7. Test determinism, undo and redo, parameter extremes, version upgrades, broken or missing source assets, and regeneration of existing content.
8. Document the artistic intent of controls and common workflows rather than only technical parameter definitions.

## Decision rules
- Automate repetition, not taste.
- Procedural output should remain art-directable.
- Deterministic seeds or state matter when content must be reproduced on another machine.
- Do not build a universal tool before one real workflow proves the abstraction.

## Quality gate
The tool is ready when artists can produce useful controlled variation faster than manually, outputs are reproducible and editable, pathological parameters are bounded, regeneration and version behavior are predictable, and documentation explains the artistic workflow rather than merely listing controls.