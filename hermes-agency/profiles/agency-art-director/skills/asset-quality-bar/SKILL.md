---
name: asset-quality-bar
description: Define and apply a measurable acceptance bar for visual assets covering artistic coherence, readability, technical fitness, reuse, and final-context validation.
---
# Asset Quality Bar

Use when a project needs consistent acceptance criteria for visual assets before integration or release.

## Procedure
1. Define the asset categories, usage distances or sizes, target platforms, style requirements, and technical constraints that make quality context-dependent.
2. Specify the visual checks that matter for the category, such as silhouette, value grouping, texture density, material response, topology readability, icon clarity, or animation cleanliness.
3. Specify technical acceptance checks such as dimensions, format, naming, pivots, collision, LOD, UVs, compression, alpha, memory, or export settings only where relevant.
4. Define what must be tested in final context rather than approved from an isolated editor preview.
5. Create severity levels for blocking defects, polish issues, and optional enhancements.
6. Use representative good and bad examples to calibrate the bar across reviewers and creators.
7. Apply the bar consistently while allowing intentional exceptions approved by art direction.
8. Revisit the bar when platform targets, engine constraints, or visual direction change materially.

## Decision rules
- Quality is fitness for use, not maximum detail.
- Technical perfection cannot rescue an asset that fails the approved visual direction.
- Do not force every asset category through irrelevant checks.
- Final-context validation is mandatory when lighting, scale, motion, or neighboring content changes perception.

## Quality gate
The quality bar is ready when creators and reviewers can independently classify asset readiness with similar results, irrelevant checks are excluded, final-context proof is required where perception depends on it, and exceptions remain explicit rather than accidental.