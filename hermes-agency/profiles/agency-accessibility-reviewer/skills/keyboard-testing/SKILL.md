---
name: keyboard-testing
description: Validate a user flow with keyboard or equivalent non-pointer input by checking reachability, order, focus visibility, activation, escape, shortcuts, custom widgets, and recovery from dynamic UI changes.
---
# Keyboard Testing

Use when an interactive interface needs manual verification that pointer-free users can operate the critical flow.

## Procedure
1. Define the flow, target platform, supported input conventions, and starting state before testing. Include dialogs, menus, forms, tables, navigation, custom controls, and dynamic content implicated by the task.
2. Complete the flow without a mouse or touch input. Use the platform's normal keyboard navigation and activation keys rather than developer shortcuts that ordinary users do not know.
3. Verify every required interactive control is reachable in a logical order and that decorative/noninteractive elements do not create unnecessary stops.
4. Check that focus is visibly distinguishable in every state and is not hidden behind overlays, clipped containers, scrolling, or custom styling.
5. Verify activation and editing behavior matches the control semantics: buttons, links, form fields, selects, menus, tabs, grids, sliders, and custom widgets should use expected keys for the platform/pattern.
6. Test entry and exit from transient UI. Dialogs, popovers, menus, drawers, and modal flows should place focus intentionally, contain it only when appropriate, provide an escape/dismiss path, and restore focus meaningfully.
7. Trigger validation errors, async loading/results, route changes, disabled/enabled changes, inserted/removed controls, and repeated actions. Ensure focus is not lost, reset unexpectedly, or trapped on content that disappeared.
8. Check keyboard-only scrolling and viewport behavior, including zoom/reflow where relevant, so focused controls remain perceivable.
9. Record each barrier with exact steps, key sequence, starting focus, expected behavior, actual focus/result, browser/app/platform, and evidence.
10. Re-test corrected critical flows from a fresh starting state rather than checking only the repaired control in isolation.

## Decision rules
- Tab order should normally follow meaningful DOM/native order rather than positive tabindex or custom sequencing.
- A visible pointer hover state is not a keyboard focus state unless keyboard users can perceive it reliably.
- Custom keyboard behavior should follow the established widget/platform pattern rather than inventing novel shortcuts.
- Automated accessibility tools cannot prove keyboard flow or focus behavior.

## Quality gate
Keyboard testing is complete when the critical flow can be reached, operated, escaped, and recovered from using non-pointer input; focus order and visibility remain coherent through dynamic states; custom widgets behave predictably; and every confirmed barrier has reproducible evidence and a clear user consequence.