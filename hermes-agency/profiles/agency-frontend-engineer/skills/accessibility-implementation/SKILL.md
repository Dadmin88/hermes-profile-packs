---
name: accessibility-implementation
description: Implement accessible frontend behavior using semantic structure, native controls, keyboard and focus management, clear names and errors, adaptable visuals, and assistive-technology-aware state changes.
---
# Accessibility Implementation

Use when building or changing interactive UI so accessibility is part of the implementation rather than a post-release patch.

## Procedure
1. Start from semantic structure. Use the correct document/app landmarks, headings, lists, form associations, links, buttons, tables, and native controls before adding ARIA.
2. Ensure every interactive control has a clear accessible name, purpose, state, and relationship to relevant instructions or errors. Visible labels should normally provide the accessible name.
3. Make the complete interaction operable from the keyboard or equivalent non-pointer input. Preserve logical tab order, visible focus, expected activation keys, and an escape path from transient UI.
4. Manage focus intentionally when context changes. Dialogs, menus, popovers, route changes, validation failures, inserted content, and removed controls should not strand or unexpectedly steal focus.
5. For custom widgets, implement the established interaction pattern completely, including roles, states/properties, keyboard behavior, focus movement, and dismissal. Prefer native elements when they already provide the required semantics and behavior.
6. Communicate dynamic status appropriately. Loading, saving, errors, success, counts, validation feedback, and asynchronously inserted results should be perceivable without forcing every update into a noisy live region.
7. Preserve usability under zoom, text enlargement, reflow, orientation changes, high contrast/forced colors where applicable, reduced motion preferences, and different viewport sizes. Do not encode meaning using color alone.
8. Give non-text content an appropriate equivalent or intentionally mark it decorative. Captions, transcripts, labels, descriptions, and control names should reflect the actual user task.
9. Test the critical flow with keyboard-only interaction. Inspect the accessibility tree or accessible names/states, run automated checks where available, and use representative assistive technology for complex or high-impact interactions when possible.
10. Hand off ambiguous interaction semantics or broad accessibility risk to `agency-accessibility-reviewer`; implementation remains responsible for fixing accepted findings.

## Decision rules
- Native semantics first; ARIA fills semantic gaps, it does not repair incorrect interaction design by itself.
- Do not remove focus outlines without providing an equally visible replacement.
- Do not create a custom control when a native element meets the behavior and styling requirements.
- Automated scanners are useful detectors, not proof that a flow is accessible.
- Accessibility behavior is part of the component contract and should be covered by regression tests where practical.

## Quality gate
The implementation is ready when the critical flow is semantically understandable, keyboard-operable, focus-safe, perceivable across relevant visual adaptations, exposes correct names/states to accessibility APIs, and any remaining accessibility uncertainty is explicitly handed to independent review.