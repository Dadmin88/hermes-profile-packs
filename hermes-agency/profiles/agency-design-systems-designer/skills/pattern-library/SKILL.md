---
name: pattern-library
description: Define reusable interaction and composition patterns with anatomy, behavior, states, accessibility, variants, content guidance, and selection criteria beyond individual components.
---
# Pattern Library

Use when teams repeatedly solve the same multi-component interaction or layout problem.

## Procedure
1. Identify repeated user problems such as forms, search or filter, tables, navigation, empty states, onboarding, confirmation, or other recurring compositions.
2. Document the problem and when the pattern should or should not be used before showing its visual form.
3. Define anatomy and component relationships, including optional and required regions and content responsibilities.
4. Specify interaction behavior, keyboard and focus expectations, responsive changes, loading, error, empty, and success states, and accessibility considerations.
5. Define variants only for recurring legitimate differences rather than every one-off customization request.
6. Provide realistic examples with content and edge cases that reveal how the pattern behaves under stress.
7. Map the pattern to implementation components and tokens and identify extension points or escape hatches.
8. Validate adoption through real product use and revise patterns that teams routinely bypass for good reasons.

## Decision rules
- A pattern library solves recurring user and design problems, not merely catalogs screenshots.
- Patterns need selection criteria and anti-pattern guidance.
- Realistic content and edge states are part of the pattern.
- Repeated escape hatches may indicate the pattern is too rigid or scoped incorrectly.

## Quality gate
The pattern is ready when teams know when to use it, anatomy and behavior are complete across important states, accessibility and responsive behavior are specified, implementation mapping is clear, and real product use demonstrates that it reduces reinvention without suppressing legitimate variation.