---
name: contribution-governance
description: Govern additions and changes to a design system through evidence of recurring need, ownership, review, compatibility, documentation, release, adoption, and deprecation.
---
# Design System Contribution Governance

Use when teams propose new components, tokens, patterns, variants, or changes to the shared design system.

## Procedure
1. Require a clear consumer problem and evidence of repeated or strategically important need before centralizing a solution.
2. Check existing components or patterns for extension before creating a parallel primitive.
3. Define the proposed API or anatomy, states, accessibility, tokens, content, responsive behavior, and implementation ownership.
4. Review with relevant design, engineering, accessibility, and product stakeholders based on the affected contract.
5. Prototype the contribution in at least one real consumer context and check whether abstraction improves rather than complicates use.
6. Define documentation, examples, tests, versioning, release notes, and migration requirements before merging into the shared system.
7. Track adoption and support burden after release; a theoretically elegant component that nobody can use is not a successful contribution.
8. Deprecate and remove old patterns with an explicit migration path and enough compatibility time for real consumers.

## Decision rules
- Shared-system surface area has long-term cost; centralize only durable recurring needs.
- One product request is not automatically a system requirement.
- Compatibility and migration matter because design-system consumers update at different times.
- Governance should speed good contributions, not create ritual approval queues.

## Quality gate
A contribution is ready when the recurring need is demonstrated, the abstraction works in real contexts, accessibility and implementation contracts are complete, documentation, tests, and migration are included, ownership is explicit, and adoption can be measured after release.