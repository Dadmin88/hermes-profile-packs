# Hermes Academy Continuing Education

Status: **Phase 14 controlled real-world preflight PASSED; Phase 15 production-profile validation is pending.** Do not describe Continuing Education as production-validated until the Phase 15 persistent-profile test and Phase 16 release/whole-change review pass.

Hermes Academy Continuing Education lets an installed Hermes profile learn a bounded reusable capability from Academy faculty without introducing a second agent runtime, scheduler, memory system, or skill database.

## What is implemented

The current merged flow uses normal Hermes primitives. Every Agency distribution declares `academy-continuing-education` in its `preload_skills`, so the full learner contract is active before the profile's first model turn instead of depending on probabilistic skill routing.

1. A learner receives a natural-language request such as `Go learn API security.`
2. If the user did not name a teacher, `academy-dean` routes to the most specific installed faculty member.
3. In canonical Bot Chat, the learner uses `goal_manage(action="set", ...)` to establish the current session's real native `/goal`/`GoalContract` state. `goal_manage` is only a thin bridge to Hermes' existing GoalManager; it is not an Academy scheduler or replacement loop.
4. One-to-one teaching uses canonical Bot Chat + native `message_agent`.
5. The instructor baselines the requested competency, teaches only demonstrated gaps, and requires meaningfully different transfer evidence when instruction was needed.
6. Native goal peer-wait parks while an instructor reply is outstanding instead of burning turns or sending duplicate requests.
7. The learner invokes native `/learn` only when the session produced a reusable capability delta.
8. Hermes' normal `skill_manage` path extends a relevant learner skill or creates a new learner-local skill.
9. The learner verifies the resulting skill and confirms unrelated pre-existing skills were preserved.

Native Bot groups are a validated optional group-learning surface, but they are not the default Continuing Education transport.

## Current Hermes compatibility

The Phase 14 preflight proved three generic Hermes seams. First, native goal **peer-wait** already worked once a goal existed, but a Bot lacked a safe way to establish that standing goal itself; the Bot-Chat-only `goal_manage` bridge now calls Hermes' existing `GoalManager` directly. Second, skill-index routing was not deterministic enough for a profile-defining workflow; downstream Hermes profile distributions now support `preload_skills`, and every Agency distribution preloads the CE learner contract before the first turn. Third, a failed goal-judge reason was persisted but not fed back into the next continuation, allowing repeated incomplete completion claims; native goal continuation now includes the previous bounded `continue` reason so the agent can correct the specific proof gap.

All three generic seams are merged in the maintained downstream Hermes Agent: `goal_manage` in PR #24 / merge `9b8de86a80`, profile-distribution `preload_skills` in PR #26 / merge `4c38d408f7`, and bounded goal-judge feedback propagation in PR #27 / merge `406ea5c64e`. `goal_manage` exposes only `set`, `status`, and `add_subgoal`; it cannot replace, pause, resume, clear, or target another session's goal. `preload_skills` activates only installed, non-disabled skills from the current profile and grants no additional tools or permissions. Judge feedback is bounded and only replayed for `continue`, never `wait`/`done`. Until equivalent support is present in the normal Hermes release used by Profile Packs, Continuing Education remains pre-release and must not be described as stock-install production ready.

## User experience

Users should not need to know about slash commands or Bot internals. Typical requests are ordinary language:

```text
Go learn API security.
Get better at database performance with Academy.
Study statistical experiment design.
Learn this from the Cybersecurity Instructor.
```

Normal status messages stay compact, for example:

```text
Learning API security with Cybersecurity Instructor.
Working on a gap in authorization-boundary reasoning.
Continuing education complete: transfer assessment passed; updated auth-boundary-review.
```

`School for Bots` is a useful informal description of the idea, not the runtime protocol. Production behavior is minimum-sufficient competency transfer, not classroom roleplay or fixed lesson lengths.

## Safety and authority boundaries

- Instructors teach and assess. They never directly edit learner skills, `SOUL.md`, configuration, permissions, memory, or unrelated state.
- The learner owns the `/learn` decision and the resulting skill write.
- `skills.write_approval` remains authoritative when enabled.
- Before `/learn`, the learner records its current skills. `/learn` may extend one relevant skill or create one new skill, but unrelated skills must remain present. Unexpected skill loss fails the CE event closed.
- Source Profile Packs are read-only during local learning. Learned behavior remains local to the learner unless a separate human-controlled contribution process upstreams it later.
- One class cannot silently launch another. Further study requires a user request or an explicit learner decision under the active goal.
- Existing Academy subject/safety boundaries remain in force.
- Continuing Education has zero runtime dependency on Fleet, Keryx, Nodescale, Templar, RunAuthority, or Run Capsules.

## Current validation evidence

The merged implementation has passed:

- canonical `message_agent` transport validation and real multi-turn teaching evidence;
- Phase 3 native goal peer-wait verification showing no additional wait scheduler/core loop was needed once a standing goal exists;
- Phase 14 proof that natural-language Bot learning needed a generic agent-to-GoalManager bridge, now provided by downstream Hermes `goal_manage`;
- live proof that probabilistic skill routing could bypass the CE contract, followed by generic profile-distribution `preload_skills` support and Agency-wide deterministic CE preloading;
- Phase 14 proof that failed native goal-judge reasons must reach the next continuation turn, followed by bounded generic feedback propagation in downstream Hermes PR #27;
- learner-only native skill-placement proof and source-pack/instructor isolation;
- shared-skill packaging and byte-identity validation;
- Dean routing tests, including ambiguous-keyword false-positive regressions;
- security/trust review with permanent adversarial tests;
- **165** selected native Hermes goal/subgoal, Bot Chat, profile-preload, `/learn`, skill-manager, write-approval, restart/resume, and canonical-session tests plus **2** direct async gateway goal-resume checks against a disposable Hermes home;
- repository, Agency, Council, and Academy validation with no Fleet dependency.

The accepted Phase 14 disposable-profile preflight used the natural request `Go learn API security from the Academy Cybersecurity Instructor.` It exercised deterministic CE preload, native `goal_manage`, `message_agent`, peer-wait, instructor assessment, transfer, native learner-local persistence, and fresh-session learned-skill reuse. Exactly one learner skill was added (`api-security-review`), all pre-existing learner skills were preserved, and the instructor/source-pack hashes were unchanged. A sealed held-out A/B check on the same model/runtime scored an untrained control **9/10** and the trained learner **10/10**; the trained fresh session naturally loaded `api-security-review`. Phase 15 must still validate the actual persistent learner before production-readiness claims.

## Source locations

- Learner skill: `hermes-academy/shared-skills/academy-continuing-education/SKILL.md`
- Instructor skill: `hermes-academy/shared-skills/teach-profile/SKILL.md`
- Dean routing: `hermes-academy/routing.py`
- Architecture contract: `docs/CONTINUING_EDUCATION_ARCHITECTURE.md`
- Academy manifest: `hermes-academy/academy.json`

The Academy installer materializes the canonical shared skills into their participating profile distributions; validators enforce byte identity so contributors edit the canonical source rather than divergent copies.
