---
name: design-handoff-review
description: Review a design handoff for implementation readiness by checking source artifacts, flows, states, responsive behavior, components, tokens, content, accessibility, assets, interaction details, and unresolved decisions.
---
# Design Handoff Review

Use immediately before or during engineering handoff when the design must contain enough detail to implement without reconstructing intent from scattered artifacts.

## Procedure
1. Confirm the authoritative design/spec source, product requirements, target platforms, current design-system version, and the exact scope being handed off.
2. Walk the complete primary and alternate flows and verify each screen/view/component is connected to an explicit state and user action rather than a gallery of disconnected mockups.
3. Check responsive/adaptive behavior: breakpoints or layout rules, content priority, overflow, resizing, orientation, density, long/short content, and component rearrangement where relevant.
4. Verify component and token use: canonical components/variants, typography, spacing, color, iconography, motion, and documented exceptions that require new design-system work.
5. Check interaction details that static images cannot communicate: hover/focus/pressed/disabled/selected states, keyboard behavior, transitions, drag/gesture rules, loading/progress, confirmation, undo, and error recovery.
6. Check content and data assumptions: realistic strings/data ranges, truncation/wrapping, empty/large lists, dates/numbers/localization, optional fields, and placeholders that should not reach production.
7. Check accessibility annotations or requirements for semantics, accessible names, focus, announcements, contrast/adaptation, alternatives, and custom widget behavior.
8. Verify required assets and specifications are available in implementable formats with naming/export guidance where design owns them.
9. List unresolved decisions, their owner, and whether they block implementation. Separate product/design decisions from engineering implementation choices.
10. Produce a concise handoff-readiness result with blocking gaps, non-blocking clarifications, source links/artifacts, and what engineering can safely decide independently.

## Decision rules
- A handoff is a behavior contract, not merely a set of polished screens.
- Avoid specifying implementation details owned by engineering unless they are necessary to preserve the intended user behavior.
- Missing product behavior should return to Product/Design rather than become an engineer's accidental decision.
- Design Reviewer identifies readiness gaps; Product Designer remains owner of design corrections.

## Quality gate
The handoff is ready when authoritative artifacts and scope are clear, flows and states are complete, responsive/component/content/accessibility details are implementable, blocking decisions have owners, and engineers can make local technical choices without guessing user-visible product behavior.