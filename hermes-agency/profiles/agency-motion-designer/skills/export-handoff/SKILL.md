---
name: export-handoff
description: Prepare motion deliverables for engineering, video, web, social, or runtime use with correct dimensions, frame rate, alpha, color, compression, loop points, states, timing specs, and source traceability.
---
# Motion Export Handoff

Use when completed motion work must move reliably into another production or runtime system.

## Procedure
1. Confirm the receiving platform and exact deliverable contract: dimensions or aspect, frame rate, duration, codec or format, alpha, color space, file-size budget, looping, and supported features.
2. Separate baked video or raster deliverables from parameterized or runtime animation handoffs; do not export video when engineering needs states, curves, or vector assets.
3. Name and version deliverables consistently and preserve the approved source or project revision.
4. Check safe areas, crop behavior, text legibility, localization space, and platform UI overlays for published video or social formats.
5. Verify alpha edges, premultiplication, gradients, banding, color shifts, frame cadence, audio sync, and loop seams after export.
6. For runtime handoff, provide state names, triggers, durations, easing, transforms or properties, asset dependencies, reduced-motion behavior, and interruption rules.
7. Import or preview the result in the actual receiving system where possible rather than trusting the export preview.
8. Package source or reference files and notes with portable relative structure rather than machine-local absolute paths.

## Decision rules
- Choose deliverables from the receiver's needs, not the motion tool's easiest export.
- Video, vector animation, sprite sequence, native UI animation, and engine animation have different constraints.
- Always validate the encoded or imported result.
- Portable handoff matters when work can move across Fleet nodes.

## Quality gate
The handoff is complete when the receiving system reproduces the approved motion without color, alpha, timing, or loop surprises, implementation states and accessibility behavior are documented where needed, files meet platform budgets, and source-to-export traceability is preserved.