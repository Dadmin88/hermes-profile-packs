# Catalog adaptation mapping

The Profile Packs source and the Hermes Bot Catalog are different distributions. A source fix reaches the catalog only after an explicit adaptation and review.

## Council first batch

Source baseline: `3821183d2b7d5af3cd18bc1c7c4da58ad9bb784e`.
Catalog base: `notwitcheer/hermes-agent-fork`, branch `bot-catalog-community-batch1`, commit `b10eeae1a8f0413760b05d928234e0c08eec3f32`, proposed in [Hermes #130283](https://github.com/NousResearch/hermes-agent/pull/130283).
Catalog foundation: [Hermes #119260](https://github.com/NousResearch/hermes-agent/pull/119260), observed open at `2c895d7534e280610cbb0cd78e0e1ff5c2256df0` on 2026-10-06.

| Source profile directory | Catalog YAML | Catalog workflow directory |
| --- | --- | --- |
| hermes-council/profiles/council-steward | bot-catalog/council-steward.yaml | optional-skills/bots/council-steward |
| hermes-council/profiles/council-life-coach | bot-catalog/council-life-coach.yaml | optional-skills/bots/council-life-coach |
| hermes-council/profiles/council-resilience-coach | bot-catalog/council-resilience-coach.yaml | optional-skills/bots/council-resilience-coach |
| hermes-council/profiles/council-time-attention-coach | bot-catalog/council-time-attention-coach.yaml | optional-skills/bots/council-time-attention-coach |

Each workflow consolidates its source profile's four manifest-owned skills into a catalog skill plus sample, rubric and template. Record versions from actual distributions; do not infer equivalence from matching names.

## Intentional differences

- Catalog source contains condensed SOUL content and consolidated workflows; it must preserve essential intent and authority boundaries.
- First-use synthetic samples can explicitly require an artifact. Ordinary chat allows listening or direct answers without mandatory files, actions or questions.
- Catalog bots are independently usable. Handoff names and a user-carried note do not imply installed sibling profiles or automatic dispatch.
- Catalog no-contact/no-buy/no-book/no-schedule rules stay in force. Suggested routines remain inactive until explicit setup and activation.
- Existing Profile Packs installation remains the source distribution path; this work does not introduce a second catalog runtime.

## Licensing

Profile Packs remains AGPL-3.0-only. Kyle's [grant on #130283](https://github.com/NousResearch/hermes-agent/pull/130283#issuecomment-5929526200) licenses `bot-catalog/council-*.yaml` and `optional-skills/bots/council-*/` **in that PR** under MIT. Preserve source attribution. Do not treat this as a blanket grant for unrelated paths, future Academy adaptations, or the source repository.

## Academy

No Academy catalog submission or selected roster was identified in this execution baseline. Source teaching improvements cover the existing 30 profiles. Catalog packaging and licensing require an actual proposed batch; do not invent an upstream commitment. Ordinary tutoring and optional profile-to-profile Continuing Education must be described separately. CE availability remains conditional on verified native capabilities.

## Verification record

Last verified target model/runtime, candidate revisions, live cases, versions and unresolved integration state are recorded in `QUALITY_ACCEPTANCE.md`. Source completion and upstream merge are separate claims.

### Candidate profile versions and included source skills

| Profile | Source version | Catalog version | Workflow version | Source skills consolidated |
| --- | --- | --- | --- | --- |
| council-steward | 0.1.1 | 1.0.1 | 0.1.1 | council-routing, whole-life-review, privacy-aware-handoff, decision-synthesis |
| council-life-coach | 0.1.1 | 1.0.1 | 0.1.1 | clarity-reflection, next-step-coaching, boundary-check, personal-experiments |
| council-resilience-coach | 0.1.1 | 1.0.1 | 0.1.1 | stress-debrief, regulation-plan, recovery-routine, coping-toolbox |
| council-time-attention-coach | 0.1.1 | 1.0.1 | 0.1.1 | weekly-time-plan, attention-audit, focus-session, calendar-boundaries |
