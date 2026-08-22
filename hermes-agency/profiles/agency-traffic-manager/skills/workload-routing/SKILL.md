---
name: workload-routing
description: Route incoming work to the correct Agency owner from decision responsibility, capability, urgency, dependencies, and current organizational load while leaving machine placement to Fleet.
---
# Workload Routing

Use when incoming requests need to be assigned to the right professional profile, team, or queue before execution begins.

## Procedure
1. Normalize the request into the outcome, deliverable, decision owner, urgency, dependencies, and acceptance evidence.
2. Route by professional responsibility and capability rather than keyword matching or whoever is currently visible.
3. Compare adjacent roles when ownership overlaps and choose the profile that owns the primary decision or deliverable.
4. Consider organizational workload, deadlines, blocked work, and specialist scarcity when sequencing assignments.
5. Split multi-specialty requests into bounded work packets only where distinct ownership or useful parallelism exists.
6. Preserve dependencies and required review/handoff roles in the durable work system.
7. If the required profile is unavailable in the current distributed runtime, request Fleet placement/discovery rather than substituting an inappropriate profession.
8. Re-route only when scope, ownership, capability, or availability materially changes, and preserve the prior handoff context.

## Decision rules
- Traffic Manager routes professional work; Fleet selects the node that will execute the chosen profile.
- Do not route based on machine hostname, node ID, or local installation assumptions.
- The smallest capable specialist set is usually best.
- Temporary capacity pressure should not permanently blur role boundaries.

## Quality gate
Routing is correct when every assignment has the professional owner best matched to the outcome, dependencies and review needs are explicit, load considerations are visible, and distributed node selection remains delegated to Fleet rather than encoded in Agency work routing.