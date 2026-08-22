---
name: regression-risk-review
description: Review a change for behavior it can accidentally break by tracing affected callers, data, state, interfaces, concurrency, configuration, migrations, and operational assumptions.
---
# Regression Risk Review

Use when a code change appears locally correct but may affect existing behavior outside the immediate implementation path.

## Procedure
1. Read the intended change and identify what must remain unchanged. Regression review starts from preserved contracts, not only new acceptance criteria.
2. Map the changed surface: functions/modules, callers, shared types, persistence, caches, events, queues, configuration, feature flags, generated artifacts, schemas, migrations, external APIs, and user-visible states touched directly or indirectly.
3. Trace important downstream and upstream dependencies. Look for shared helpers or data structures whose behavior is relied on by code outside the edited files.
4. Review behavioral deltas that can hide inside apparently compatible code: defaults, ordering, null/empty handling, timing, retries, idempotency, transaction scope, error type/message contracts, serialization, precision, timezone, locale, and permission behavior.
5. Review state and concurrency assumptions. Check whether new code can race with old paths, leave stale cache/state, duplicate side effects, break replay/retry behavior, or change lock/transaction boundaries.
6. Review data changes for old and mixed-version data. Confirm migrations, backfills, rolling deployments, downgrade/rollback assumptions, and partial migration states where relevant.
7. Review configuration and environment sensitivity. A change that works with local defaults may fail when optional integrations, alternate storage, platform differences, or production feature flags are active.
8. Inspect existing tests around adjacent behavior, not only tests added in the patch. Identify preserved contracts that have no regression coverage and request focused tests when the risk is material.
9. Run or recommend targeted validation based on the risk map. Broader testing should be proportional to the shared surface and blast radius rather than automatically running everything or nothing.
10. Report concrete regression scenarios with the affected contract, path, consequence, and evidence. Separate proven defects from areas that merely need additional validation.

## Decision rules
- Diff size is not blast radius. A one-line shared-helper change can carry more regression risk than a large isolated feature.
- Existing behavior can be a contract even when it was not explicitly documented.
- Additive schema/API changes can still break consumers through defaults, ordering, limits, performance, or new required behavior.
- Do not demand exhaustive tests for every theoretical interaction; prioritize plausible, consequential regressions.

## Quality gate
The review is complete when the preserved contracts and affected surfaces are understood, meaningful hidden behavior changes have been checked, state/data/configuration risks are addressed, test coverage matches the plausible blast radius, and blocking regression findings are specific and actionable.