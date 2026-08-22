---
name: design-system-component
description: Define or evolve a design-system component by reusing existing primitives and tokens first, then specifying semantics, variants, states, accessibility, responsive behavior, and implementation guidance only where a recurring gap truly exists.
---
# Design-System Component

Use when a recurring interface pattern may belong in the shared design system.

## Procedure
1. Confirm the recurring user/interface need and inspect the current design-system documentation, neighboring product surfaces, coded primitives, helpers, and tokens before proposing anything new.
2. Determine whether an existing component, composition, or variant already solves the need. Prefer extending a coherent primitive over creating a parallel button, input, modal, formatter, palette, or UI kit.
3. Define semantic purpose before visual variants and separate reusable system behavior from one screen's local presentation.
4. Specify anatomy, variants, sizes, states, interaction, content rules, responsive behavior, and composition constraints only to the extent the recurring pattern requires them.
5. Map color, spacing, typography, radius, elevation, motion, and other visual decisions to existing tokens or established system rules. Introduce new tokens only when a genuine reusable semantic need is missing.
6. Define accessibility: native semantics where possible, names/roles, keyboard behavior, focus, disabled/loading/error states, contrast, motion, zoom/reflow, and assistive-technology expectations.
7. When working from an approved design/mock/reference, map the reference onto existing primitives first and document any intentional divergence instead of approximating or inventing decorative chrome that neither the design nor the product system uses.
8. Provide examples of correct use, misuse, composition limits, and migration from older/local patterns when relevant.
9. Collaborate with frontend implementation and validate the coded component in the actual rendered product, including important states and responsive behavior.

## Decision rules
- A recurring need does not automatically require a new component.
- Prefer a variant/composition of an established primitive when it preserves semantic clarity and consistency.
- One-off colors, borders, shadows, badges, or helpers should not quietly become a second design system.
- New tokens and primitives need reusable semantic justification, not one mockup's convenience.

## Quality gate
A component belongs in the system when existing primitives genuinely cannot express the recurring need cleanly, the new contract is semantically and visually consistent with the system, accessibility and responsive states are explicit, implementation uses shared tokens/primitives, and the rendered result has been verified rather than approved from specs alone.