# Hermes Academy Continuing Education — Architecture Contract

Status: Phase 0 (frozen). This document is the normative, short architecture
contract for Hermes Academy Continuing Education. It freezes the actors,
hard invariants, and naming decisions so later phases (1–16 of the master
plan) cannot quietly balloon into a new framework. Later phases implement
against this contract; they do not amend it except through an explicit,
documented change to this file.

## Scope independence

Hermes Academy Continuing Education is independent of Hermes Fleet.

It runs on a normal Hermes Agent installation with Profile Packs. It must
not require Fleet, Keryx, Nodescale, Templar, RunAuthority, Run Capsules,
or any equivalent distributed-runtime system to exist, to be reachable, or
to be installed. If any such system is present, Continuing Education must
not depend on it.

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

## Transport decision (deferred)

The classroom transport must be a **native Bot Mode** conversation
mechanism. The specific choice — canonical Bot Chat + `message_agent`
(Preferred A) versus a native Bot Mode group classroom (Alternative B) —
is selected by the later Phase 2 experiments. This contract only requires
that the mechanism be native Hermes Bot Mode; no new message bus is built.

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
