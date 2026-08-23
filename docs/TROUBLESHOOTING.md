# Troubleshooting

## `recipes.py` says a recipe is unknown

Run:

```bash
python recipes.py --list
```

Recipe IDs are stable lowercase kebab-case names such as `software-delivery` and `personal-reset`.

## A recipe recommendation is not what I want

Recommendations are local deterministic matching, not an LLM judgment. Rephrase the outcome with concrete domain words, inspect several candidates, or choose a recipe directly.

The recommendation is advice. You remain the selector.

## The recipe seems too large

Use `--tier minimal` and inspect the plan. Expanded tiers are not better by default.

```bash
python recipes.py software-delivery --tier minimal --dry-run
```

## The recipe is missing a specialist I need

First confirm that the specialist owns a genuinely distinct decision, review, or work package. You can install an additional profile through the existing root installer without changing the recipe.

A recurring gap across many real uses is evidence for proposing a recipe change.

## Installation fails because Hermes is unavailable

Pack installation requires the `hermes` executable on `PATH`. The repository cannot repair a missing Hermes installation or provider configuration. Fix the Hermes environment, then re-run the same dry-run/installation selection.

## A profile installed but behaves generically

Open a fresh session and verify you are actually using the intended installed profile/alias. Compare its role and boundaries with the source `SOUL.md`. If the wrong identity loads, treat that as a Hermes/profile-selection problem rather than rewriting the SOUL to mask it.

## A bundled skill appears missing

Confirm the profile distribution itself contains the expected `skills/<name>/SKILL.md` and that installation completed successfully. Do not copy live runtime skill state back into the repository as a workaround.

## Too many agents are talking

Reduce the coordination pattern. Route the outcome to one owner, add a reviewer only if needed, and use a larger team only when work has clean independently verifiable seams.

See `docs/OPERATING_PLAYBOOK.md`.

## The group chat made a decision but nobody owns it

Conversation is not the durable commitment layer. Create/update the corresponding Kanban task or other operator-selected system of record with owner, outcome, dependencies, and acceptance criteria.

## I want recurring team routines

Recipes may suggest routines, but installation never creates cron jobs automatically. Configure a Hermes routine explicitly only after deciding its owner, useful output, cadence, and escalation behavior.

## My local profile learned something. Should I commit it here?

Not automatically. Local memory and learned skills belong to the installed profile. Public Profile Packs source remains deterministic. Upstreaming a learned procedure is a separate human-reviewed contribution.

## Validation fails on `recipes.json`

The validator enforces:

- valid unique recipe IDs;
- known owning pack;
- existing profile references;
- no cross-pack references inside a recipe;
- non-empty workflow/success criteria;
- minimal subset of recommended subset of expanded.

Fix the recipe data rather than weakening validation.
