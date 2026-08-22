---
name: scene-architecture
description: Design Godot scene and resource architecture around ownership, composition, lifecycle, reusable data, signals/interfaces, autoload boundaries, instancing, and testable gameplay/UI responsibilities.
---
# Godot Scene Architecture

Use when a Godot feature or project needs durable scene/node/resource boundaries rather than ad hoc node references and global state.

## Procedure
1. Confirm the project's Godot version, existing scene conventions, autoloads, resource/data patterns, and target platforms before introducing a new architecture style.
2. Define ownership by lifecycle: which scene/node creates, owns, and frees each piece of state or behavior, and which objects must survive scene transitions.
3. Use scene composition for reusable runtime structures and Resources or other data objects for reusable/configurable data where that matches the project's established pattern.
4. Keep child-internal implementation behind clear methods, signals, groups, or typed/public interfaces rather than deep brittle node-path access from unrelated scenes.
5. Choose signal versus direct reference based on ownership and coupling. Parent-to-owned-child calls can be direct; decoupled event notification can use signals without turning every interaction into a global event bus.
6. Use autoload/singleton scope only for truly application-wide services/state whose lifetime requires it. Do not move local feature state global merely to make references easy.
7. Separate domain/game state from presentation/scene-instance state so reloading or re-instancing visuals does not accidentally reset authoritative progress unless that is the intended lifecycle.
8. Define instancing, initialization, dependencies, and cleanup so scenes can be opened/tested in isolation when practical and do not depend on hidden editor hierarchy accidents.
9. Handle scene changes, freed nodes, deferred operations, and signal disconnect/lifetime behavior explicitly for objects that outlive or observe one another.
10. Validate by instancing/reloading representative scenes, running transitions, and checking the editor/runtime for missing references, orphaned/global state, duplicate initialization, and unexpected persistence.

## Decision rules
- Scene trees are ownership/lifecycle structures, not merely folders for visual objects.
- Avoid deep `get_node` knowledge across feature boundaries when a small explicit interface can protect the scene structure.
- Autoload is a lifecycle tool, not the default dependency-injection mechanism.
- Verify version-specific engine APIs and scene/resource behavior against current official Godot documentation during implementation.

## Quality gate
The architecture is ready when scene/resource ownership and lifetime are clear, reusable data and runtime instances are separated appropriately, dependencies do not rely on fragile hierarchy knowledge, global state is justified, scene transitions/reloads preserve intended state, and representative scenes can be instantiated and exercised without hidden setup.