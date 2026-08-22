---
name: godot-feature-implementation
description: Implement and validate a Godot feature using scene/resource ownership, signals, node lifecycle, engine APIs, performance awareness, and in-editor/runtime proof.
---
# Godot Feature Implementation

Use for Godot gameplay, tools, UI, scene, resource, or engine-integration work.

## Procedure
1. Identify the Godot version, project conventions, scene ownership, resource types, and target platforms.
2. Inspect existing scene trees, autoloads, signals, groups, scripts, and data flow before adding parallel systems.
3. Choose node/resource boundaries that fit Godot's lifecycle and keep reusable data separate from scene-instance state.
4. Use signals or direct references intentionally; avoid global coupling where local ownership is clearer.
5. Handle `_ready`, process/physics timing, input, deferred calls, and freed-node references carefully.
6. Validate the feature in the editor/runtime under realistic scene transitions and reloads.
7. Check warnings/errors, exported properties, serialization, performance hot paths, and project settings affected by the change.

## Quality gate
The feature must survive normal scene lifecycle and run in the target project, not merely compile as GDScript.