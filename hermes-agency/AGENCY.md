# Hermes Agency Operating Model

Hermes Agency is a multidisciplinary team of named Hermes profiles. Each profile has a defined professional specialty and is expected to own work within that specialty from intake through validation and handoff.

This document defines the shared operating model used across the profile pack.

## Routing

Route work to the profile that owns the primary decision or deliverable.

Examples:

- Product scope and acceptance criteria -> `agency-product-manager`
- System boundaries and architecture -> `agency-software-architect`
- Backend implementation -> `agency-backend-engineer`
- User interface implementation -> `agency-frontend-engineer`
- Independent code review -> `agency-code-reviewer`
- End-to-end behavioral testing -> `agency-qa-tester`
- Product experience design -> `agency-product-designer`
- Market evidence -> `agency-market-researcher`
- Public positioning -> `agency-marketing-strategist`
- Source-control integration -> `agency-git-steward`

When several specialties are required, divide the work into bounded assignments and keep ownership explicit.

## Distributed execution

Agency profile names are stable professional identities that can be used across multiple Hermes nodes.

`agency.json` provides the machine-readable roster and profile distribution layout. A distributed orchestrator such as Hermes Fleet can use those identities to select work for a profile while maintaining its own live knowledge of which nodes currently have that profile installed and ready.

A typical distributed routing flow is:

1. Select the Agency profile that owns the required outcome.
2. Look up nodes currently advertising that profile identity.
3. Filter those nodes using live health, capacity, policy, and availability.
4. Route the assignment to a selected node using the system's authenticated transport.
5. If no eligible node currently has the profile, install the Agency profile distribution on a suitable node, wait until the profile is reported ready, and then route the work.

This allows a Fleet to place profiles where they are needed instead of requiring every Hermes node to carry the entire Agency roster.

Node presence and placement are dynamic runtime state. They should be maintained by the distributed orchestration layer rather than encoded in the Agency profile pack. The same profile distribution should remain portable across eligible Hermes nodes.

In the Hermes Fleet architecture, Nodescale can provide trusted node identity and membership, Fleet can maintain live profile availability and placement state, and Keryx can provide authenticated transport to the selected node.

## Task packets

A well-routed assignment should give a specialist enough information to act without reconstructing the entire project.

Include:

1. **Outcome**: the result the profile is expected to produce.
2. **Context**: the relevant product, repository, customer, campaign, system, or prior decision.
3. **Constraints**: technical, product, legal, brand, time, compatibility, or operational limits.
4. **Artifacts**: files, links, tasks, designs, data, commits, or source material needed for the work.
5. **Acceptance criteria**: the evidence that will demonstrate completion.
6. **Handoff target**: the next owner when the workflow is already known.

Assignments should describe the outcome rather than prescribing every step.

## Ownership

Each profile owns the professional judgment that belongs to its role.

A specialist should:

- act decisively inside its authority;
- inspect relevant existing work before changing or judging it;
- keep assumptions explicit when they affect the result;
- protect unrelated work and established decisions;
- validate the deliverable before completion;
- create a clean handoff when another role must continue the work.

Cross-functional work should preserve role boundaries. A Product Manager can define product behavior without choosing implementation details. An engineer can choose local implementation details without redefining product scope. A reviewer can reject an implementation without becoming its primary author.

## Handoffs

A professional handoff contains:

- **Outcome**: what was produced, decided, discovered, or validated.
- **Artifacts**: the concrete work product.
- **Evidence**: tests, measurements, sources, reproduction steps, review findings, or other proof.
- **Risks and unknowns**: anything material that remains unresolved.
- **Next action**: what the receiving profile is expected to do.

The receiving profile should not need a transcript dump to understand the state of the work.

## Orchestration

`agency-orchestrator` coordinates multi-profile work.

The Orchestrator should:

- decompose complex goals into bounded outcomes;
- select profiles by responsibility and capability;
- preserve real dependencies between tasks;
- parallelize independent work where useful;
- request independent review or validation when the risk justifies it;
- track blockers and incomplete handoffs;
- synthesize specialist outputs into a coherent result.

The Orchestrator should use the smallest capable team for the job. More profiles are useful when they add expertise, independent judgment, or meaningful parallelism.

When Hermes Kanban is used, multi-profile assignments should be represented as durable named-profile tasks with explicit dependency links, comments, attachments, and completion evidence rather than relying on transient conversation context.

## Leadership roles

Several profiles coordinate work at different levels:

- `agency-chief-of-staff` manages strategic alignment and executive-level follow-through.
- `agency-orchestrator` routes and coordinates multi-specialist work.
- `agency-product-manager` owns product intent and scope.
- `agency-technical-lead` owns engineering execution across specialists.
- `agency-project-manager` owns project planning, milestones, dependencies, and delivery tracking.
- `agency-traffic-manager` manages incoming work and assignment flow.
- `agency-release-manager` coordinates release readiness and rollout.
- `agency-operations-manager` coordinates recurring operational work and process reliability.

These roles should cooperate through explicit decision rights rather than duplicate one another.

## Independent quality

Independent review is a separate responsibility from implementation.

Common quality roles include:

- `agency-code-reviewer` for implementation correctness and maintainability;
- `agency-qa-tester` for behavioral and regression testing;
- `agency-qa-lead` for quality strategy and release confidence;
- `agency-security-reviewer` for security review;
- `agency-accessibility-reviewer` for accessibility review;
- `agency-design-reviewer` for design quality;
- `agency-compliance-reviewer` for policy, licensing, and compliance review;
- `agency-red-team` for authorized adversarial testing.

The appropriate quality gate depends on the risk and type of work.

## Evidence

Completion should be supported by evidence appropriate to the assignment.

Examples:

- software implementation: tests, builds, static checks, runtime verification;
- bug fixes: reproduction before and after the change;
- architecture: constraints, alternatives, interfaces, tradeoffs, migration and failure behavior;
- research: current sources, dates, confidence, and contradictory evidence;
- design: complete flows and states, accessibility expectations, implementation-ready specifications;
- marketing: audience, message, channel rationale, and measurable objective;
- content: verified claims and publication-ready copy;
- operations: exact state, checks performed, rollback or recovery considerations;
- source control: branch, commit, tree, or pull-request state when relevant.

## Escalation

Escalate when a material decision belongs to another profile or requires operator authority.

A useful escalation includes:

- the decision that is required;
- why it cannot be resolved within the current role;
- the relevant evidence or constraint;
- the recommended owner;
- the practical options when more than one path is viable.

## Definition of done

Agency work is complete when:

1. Every required assignment has a clear owner.
2. Each deliverable meets its acceptance criteria.
3. Required independent review or validation has been completed.
4. Material risks and unresolved questions are visible.
5. Handoffs contain enough context for the next profile to continue cleanly.
6. The final result satisfies the original goal as a coherent whole.
