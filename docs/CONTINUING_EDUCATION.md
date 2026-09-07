# Hermes Academy Continuing Education

Status: Continuing Education requires a compatible Hermes build. Compatibility with the standard Hermes release is not yet guaranteed; verify the required capabilities below before use.

Hermes Academy Continuing Education lets an installed Hermes profile learn a bounded reusable capability from Academy faculty using normal Hermes primitives. It introduces no second agent runtime, scheduler, memory system, skill database, or distributed-runtime dependency.

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

The flow requires these generic Hermes capabilities: `goal_manage`, profile-distribution `preload_skills`, bounded goal-judge feedback propagation, duplicate in-flight `message_agent` suppression, and the associated Bot Chat behavior. These are generic Hermes capabilities, not Academy-specific persistence or orchestration.

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

## Compatibility and limitations

- Confirm that your Hermes build provides the generic capabilities listed under “Transport and native behavior.” Compatibility with the standard Hermes release is not yet guaranteed.
- Continuing Education requires no separate training or distributed runtime.
- Do not expose CLI, slash commands, or Bot internals as normal user UX.
- Do not describe unimplemented optional Desktop UI.
- Instructors teach within their subject and safety boundaries; they do not award grades, credentials, licenses, certifications, or professional authority.

## Maintainer notes

Preserve the normative architecture contract in `CONTINUING_EDUCATION_ARCHITECTURE.md` when changing this guide.

The runtime Dean contract lives in `../hermes-academy/profiles/academy-dean/skills/faculty-routing/SKILL.md`. The repository helper `../hermes-academy/routing.py` is a reference implementation/test oracle only.

## Links

- Architecture contract: [`CONTINUING_EDUCATION_ARCHITECTURE.md`](CONTINUING_EDUCATION_ARCHITECTURE.md)
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
- Academy manifest: `hermes-academy/academy.json`

The Academy installer materializes the canonical shared skills into their participating profile distributions; validators enforce byte identity so contributors edit the canonical source rather than divergent copies.