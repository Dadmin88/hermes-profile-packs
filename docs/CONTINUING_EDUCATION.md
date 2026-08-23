# Hermes Academy Continuing Education

Status: **implemented through the Phase 10–13 quality gate; controlled real-world preflight is still in progress.** Do not describe Continuing Education as production-validated until the Phase 14/15 capability tests pass.

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

The Phase 14 v3 preflight proved two generic seams. First, native goal **peer-wait** already worked once a goal existed, but a Bot lacked a safe way to establish that standing goal itself; the Bot-Chat-only `goal_manage` bridge now calls Hermes' existing `GoalManager` directly. Second, skill-index routing was not deterministic enough for a profile-defining workflow; downstream Hermes profile distributions now support `preload_skills`, and every Agency distribution preloads the CE learner contract before the first turn.

Both generic seams are merged in the maintained downstream Hermes Agent: `goal_manage` in PR #24 / merge `9b8de86a80`, and profile-distribution `preload_skills` in PR #26 / merge `4c38d408f7`. `goal_manage` exposes only `set`, `status`, and `add_subgoal`; it cannot replace, pause, resume, clear, or target another session's goal. `preload_skills` activates only installed, non-disabled skills from the current profile and grants no additional tools or permissions. Until equivalent support is present in the normal Hermes release used by Profile Packs, Continuing Education remains pre-release and must not be described as stock-install production ready.

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

Before the controlled real-world preflight, the merged implementation has already passed:

- canonical `message_agent` transport validation and real multi-turn teaching evidence;
- Phase 3 native goal peer-wait verification showing no additional wait scheduler/core loop was needed once a standing goal exists;
- Phase 14 v3 proof that natural-language Bot learning needed a generic agent-to-GoalManager bridge, now provided by downstream Hermes `goal_manage`;
- live proof that probabilistic skill routing could bypass the CE contract, followed by generic profile-distribution `preload_skills` support and Agency-wide deterministic CE preloading;
- learner-only native skill-placement proof;
- shared-skill packaging and byte-identity validation;
- Dean routing tests, including ambiguous-keyword false-positive regressions;
- security/trust review with permanent adversarial tests;
- native Hermes goal/subgoal, Bot Chat, `/learn`, skill-manager, write-approval, restart/resume, and canonical-session tests against a disposable Hermes home;
- repository, Agency, Council, and Academy validation with no Fleet dependency.

The Phase 14 controlled preflight must still prove persistent capability improvement in a fresh learner session. An earlier Phase 14 attempt is not accepted because it used an outdated learner distribution that did not contain the CE learner skill and bypassed the complete merged flow.

## Source locations

- Learner skill: `hermes-academy/shared-skills/academy-continuing-education/SKILL.md`
- Instructor skill: `hermes-academy/shared-skills/teach-profile/SKILL.md`
- Dean routing: `hermes-academy/routing.py`
- Architecture contract: `docs/CONTINUING_EDUCATION_ARCHITECTURE.md`
- Academy manifest: `hermes-academy/academy.json`

The Academy installer materializes the canonical shared skills into their participating profile distributions; validators enforce byte identity so contributors edit the canonical source rather than divergent copies.
