# 3D concept-to-runtime pipeline

Use this reference when the output is a model, material, texture set, rig, animation, or 3D prop
family. An appealing render proves appearance only; it does not prove production geometry.

## Default pipeline

1. Lock camera/view, scale, gameplay footprint, material language, polygon/texture budgets, target
   engine, renderer, and platform.
2. Create or select orthographic/turnaround concepts with consistent proportions. Treat generated
   multi-view sheets as references that still require geometric interpretation.
3. Author or clean the model in a DCC such as Blender. Inspect topology, normals, watertightness,
   UVs, texel density, material slots, rig, weights, and animation clips.
4. Apply/normalize transforms and set a gameplay-meaningful origin and pivot.
5. Create simplified collision proxies. Do not use a detailed render mesh as default collision.
6. Define LODs and material/texture reuse for repeated or distant objects.
7. Export using the engine's preferred interchange path. Use GLB/glTF 2.0 as the general runtime
   delivery default when the target supports it; keep editable DCC sources separately.
8. Import into the real engine, check scale/orientation/materials/animation, profile memory and draw
   calls, and capture representative screenshots before approval.

## Geometry gates

- silhouette fits gameplay and LOD transitions preserve it
- no accidental internal faces, non-manifold regions, inverted normals, or degenerate geometry
- deformation loops support the required rig motion
- pivots/origins support doors, wheels, pickups, weapons, placement, and snapping
- units and forward/up axes match the project convention
- collision proxies match gameplay intent without excessive detail

## Material and texture gates

- use consistent PBR channel conventions and color spaces
- avoid baking lighting into base color unless the art direction explicitly requires it
- pack channels only when the target pipeline documents the mapping
- keep texel density consistent across an asset family
- size textures from on-screen coverage; source resolution is not a runtime budget
- reuse materials/atlases where it reduces draw calls without harming iteration
- validate normal-map orientation and compression in the target renderer

## Generated 3D caution

If a tool can generate meshes, inspect the result with the same gates as an authored mesh. Never
infer clean topology, UVs, rigging, licensing, or efficient materials from a preview render. Keep
the tool/version and generation input in the asset manifest.

## Primary documentation

- [Khronos glTF registry and 2.0.1 specification](https://registry.khronos.org/glTF/)
- [Godot 4.7 importing 3D scenes](https://docs.godotengine.org/en/4.7/tutorials/assets_pipeline/importing_3d_scenes/index.html)
- [Unity 6.3 Model tab import settings](https://docs.unity3d.com/6000.3/Documentation/Manual/FBXImporter-Model.html)
- [Unreal Engine importing static meshes](https://dev.epicgames.com/documentation/en-us/unreal-engine/importing-static-meshes-using-fbx-in-unreal-engine)
- [three.js GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html)
