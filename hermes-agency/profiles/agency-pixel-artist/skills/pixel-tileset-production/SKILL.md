---
name: pixel-tileset-production
description: Design or curate pixel terrain tiles, test seamless repetition and adjacency, and deliver paintable atlases with explicit grid and terrain rules.
---
# Pixel Tileset Production

1. Confirm tile size, projection, terrain scheme, atlas origin, margin and spacing, and whether collision or overlays are separate. Read the engine's existing terrain rules before choosing a mask format. For sourced tiles, verify usage rights and record source, author, license, and attribution.
2. Start with the repeatable base. Preview a patch of at least 3×3 copies at 1×. Check edge alignment, obvious repeating motifs, directional shadows, and noise that competes with gameplay. Add controlled variants whose boundary pixels work against the base and one another.
3. List the required connections before drawing transitions. Include outer edges, convex corners, concave corners, isolated cells and diagonal cases if supported by the terrain scheme. Keep decorative overlays and collision intent separate when the project supports that split.
4. Build a small adjacency sheet or paint test containing all supported transitions, a long run, and mixed variants. Mark missing transitions explicitly and correct atlas row or column offsets before adding more tiles.
5. Export the native PNG atlas and give the importer tile dimensions, atlas origin and spacing, terrain groups, variant intent, and any overlay/collision conventions. Include an adjacency preview and state whether it was checked in the target engine.

**Quality gate** — A new painter can place the delivered tiles on the intended grid, and repeat and transition checks cover every claimed connection.
