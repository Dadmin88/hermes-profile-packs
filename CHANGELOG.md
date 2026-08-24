# Changelog

All notable changes to Hermes Profile Packs will be documented here.

## Unreleased

### Added

- Added the merged Hermes Academy Continuing Education implementation through Phase 15 independent production verification: canonical learner/instructor shared skills, Dean routing, native Bot Chat + `message_agent` teaching transport, native `/goal`/`/subgoal`/`/learn` contracts, minimum-sufficient competency transfer, and deterministic/native-runtime regression coverage. Phase 14 introduced three merged generic Hermes seams used by this flow: the Bot-Chat-only `goal_manage` bridge for agent-owned native goals (downstream PR #24), profile-distribution `preload_skills` for deterministic profile-defining skill activation (PR #26), and bounded goal-judge failure feedback in the next native continuation turn (PR #27). All 109 Agency distributions preload `academy-continuing-education`. Phase 15 production hardening additionally requires evidenced Dean routing for unnamed instructors, deterministic `teach-profile` preloading across all 29 faculty, deterministic `faculty-routing` preloading for the Dean, baseline-diagnostic mode that forbids broad lesson replay when a learner already supplied evidence, assessment of the newest transfer submission instead of generic lesson replay, and explicit instructor `MASTERED` before persistence. Independent Phase 15 verification passed: exact 90-skill union with only `auth-integration` changed, CE contract byte-identical to source, real Dean route, clean instructor diagnostic/NEEDS_CORRECTION/MASTERED sequence, native goal DONE at 4/30, fresh-session 8/8 reuse of the learned skill, Academy-owned instructor skills byte-identical to source, Profile Packs source tree unchanged, downstream Hermes PR #29 verified with 89/89 focused tests, and no distributed-runtime dependency. No secret leakage, no overbroad content, and no duplicate skills were found. Residual risks are acceptable and documented. Continuing Education has zero dependency on Hermes Fleet or equivalent distributed runtime.
- Added `docs/CONTINUING_EDUCATION.md` as the current behavior/status guide and updated the normative architecture contract with the selected transport and learner-skill preservation invariant.
- Integrated Team Recipes into the canonical root `install.py` wizard and agent/script interface, including direct recipe browsing, `--list-recipes`, `--recipe`, and `--tier` selection.
- Added confidence-aware recipe promotion: a recipe must clear both a minimum score and a minimum lead over alternatives before the installer presents it as a clear match; ambiguous goals fall back to individual profiles.
- Added additive `recipe_match` and `recipe_recommendations` fields to `--recommend --json` while preserving the existing individual-profile `recommendations` contract.
- Added shared `recipe_catalog.py` so `install.py` and the focused `recipes.py` client use one recipe registry/scoring/confidence implementation.
- Added exact root-installer recipe dry-run coverage and compatibility tests, plus the detailed Recipe-Aware Root Installer implementation plan.
- Added a validated `recipes.json` team-composition layer with minimal, recommended, and expanded tiers across Agency, Council, and Academy.
- Added `recipes.py` for deterministic recipe discovery, recommendation, dry-run planning, JSON output, and explicit `--yes` installation through the existing profile installer.
- Added first-team onboarding, team operating guidance, post-install verification, troubleshooting, and sanitized worked examples.
- Added `coordination-pattern-selection` to Agency Orchestrator and strengthened its SOUL to prefer the smallest capable team instead of delegation-by-default.
- Added recipe schema validation and root recipe tests for tier monotonicity, profile resolution, recommendation behavior, and JSON dry-run plans.
- Added the detailed Team Operating Layer implementation/acceptance plan and documented the source/runtime boundary for recipes and optional routines.
- Added an interactive root installer wizard that recommends a small profile set from plain-language goals, supports pack/category browsing and direct search, previews the exact install plan, and still offers an explicit install-everything path.
- Added a deterministic agent/script interface with JSON catalog and recommendation output, exact profile/category selection, pack filtering, dry-run planning, and non-interactive `--yes` installation.
- Added profile-selection payload estimates so sparse installs show how much of the catalog they avoid installing.
- Added root installer tests and CI coverage while preserving the existing pack-first installer commands.

## 0.4.0 - 2026-08-22

### Added

- Expanded **Hermes Academy** from 15 to 30 faculty profiles and from 60 to 120 purpose-built teaching skills.
- Added dedicated faculty for physics, chemistry, biology, statistics, data science, philosophy, law and legal studies, theology and religious studies, education and pedagogy, cybersecurity, cloud and systems, project management, automotive, culinary arts, and music.
- Added explicit specialist routing so clearly specialized requests prefer the dedicated faculty member while preserving `academy-natural-sciences-professor` as the interdisciplinary natural-sciences chair.
- Added Academy v0.2 tests that enforce the 30-profile / 120-skill release target, second-wave faculty presence, broad-chair preservation, and valid specialist routing.

## 0.3.0 - 2026-08-22

### Added

- Added **Hermes Academy**, a new `academy-*` profile pack for academic, technical, vocational, and professional teaching.
- Added an initial 15-profile faculty led by `academy-dean`, with 60 purpose-built teaching skills.
- Added professors for mathematics, writing and rhetoric, natural sciences, computer science, engineering, history, social sciences, economics, business, research methods, and health sciences.
- Added instructors for languages, skilled trades, and arts/design.
- Added the Academy teaching contract, installer, validator, tests, documentation, root routing, and CI coverage.

## 0.2.0 - 2026-08-22

### Added

- Expanded Hermes Council from 11 to 21 profiles and from 44 to 84 purpose-built skills.
- Added `council-health-navigator` for healthcare preparation, neutral health logging, preventive-care organization, and follow-up.
- Added `council-resilience-coach` for non-clinical stress regulation, recovery, and healthy coping.
- Added `council-time-attention-coach` for realistic planning, focus, attention management, and calendar boundaries.
- Added `council-career-coach` for career direction, opportunity evaluation, job-search strategy, and work boundaries.
- Added `council-personal-admin-steward` for documents, forms, renewals, appointments, accounts, and subscriptions.
- Added `council-preparedness-steward` for household emergency planning, go-bags, contact plans, and contingencies.
- Added `council-recreation-guide` for hobbies, restorative leisure, play, outings, and low-pressure novelty.
- Added `council-travel-planner` for current, practical trip planning, itineraries, packing, and budgets.
- Added `council-communication-coach` for assertiveness, listening, repair, conversation rehearsal, and message clarity.
- Added `council-community-coach` for friendship, belonging, support networks, and community participation.
- Expanded Council documentation with clearer safety, authority, and specialist-boundary guidance.

## 0.1.0 - 2026-08-22

### Added

- Initial public monorepo structure for reusable Hermes profile packs.
- Imported Hermes Agency with 109 professional profiles from the existing standalone profile-pack repository.
- Added Hermes Council with 11 personal-life profiles and 44 purpose-built skills.
- Added `council-steward` as the Council coordinator and minimum-context routing owner.
- Preserved the authored `council-life-coach` and `council-fitness-coach` SOUL definitions while converting them into portable profile distributions.
- Added repository-wide installation, validation, portability checks, CI, contribution guidance, security policy, and pack specification.
