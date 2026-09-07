# Hermes Academy Continuing Education — Architecture Contract

Status: normative architecture contract. This document defines the actors, hard invariants, transport, and naming decisions for Continuing Education. Changes to these decisions require an explicit, documented edit here.

## Runtime scope

Continuing Education must use normal Hermes Agent primitives with Profile Packs. It must not require a separate training runtime, routing daemon, scheduler, message bus, persistence service, or distributed-runtime system.

### Current Hermes compatibility

Continuing Education needs three generic Hermes capabilities. First, the Bot-Chat-only `goal_manage` bridge lets an agent establish native `GoalManager`/`GoalContract` state without adding Academy state or a second goal loop. Second, profile-distribution `preload_skills` activates installed, non-disabled skills before the first model turn without granting extra tools or authority. Third, native continuation includes the previous bounded `continue` reason so an agent can respond to failed goal-judge feedback while keeping `wait` and `done` feedback out of later turns.

Every participating Agency distribution declares `academy-continuing-education` as a preload. The flow requires a Hermes build that provides `goal_manage`, profile-distribution `preload_skills`, bounded goal-judge feedback, duplicate in-flight `message_agent` suppression, and the associated Bot Chat behavior. Compatibility with the standard Hermes release is not yet guaranteed. This compatibility gap must not be “solved” by adding an Academy-specific runtime.

## Actors (exhaustive)

Only these concepts exist. No other agent type, role, or persistence primitive is introduced by this system.

- **Learner** — any installed Hermes profile receiving education.
- **Instructor** — an Academy profile teaching a bounded subject.
- **Dean** — `academy-dean`, used when the learner does not know which instructor it needs; routes to the most specific available faculty.
- **Continuing Education Session** — an ordinary Hermes conversation-based teaching interaction. It is NOT a new persistence primitive.
- **Learned Skill** — the normal Hermes skill produced or extended through `/learn` and persisted via `skill_manage`.

There is **no new Agent type**. The five actors above are the full set.

## Hard invariants

These requirements are non-negotiable.

