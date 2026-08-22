# AGENTS.md

## Repository purpose

This repository contains public, portable Hermes Agent profile packs. Treat profile names, pack manifests, installer behavior, and distribution layout as user-facing API.

## Required invariants

- `agency-*` belongs only under `hermes-agency/profiles/`.
- `council-*` belongs only under `hermes-council/profiles/`.
- `academy-*` belongs only under `hermes-academy/profiles/`.
- Never copy a live Hermes profile directory wholesale into the repository.
- Never commit auth files, `.env`, state databases, caches, logs, session dumps, PIDs, local mount paths, or personal home paths.
- `distribution.yaml` names must match their directory names.
- Manifest `jobs` must match the profile-specific skill directories for Council profiles.
- Preserve unrelated work.

## Editing profiles

Prefer extending an existing specialist with a focused skill when ownership already exists. Add a new profile only when it has a distinct, durable responsibility.

Council profiles should use minimum-necessary personal context and hand off to specialists rather than accumulating every personal domain into one persona.

Agency profiles imported from the standalone pack should remain compatible with that distribution unless a deliberate migration is being performed.

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
