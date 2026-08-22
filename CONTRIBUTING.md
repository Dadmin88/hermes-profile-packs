# Contributing

Contributions should improve a profile pack as a coherent system, not merely add another persona.

## Before opening a change

- Choose the correct pack and namespace.
- Confirm the proposed profile owns a distinct, durable responsibility.
- Prefer adding a focused skill to an existing profile when a new persona would create overlapping ownership.
- Keep all artifacts portable and free of runtime state or secrets.

## Profile changes

A new profile requires:

1. A manifest entry with role and jobs.
2. `distribution.yaml`.
3. `SOUL.md`.
4. At least one profile-specific skill.
5. Documentation updates when the public roster changes.
6. A clean `python validate.py` run.

Keep guidance concrete. Avoid generic motivational prose, fake expertise, and instructions that encourage a profile to exceed its domain.

## Commit hygiene

Use focused commits, preserve unrelated work, and never include generated runtime directories. Run validation before pushing.
