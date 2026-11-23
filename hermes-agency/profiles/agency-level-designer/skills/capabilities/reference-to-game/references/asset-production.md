# Reference-guided asset production

Plan per asset, not per model. In `assets.json`, record identity, source reference IDs, intended screen size, representation, required views/states, collision role, pivots/sockets, quality constraints, status and final runtime path. Include provenance and permitted use. Reuse suitable originals and accepted outputs before generating replacements.

## Choose the representation that protects style

| Need | Useful approach | Runtime acceptance |
|---|---|---|
| Painted character with fixed camera | Isolated transparent turnaround and animation strips | Same face/costume/proportions in every view; aligned feet and baseline; no matte fringe |
| Free-view vehicle or prop | Reference isolation → image-to-3D → mesh cleanup | Scale, silhouette, rear/side views, normals, materials, pivots, sockets, reasonable topology |
| Repeated environment | Small varied modular kit, procedural placement, texture/foliage atlases | No obvious repetition, valid transitions, collision clearance, LOD continuity |
| UI family | Consistent icon sheet / vector or raster assets; real text in DOM | Readable at actual size, consistent weight, transparent background, no baked gibberish |
| Materials | Seamless or projected textures, controlled procedural shader | Correct color space, repeat seams, scale, roughness, normal strength, animated stability |
| Sound and music | Designed or generated cues and loops | Listen, trim silence, crossfade seams, headroom, rate limits, gameplay-triggered timing |
| Motion reference | Short controlled animation study | Reference only; implement action-driven animation rather than playing it as the game |

## Mesh and sprite integration

A beautiful isolated output can fail in game. Check it under the actual camera and lighting. Normalize geometry and ground contact, preserve UVs, inspect alpha edges, and define attachment sockets in the correct local coordinate frame. If the object needs independent limbs, generation of one static mesh does not provide a rig. Choose skeletal animation, authored parts, blend shapes, view-specific sprites or a clearly scoped deformation strategy.

Keep a small acceptance record: source → generation/edit → cleanup → runtime file → in-engine capture. Reject an unsuitable output explicitly; do not silently keep expensive dead assets in the bundle. Preserve originals and derivation scripts so a future edit does not require guessing how an asset was transformed.

Use consistent reference images and identity constraints across generation calls. Changing the hero's face, costume blocks or silhouette to get a prettier single frame is a regression. Generate assets at the resolution and view coverage they need; an environment backdrop should not replace the playable level.
