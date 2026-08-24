# Hermes Academy

Hermes Academy is the education profile pack for Hermes Agent: a faculty of professors and instructors that teaches academic subjects, technical disciplines, vocational skills, and professional foundations.

## The idea

Opening an Academy profile should feel like walking into the office, classroom, lab, studio, or training room of the instructor you need.

Academy v0.2 contains **30 faculty profiles and 120 purpose-built teaching skills**. It keeps broad chairs for interdisciplinary learning while adding dedicated specialists for subjects that benefit from deeper routing.

## Continuing Education

Academy can also teach another installed Hermes profile through the Continuing Education flow. A learner can receive an ordinary request such as `Go learn API security`, route through an actual `academy-dean` Bot exchange when the user did not name a teacher, use the Bot Chat `goal_manage` bridge into Hermes' native goal state plus `message_agent`/`/learn` underneath, and persist a reusable capability in its own normal skill store. Academy faculty preload `teach-profile`, the Dean preloads `faculty-routing`, and instruction may be persisted only after the selected instructor explicitly returns `MASTERED` for the learner's specific transfer.

The implementation is merged and validated through the Phase 10–13 quality gate, and the Phase 14 controlled disposable-profile preflight has passed. Treat this as **pre-release/experimental**, not yet production-validated, until Phase 15 validates the actual persistent learner and Phase 16 completes release/whole-change review. The current flow uses generic downstream Hermes support for `goal_manage`, profile-distribution `preload_skills`, and bounded goal-judge feedback propagation, merged in PRs #24, #26, and #27. Agency profiles declare `academy-continuing-education` as a preload so the learner contract is active before the first model turn. Final stock-install readiness requires equivalent support in the normal Hermes release. See [`../docs/CONTINUING_EDUCATION.md`](../docs/CONTINUING_EDUCATION.md) for current behavior and status.

## User journey and limitations

A learner receives an ordinary request such as `Go learn API security with Academy.` If the user did not name a teacher, the learner sends one native `message_agent` request to `@academy-dean`, waits for the Dean reply, and uses the installed faculty profile explicitly named by that reply. In canonical Bot Chat, the learner uses `goal_manage(action="set", ...)` to establish the session's real native `/goal`/`GoalContract` state, then attempts a baseline before instruction. One-to-one teaching uses canonical Bot Chat + native `message_agent`. Assessment returns `MASTERED`, `NEEDS_CORRECTION`, or `BLOCKED`. If instruction occurred, persistence is forbidden until the selected instructor explicitly returns `MASTERED` for the learner's specific transfer. Only after that gate may the learner invoke native `/learn` for a reusable capability delta. See [`../docs/CONTINUING_EDUCATION.md`](../docs/CONTINUING_EDUCATION.md) for current behavior, status, troubleshooting, and limitations.

Continuing Education remains **pre-release/experimental** until Phase 16 release/whole-change review completes. The current flow requires generic downstream Hermes support for `goal_manage`, profile-distribution `preload_skills`, and bounded goal-judge feedback propagation. Stock-install readiness requires equivalent support in the normal Hermes release used by Profile Packs. Continuing Education is **independent of Hermes Fleet** and requires no Fleet/Keryx/Nodescale/Templar/RunAuthority/Run Capsules. Do not expose CLI, slash commands, or Bot internals as normal user UX. There is no implemented optional Desktop UI for this flow. Instructors teach within their subject and safety boundaries; they do not award grades, credentials, licenses, certifications, or professional authority.

## Faculty

| Profile | Teaching domain |
| --- | --- |
| `academy-dean` | Faculty routing, learner brief, curriculum path, cross-faculty synthesis |
| `academy-mathematics-professor` | Mathematics and quantitative problem solving |
| `academy-writing-rhetoric-professor` | Writing, rhetoric, grammar, argument, revision |
| `academy-natural-sciences-professor` | Interdisciplinary natural sciences and scientific reasoning |
| `academy-physics-professor` | Physics, models, diagrams, quantitative problem solving |
| `academy-chemistry-professor` | Chemistry, molecular structure, reactions, stoichiometry |
| `academy-biology-professor` | Biology, systems, genetics, evolution |
| `academy-statistics-professor` | Statistics, inference, uncertainty, quantitative evidence |
| `academy-data-science-professor` | Data analysis, modeling, evaluation, data-science workflows |
| `academy-computer-science-professor` | Programming, algorithms, data structures, systems, computation |
| `academy-engineering-professor` | Engineering analysis, design, models, tradeoffs |
| `academy-cybersecurity-instructor` | Defensive security, threat modeling, secure design, authorized labs |
| `academy-cloud-systems-instructor` | Cloud, infrastructure, systems architecture, reliability |
| `academy-history-professor` | Historical context, sources, causation, historiography |
| `academy-philosophy-professor` | Philosophy, arguments, thought experiments, competing positions |
| `academy-law-professor` | Law, legal reasoning, cases, doctrine, institutions |
| `academy-theology-religious-studies-professor` | Theology, religious studies, texts, traditions, doctrine |
| `academy-social-sciences-professor` | Psychology, sociology, political science, anthropology foundations |
| `academy-economics-professor` | Micro, macro, markets, models, policy reasoning |
| `academy-business-professor` | Accounting, finance, management, marketing, operations, strategy |
| `academy-education-professor` | Pedagogy, learning science, lesson and assessment design |
| `academy-project-management-instructor` | Planning, estimation, risk, dependencies, delivery methods |
| `academy-language-instructor` | Language acquisition and conversation |
| `academy-research-methods-professor` | Research design, evidence, sources, methods, critique |
| `academy-skilled-trades-instructor` | Safety-first trade foundations, tools, measurement, procedures |
| `academy-automotive-instructor` | Automotive systems, diagnostics, maintenance, shop safety |
| `academy-culinary-arts-instructor` | Culinary technique, food safety, recipes, kitchen practice |
| `academy-health-sciences-professor` | Anatomy, physiology, terminology, health-science reasoning |
| `academy-arts-design-instructor` | Art/design fundamentals, critique, practice, portfolio learning |
| `academy-music-instructor` | Music theory, rhythm, ear training, composition, performance |

## Broad chairs and specialists

Broad profiles remain useful. `academy-natural-sciences-professor` is intentionally preserved for interdisciplinary science, scientific reasoning, and learning that spans multiple natural-science disciplines.

When the topic is clearly specialized, the Dean should prefer the dedicated faculty member. A physics request routes to `academy-physics-professor`, chemistry to `academy-chemistry-professor`, and biology to `academy-biology-professor`. The same specific-over-broad rule applies across the v0.2 specialist faculty.

## Teaching philosophy

Academy exists to help people **learn**, not merely receive plausible answers. Profiles adapt to learner level, explain concepts, demonstrate reasoning, provide guided practice, check understanding, correct misconceptions, and build transferable capability.

Professors and instructors may answer directly when that is what the learner wants. They should not manufacture friction or force a quiz. But when the goal is learning, they should teach in a way that makes the learner progressively less dependent on the profile.

Academy profiles do not claim to award grades, credentials, licenses, certifications, or professional authority. High-risk technical or health instruction remains educational and respects appropriate real-world supervision, codes, standards, and professional boundaries.

## Install

```bash
python install.py --list
python install.py academy-cybersecurity-instructor academy-physics-professor
python install.py
```
