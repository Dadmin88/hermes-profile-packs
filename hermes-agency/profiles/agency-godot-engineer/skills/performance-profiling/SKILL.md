---
name: performance-profiling
description: Profile Godot runtime performance across frame time, script/engine work, physics, rendering/GPU, memory/allocations, nodes/resources, asset loading, and platform/export differences using measured engine evidence.
---
# Godot Performance Profiling

Use when a Godot project has frame drops, slow scenes, input lag, physics cost, excessive loading, memory pressure, or platform-specific performance problems.

## Procedure
1. Define the symptom and target platform with a measurable scenario: frame time/FPS distribution, input responsiveness, scene load, physics step, memory, draw/render cost, or another user-visible metric.
2. Reproduce using the relevant build/editor/export mode and representative scene/entity/asset count. Record Godot version, renderer/platform, resolution, project settings, and hardware that materially affect the result.
3. Use Godot's current profiling/monitor/debug tools and platform GPU/CPU tools where appropriate to separate script, physics, rendering, GPU, memory, navigation/audio/other engine subsystems, and waiting/idle behavior.
4. Identify whether the bottleneck is CPU main thread, script, physics, render submission, GPU, asset/resource loading, allocation/GC-like churn, excessive nodes/signals, or another measured subsystem before changing architecture.
5. Drill into the dominant path: expensive callbacks, per-frame loops, repeated lookups/allocations, too many active entities, physics queries/bodies, draw calls/material/state changes, overdraw/shaders, texture/mesh size, streaming/load synchronization, or project-specific work as evidence suggests.
6. Disable/simplify one suspected subsystem or workload dimension at a time to test causality. Measure the response instead of trusting intuition.
7. Optimize according to the bottleneck using engine-appropriate patterns for the project's Godot version, then re-profile the same scenario.
8. Check shifted costs and correctness: memory versus speed, CPU versus GPU, visual quality, physics fidelity, input, lifecycle, and loading behavior.
9. Validate on target exported builds/devices because editor/debug behavior and desktop hardware can differ materially from shipped targets.
10. Preserve a representative benchmark/profile scene or automated performance check when the budget is a durable requirement.

## Decision rules
- Do not optimize GDScript because the project is slow until profiling shows script cost is actually dominant.
- Node count, draw calls, allocations, or physics objects are clues, not universal thresholds; measure the project's bottleneck.
- Verify version-specific Godot optimization APIs/settings against current official documentation.
- Art/shader/asset bottlenecks may require `agency-technical-artist` ownership; system-wide benchmark methodology can involve `agency-performance-engineer`.

## Quality gate
The performance problem is solved when the target scenario is measured on relevant builds/hardware, the dominant engine/resource bottleneck is identified with profiler evidence, the optimization measurably improves the target without unacceptable quality/correctness tradeoffs, and regression evidence exists for performance that must remain bounded.