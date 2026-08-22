---
name: technical-research
description: Research technical approaches from project documents of record through current primary sources and prior art, evaluate evidence and licenses, and convert findings into architecture or implementation implications without answering from memory.
---
# Technical Research

Use when an architecture or engineering decision depends on how a technology actually works, current vendor behavior, prior art, research literature, or existing implementations.

## Procedure
1. Define the decision, unknowns, constraints, required freshness, and what evidence would materially change the recommendation.
2. Read the project's documents of record first: requirements, ADRs, plans, issues, existing code, git history, vendored source, and established decisions relevant to the question.
3. Resolve contradictions inside project sources explicitly rather than silently choosing the most convenient interpretation.
4. Then inspect current primary external sources appropriate to the question: official documentation/changelogs, canonical source repositories, specifications, standards, papers, or maintainer statements.
5. Read implementation source when behavior, edge cases, or compatibility matter beyond high-level documentation.
6. For reusable third-party code, libraries, or agent skills, record canonical source, license, reviewed revision/version, maintenance state, assumptions, and what can actually be reused.
7. Compare multiple serious approaches on the constraints that matter: correctness, failure behavior, complexity, interoperability, security, portability, operations, migration, and maintenance.
8. Grade evidence strength and separate verified fact, source-supported inference, experiment result, estimate, and unresolved unknown.
9. Use parallel research/delegation for breadth when useful, but give each lane a bounded question and synthesize the results into one decision surface.
10. End with the recommended implication for the current architecture or implementation, alternatives worth preserving, and any experiment needed before commitment.

## Decision rules
- Do not call memory or a link list “research.”
- Current vendor/API/standard claims require current authoritative evidence when they can change.
- Popularity is not proof of technical fit.
- Research should reduce uncertainty for a decision, not become an unbounded survey.
- Agency research produces portable evidence and recommendations; Fleet decides where research profiles execute.

## Quality gate
The research is decision-ready when project truth has been reconciled, material external claims trace to current primary sources, reusable prior art has license/revision provenance, alternatives are compared against real constraints, fact and inference are separated, and the recommendation states what should change or be tested next.