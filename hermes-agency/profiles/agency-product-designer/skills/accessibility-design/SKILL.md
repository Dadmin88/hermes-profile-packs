---
name: accessibility-design
description: Design product experiences with accessible information hierarchy, semantics, input methods, focus behavior, visual adaptations, content alternatives, and recovery patterns before implementation.
---
# Accessibility Design

Use when designing a new or changed product flow so accessibility constraints and opportunities shape the interaction rather than arrive as implementation-only fixes.

## Procedure
1. Identify the core user goals and interaction tasks independent of a single input or sensory mode. Ensure the design does not require vision, color perception, precise pointing, hearing, or time-sensitive action unless the product genuinely cannot avoid it.
2. Define semantic information hierarchy: landmarks/regions, headings, grouping, labels, relationships, reading order, and the meaning of controls or status changes. Visual composition should reinforce rather than contradict this structure.
3. Prefer interaction patterns with established accessible semantics and keyboard behavior. When a custom pattern is necessary, document the intended roles, states, focus model, keyboard/touch behavior, and escape/recovery behavior for implementation.
4. Design visible focus and a logical navigation order. Modal/transient surfaces, menus, drawers, inserted content, route changes, and validation errors should have an intentional focus destination and return path.
5. Define visual behavior across text enlargement, zoom/reflow, responsive widths, high contrast/forced-colors where relevant, reduced motion, and color-vision differences. Never make color, animation, position, or shape the sole carrier of essential meaning.
6. Define names, instructions, errors, status messages, and non-text alternatives in coordination with content/copy roles where needed. Error recovery should identify the problem and next action without relying only on visual placement.
7. Design media alternatives as appropriate: captions, transcripts, audio descriptions, text alternatives, controls for autoplay/motion, or other equivalents driven by the actual content.
8. Include accessibility-specific states in prototypes and handoff: keyboard focus, disabled/read-only distinctions, errors, loading/progress, expanded/collapsed state, selection, drag alternatives, and any live updates that need announcement.
9. Validate high-risk custom interactions with accessibility review and representative assistive technology/user research when the consequence or novelty warrants it.
10. Hand off the behavior precisely enough for Frontend Engineer to implement while retaining `agency-accessibility-reviewer` as the independent review role.

## Decision rules
- Accessibility is product behavior, not a checklist applied after visual design.
- Native/common patterns reduce risk but still need correct labels, states, focus, and content.
- Do not use disabled styling where an explanation/action is needed but the control becomes unreachable to some users.
- Automated tooling cannot validate the design's complete interaction model.
- Design should provide equivalent outcomes, not necessarily identical interaction for every user.

## Quality gate
Accessibility design is ready when the primary outcome can be understood and operated through relevant alternative input/sensory modes, semantic and focus behavior are specified, visual adaptations preserve meaning and usability, custom high-risk patterns have a validation plan, and implementation can proceed without inventing accessibility behavior.