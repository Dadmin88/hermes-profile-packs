# Hermes Academy Continuing Education — Phase 16 Release Review

Status: **IMPLEMENTATION/WHOLE-CHANGE REVIEW PASSED for the maintained downstream Hermes integration. STOCK-INSTALL RELEASE COMPATIBILITY remains OPEN.**

This document records the Profile Packs Phase 16 whole-change/release review for Hermes Academy Continuing Education. It records what was reviewed, what the review found, what was corrected, what was revalidated, and the compatibility boundary that still prevents an unqualified stock-Hermes release claim.

## Release decision

The Continuing Education implementation is **production-validated on the maintained `Dadmin88/hermes-agent-downstream` integration path**.

The implementation is **not yet stock-upstream-Hermes ready**. The normal NousResearch Hermes release used by a Profile Packs installation must provide equivalent generic support for the native seams Continuing Education requires before the architecture's stock-install release invariant is satisfied.

This distinction is deliberate:

- Phase 16 implementation/whole-change review: **PASS**.
- Maintained downstream Hermes integration: **PASS**.
- Stock-install release compatibility: **OPEN / BLOCKED ON UPSTREAM EQUIVALENT SUPPORT**.
- Hermes Fleet dependency: **NONE**.

Passing the Profile Packs review does not waive the stock-install architecture invariant. It means the Academy/Profile Packs implementation is release-reviewed and ready to integrate with a compatible Hermes build while upstream compatibility remains an explicit external gate.

## Scope reviewed

The review covered the complete Continuing Education path rather than only the teaching prompts:

- natural-language learner entry;
- required Dean routing when the user did not name an instructor;
- deterministic learner/instructor role-skill preloading;
- canonical Bot Chat and native `message_agent` transport;
- learner-owned native goal state through the generic Bot-Chat `goal_manage` bridge;
- baseline-first, minimum-sufficient instruction;
- instructor-owned transfer assessment;
- `MASTERED` gating before persistence;
- native `/learn` and normal `skill_manage` persistence;
- unrelated learner-skill preservation;
- source-pack and instructor isolation;
- cancellation, write approval, restart/resume, unavailable-instructor, and no-Fleet behavior;
- Academy routing policy, install/distribution behavior, validators, public documentation, and release status language.

## Phase 16 findings and corrections

### 1. Cross-domain Dean routing could choose an unrelated broad chair

The repository reference router previously treated any recognized multi-domain objective as an interdisciplinary request and returned the first configured `routing.broad_chairs` entry. The Academy manifest currently preserves `academy-natural-sciences-professor` as a broad natural-science chair, so an unrelated objective such as cybersecurity plus project management could be incorrectly routed to Natural Sciences.

Phase 16 corrected the policy:

- same-category multi-specialty objectives may use that category's broad fallback;
- cross-category Continuing Education objectives fail closed and ask the learner to narrow the competency or choose an instructor;
- a broad chair is never treated as a universal fallback;
- missing specialists may fall back only to an installed broad faculty member from the same category;
- role-description fallback uses meaningful exact-word overlap and fails closed on an equally strong tie;
- current installed-profile availability can be supplied explicitly and uninstalled profiles are not eligible.

The category fallback map is now manifest-owned under `routing.category_fallbacks`, and the Academy validator checks every category, target, and category/target relationship.

### 2. The installed Dean documentation implied a pack-root runtime dependency

The Dean's preloaded `faculty-routing` skill previously told the profile to use `hermes-academy/routing.py`. That file is a repository-level helper and is not part of a normal installed Dean profile distribution.

Phase 16 corrected the ownership boundary instead of adding another runtime:

- `hermes-academy/routing.py` is now explicitly a maintainer/test reference implementation and policy oracle;
- the installed `academy-dean` profile carries a self-contained routing contract in its preloaded `faculty-routing` skill;
- the Dean skill defines exact, approximate, and blocked routing outcomes and a compact machine-legible response shape;
- the skill requires real current-profile/Bot availability evidence before calling a faculty member installed;
- the Academy validator enforces parity between manifest category fallbacks and the installed Dean skill;
- no Academy routing daemon, scheduler, message bus, or second agent runtime was introduced.

