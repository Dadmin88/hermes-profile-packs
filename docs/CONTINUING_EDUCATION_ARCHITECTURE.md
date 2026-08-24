# Hermes Academy Continuing Education — Architecture Contract

Status: normative architecture contract; implementation is merged and independently validated through Phase 15, and the Phase 16 implementation/whole-change review has passed for the maintained downstream Hermes integration. The stock-install release compatibility gate remains pending until the normal NousResearch Hermes release provides equivalent generic native seams. This document freezes the actors, hard invariants, transport decision, and naming decisions so later work cannot quietly balloon into a new framework. Changes to these decisions require an explicit, documented edit here.

## Scope independence

Hermes Academy Continuing Education is independent of Hermes Fleet.

It must run on a normal Hermes Agent installation with Profile Packs. It must not require Fleet, Keryx, Nodescale, Templar, RunAuthority, Run Capsules, or any equivalent distributed-runtime system to exist, to be reachable, or to be installed. If any such system is present, Continuing Education must not depend on it.

### Current Hermes compatibility

The controlled preflight proved three generic Hermes seams were needed. First, an agent could use `message_agent` but could not programmatically establish the same native standing goal that a human reaches through `/goal`; the generic Bot-Chat-only `goal_manage` bridge now wraps the existing `GoalManager`/`GoalContract` without adding Academy state or a second goal loop. Second, skill-index routing was not deterministic enough for a profile-defining workflow; generic profile distributions now support `preload_skills`, which activates installed, non-disabled skills from that profile before the first model turn without granting extra tools or authority. Third, a failed goal-judge reason was persisted but not included in the next continuation turn, so an agent could repeat the same insufficient completion claim. Native continuation now includes the previous bounded `continue` reason while keeping `wait` and `done` feedback out of later turns.

All three capabilities are merged in the maintained downstream Hermes Agent: `goal_manage` in `Dadmin88/hermes-agent-downstream` PR #24 / merge `9b8de86a80`, distribution `preload_skills` in PR #26 / merge `4c38d408f7`, and bounded goal-judge feedback propagation in PR #27 / merge `406ea5c64e`. The downstream Bot Mode path also includes duplicate in-flight `message_agent` suppression. Every Agency distribution declares `academy-continuing-education` as a preload.

The maintained downstream integration satisfies the functional CE contract and has passed production-profile verification. Equivalent `goal_manage` and `preload_skills` support are not yet present in the stock NousResearch Hermes reference used by the latest downstream reconciliation, so the architecture's stock-install release invariant is not yet satisfied by the normal upstream release. Profile Packs must not claim unqualified stock-Hermes readiness until equivalent generic support lands upstream. This compatibility gap must not be “solved” by adding an Academy-specific runtime.

## Actors (exhaustive)

Only these concepts exist. No other agent type, role, or persistence primitive is introduced by this system.

- **Learner** — any installed Hermes profile receiving education.
- **Instructor** — an Academy profile teaching a bounded subject.
- **Dean** — `academy-dean`, used when the learner does not know which instructor it needs; routes to the most specific available faculty.
- **Continuing Education Session** — an ordinary Hermes conversation-based teaching interaction. It is NOT a new persistence primitive.
- **Learned Skill** — the normal Hermes skill produced or extended through `/learn` and persisted via `skill_manage`.

There is **no new Agent type**. The five actors above are the full set.

## Hard invariants

These are non-negotiable. They are the acceptance criteria for Phase 0 and the constraints for every later phase.

