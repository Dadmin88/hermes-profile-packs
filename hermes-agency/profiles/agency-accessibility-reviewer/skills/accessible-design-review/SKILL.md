---
name: accessible-design-review
description: Review product design artifacts before implementation for accessibility of information, interaction, focus, input, error recovery, responsive/reflow behavior, motion, contrast, content alternatives, and assistive-technology semantics.
---
# Accessible Design Review

Use when flows, wireframes, mockups, prototypes, or design-system proposals need accessibility review before engineering decisions harden.

## Procedure
1. Define the user goals, supported platforms, input methods, content types, and accessibility target/known user needs for the design.
2. Walk every important state and transition, including loading, empty, errors, success, disabled/permission, modal/transient UI, destructive actions, and interruption/recovery.
3. Review information hierarchy and reading order so headings, labels, groups, instructions, and relationships make sense without relying on visual position alone.
4. Review control semantics and interaction pattern. Identify where native controls can express the intended behavior and where a custom widget will need explicit role/state/keyboard/focus behavior.
5. Specify focus expectations for entry, validation failure, dialogs/menus, route/view changes, inserted or removed content, and completion so implementation does not invent focus behavior late.
6. Check visual design for text/background and non-text contrast requirements relevant to the target, visible focus, color-independent meaning, zoom/reflow, text enlargement, orientation/responsiveness, and forced/high-contrast considerations where applicable.
7. Review animation, autoplay, time limits, dragging/complex gestures, target sizing, and alternative input paths so interaction is not dependent on one motor/sensory capability.
8. Review images, icons, charts, media, and other non-text content for the intended alternative/equivalent information or decorative treatment.
9. Annotate implementation-critical accessibility behavior directly in the design handoff: accessible names, labels/descriptions, status announcements, semantic grouping, keyboard/focus model, and responsive transformations where needed.
10. Separate confirmed design barriers from implementation questions and hand ambiguous standards interpretation to a formal WCAG/accessibility requirement review when necessary.

## Decision rules
- Accessibility decisions made in design are cheaper and more coherent than retrofitting semantics onto an inaccessible interaction later.
- Visual similarity does not imply semantic equivalence across native and custom controls.
- Do not prescribe ARIA attributes from static mockups when the correct native/implementation pattern has not yet been chosen.
- The designer owns the solution; the reviewer owns identifying barriers, missing states, and accessibility requirements.

## Quality gate
The design is accessibility-ready when critical flows have complete non-pointer and assistive-technology expectations, hierarchy and control meaning do not depend on visual presentation alone, error/focus/dynamic states are specified, visual adaptation/motion/non-text content are addressed, and engineering can implement without inventing fundamental accessibility behavior.