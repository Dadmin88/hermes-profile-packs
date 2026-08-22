---
name: design-tokens
description: Design and govern semantic design tokens for color, typography, spacing, size, motion, elevation, and other reusable decisions with clear naming, themes, aliases, and implementation contracts.
---
# Design Tokens

Use when a design system needs reusable decisions that can flow reliably from design to code and across themes or platforms.

## Procedure
1. Inventory repeated design decisions and identify which deserve tokenization because they express a reusable semantic role.
2. Separate primitive or reference values from semantic tokens and component-specific tokens so meaning is not tied directly to raw values.
3. Name tokens by purpose and state rather than one visual value that may change across themes.
4. Define token types, units, scales, aliases, themes or modes, and fallback behavior required by target platforms.
5. Map accessibility-sensitive relationships such as foreground and background pairs, focus states, or motion preferences rather than tokenizing colors independently.
6. Define source-of-truth and transformation or export behavior so design and implementation do not silently fork.
7. Test token changes against representative components and themes for unintended cascade or contrast and layout regressions.
8. Document deprecation and migration rules for renamed or removed tokens.

## Decision rules
- Tokenize decisions that need coordinated reuse, not every numeric value.
- Semantic names survive redesign better than value-based names.
- Design tokens are an interface and should have compatibility discipline.
- Accessibility relationships may need validation beyond individual token values.

## Quality gate
The token system is ready when repeated decisions map to clear semantic roles, themes and platform transforms are predictable, design and code share one governed source, changes can be migrated safely, and representative components validate that the abstraction improves consistency rather than adding indirection.