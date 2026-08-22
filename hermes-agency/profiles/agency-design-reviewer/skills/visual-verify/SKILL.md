---
name: visual-verify
description: Prove a visual or interaction change on the rendered product by capturing the real surface, comparing it with the intended reference and neighboring system, checking relevant states, and recording visible discrepancies before sign-off.
---
# Visual Verification

Use after UI, layout, theme, responsive, motion, design-system, or other user-visible changes when code/tests alone cannot prove visual correctness.

## Procedure
1. Identify the exact build/revision, target surface, viewport/device/platform, and reference: approved design, screenshot, specification, established neighboring surface, or intentionally documented before state.
2. Run or access the actual rendered product in a representative environment rather than reviewing only source code or component definitions.
3. Capture evidence such as screenshots or video for the important state and note the environment used.
4. Compare structure, hierarchy, spacing, sizing, alignment, typography, color/contrast, borders/elevation, imagery, icons, content, and responsive behavior relevant to the change.
5. Exercise interactive states where applicable: hover, focus, active, selected, disabled, loading, error, empty, modal/popover, animation, and transitions.
6. Check at least the breakpoints, themes, zoom/text scaling, or device states whose behavior could plausibly differ because of the change.
7. Compare against existing design-system primitives and neighboring product surfaces so local correctness does not create system inconsistency.
8. Record discrepancies as observable differences with evidence and expected behavior, not aesthetic vibes alone.
9. After corrections, capture the surface again and verify the original discrepancy plus any nearby state the fix could have affected.
10. Sign off only on the environments and states actually examined; state any visual coverage limits explicitly.

## Decision rules
- Passing unit/type/build checks cannot prove rendered visual correctness.
- A design file is a reference, but platform constraints and approved implementation decisions may explain deliberate differences.
- Do not claim responsive or cross-platform correctness from one desktop screenshot.
- Visual verification reviews the implemented result; Product/Design owners still own intentional product/design changes.

## Quality gate
Visual verification is complete when the real current revision has been observed, the changed states have concrete capture evidence, material differences against the intended reference or system are resolved or explicitly accepted, and the sign-off states exactly which platforms/viewports/states were actually checked.