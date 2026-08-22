---
name: accessibility-patterns
description: Codify reusable accessible interaction patterns with semantic intent, keyboard and focus behavior, state communication, content guidance, and implementation notes for recurring UI needs.
---
# Accessibility Patterns

Use when a design system must prevent teams from reinventing accessibility behavior for common interactions.

## Procedure
1. Identify recurring interactive patterns whose accessibility behavior is frequently inconsistent or error-prone.
2. Start from native platform semantics and established accessible interaction patterns before inventing custom widgets.
3. Define roles or semantic structure, names and descriptions, state or properties, keyboard interaction, focus movement, dismissal, and dynamic announcements needed for the pattern.
4. Specify visual requirements such as focus visibility, contrast, target size, reflow, reduced motion, and non-color state communication where relevant.
5. Provide content guidance for labels, instructions, validation, errors, and status text that materially affects accessibility.
6. Map responsibilities between design and engineering so static specs do not falsely imply they alone guarantee accessibility.
7. Provide tested examples and known limitations across target platforms or assistive technology where evidence exists.
8. Route formal standards interpretation to Accessibility Reviewer and revise the system when real audits expose pattern defects.

## Decision rules
- Use native controls when they meet the interaction need.
- ARIA is not a substitute for correct behavior.
- Accessibility belongs in reusable patterns so product teams do not repeatedly relearn the same failures.
- Document evidence and platform limitations instead of claiming universal assistive-technology behavior.

## Quality gate
The pattern is ready when semantics, keyboard and focus, visual adaptation, state communication, and content expectations are explicit, implementation responsibilities are clear, representative examples have been validated, and teams can reuse the pattern without inventing fundamental accessibility behavior.