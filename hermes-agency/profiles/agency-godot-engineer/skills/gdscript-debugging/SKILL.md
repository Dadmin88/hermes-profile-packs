---
name: gdscript-debugging
description: Diagnose Godot/GDScript failures by reproducing the scene lifecycle, reading engine/runtime evidence, tracing signals and references, isolating timing/state assumptions, and validating the fix in the real project.
---
# GDScript Debugging

Use for GDScript errors, wrong scene behavior, missing signals, invalid references, lifecycle/timing bugs, state corruption, or intermittent engine-side behavior.

## Procedure
1. Record the Godot version, project/scene, reproduction steps, editor versus exported/runtime context, exact error/warning, and whether the failure depends on reload, scene transition, input, frame/physics timing, or platform.
2. Reproduce from a known scene/project state before editing and inspect the full debugger/output/stack evidence instead of only the last message.
3. Trace node/resource ownership and lifecycle around the failure: when the object is instantiated, enters/exits tree, becomes ready, processes, emits/receives signals, is queued/freed, or survives a scene change.
4. Verify node/resource references and exported dependencies against the actual scene tree/instances. Check for stale references, duplicated instances, missing initialization, and assumptions about editor-only nodes/resources.
5. Trace signal connections and callbacks, including who connects, how many times, argument shape, object lifetime, and whether deferred/awaited work runs after the owning node changes or is freed.
6. Check state/timing boundaries: `_process` versus physics/update timing, deferred calls, async/await continuation, timers, animation events, input ordering, and scene changes as relevant to the actual Godot version/project.
7. Form one hypothesis and add the smallest logging/breakpoint/assertion or isolated reproduction needed to test it. Avoid rewriting scene architecture before locating the first bad state transition.
8. Apply the fix at the owning lifecycle/state boundary and clean up temporary diagnostics that would create noise.
9. Re-run the original flow plus scene reload/transition/restart or export path implicated by the bug, and check the editor/runtime for new warnings/errors.
10. Add a focused automated or reproducible regression check when the project/test framework can capture the failure reliably.

## Decision rules
- Many Godot bugs are lifecycle/ownership bugs disguised as null-reference or timing errors; inspect when the node/resource is valid, not only whether a path exists.
- Do not suppress engine warnings blindly; determine whether they reveal an actual project defect.
- Version-specific lifecycle/API behavior should be confirmed from current official Godot documentation when uncertain.
- If the issue is asset/shader/pipeline-specific, hand the reproduction to `agency-technical-artist` with the scene/runtime evidence.

## Quality gate
The bug is resolved when the failing scene flow is reproducible and explained, the first invalid state/lifecycle assumption is identified, the fix lives at the responsible boundary, the original and adjacent transition/reload/export paths pass, and runtime/editor diagnostics no longer show the defect.