1. **No separate runtime.** No special Academy runtime, daemon, service, scheduler, transport, or persistence layer is required.
2. **Standard installation target.** The target is a normal Hermes Agent installation with Profile Packs. Until the standard Hermes release contains and verifies the required generic native capabilities, documentation must retain the compatibility caveat rather than weakening this invariant.
3. **Natural-language UX.** Normal conversational language is the primary interface. The user must not need CLI commands, profile IDs, skill names, or syntax. `Dean` may resolve an instructor so the user never names one.
4. **Teachers never mutate learner internals.** An Instructor never directly edits the learner's skills, `SOUL.md`, or configuration. Teaching is content delivered through conversation.
5. **Durable learning is native.** Persistent improvement happens only through Hermes `/learn`; skill creation/update happens only through Hermes `skill_manage`. No custom persistence layer is built.
6. **Learner state stays in the learner.** Identity and state remain in the learner's normal Hermes profile. The instructor does not own or mirror it.
7. **Source packs are read-only to learning.** Profile Packs source distributions (`hermes-profile-packs/...`) are not modified merely because an installed profile learned something. Local learning is local.
8. **One explicit event.** Every training event has exactly one explicit learner, one teaching objective, and one instructor (or Dean-routed faculty member).
9. **No recursive training.** One class may not silently trigger another student → teacher → student chain. Further study requires an instructor recommendation plus a learner decision under an active goal, or a user instruction.
10. **No parallel infrastructure.** Do not create a candidate-skill database, skill registry, session store, scheduler, or orchestration runtime. Prefer an existing Hermes primitive over custom code every time. A parallel store is permitted only if upstream Hermes provably cannot represent something actually required, and that exception must be documented here first.
11. **Minimum sufficient instruction.** Continuing Education is a competency-transfer system, not a school simulation. Baseline before teaching; teach only demonstrated gaps; combine instructional functions into as few turns as practical; skip instruction when competency is already demonstrated; correct only what failed; require meaningfully different transfer evidence when instruction was needed; and stop as soon as the completion contract is satisfied. Do not impose fixed lesson lengths, modules, ceremonial quizzes, acknowledgement turns, or other classroom roleplay. Invoke `/learn` only when the event produced a reusable capability delta worth persisting. QA scripts may use fixed turn sequences to prove mechanics, but those sequences are test scaffolding and must not become the production teaching protocol.
12. **Learner skill preservation.** Before native `/learn`, record the learner's existing skill names. The persistence request may extend one relevant skill or create one new skill, but it must preserve unrelated learner skills. After `/learn`, verify every unrelated pre-existing skill still exists. Any unexplained loss, relocation, or overwrite fails the Continuing Education event closed; do not report successful learning until recovery is complete.
13. **Dean routing must be evidenced.** When the user did not name an instructor, the learner must actually ask `academy-dean` through native Bot messaging and wait for its reply before selecting or contacting faculty. Topic inference is not a substitute for Dean routing, and a learner must never claim a Dean recommendation that was not received in the session.
14. **Assessment gates persistence.** When instruction occurred, durable learning is forbidden until the selected instructor explicitly returns `MASTERED` for the learner's specific transfer submission. A generic lesson, repeated overview, learner self-assessment, missing or ambiguous evaluation, unavailable instructor, transport failure, or native goal stop condition is not mastery. `NEEDS_CORRECTION` requires the minimum correction and a new instructor judgment; `BLOCKED` stops without persistence.
15. **Academy role skills are deterministic.** Academy faculty distributions preload `teach-profile`, and `academy-dean` preloads `faculty-routing`, so teaching/assessment and faculty routing do not depend on probabilistic skill selection.
16. **Dean routing fails closed.** A Continuing Education objective that strongly spans different Academy categories must be narrowed rather than arbitrarily assigned to a broad chair. Missing specialists may use only a safe installed fallback from the same category. Installed availability is evidence, not an assumption.
17. **Installed Dean is self-contained.** Pack-root `hermes-academy/routing.py` is a reference implementation and regression-test oracle, not a runtime dependency of an installed Dean distribution. The preloaded `faculty-routing` skill owns the installed routing contract, and validators keep it aligned with manifest routing policy.

## Transport decision (selected)

The canonical one-to-one classroom transport is **canonical Bot Chat + native `message_agent`**. This path provides sender validation and attribution, asynchronous delivery, recipient wake-up, canonical history persistence and ordering, and multi-turn instructional exchange. Native Bot groups are an optional group/classroom surface, but they are not the default Continuing Education transport. No new message bus is built.

## Naming decisions (frozen)

These names are canonical and must be used consistently by the installer and distributions.

| Concept | Canonical name |
| --- | --- |
| Architecture contract (this file) | `docs/CONTINUING_EDUCATION_ARCHITECTURE.md` |
| User/maintainer guide | `docs/CONTINUING_EDUCATION.md` |
| Canonical learner skill | `academy-continuing-education` |
| Canonical instructor skill | `teach-profile` |

The learner skill `academy-continuing-education` is conceptually Academy's but is installed into participating learner profiles from one canonical source. The instructor skill `teach-profile` is delivered to Academy instructors alongside their subject-specific teaching skills.

## Relationship to the rest of the repository

- Continuing Education extends **Hermes Academy** (`academy-*`), whose faculty and teaching model are defined in `hermes-academy/ACADEMY.md`.
- It does not weaken, bypass, or relocate the invariants in the repository `AGENTS.md` or `hermes-agency/AGENTS.md`.
- The `agency-*`, `council-*`, and `academy-*` namespace boundaries and the "no live node registries / peer discovery / scheduling / remote-execution services" rules remain in force.

This contract is intentionally stable. Compatibility work may add the required generic Hermes capabilities to the standard release; it must not add actors, remove invariants, or introduce the separate infrastructure this document forbids.