## Maintained downstream Hermes compatibility

Continuing Education relies on generic Hermes capabilities that were implemented in the maintained downstream fork without Academy-specific runtime state:

- Bot-Chat-only `goal_manage`, merged through downstream PR #24;
- profile-distribution `preload_skills`, merged through downstream PR #26;
- bounded native goal-judge `continue` feedback propagation, merged through downstream PR #27;
- duplicate in-flight `message_agent` suppression, hardened later in the downstream Bot Mode path.

The downstream fork was subsequently reconciled with `NousResearch/hermes-agent@91e867631e9d2eb9fbd69edd4459475d38070979` while preserving those contracts. The reconciliation reported 533 Bot Mode tests, 127 targeted Desktop/session/profile tests, 200 focused Hermes/Academy Python tests, TypeScript typechecks, metadata validation, and diff checks passing locally.

The downstream reconciliation's GitHub Actions were not used as positive release evidence because those runs failed before the substantive test jobs at environment/scope/OSV setup. Phase 16 does not relabel infrastructure-red workflows as green application tests.

## Stock upstream compatibility boundary

At the upstream reference used for the downstream reconciliation, equivalent `goal_manage` and profile-distribution `preload_skills` support are not present in stock NousResearch Hermes.

Therefore:

- Profile Packs may describe Continuing Education as production-validated **with the maintained downstream Hermes integration**;
- Profile Packs must not describe it as stock-Hermes production ready yet;
- the user-facing flow must fail clearly when required native capabilities are unavailable rather than simulating them in Academy;
- upstreaming or otherwise landing equivalent generic Hermes seams is the remaining stock-release compatibility milestone.

## Exact Profile Packs validation

The Phase 16 correction branch passed the exact pull-request-head validation gate after the routing, installed-Dean, documentation, and status-regression corrections:

- repository validation: **PASS**;
- Academy manifest: **30 profiles, 120 owned teaching skills, 2 shared skills**;
- root installer/unit tests: **16/16 PASS**;
- Agency tests: **19/19 PASS**;
- Council tests: **3/3 PASS**;
- Academy tests: **200 PASS, 1 expected opt-in runtime skip**.

The Academy validator additionally proves:

- every routing specialist target exists;
- every category except coordination has exactly one declared category fallback;
- every category fallback exists and belongs to the declared category;
- the installed Dean skill mirrors every manifest category fallback;
- the installed Dean skill explicitly rejects a dependency on pack-root `routing.py`;
- shared learner/instructor skills retain canonical byte identity across materialized profile copies;
- portable-source hygiene remains enforced.

The final merge candidate must retain the same green repository/pack test gate before merge.

## Preserved invariants

Phase 16 did not waive the architecture contract:

- Hermes Academy Continuing Education remains independent of Hermes Fleet.
- A stock Hermes Agent installation with Profile Packs remains the canonical release target.
- No new Agent type exists.
- No Academy training database, scheduler, message bus, or candidate-skill registry exists.
- Instructors do not directly mutate learner state.
- Durable learning remains native `/learn` plus normal `skill_manage`.
- One Continuing Education event has one learner, one bounded objective, and one instructor.
- Assessment gates persistence.
- Source distributions remain read-only during local learning.
- Safety and write-approval boundaries remain authoritative.

## Phase 16 disposition

**IMPLEMENTATION PASS.** The Profile Packs Continuing Education implementation, routing policy, distribution contracts, validation rules, and public documentation are whole-change-review complete for the maintained downstream Hermes integration.

**STOCK RELEASE GATE OPEN.** The remaining compatibility milestone is to obtain equivalent generic support in the normal upstream Hermes release. Until then, the maintained downstream qualifier stays mandatory and the architecture's stock-install invariant remains visibly unsatisfied by stock upstream.