---
name: dependency-tracking
description: Track project dependencies as explicit predecessor outcomes, owners, needed-by dates, readiness evidence, and blocking consequences instead of vague links between tasks.
---
# Dependency Tracking

Use when delivery depends on outputs, approvals, decisions, vendors, environments, or other work completing in sequence.

## Procedure
1. Define each dependency as the concrete condition or artifact required, not merely the name of another task.
2. Record provider owner, consumer owner, needed-by date, current state, and evidence that marks the dependency satisfied.
3. Distinguish hard blockers from preferred sequencing and informational relationships.
4. Trace transitive dependencies enough to identify critical chains without turning the project map into noise.
5. Monitor changes to upstream scope or dates and recalculate affected downstream commitments.
6. Escalate dependencies whose owners, dates, or acceptance conditions are unresolved before they become silent blockers.
7. Where useful, split independent work to preserve parallelism rather than serializing everything behind one dependency.
8. Close a dependency only when the consuming owner has the required usable outcome, not when the provider reports activity complete.

## Decision rules
- A dependency is an outcome relationship, not a status label.
- Soft dependencies should not block work unnecessarily.
- Dynamic Fleet node placement is runtime orchestration state, not a project dependency unless a deliverable genuinely requires a specific environment capability.
- Keep dependency data current enough to drive scheduling decisions.

## Quality gate
Dependencies are healthy when blockers and sequencing are explicit, owners and acceptance evidence are known, downstream impact is visible when dates move, and teams can tell which work is truly blocked versus merely related.