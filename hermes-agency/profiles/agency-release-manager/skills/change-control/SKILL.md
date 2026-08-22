---
name: change-control
description: Control consequential release changes by making scope, revision, evidence, approvals, timing, exceptions, and post-approval drift explicit without turning every small change into bureaucracy.
---
# Change Control

Use when a release or operational change requires formal coordination, approval, freeze discipline, or auditable exception handling.

## Procedure
1. Define which changes require control based on risk, environment, customer impact, regulation, contract, or organizational policy.
2. Record the exact change scope, artifact/revision, affected systems, implementation window, owner, and supporting validation.
3. Identify required reviewers or approvers by the decision they own, not by a generic long distribution list.
4. Surface dependencies, migrations, maintenance windows, communications, rollback/recovery, and known residual risk before approval.
5. Establish the point at which approved scope is frozen and how material post-approval changes trigger re-review.
6. Handle emergency changes through an explicit accelerated path that still records authority, evidence, and follow-up.
7. Record approval, rejection, exception, or risk acceptance with timestamp and owner.
8. Reconcile the actually deployed change against the approved revision and document deviations.

## Decision rules
- Change control should scale with consequence.
- Approval of one revision does not automatically approve later drift.
- Emergency does not mean undocumented.
- Avoid rubber-stamp approvals that do not correspond to real decision rights.

## Quality gate
The controlled change is ready when scope and revision are exact, required evidence and owners are present, material risks and recovery are visible, approval applies to the actual release, and any exception or drift is explicitly recorded.