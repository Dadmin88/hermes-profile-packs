# Recipe-Aware Root Installer Plan

Status: implementation target for `feat/recipe-aware-installer`.

## Goal

Make the root `install.py` the canonical discovery surface for both individual profiles and validated Team Recipes, without collapsing the two concepts or breaking existing agent/script consumers.

The installer should answer a plain-language goal in two stages:

1. Does this map strongly and unambiguously to a known recipe?
2. Regardless of recipe fit, which individual profiles match the goal?

A recipe is promoted only when it clears a deterministic confidence gate. Ambiguous goals fall back to the existing profile-level recommendation experience.

## Invariants

- `recipes.json` remains the canonical recipe registry.
- Pack manifests remain the canonical profile rosters.
- No duplicate profile catalog is introduced.
- Recipe scoring has one implementation shared by `install.py` and `recipes.py`.
- `--recommend` remains read-only.
- Existing JSON key `recommendations` remains the individual-profile list for backward compatibility.
- Recipe information is additive through `recipe_match` and `recipe_recommendations`.
- Installation still delegates to existing pack installers and Hermes-native `hermes profile install`.
- Recipe selection never creates runtime memory, cron, groups, Kanban state, credentials, model config, or Fleet state.
- Legacy pack-first commands remain supported.

## Phase 1: Extract shared recipe engine

Create `recipe_catalog.py` as the dependency-neutral recipe core.

It owns:

- `Recipe` and `RecipeError`;
- registry loading;
- tier constants;
- profile resolution by recipe/tier;
- recipe scoring;
- recipe ranking;
- confidence policy.

It does not import `install.py`. Callers supply the existing profile-query expansion/tokenization and pack-intent maps, avoiding a circular import while retaining one recipe scoring implementation.

Acceptance:

- `recipes.py` and `install.py` both call the same scoring and confidence code.
- Existing recipe CLI behavior remains available.

## Phase 2: Define a conservative confidence gate

A recipe should not be promoted merely because it has the highest score.

Default gate:

- top score must be at least 24;
- top recipe must beat the second recipe by at least 8 points.

This intentionally prefers a false negative over a false positive. If several recipes are plausible, the installer should show profile-level matches rather than pretending one formation is canonical.

Acceptance:

- `build and ship a web app` promotes `software-delivery`.
- `learn cybersecurity` promotes `cybersecurity-learning`.
- low-score or closely tied synthetic rankings do not produce a confident recipe match.

## Phase 3: Upgrade interactive recommendation

Change wizard option 1 from profile-only matching to recipe-aware matching.

Flow:

1. user describes the goal;
2. score recipes and profiles independently;
3. if one recipe clears the confidence gate, show it first with explanation;
4. user may accept or decline;
5. if accepted, choose `minimal`, `recommended`, or `expanded`;
6. show exact profiles;
7. continue to the existing final install confirmation;
8. if declined or no recipe is confident, show individual profile matches exactly as before.

The wizard must never silently choose a tier or install a recipe.

## Phase 4: Add direct recipe browsing to the wizard

Add a dedicated `Browse team recipes` path.

The main menu becomes:

1. Recommend a small team for me
2. Browse team recipes
3. Browse packs and categories
4. Search profiles directly
5. Install everything
6. Exit

Recipe browsing shows pack, purpose, and tier sizes. The user chooses one recipe and one tier before the normal install confirmation.

## Phase 5: Add recipe selection to the root CLI

Add:

```bash
python install.py --list-recipes
python install.py --list-recipes --json
python install.py --recipe software-delivery --tier minimal --dry-run
python install.py --recipe software-delivery --tier recommended --yes --json
```

Rules:

- `--recipe` is mutually exclusive with `--profiles`, `--category`, and `--all`;
- `--tier` requires `--recipe`;
- omitted tier defaults to `recommended`;
- `--pack` may filter recipe discovery and must reject a recipe outside the requested pack;
- dry-run uses the same exact plan/stats machinery as profile selection;
- non-interactive writes still require `--yes`.

## Phase 6: Preserve agent/script compatibility

Existing profile recommendation JSON remains:

```json
{
  "recommendations": [ ...profile results... ]
}
```

Additive fields:

```json
{
  "recipe_match": { ... } | null,
  "recipe_recommendations": [ ... ]
}
```

`recipe_match` exists only when the confidence gate passes.

Update `--agent-help --json` with recipe discovery, dry-run, and install examples.

## Phase 7: Keep the focused recipe CLI

`recipes.py` remains supported as a recipe-first convenience surface.

It should become a thin client over `recipe_catalog.py` plus the root installer's profile/install primitives. This keeps existing documentation and scripts working while making `install.py` the preferred all-purpose entry point.

## Phase 8: Tests

Add deterministic coverage for:

- shared registry loading;
- tier monotonicity and same-pack resolution;
- strong recipe recommendation;
- confidence minimum score;
- confidence minimum margin;
- root `recommend_goal` promoting a clear recipe while still returning profile matches;
- root `--recommend --json` preserving `recommendations` and adding recipe fields;
- root `--recipe ... --dry-run --json` exact resolution;
- standalone `recipes.py` dry-run regression.

Existing installer, Agency, Council, and Academy suites remain part of the gate.

## Phase 9: Documentation

Update:

- root README;
- `docs/INSTALLER.md`;
- `docs/TEAM_RECIPES.md`;
- changelog.

Document the confidence behavior explicitly so users understand that “no recipe promoted” means “no single recipe was sufficiently unambiguous,” not “recipes are unavailable.”

## Release gate

Required exact-head CI:

```bash
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
python -m unittest discover -s hermes-agency/tests -p 'test_*.py'
python -m unittest discover -s hermes-council/tests -p 'test_*.py'
python -m unittest discover -s hermes-academy/tests -p 'test_*.py'
```

Merge only after the pull-request head passes the full gate.
