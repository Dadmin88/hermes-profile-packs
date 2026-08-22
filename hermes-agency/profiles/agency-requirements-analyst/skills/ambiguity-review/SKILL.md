---
name: ambiguity-review
description: Review requirements for undefined actors, terms, states, timing, ownership, limits, conflicts, assumptions, and hidden implementation choices before ambiguity turns into divergent work.
---
# Ambiguity Review

Use when a specification appears complete but different specialists could reasonably interpret it in incompatible ways.

## Procedure
1. Read the requirement as an implementer, designer, tester, operator, and user would and note every place an outcome depends on unstated interpretation.
2. Identify undefined actors, resources, terminology, states, defaults, limits, units, timing, ordering, permissions, and success or failure semantics.
3. Find words that hide judgment such as appropriate, recent, quick, support, valid, normal, automatic, or secure and ask what observable behavior they imply.
4. Check pronouns, scope, optionality, precedence, and exception handling for multiple plausible readings.
5. Compare related requirements for contradictions, duplicate concepts with different names, or assumptions that one document does not actually guarantee.
6. Separate product ambiguity from implementation freedom; do not demand answers to technical details the requirement intentionally leaves open.
7. Route each unresolved question to the role with decision authority and record the accepted clarification in the source artifact.
8. Re-read the revised requirement without relying on the discussion that produced it.

## Decision rules
- If the document only makes sense with remembered conversation context, it is still ambiguous.
- Ambiguity is material when plausible interpretations produce meaningfully different outcomes.
- Preserve implementation freedom that does not change accepted behavior.
- Clarifications belong in durable source artifacts, not only chat threads.

## Quality gate
The review is complete when material terms and outcomes have one durable interpretation, conflicting requirements are resolved or explicitly owned, technical freedom is not mistaken for missing product definition, and a new specialist can read the artifact without needing the original conversation.