---
name: validation-planning
description: Design proportionate, independent validation for multi-role work by mapping important claims and risks to the specialist, evidence, environment, and gate capable of proving them.
---
# Validation Planning

Use when a multi-specialist goal needs a clear answer to what must be proven before integration, release, publication, or completion.

## Procedure
1. List the claims the final outcome will depend on: functional behavior, compatibility, security, accessibility, performance, data correctness, design fidelity, source accuracy, release readiness, or other domain-specific properties.
2. Rank the claims by consequence and uncertainty. Spend independent validation effort where a mistaken claim would be costly, hard to reverse, externally visible, or difficult for the implementer to self-detect.
3. Assign each validation claim to the specialty that can judge it independently. Code Reviewer evaluates implementation risk, QA validates behavior, Security roles assess abuse/trust boundaries, design reviewers judge experience/design, and other specialists validate their own professional domains.
4. Define the evidence required before creating the validation task: changed artifacts, acceptance criteria, build or environment, reproduction path, test results, source material, measurements, or other inputs the reviewer needs.
5. Choose the validation method that can actually prove the claim. Inspection, unit/integration/E2E tests, manual interaction, benchmark, security testing, primary-source verification, comparison, or another method should follow the risk rather than a universal checklist.
6. Keep implementer validation and independent validation distinct. An owner should test its own work, but self-checking does not replace an independent gate where independence is part of the confidence model.
7. Place validation in the dependency graph at the point where the artifact is stable enough to review but early enough that findings can be fixed without expensive downstream rework.
8. Define what constitutes a blocker, what is advisory, how fixes are re-reviewed, and what residual risk can be accepted only by the role or user with authority to accept it.
9. For Hermes Kanban, create or link validation tasks to the artifact-producing tasks and preserve findings, evidence, comments, and completion state on the board so the final synthesis does not rely on memory.

## Decision rules
- Validation depth should be proportional to risk, not equal across every task.
- Independent review is a confidence mechanism, not an opportunity to duplicate the implementer's work.
- A passing automated suite does not prove properties it does not test.
- Do not create review gates whose owner, evidence, and pass condition are undefined.

## Quality gate
The validation plan is ready when consequential claims have named independent owners where appropriate, each gate has evidence and a meaningful pass condition, validation is sequenced into the dependency graph, and residual risk cannot disappear merely because every implementation task says done.