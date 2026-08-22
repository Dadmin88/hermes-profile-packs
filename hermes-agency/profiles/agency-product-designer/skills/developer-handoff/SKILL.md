---
name: developer-handoff
description: Hand product design to engineering with complete flows, states, responsive and accessibility behavior, component intent, assets, content, constraints, and explicit open decisions while preserving implementation ownership.
---
# Developer Handoff

Use when approved product design is ready to be implemented by frontend or other engineering specialists.

## Procedure
1. Start from the accepted product outcome and requirements so the handoff distinguishes mandatory product behavior from visual/design preference and exploratory concepts.
2. Provide the complete flow, not isolated polished screens. Include entry points, success, empty, loading, validation, permission, failure, interruption, recovery, and relevant destructive/confirmation behavior.
3. Specify interaction behavior: control intent, navigation, transitions, selection/editing rules, keyboard/focus expectations, input methods, cancellation, persistence, and other user-observable details that engineering should not invent.
4. Specify responsive/adaptive behavior by principles and critical breakpoints/states where layout meaning changes. Avoid demanding pixel-perfect screenshots that do not explain what should happen between sizes.
5. Identify design-system components/tokens/patterns that should be used when semantically appropriate. Flag new component behavior separately so Design Systems or engineering can decide the reusable implementation boundary.
6. Provide accessibility behavior including semantics, accessible names/content intent, focus order/management, keyboard alternatives, announcements/status behavior, reduced motion, contrast/adaptation expectations, and known review risks.
7. Provide production-ready assets or exact source/export requirements with naming, dimensions/ratios, formats, states, and licensing/attribution constraints where relevant.
8. Provide final or clearly marked placeholder content. Route unresolved product copy to the appropriate content/copy specialist instead of letting engineering invent customer-facing language by accident.
9. Call out data/API assumptions that affect the experience, such as pagination, permissions, latency, optimistic behavior, upload limits, or unavailable fields, but do not prescribe backend/frontend architecture beyond the accepted contract.
10. List open questions and decision owners. Anything that can materially change product behavior should be resolved or explicitly owned before implementation proceeds too far.
11. During implementation, answer genuine design ambiguities and review the built flow against intended behavior without taking over code-level implementation decisions.

## Decision rules
- Handoff should specify observable behavior and design intent, not framework/component code unless the design system itself defines that contract.
- A Figma link or image alone is not a complete handoff.
- Do not freeze implementation around arbitrary pixel values when responsive rules or semantic intent communicate the design better.
- Engineering may identify technical constraints; route resulting product/design tradeoffs back to their owning roles rather than silently degrading the experience.

## Quality gate
The handoff is ready when engineering has complete states and interaction rules, responsive/accessibility expectations, usable assets/content, known system assumptions, and explicit open decisions; implementation freedom is preserved where it belongs; and the built product can later be reviewed against a clear design contract.