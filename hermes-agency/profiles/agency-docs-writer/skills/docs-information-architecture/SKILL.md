---
name: docs-information-architecture
description: Organize documentation by user audience, task, learning stage, concept, reference surface, and maintenance ownership so readers can find the right kind of answer without knowing repository structure.
---
# Documentation Information Architecture

Use when a documentation set is growing, hard to navigate, duplicative, or organized around internal components instead of user needs.

## Procedure
1. Identify documentation audiences, recurring tasks, learning journeys, product areas, and the questions readers arrive with.
2. Inventory existing pages and classify them by purpose such as tutorial, how-to, concept or explanation, reference, troubleshooting, release or migration, and policy.
3. Group pages around user-recognizable product concepts and workflows rather than team ownership or source-code directories unless the docs are explicitly developer-internal.
4. Define navigation hierarchy, labels, landing pages, cross-links, search terms, and breadcrumbs according to how users move between related questions.
5. Identify duplicate, conflicting, orphaned, overly broad, and missing documentation and assign consolidation or creation work.
6. Separate stable conceptual material from fast-changing version or release detail where that improves maintenance.
7. Define page ownership and review signals for areas whose accuracy decays quickly.
8. Test findability with realistic user questions and revise taxonomy that requires insider terminology.

## Decision rules
- Documentation architecture should mirror user questions, not repository history.
- Different page types solve different information needs and should not be merged solely to reduce file count.
- Internal terminology should not be required to find beginner documentation.
- Navigation and search complement each other.

## Quality gate
The architecture is ready when major audience questions map to obvious destinations, page purpose and hierarchy are understandable, duplication and ownership are addressed, fast-changing material is maintainable, and a new user can locate answers without knowing the codebase or organization chart.