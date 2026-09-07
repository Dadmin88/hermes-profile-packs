---
name: config-verification-and-rollback
description: Verify effective Hermes configuration after rollout, detect drift or partial application, and restore approved prior values safely.
---
# Hermes Configuration Verification and Rollback

Use after configuration changes, when reported state disagrees with effective behavior, or when the user asks to undo a prior approved rollout.

## Procedure

1. Load the approved change record and current inventory. Verify exact profile identities, keys, intended effective values, prior explicit/inherited state, provider dependencies, and restart/new-session expectations.
2. Read back every target through supported profile-scoped configuration commands. Do not treat process exit status, file timestamps, or the planned value as proof.
3. Classify each target as verified, already compliant, drifted, failed, unavailable, pending fresh-session activation, or pending operator restart. Reconcile totals programmatically with the approved target count.
4. For behavior-sensitive settings such as model/provider selection, run the smallest safe fresh-session smoke test needed to confirm effective use. Avoid costly or side-effecting prompts and never expose credentials.
5. Diagnose only configuration-layer discrepancies: explicit override precedence, global inheritance, unsupported key, malformed value, provider readiness, stale process/session, or failed write. Hand unexplained runtime failure to `agency-technical-support-engineer`.
6. Before rollback, show the exact profiles and inverse operations. Obtain approval unless rollback was pre-authorized for the observed failure condition.
7. Restore the previous explicit value, or unset the introduced override when the profile previously inherited or lacked the key. Apply bounded batches and verify every restored effective value.
8. Report final state, unresolved drift, unavailable profiles, provider/credential implications, and any gateway or service action owned by the operator.

## Quality gate

Verification or rollback is complete when every target is reconciled, effective values—not merely writes—match the intended state, inverse operations preserve prior inheritance semantics, totals match the enumerated list, secrets were not accessed, and remaining runtime or infrastructure work has an explicit owner.