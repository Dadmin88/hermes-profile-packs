---
name: interaction-consistency
description: Review interaction patterns across a product for consistent control behavior, navigation, input, feedback, terminology, selection, destructive actions, loading, and recovery without forcing visual sameness where context differs.
---
# Interaction Consistency

Use when a design or implemented product contains repeated interaction patterns that may behave differently across screens, flows, platforms, or components.

## Procedure
1. Identify the repeated user tasks and comparable patterns in scope: navigation, forms, selection, menus, tables/lists, search/filter, create/edit/delete, save/cancel, drag/drop, pagination, dialogs, notifications, and other recurring interactions.
2. Compare behavior rather than screenshots alone: trigger, control type, label/terminology, focus/keyboard behavior, selected/current state, validation timing, confirmation, loading, success, error, and recovery.
3. Check whether different behavior reflects a genuine context/platform requirement or accidental divergence. Record the underlying user expectation that should remain stable.
4. Review terminology and action placement for semantic consistency. The same concept should not acquire different names or consequences without a reason users can understand.
5. Review destructive and irreversible actions for consistent intent, confirmation/undo/recovery, and feedback proportional to consequence.
6. Review state persistence across navigation/refresh/back behavior where users reasonably expect filters, selections, form drafts, or progress to remain or reset consistently.
7. Compare desktop/mobile/responsive adaptations by task outcome, not literal layout. Different presentation may be correct if the interaction contract remains clear.
8. Check alignment with the product's existing design-system patterns and platform conventions, but flag cases where forced reuse makes the interaction semantically wrong.
9. Rank inconsistencies by user confusion, error risk, learnability cost, and implementation fragmentation rather than cosmetic difference alone.
10. Recommend a canonical behavior or explicit exception and identify the owning designer/system pattern that should be updated.

## Decision rules
- Consistency means predictable semantics, not identical visuals everywhere.
- Platform-native differences can improve consistency with user expectations even when the cross-platform UI differs.
- Do not standardize an inferior pattern merely because it appears most often.
- Component reuse is evidence of consistency only when the underlying task semantics match.

## Quality gate
The review is complete when repeated interactions have clear canonical behavior or justified exceptions, terminology and feedback are predictable, high-impact divergence is prioritized, responsive/platform adaptations preserve task semantics, and recommendations identify where the product/design system should converge without erasing legitimate context.