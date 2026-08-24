# Hermes Academy Continuing Education

Status: **Phase 16 whole-change/release review PASSED for the maintained downstream Hermes integration.** Continuing Education is production-validated on that integration path. Stock NousResearch Hermes compatibility remains pending until the normal Hermes release provides equivalent generic support for the required native seams.

Hermes Academy Continuing Education lets an installed Hermes profile learn a bounded reusable capability from Academy faculty using normal Hermes primitives. It introduces no second agent runtime, scheduler, memory system, skill database, or distributed-runtime dependency.

See [`CONTINUING_EDUCATION_RELEASE_REVIEW.md`](CONTINUING_EDUCATION_RELEASE_REVIEW.md) for the Phase 16 release decision, findings, corrections, and compatibility boundary.

## Actors

- **Learner** — any installed Hermes profile receiving education.
- **Instructor** — an Academy profile teaching a bounded subject.
- **Dean** — `academy-dean`, used when the learner does not know which instructor it needs; routes to the most specific safe installed faculty member.
- **Continuing Education Session** — an ordinary Hermes conversation-based teaching interaction. It is not a new persistence primitive.
- **Learned Skill** — the normal Hermes skill produced or extended through native `/learn` and persisted via `skill_manage`.

There is no new Agent type, transport bus, or runtime service.

## Natural-language user journey

Users should not need slash commands, profile IDs, skill names, or Bot internals. Typical requests are ordinary language:

```text
Go learn API security.
Get better at database performance with Academy.
Study statistical experiment design.
Learn this from the Cybersecurity Instructor.
```

### Typical flow

1. **Request** — The user makes a natural-language learning request to any installed profile participating in Continuing Education.
2. **Dean routing** — If the user did not name a teacher, the learner sends exactly one native `message_agent` request to `@academy-dean`, waits for the Dean reply, and uses the installed faculty profile explicitly named by that reply. The Dean prefers the most specific safe installed specialist. Same-category interdisciplinary requests may use that category's broad fallback; cross-category CE objectives fail closed and must be narrowed rather than being sent to an unrelated broad chair.
3. **Goal setup** — In canonical Bot Chat, the learner uses `goal_manage(action="set", ...)` to establish the session's real native `/goal`/`GoalContract` state. `goal_manage` is only a thin bridge to Hermes' existing `GoalManager`; it is not an Academy scheduler or replacement loop.
4. **Baseline** — The learner attempts a representative task or answer before instruction. If the baseline already demonstrates the competency strongly enough, the session stops with no skill write.
5. **Targeted instruction** — One-to-one teaching uses canonical Bot Chat + native `message_agent`. The instructor teaches only the demonstrated gaps.
6. **Assessment** — After instruction, the learner proves transfer on a meaningfully different problem. The selected instructor returns `MASTERED`, `NEEDS_CORRECTION`, or `BLOCKED`.
7. **Persistence** — If the instructor explicitly returns `MASTERED` for the learner's specific transfer, the learner may run native `/learn` through the normal Hermes `skill_manage` path. Otherwise, no durable skill write occurs.
8. **Verification** — The learner confirms the resulting skill and that unrelated pre-existing skills were preserved.

## Dean routing contract

The installed Dean's preloaded `faculty-routing` skill is the runtime routing contract. `hermes-academy/routing.py` is the repository's deterministic reference implementation and regression-test oracle; it is deliberately **not** a runtime dependency of an installed Dean profile.

Routing follows these rules:

- prefer the most specific installed specialist;
- when several strong specialties all belong to one Academy category, use that category's installed broad fallback and label the route approximate;
- never treat `academy-natural-sciences-professor` or any other broad faculty member as a universal fallback;
- when one CE objective strongly spans different Academy categories, return blocked and ask the learner to narrow the competency or choose an instructor;
- if a specialist is unavailable, use only an installed broad fallback from the same category;
- role-description fallback requires meaningful exact-word evidence and fails closed on an equally plausible tie;
- never claim a faculty profile is installed unless current Hermes Bot/profile context establishes its availability;
- return an exact, approximate, or blocked routing result so the learner does not have to reinterpret an ambiguous recommendation.

The manifest owns specialist preferences and category fallbacks; validation keeps that policy synchronized with the installed Dean skill.

## Transport and native behavior

The canonical one-to-one transport is **canonical Bot Chat + native `message_agent`**. Native goal peer-wait parks while an instructor reply is outstanding instead of burning turns or sending duplicate requests.