1. **Zero Fleet dependency.** No import, runtime call, configuration reference, or behavioral coupling into any of: **Fleet, Keryx, Nodescale, Templar, RunAuthority, Run Capsules**. This prohibition is absolute and applies to skills, scripts, SOUL behavior, and any later implementation code.
2. **Works on a stock install.** Must function on a normal Hermes Agent installation with Profile Packs; no special Academy runtime, daemon, service, or node is required. Until the normal Hermes release contains the required generic native seams, this remains an explicit open release-compatibility gate rather than an invariant to weaken.
3. **Natural-language UX.** Normal conversational language is the primary interface. The user must not need CLI commands, profile IDs, skill names, or syntax. `Dean` may resolve an instructor so the user never names one.
4. **Teachers never mutate learner internals.** An Instructor never directly edits the learner's skills, `SOUL.md`, or configuration. Teaching is content delivered through conversation.
5. **Durable learning is native.** Persistent improvement happens only through Hermes `/learn`; skill creation/update happens only through Hermes `skill_manage`. No custom persistence layer is built.
6. **Learner state stays in the learner.** Identity and state remain in the learner's normal Hermes profile. The instructor does not own or mirror it.
7. **Source packs are read-only to learning.** Profile Packs source distributions (`hermes-profile-packs/...`) are not modified merely because an installed profile learned something. Local learning is local.
8. **One explicit event.** Every training event has exactly one explicit learner, one teaching objective, and one instructor (or Dean-routed faculty member).
9. **No recursive training.** One class may not silently trigger another student → teacher → student chain. Further study requires an instructor recommendation plus a learner decision under an active goal, or a user instruction.
10. **No parallel infrastructure.** Do not create a candidate-skill database, skill registry, session store, scheduler, or orchestration runtime. Prefer an existing Hermes primitive over custom code every time. A parallel store is permitted only if upstream Hermes provably cannot represent something actually required, and that exception must be documented here first.
11. **Minimum sufficient instruction.** Continuing Education is a competency-transfer system, not a school simulation. Baseline before teaching; teach only demonstrated gaps; combine instructional functions into as few turns as practical; skip instruction when competency is already demonstrated; correct only what failed; require meaningfully different transfer evidence when instruction was needed; and stop as soon as the completion contract is satisfied. Do not impose fixed lesson lengths, modules, ceremonial quizzes, acknowledgement turns, or other classroom roleplay. Invoke `/learn` only when the event produced a reusable capability delta worth persisting. Phase-specific QA scripts may use fixed turn sequences to prove mechanics, but those sequences are test scaffolding and must not become the production teaching protocol.
12. **Learner skill preservation.** Before native `/learn`, record the learner's existing skill names. The persistence request may extend one relevant skill or create one new skill, but it must preserve unrelated learner skills. After `/learn`, verify every unrelated pre-existing skill still exists. Any unexplained loss, relocation, or overwrite fails the Continuing Education event closed; do not report successful learning until recovery is complete.
13. **Dean routing must be evidenced.** When the user did not name an instructor, the learner must actually ask `academy-dean` through native Bot messaging and wait for its reply before selecting or contacting faculty. Topic inference is not a substitute for Dean routing, and a learner must never claim a Dean recommendation that was not received in the session.
14. **Assessment gates persistence.** When instruction occurred, durable learning is forbidden until the selected instructor explicitly returns `MASTERED` for the learner's specific transfer submission. A generic lesson, repeated overview, learner self-assessment, missing or ambiguous evaluation, unavailable instructor, transport failure, or native goal stop condition is not mastery. `NEEDS_CORRECTION` requires the minimum correction and a new instructor judgment; `BLOCKED` stops without persistence.
15. **Academy role skills are deterministic.** Academy faculty distributions preload `teach-profile`, and `academy-dean` preloads `faculty-routing`, so teaching/assessment and faculty routing do not depend on probabilistic skill selection.
16. **Dean routing fails closed.** A Continuing Education objective that strongly spans different Academy categories must be narrowed rather than arbitrarily assigned to a broad chair. Missing specialists may use only a safe installed fallback from the same category. Installed availability is evidence, not an assumption.
17. **Installed Dean is self-contained.** Pack-root `hermes-academy/routing.py` is a reference implementation and regression-test oracle, not a runtime dependency of an installed Dean distribution. The preloaded `faculty-routing` skill owns the installed routing contract, and validators keep it aligned with manifest routing policy.

## Transport decision (selected)

The canonical one-to-one classroom transport is **canonical Bot Chat + native `message_agent`**. Phase 2 proved sender validation/attribution, asynchronous delivery, recipient wake-up, canonical history persistence/ordering, and a multi-turn instructional exchange. Native Bot groups were also validated as a useful optional group/classroom surface, but they are not the default CE transport. No new message bus is built.

## Naming decisions (frozen)

These names are canonical and must be used consistently by later phases and by the installer/distribution.

| Concept | Canonical name |
| --- | --- |
| Architecture contract (this file) | `docs/CONTINUING_EDUCATION_ARCHITECTURE.md` |
| User/maintainer guide | `docs/CONTINUING_EDUCATION.md` |
| Phase 16 release record | `docs/CONTINUING_EDUCATION_RELEASE_REVIEW.md` |
| Canonical learner skill | `academy-continuing-education` |
| Canonical instructor skill | `teach-profile` |

The learner skill `academy-continuing-education` is conceptually Academy's but is installed into participating learner profiles from one canonical source. The instructor skill `teach-profile` is delivered to Academy instructors alongside their subject-specific teaching skills.

## Relationship to the rest of the repository

- Continuing Education extends **Hermes Academy** (`academy-*`), whose faculty and teaching model are defined in `hermes-academy/ACADEMY.md`.
- It does not weaken, bypass, or relocate the invariants in the repository `AGENTS.md` or `hermes-agency/AGENTS.md`.
- The `agency-*`, `council-*`, and `academy-*` namespace boundaries and the "no live node registries / peer discovery / scheduling / remote-execution services" rules remain in force.

## Phase 16 disposition

The Phase 16 implementation/whole-change review is recorded in `docs/CONTINUING_EDUCATION_RELEASE_REVIEW.md` and is **PASS** for the maintained downstream Hermes integration. That review found and corrected category-unsafe broad-chair routing and the false implication that an installed Dean could depend on pack-root `routing.py`, then re-ran the full Profile Packs gate with validator-enforced routing parity.

The stock-install release compatibility gate remains **OPEN** until equivalent generic native support is present in the normal NousResearch Hermes release. That open gate does not authorize a parallel Academy runtime and must not be erased by documentation wording.

## Phase 0 acceptance (this document satisfies)

- A short architecture document exists describing the invariants above.
- It states, verbatim: _Hermes Academy Continuing Education is independent of Hermes Fleet._
- It explicitly prohibits imports/runtime calls to Fleet, Keryx, Nodescale, Templar, RunAuthority, and Run Capsules.

This contract is intentionally frozen. Later compatibility work may land required generic Hermes seams upstream; it must not add actors, remove invariants, or introduce coupling this document forbids.