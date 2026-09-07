---
name: profile-selection-and-change-plan
description: Resolve profile criteria and requested Hermes settings into an exact, user-approved dry-run matrix with exceptions, risks, and rollback values.
---
# Profile Selection and Change Plan

Use when a user asks to change one profile or a group selected by category, role, namespace, current setting, inclusion list, exclusion list, or combined criteria.

## Procedure

1. Normalize the request into: intended outcome, configuration key or supported workflow, proposed value, selector, exclusions, desired scope, timing, and success evidence.
2. Ask focused questions only for decisions that materially alter the operation. Typical ambiguities include global default versus profile override, provider versus model, exact category source, whether current-value filters are before or after inheritance, exception precedence, and whether active profiles may be included.
3. Resolve selectors against the current inventory using exact semantics:
   - explicit names match stable profile identities;
   - namespace matches the complete prefix contract;
   - category and role match authoritative metadata, not guessed keywords;
   - current-value filters state whether they compare explicit or effective values;
   - exclusions win over inclusions unless the user explicitly chooses another precedence.
4. Deduplicate targets and classify unavailable, ambiguous, protected, active, and already-compliant profiles. Exclude the current Configuration Manager by default.
5. Validate the requested key and value against the running Hermes version. For models/providers, confirm exact IDs, compatible provider selection, authentication readiness, and whether the change affects only new sessions.
6. Build a dry-run matrix containing exact profile, selection reason, current explicit value, current effective value, proposed operation, resulting effective value, exception/status, verification method, and rollback operation.
7. Summarize counts programmatically and reconcile them with the enumerated matrix. State batch size, stop policy, active-session behavior, and any gateway or operator handoff.
8. Obtain user approval for the exact matrix and execution policy. A general request to "update engineering" is not approval for an unresolved or subsequently changed target list.

## Decision rules

- If the target set changes after approval, pause and request approval for the revised set.
- Prefer the narrowest scope that achieves the outcome; do not create profile overrides when changing a global inherited default is explicitly intended and safe.
- Do not use a bulk wildcard as the execution authority. Execute against the approved enumerated identities.
- Treat credential addition/removal, provider logout, insecure transport, approval weakening, and changes to the active Configuration Manager as separately material decisions.

## Quality gate

The plan is ready only when target counts equal the enumerated profiles, every profile has a current and rollback disposition, ambiguities are resolved, provider/model prerequisites are verified, the current manager is excluded or explicitly approved, and the user has approved the exact side effects rather than a fuzzy selector.