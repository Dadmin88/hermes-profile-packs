---
name: information-architecture
description: Organize product content and capabilities into understandable structures, labels, navigation, grouping, hierarchy, and findability based on user goals and mental models.
---
# Information Architecture

Use when a product or feature has confusing organization, navigation, terminology, or growing content complexity.

## Procedure
1. Identify primary audiences, tasks, content or capability inventory, constraints, and evidence about how users currently look for information.
2. Group items by user-recognizable concepts rather than internal team, database, or implementation structure.
3. Define hierarchy depth and breadth around frequency, importance, relationships, and progressive disclosure.
4. Create labels using user language that clearly distinguish sibling destinations or actions.
5. Design navigation, search, and filter relationships so users have more than one appropriate retrieval path where needed.
6. Test edge cases such as items belonging to multiple categories, empty sections, permissions, long labels, localization, and rapidly growing collections.
7. Validate the proposed structure with methods such as card sorting, tree testing, usability testing, analytics, or targeted stakeholder review depending on risk.
8. Document the structure, naming rationale, and unresolved taxonomy decisions so implementation does not silently reshape it.

## Decision rules
- Information architecture should mirror user concepts, not organizational charts.
- Deep hierarchy is not automatically bad if labels and paths match user mental models.
- Search does not compensate for incomprehensible navigation.
- Terminology is part of the information architecture contract.

## Quality gate
The architecture is ready when primary tasks have understandable paths, sibling categories and labels are distinguishable, edge and growth cases are handled, the structure has evidence beyond designer intuition, and implementation can reproduce it without inventing taxonomy.