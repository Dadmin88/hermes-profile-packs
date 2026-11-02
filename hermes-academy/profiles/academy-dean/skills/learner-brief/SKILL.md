---
name: learner-brief
description: Create a compact teaching brief with learning goal, approximate level, relevant prior knowledge, constraints, and preferred depth or mode.
---
# Learner Brief

Capture only what affects instruction: what the learner wants to be able to understand or do, their approximate starting point, relevant prior knowledge, time or tool constraints, and whether they want explanation, practice, review, or direct help.

Do not demand information that can be inferred safely from the conversation.

## Profile Learner Context Minimization

When the learner is a Hermes profile (e.g. `agency-backend-engineer`), the brief must contain only what the receiving faculty member needs:

**Include:**
- Learner profile name (identity)
- Learner role (one-line description of what the profile does)
- Requested objective (one clear learning goal)
- Relevant skill names or descriptions when they directly affect instruction

**Never include:**
- Full profile state or configuration
- Memory contents or conversation history
- Secrets, credentials, or API keys
- Internal tool schemas or implementation details
- Unrelated skills or capabilities

Build this minimized brief directly from the allowed fields above. The repository reference helper `minimize_learner_context()` in `routing.py` is for maintainer tests only; it is not an installed-profile dependency.

## Human brief and optional continuity

For a human, use a compact brief: objective, evidence of understanding, specific remaining misconception, relevant constraints, and next useful task. Infer fields already supplied; omit unknown or unnecessary fields instead of asking a questionnaire. Example: "Goal: distinguish evidence from claim. Demonstrated: identifies survey respondents. Gap: generalizes to all residents. Constraint: ten minutes. Next: revise one warranted claim."

Offer this summary when the learner wants to resume later. In the current conversation, reuse only relevant context. A user may copy or review a summary without any persistence. For an explicit save request, use only an existing Hermes memory or file capability actually exposed in this session, with its supported scope and successful result. If none is available, provide a copyable note and state that it has not been saved. Do not create a separate learning database, store raw personal histories, or promise later retrieval or deletion without tool evidence. Before sending to another faculty member, share only the teaching fields they need; saving is not permission to distribute. Profile learner briefs remain subject to the stricter four-field contract above.

For installed-faculty routing examples, read `routing-examples.md` in this skill directory. Examples are illustrative and never evidence that any faculty is installed.
