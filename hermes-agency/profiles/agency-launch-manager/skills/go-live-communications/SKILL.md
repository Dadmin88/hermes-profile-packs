---
name: go-live-communications
description: Coordinate launch-window communications so internal teams, users, customers, partners, support, and operators receive the right message, timing, action, and source of truth for their role.
---
# Go-Live Communications

Use when launch success depends on several audiences knowing what is changing, when, why, and what they should do.

## Procedure
1. Identify communication audiences and their distinct needs: users, customers, internal operators, support, sales, partners, leadership, or public channels as applicable.
2. Define the message for each audience around impact, benefit, timing, required action, limitations, migration, support path, and where current status lives.
3. Establish one source of truth for launch timing and status so scheduled messages do not diverge from the actual rollout decision.
4. Sequence internal enablement before external announcements when teams must support or sell the change.
5. Coordinate product copy, docs, release notes, email, social, PR, partner, and status-page communications with the specialists who own those artifacts.
6. Prepare contingency messages for delay, rollback, partial availability, known limitation, or incident where the risk warrants it.
7. Verify links, dates, time zones, audience segmentation, localization, support contact, and any claims that depend on final released behavior.
8. After go-live, update or retire temporary messaging and communicate material changes from the original launch state.

## Decision rules
- Launch communication is coordinated truth, not one universal announcement copied everywhere.
- Do not publish before the actual go-live authority confirms the state the message claims.
- Internal support readiness should precede external demand creation when support is required.
- Product claims must match the shipped behavior and availability.

## Quality gate
Communications are ready when each audience has an owned message and timing, all claims match the actual launch state, internal enablement and contingency messages exist where needed, links and dates are verified, and one authoritative status source prevents contradictory updates.