- `goal_manage` exposes only `set`, `status`, and `add_subgoal`; it cannot replace, pause, resume, clear, or target another session's goal.
- `preload_skills` activates only installed, non-disabled skills from the current profile and grants no additional tools or permissions.
- Judge feedback from native goal continuation is bounded and only replayed for `continue`, never for `wait` or `done`.

The generic Hermes seams required by the controlled preflight are merged in the maintained downstream Hermes Agent: `goal_manage` in PR #24, profile-distribution `preload_skills` in PR #26, and bounded goal-judge feedback propagation in PR #27. The downstream Bot Mode path also includes duplicate in-flight `message_agent` suppression. These are generic Hermes capabilities, not Academy-specific persistence or orchestration.

## Progress, cancellation, and write approval

- **Progress** — Keep status compact and user-facing. Examples:
  - Start: `Learning API security with Cybersecurity Instructor.`
  - Meaningful change: `The instructor found a gap in authorization-boundary reasoning. I'm working one more case.`
  - Completion: `Continuing education complete: transfer assessment passed; extended auth-boundary-review.`
- **Cancellation** — Normal Hermes messages may interrupt or change the active goal. Requests such as `Stop the class` or `Focus more on OAuth` are handled through native goal/preemption behavior.
- **Write approval** — `skills.write_approval` remains authoritative when enabled. Academy cannot bypass, auto-approve, or weaken it.

## Skill isolation and safety

- Instructors teach and assess. They never directly edit learner skills, `SOUL.md`, configuration, permissions, memory, or unrelated state.
- The learner owns the `/learn` decision and the resulting skill write.
- Before `/learn`, the learner records its current skills. `/learn` may extend one relevant skill or create one new skill, but unrelated skills must remain present. Unexpected skill loss fails the CE event closed.
- Source Profile Packs are read-only during local learning. Learned behavior remains local to the learner unless a separate human-controlled contribution process upstreams it later.
- One class cannot silently launch another. Further study requires a user request or an explicit learner decision under the active goal.

## Troubleshooting

**The Dean cannot establish a safe installed faculty match**
If the objective crosses categories, the apparent specialist is not installed, or current faculty availability cannot be established safely, stop blocked. Narrow the objective or let the user choose a known instructor. Do not substitute an unrelated broad chair.

**The instructor is unavailable**
If the selected instructor is unavailable and no safe alternative is resolved, stop blocked and report the instructor as unavailable. Let the user choose whether to retry or select an alternative.

**`goal_manage` is unavailable**
If `goal_manage` is unavailable in canonical Bot Chat, stop and report that Continuing Education requires the learner's canonical Bot Chat on a compatible Hermes build. Do not imitate `/goal` or continue as a one-shot lesson.

**Goal budget exhausted**
If the native goal budget is exhausted before the evidence contract is satisfied, pause and report: `Training paused because the learning objective has not yet been demonstrated.` Never convert budget exhaustion into success.

**`NEEDS_CORRECTION`**
Correct only the identified gap and obtain a new instructor judgment on the corrected transfer before persistence. Do not replay the whole lesson.

**`BLOCKED`**
Stop without persistence and surface the blocker. If the objective cannot be safely or reliably completed in the current session, report why and suggest a bounded retry if appropriate.

**Write-approval prompt**
If `skills.write_approval` is enabled, stop at the normal Hermes approval boundary and surface that approval request. Do not bypass approval because Academy initiated the learning.

## Validation evidence

The implementation has passed:

- canonical `message_agent` transport validation and real multi-turn teaching evidence;
- native goal peer-wait verification showing no Academy wait scheduler/core loop was required once a standing goal exists;
- the controlled proof that natural-language Bot learning required a generic agent-to-GoalManager bridge, now provided by downstream Hermes `goal_manage`;
- live proof that probabilistic skill routing could bypass the CE contract, followed by generic profile-distribution `preload_skills` support and Agency-wide deterministic CE preloading;
- proof that failed native goal-judge reasons must reach the next continuation turn, followed by bounded generic feedback propagation;
- learner-only native skill-placement proof and source-pack/instructor isolation;
- shared-skill packaging and byte-identity validation;
- Dean routing tests, including ambiguous-keyword, cross-category, missing-faculty, installed-profile, manifest-override, and tie regressions;
- security/trust review with permanent adversarial tests;
- selected native Hermes goal/subgoal, Bot Chat, profile-preload, `/learn`, skill-manager, write-approval, restart/resume, and canonical-session tests plus direct async gateway goal-resume checks against a disposable Hermes home;
- repository, Agency, Council, and Academy validation with no Fleet dependency.

