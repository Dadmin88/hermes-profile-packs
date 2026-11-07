---
name: pixel-asset-export
description: Safely operate Pixelorama or Aseprite and verify pixel-art delivery files, spritesheets, atlas metadata, transparency, and runtime import handoffs.
---
# Pixel Asset Export

1. Select the editor that owns the editable source. Use `profile-capabilities` to discover approved tools and read [editor setup](references/editors.md) for the bridge contract and CLI fallback. If neither editor is available, separate any preview PNG you can produce from the editable deliverable the request needs.
2. Record source path, grid, origin, frame order, durations, and output destination. Inspect the active project and layer/cel or the exact working file before changing it. Export to a new path or confirm the intended replacement. Preserve the original.
3. Export at native resolution. Preserve alpha and the agreed color mode. Keep frame bounds fixed unless the consumer supports trim offsets and stable pivots. Record frame cell size, sheet order, margin, spacing or extruded padding, tags, and duration. Verify an atlas and its metadata together.
4. Open the export independently and check actual dimensions, transparency, palette, grid, and frame count or tile indices. Inspect at 1× and integer nearest-neighbor zoom. If the project is available, verify the import at intended scale and filtering. For Godot, check project or node texture filtering, integer presentation where required, and the imported atlas cell or region dimensions.
5. Deliver the editable project, native export, applicable metadata, and a preview. Record checks actually performed and any remaining engine-side work.

**Quality gate** — The export can be re-opened, its layout and metadata agree, and the next owner can reproduce the import with the supplied settings.
