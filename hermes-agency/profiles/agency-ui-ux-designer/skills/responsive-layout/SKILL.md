---
name: responsive-layout
description: Design layouts that preserve hierarchy, readability, interaction, and content priority across viewport, window, orientation, zoom, text expansion, and input differences without treating breakpoints as separate products.
---
# Responsive Layout

Use when an interface must adapt across screen sizes or resizable application surfaces.

## Procedure
1. Identify content hierarchy, interaction priorities, minimum usable sizes, likely device or window classes, and platform conventions.
2. Design flexible relationships first using intrinsic content behavior, wrapping, reflow, flexible grids, and component constraints before choosing breakpoints.
3. Choose breakpoints where the composition actually needs structural change rather than copying device marketing widths.
4. Define how navigation, tables, forms, sidebars, dialogs, media, and dense controls reflow, collapse, scroll, or progressively disclose.
5. Test long content, localization expansion, large text or zoom, virtual keyboard, safe areas, orientation changes, pointer versus touch, and reduced available height.
6. Preserve meaningful reading and focus order when visual layout changes; avoid layout tricks that create contradictory semantic order.
7. Specify minimum and maximum widths, truncation or wrapping behavior, touch targets, and overflow handling for implementation.
8. Validate representative states at intermediate widths, not only a few pristine breakpoint screenshots.

## Decision rules
- Responsive design is continuous adaptation, not three fixed screenshots.
- Breakpoints should emerge from content and interaction needs.
- Do not hide essential capabilities on small screens without a product decision.
- Visual reorder should not break semantic or keyboard order.

## Quality gate
The responsive design is ready when hierarchy and task completion remain intact across realistic width, height, text, and input conditions, overflow and reflow rules are explicit, intermediate sizes do not collapse unpredictably, and engineering can implement behavior rather than guessing between breakpoint mockups.