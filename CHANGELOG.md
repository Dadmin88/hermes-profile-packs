# Changelog

All notable changes to Hermes Profile Packs will be documented here.

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
