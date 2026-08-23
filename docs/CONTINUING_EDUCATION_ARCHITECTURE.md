# Hermes Academy Continuing Education — Architecture Contract

Status: normative architecture contract; implementation is merged through Phase 13 and the Phase 14 controlled disposable-profile preflight has passed. Phase 15 production-profile validation and Phase 16 release/whole-change review remain pending. This document freezes the actors, hard invariants, transport decision, and naming decisions so later work cannot quietly balloon into a new framework. Changes to these decisions require an explicit, documented edit here.

## Scope independence

Hermes Academy Continuing Education is independent of Hermes Fleet.

It runs on a normal Hermes Agent installation with Profile Packs. It must
not require Fleet, Keryx, Nodescale, Templar, RunAuthority, Run Capsules,
or any equivalent distributed-runtime system to exist, to be reachable, or
to be installed. If any such system is present, Continuing Education must
not depend on it.

### Current pre-release Hermes compatibility

The Phase 14 preflight proved three generic Hermes seams were needed. First, an
agent could use `message_agent` but could not programmatically establish the
same native standing goal that a human reaches through `/goal`; the generic
Bot-Chat-only `goal_manage` bridge now wraps the existing
`GoalManager`/`GoalContract` without adding Academy state or a second goal
loop. Second, skill-index routing was not deterministic enough for a
profile-defining workflow; generic profile distributions now support
`preload_skills`, which activates installed, non-disabled skills from that
profile before the first model turn without granting extra tools or authority.
Third, a failed goal-judge reason was persisted but not included in the next
continuation turn, so an agent could repeat the same insufficient completion
claim. Native continuation now includes the previous bounded `continue`
reason while keeping `wait` and `done` feedback out of later turns.

All three capabilities are merged in the maintained downstream Hermes Agent:
`goal_manage` in `Dadmin88/hermes-agent-downstream` PR #24 / merge
`9b8de86a80`, distribution `preload_skills` in PR #26 / merge `4c38d408f7`,
and bounded goal-judge feedback propagation in PR #27 / merge `406ea5c64e`.
Every Agency distribution declares `academy-continuing-education` as a preload.
Until equivalent support is present in the normal Hermes release used by a
Profile Packs install, Continuing Education remains pre-release and must not be
advertised as stock-install production ready. The hard invariant below remains
the release requirement: no special Academy runtime may be required.

## Actors (exhaustive)

Only these concepts exist. No other agent type, role, or persistence
primitive is introduced by this system.

- **Learner** — any installed Hermes profile receiving education.
- **Instructor** — an Academy profile teaching a bounded subject.
- **Dean** — `academy-dean`, used when the learner does not know which
  instructor it needs; routes to the most specific available faculty.
- **Continuing Education Session** — an ordinary Hermes conversation-based
  teaching interaction. It is NOT a new persistence primitive.
- **Learned Skill** — the normal Hermes skill produced or extended through
  `/learn` and persisted via `skill_manage`.

There is **no new Agent type**. The five actors above are the full set.

## Hard invariants

These are non-negotiable. They are the acceptance criteria for Phase 0 and
the constraints for every later phase.

1. **Zero Fleet dependency.** No import, runtime call, configuration
   reference, or behavioral coupling into any of: **Fleet, Keryx,
   Nodescale, Templar, RunAuthority, Run Capsules**. This prohibition is
   absolute and applies to skills, scripts, SOUL behavior, and any later
   implementation code.
2. **Works on a stock install.** Must function on a normal Hermes Agent
   installation with Profile Packs; no special runtime, daemon, service,
   or node is required.
3. **Natural-language UX.** Normal conversational language is the primary
   interface. The user must not need CLI commands, profile IDs, skill names,
   or syntax. `Dean` may resolve an instructor so the user never names one.
4. **Teachers never mutate learner internals.** An Instructor never
   directly edits the learner's skills, `SOUL.md`, or configuration. Teaching
   is content delivered through conversation.
5. **Durable learning is native.** Persistent improvement happens only
   through Hermes `/learn`; skill creation/update happens only through
   Hermes `skill_manage`. No custom persistence layer is built.