The accepted controlled disposable-profile preflight used the natural request `Go learn API security from the Academy Cybersecurity Instructor.` It exercised deterministic CE preload, native `goal_manage`, `message_agent`, peer-wait, instructor assessment, transfer, native learner-local persistence, and fresh-session learned-skill reuse. Exactly one learner skill was added (`api-security-review`), all pre-existing learner skills were preserved, and the instructor/source-pack hashes were unchanged. A sealed held-out A/B check on the same model/runtime scored an untrained control **9/10** and the trained learner **10/10**; the trained fresh session naturally loaded `api-security-review`.

Phase 15 independent production verification then confirmed all 10 verification criteria: exact 90-skill union with only `auth-integration` changed, CE contract byte-identical to source, real Dean route, clean instructor baseline diagnostic/`NEEDS_CORRECTION`/`MASTERED` sequence, native goal DONE at 4/30, fresh session naturally skill-viewed `auth-integration` scoring 8/8, all Academy-owned instructor skills byte-identical to Profile Packs source, Profile Packs source tree unchanged, downstream Hermes PR #29 verified with 89/89 focused tests, and no distributed-runtime dependency. No secret leakage, no overbroad content, and no duplicate skills were found.

Phase 16 whole-change review found and corrected two release-level routing defects: unsafe universal broad-chair fallback and an installed-Dean documentation dependency on pack-root `routing.py`. The corrected release candidate adds manifest-owned category fallbacks, installed-profile-aware routing, fail-closed cross-category behavior, a self-contained installed Dean routing contract, and validator-enforced manifest/Dean parity. Its Profile Packs gate passed repository validation, **16/16** root tests, **19/19** Agency tests, **3/3** Council tests, and **199** Academy tests with one expected opt-in runtime skip.

## Compatibility and limitations

- Continuing Education is **production-validated on the maintained downstream Hermes integration**.
- Stock-install readiness remains pending until the normal NousResearch Hermes release provides equivalent generic support for the native CE seams. Do not remove this qualifier merely because the Profile Packs implementation review passed.
- Continuing Education is **independent of Hermes Fleet** and requires no Fleet/Keryx/Nodescale/Templar/RunAuthority/Run Capsules.
- Do not expose CLI, slash commands, or Bot internals as normal user UX.
- Do not describe unimplemented optional Desktop UI.
- Instructors teach within their subject and safety boundaries; they do not award grades, credentials, licenses, certifications, or professional authority.

## Maintainer notes

This document describes the released Profile Packs behavior through Phase 16. Preserve the normative architecture contract in `CONTINUING_EDUCATION_ARCHITECTURE.md` and the exact release disposition in `CONTINUING_EDUCATION_RELEASE_REVIEW.md`.

The runtime Dean contract lives in `../hermes-academy/profiles/academy-dean/skills/faculty-routing/SKILL.md`. The repository helper `../hermes-academy/routing.py` is a reference implementation/test oracle only.

## Links

- Architecture contract: [`CONTINUING_EDUCATION_ARCHITECTURE.md`](CONTINUING_EDUCATION_ARCHITECTURE.md)
- Phase 16 release review: [`CONTINUING_EDUCATION_RELEASE_REVIEW.md`](CONTINUING_EDUCATION_RELEASE_REVIEW.md)
- Academy overview: [`../hermes-academy/README.md`](../hermes-academy/README.md)
- Teaching contract: [`../hermes-academy/ACADEMY.md`](../hermes-academy/ACADEMY.md)
- Operating playbook: [`OPERATING_PLAYBOOK.md`](OPERATING_PLAYBOOK.md)
- Troubleshooting: [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)
- Installer: [`INSTALLER.md`](INSTALLER.md)
- Root README: [`../README.md`](../README.md)

## Source locations

- Learner skill: `hermes-academy/shared-skills/academy-continuing-education/SKILL.md`
- Instructor skill: `hermes-academy/shared-skills/teach-profile/SKILL.md`
- Installed Dean routing contract: `hermes-academy/profiles/academy-dean/skills/faculty-routing/SKILL.md`
- Repository routing reference/tests: `hermes-academy/routing.py`
- Architecture contract: `docs/CONTINUING_EDUCATION_ARCHITECTURE.md`
- Phase 16 release review: `docs/CONTINUING_EDUCATION_RELEASE_REVIEW.md`
- Academy manifest: `hermes-academy/academy.json`

The Academy installer materializes the canonical shared skills into their participating profile distributions; validators enforce byte identity so contributors edit the canonical source rather than divergent copies.