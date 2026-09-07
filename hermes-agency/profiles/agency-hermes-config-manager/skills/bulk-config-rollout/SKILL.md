---
name: bulk-config-rollout
description: Apply an approved Hermes configuration or provider setup plan across enumerated profiles in bounded, verifiable batches.
---
# Bulk Hermes Configuration Rollout

Use only after the exact profile target matrix, operations, exceptions, batching, and rollback policy have been approved.

## Procedure

1. Re-run read-only preflight immediately before execution. Confirm the approved profiles still exist, prior values have not drifted, target keys remain supported, provider/model prerequisites remain ready, and active-session assumptions still hold.
2. If credentials are required, use the supported Hermes authentication workflow before profile assignment:
   - prefer browser OAuth or an interactive secure prompt;
   - let the user enter secrets directly into the protected interface;
   - never accept or echo secrets in ordinary chat;
   - never place an API key in a command argument, generated script, plan, log, or report;
   - never use insecure TLS or bypass certificate validation;
   - verify success with provider status rather than reading stored credentials.
3. Preserve each target's rollback operation: restore the previous explicit value, or unset the new override when the prior state was inherited/absent. Do not snapshot credential contents.
4. Apply supported profile-scoped `config set` or `config unset` operations to a small canary batch when the scope or impact is material. Use exact profile identities and exact key/value strings.
5. Read back the canary profiles and, when configuration activation requires it, validate in fresh sessions. Stop if effective values, provider readiness, or behavior differ from the approved plan.
6. Continue in bounded batches. Record attempted, changed, already-compliant, failed, and not-attempted identities; do not retry systematic failures across the whole fleet.
7. Apply an explicitly included active Configuration Manager last. Warn that changing its model/provider or tools may not affect the current conversation and may require a new session.
8. Reconcile the complete target set and hand gateway/service restarts to the designated operator. Never restart or interrupt live messaging implicitly as part of a config write.

## Failure behavior

- Stop on target-set drift, unsupported keys, authentication regression, wrong effective values, unexpected scope, repeated command failure, or loss of the verified control path.
- Do not automatically roll back successful profiles unless the approved policy says to do so. Present mixed state and let the user choose roll-forward or rollback when either is safe.
- Credential removal, logout, pool reset, or replacement requires separate explicit approval because it can affect profiles outside the visible target set.

## Quality gate

Execution is complete only when each approved identity has one reconciled status, every changed profile has been read back, credentials never entered chat or command arguments, counts match the target matrix, active-profile and restart effects are explicit, and no unapproved target or key was changed.