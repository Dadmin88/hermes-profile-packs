# AGENTS.md

## Repository purpose

This repository contains public, portable Hermes Agent profile packs. Treat profile names, pack manifests, installer behavior, distribution layout, shared-skill sources, and Academy routing policy as user-facing API.

## Required invariants

- `agency-*` belongs only under `hermes-agency/profiles/`.
- `council-*` belongs only under `hermes-council/profiles/`.
- `academy-*` belongs only under `hermes-academy/profiles/`.
- Never copy a live Hermes profile directory wholesale into the repository.
- Never commit auth files, `.env`, state databases, caches, logs, session dumps, PIDs, local mount paths, or personal home paths.
- `distribution.yaml` names must match their directory names.
- Manifest `jobs` must match the profile-specific skill directories for Council profiles.
- Preserve unrelated work.

## Continuing Education invariants

Hermes Academy Continuing Education must not depend on a separate distributed runtime, scheduler, message bus, node-management service, or parallel persistence layer. Keep the education flow within the standard Hermes capabilities documented by this repository.

The canonical shared skills are:

- `hermes-academy/shared-skills/academy-continuing-education/SKILL.md`
- `hermes-academy/shared-skills/teach-profile/SKILL.md`

Edit those canonical sources rather than hand-editing materialized copies. Validators enforce byte identity across participating learner/faculty distributions.

Academy routing policy has two synchronized forms:

- `hermes-academy/academy.json` owns specialist preferences and category fallbacks;
- `academy-dean`'s preloaded `faculty-routing` skill owns the installed runtime contract.

`hermes-academy/routing.py` is a repository reference implementation and test oracle only. Never make an installed Dean depend on that pack-root file being present after profile installation.

Continuing Education routing must fail closed:

- prefer the most specific installed specialist;
- use a broad fallback only within the specialist's own category;
- cross-category CE objectives must be narrowed instead of being assigned to an unrelated broad chair;
- uninstalled or unverified faculty must not be reported as installed;
- ambiguous role-description ties must not be broken by roster or iteration order.

Public status language must state the Hermes capabilities required by Continuing Education and distinguish implemented pack behavior from compatibility with a given Hermes release. Do not claim unqualified production readiness until the normal Hermes release used with Profile Packs provides those capabilities.

## Native personality standard

Curated personalities are authored under `personalities/<profile-name>.json`
and materialized into native `config.yaml` by `capabilities.py`. Only
`description`, `system_prompt`, `tone`, and `style` are accepted. Preserve
SOUL.md authority and existing disabled MCP seed settings; do not treat
`AGENTS.md`, `USER.md`, `MEMORY.md`, or OpenClaw-style Markdown files as
additional automatically loaded identity layers. Every profile must have a distinct native personality source. Existing installed
config must not be replaced by a distribution update without consent.
See `docs/PROFILE_PERSONALITIES.md` for the pilot, evaluation, and release gates.

## Editing profiles

Prefer extending an existing specialist with a focused skill when ownership already exists. Add a new profile only when it has a distinct, durable responsibility.

Council profiles should use minimum-necessary personal context and hand off to specialists rather than accumulating every personal domain into one persona.

Agency profiles imported from the standalone pack should remain compatible with that distribution unless a deliberate migration is being performed.

## Existing installations and local changes

An installed Hermes distribution may have locally improved `SOUL.md` or
skill files. Native `hermes profile update` preserves local `config.yaml`
but can replace those files, so **do not run it blindly** on previously
customized profiles.

Use `scripts/reviewed_profile_sync.py` for an initial read-only
comparison against the exact source recorded in the installed
`distribution.yaml`. Review named SOUL or skill packages individually.
Apply only with an exact `--approve-plan` hash, private backup and
rollback path. The selective sync does not change an installed profile's
distribution version, config, gateway state or extra local skills.
See `docs/REVIEWED_PROFILE_SYNC.md`. Profiles with missing manifests need a
separate provenance/adoption decision, not a forced update.

## Validation

Before committing or pushing:

```bash
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
python -m unittest discover -s hermes-agency/tests -p 'test_*.py'
python -m unittest discover -s hermes-council/tests -p 'test_*.py'
python -m unittest discover -s hermes-academy/tests -p 'test_*.py'
```

Do not weaken a validator merely to make a failing artifact pass. Determine whether the finding is a real portability/security problem or an overly broad rule, then fix the correct layer.

For Continuing Education changes, keep the public guide, architecture contract, Academy teaching contract, Academy README, root README, and changelog truthful about the same compatibility boundary.