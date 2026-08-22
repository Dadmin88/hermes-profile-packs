---
name: accessibility-design-check
description: Check design artifacts for accessibility requirements and implementation-ready semantics across hierarchy, controls, focus, keyboard, errors, contrast, motion, responsive adaptation, and non-text content.
---
# Accessibility Design Check

Use as an independent design-review pass when accessibility is one quality dimension among broader product/design concerns.

## Procedure
1. Confirm the critical flows, target platforms, known accessibility target, and whether a dedicated Accessibility Reviewer has already provided requirements or findings.
2. Check information hierarchy, reading order, headings/groups, labels, instructions, and relationships for meaning that does not depend solely on layout, color, or proximity.
3. Check every interactive design for an identifiable control pattern, visible label/name, state, disabled/selected/current behavior, and a plausible keyboard/focus model.
4. Review dialogs, menus, drawers, route/view changes, validation, async results, and removed/inserted content for specified focus and status-feedback expectations.
5. Check visual states for sufficient distinguishability, visible focus treatment, color-independent meaning, zoom/reflow/text enlargement, responsive adaptation, and high-contrast/forced-color considerations where relevant.
6. Review motion, autoplay, gestures/dragging, timing, and target sizing for alternatives or user controls needed by the intended interaction.
7. Review image/icon/chart/media use for the intended alternative/equivalent information or decorative treatment.
8. Flag custom widgets or unusual interactions that need a known accessibility interaction pattern before engineering begins.
9. Verify design annotations/handoff include accessibility behavior that cannot be inferred from a static mockup.
10. Route standards-specific uncertainty or complex assistive-technology questions to `agency-accessibility-reviewer` rather than claiming formal conformance from design review alone.

## Decision rules
- This check is an independent design-quality gate, not a replacement for a dedicated accessibility audit or WCAG review.
- Static designs can reveal missing requirements but cannot prove implemented semantics or assistive-technology behavior.
- Accessibility requirements should travel in the handoff rather than rely on the engineer to remember unwritten expectations.
- Native/platform-standard interactions should be preferred when they meet the product need and reduce custom accessibility risk.

## Quality gate
The design passes this check when accessibility-critical interaction, hierarchy, focus, feedback, visual adaptation, and content-equivalent expectations are specified well enough to implement; likely barriers are identified before build; and any formal or complex accessibility question is explicitly handed to the specialist who owns it.