6. **Learner state stays in the learner.** Identity and state remain in the
   learner's normal Hermes profile. The instructor does not own or mirror it.
7. **Source packs are read-only to learning.** Profile Packs source
   distributions (`hermes-profile-packs/...`) are not modified merely because
   an installed profile learned something. Local learning is local.
8. **One explicit event.** Every training event has exactly one explicit
   learner, one teaching objective, and one instructor (or Dean-routed
   faculty member).
9. **No recursive training.** One class may not silently trigger another
   student → teacher → student chain. Further study requires an instructor
   recommendation plus a learner decision under an active goal, or a user
   instruction.
10. **No parallel infrastructure.** Do not create a candidate-skill database,
    skill registry, session store, scheduler, or orchestration runtime.
    Prefer an existing Hermes primitive over custom code every time. A
    parallel store is permitted only if upstream Hermes provably cannot
    represent something actually required — and that exception must be
    documented here first.
11. **Minimum sufficient instruction.** Continuing Education is a
    competency-transfer system, not a school simulation. Baseline before
    teaching; teach only demonstrated gaps; combine instructional functions
    into as few turns as practical; skip instruction when competency is
    already demonstrated; correct only what failed; require meaningfully
    different transfer evidence when instruction was needed; and stop as soon
    as the completion contract is satisfied. Do not impose fixed lesson
    lengths, modules, ceremonial quizzes, acknowledgement turns, or other
    classroom roleplay. Invoke `/learn` only when the event produced a
    reusable capability delta worth persisting. Phase-specific QA scripts may
    use fixed turn sequences to prove mechanics, but those sequences are test
    scaffolding and must not become the production teaching protocol.
12. **Learner skill preservation.** Before native `/learn`, record the learner's
    existing skill names. The persistence request may extend one relevant skill
    or create one new skill, but it must preserve unrelated learner skills.
    After `/learn`, verify every unrelated pre-existing skill still exists. Any
    unexplained loss, relocation, or overwrite fails the Continuing Education
    event closed; do not report successful learning until recovery is complete.

## Transport decision (selected)

The canonical one-to-one classroom transport is **canonical Bot Chat + native
`message_agent`**. Phase 2 proved sender validation/attribution, asynchronous
delivery, recipient wake-up, canonical history persistence/ordering, and a
multi-turn instructional exchange. Native Bot groups were also validated as a
useful optional group/classroom surface, but they are not the default CE
transport. No new message bus is built.

## Naming decisions (frozen)

These names are canonical and must be used consistently by later phases and
by the installer/distribution.

| Concept | Canonical name |
| --- | --- |
| Architecture contract (this file) | `docs/CONTINUING_EDUCATION_ARCHITECTURE.md` |
| Later user guide | `docs/CONTINUING_EDUCATION.md` |
| Canonical learner skill | `academy-continuing-education` |
| Canonical instructor skill | `teach-profile` |

The learner skill `academy-continuing-education` is conceptually Academy's
but is installed into participating learner profiles from one canonical
source. The instructor skill `teach-profile` is delivered to Academy
instructors alongside their subject-specific teaching skills.

## Relationship to the rest of the repository

- Continuing Education extends **Hermes Academy** (`academy-*`), whose
  faculty and teaching model are defined in `hermes-academy/ACADEMY.md`.
- It does not weaken, bypass, or relocate the invariants in the repository
  `AGENTS.md` or `hermes-agency/AGENTS.md`.
- The `agency-*`, `council-*`, and `academy-*` namespace boundaries and the
  "no live node registries / peer discovery / scheduling / remote-execution
  services" rules remain in force.

## Phase 0 acceptance (this document satisfies)

- A short architecture document exists describing the invariants above.
- It states, verbatim: _Hermes Academy Continuing Education is independent
  of Hermes Fleet._
- It explicitly prohibits imports/runtime calls to Fleet, Keryx,
  Nodescale, Templar, RunAuthority, and Run Capsules.

This contract is intentionally frozen. Later phases add behavior; they do
not add actors, remove invariants, or introduce coupling this document
forbids.
