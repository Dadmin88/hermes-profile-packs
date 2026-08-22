---
name: screen-reader-review
description: Review a critical interface flow with representative screen-reader and accessibility-tree evidence, checking names, roles, states, structure, navigation, announcements, reading order, and task completion.
---
# Screen Reader Review

Use when an interface needs manual validation of the experience exposed through platform accessibility APIs.

## Procedure
1. Define the target platform/browser/app combination, critical task, and representative screen reader or accessibility inspector available for that environment. Record versions when they materially affect behavior.
2. Start from a fresh state and navigate using the assistive technology's normal reading and structural navigation, not only keyboard tab stops.
3. Verify page/app structure conveys meaningful landmarks, headings, lists, tables, forms, regions, and relationships in an order that matches the intended experience.
4. Inspect each control's accessible name, role, value/state, description, and relationships. Visible text and the announced name should not contradict one another.
5. Test forms and validation: labels, required state, instructions, errors, error association, focus movement, and whether users can locate and correct invalid fields without visual inference.
6. Exercise custom widgets and transient UI. Confirm expected role/state changes, current selection/expanded state, menu/dialog context, focus behavior, and discoverable interaction instructions where needed.
7. Trigger loading, results, save status, errors, notifications, count changes, and asynchronously inserted/removed content. Verify important changes are announced without flooding the user with low-value live updates.
8. Check non-text content, images/icons, charts, and decorative elements for an appropriate text alternative, equivalent information, or intentional exclusion from the accessibility tree.
9. Complete the critical user goal and note barriers, confusing verbosity, missing context, duplicate announcements, inaccessible state, or reliance on visual position/color.
10. Record findings with exact screen-reader/platform context, navigation steps, announced output or accessibility-tree evidence, user consequence, expected behavior, and remediation direction.

## Decision rules
- One screen reader/browser combination provides evidence, not universal proof across all assistive technology.
- Accessible names and roles should describe the user's task, not implementation details.
- ARIA that produces an announcement is not automatically correct if the interaction model remains confusing or unusable.
- Use current platform/WAI-ARIA guidance for concrete widget expectations when a finding depends on a specific pattern/version.

## Quality gate
The review is complete when a representative assistive-technology user can understand structure, discover controls, perceive state and important dynamic changes, recover from errors, and complete the critical task; confirmed barriers have reproducible assistive-technology evidence and are separated from unverified cross-platform assumptions.