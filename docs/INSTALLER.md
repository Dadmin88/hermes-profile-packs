# Profile Selector & Installer

The root `install.py` is the recommended entry point for discovering and installing Hermes Profile Packs. It understands both individual profiles and validated Team Recipes.

It has two surfaces backed by the same profile manifests and `recipes.json` registry:

- an interactive wizard for people;
- a deterministic non-interactive interface for agents and scripts.

No second profile roster exists. Recipe installation resolves stable profile identities and then uses the same pack installers as direct profile installation.

## Interactive wizard

Run:

```bash
python install.py
```

The wizard offers five useful paths plus exit:

1. **Recommend a small team for me** — describe the outcome. A clear Team Recipe is offered first when one is strongly and unambiguously matched; otherwise the wizard falls back to individual profiles.
2. **Browse team recipes** — choose a proven composition and then `minimal`, `recommended`, or `expanded`.
3. **Browse packs and categories** — choose a pack, category, and exact profiles.
4. **Search profiles directly** — search profile names, roles, jobs, and descriptions.
5. **Install everything** — explicitly install the complete catalog.

Nothing is installed until the final confirmation.

## Recipe-aware recommendation

Recipe promotion is intentionally conservative. The installer does not equate “highest score” with “correct team.” A recipe is promoted only when it clears both a minimum score and a minimum lead over the runner-up.

That means:

- `build and ship a web app` can cleanly map to the Software Delivery Team;
- `learn cybersecurity` can cleanly map to Cybersecurity Learning;
- a broad or mixed request may show only individual profile matches because no single recipe dominates strongly enough.

When a recipe is offered interactively, you can decline it and immediately continue with individual profile selection.

## Browse recipes from the root installer

```bash
python install.py --list-recipes
python install.py --list-recipes --json
python install.py --list-recipes --pack agency
```

Recipe tiers are nested:

- `minimal` — smallest coherent formation;
- `recommended` — default balance of expertise and independent review;
- `expanded` — broader coverage for larger or higher-risk work.

Preview or install a recipe directly:

```bash
python install.py --recipe software-delivery --tier minimal --dry-run
python install.py --recipe software-delivery --tier recommended --dry-run --json
python install.py --recipe software-delivery --tier recommended --yes
```

If `--tier` is omitted, `recommended` is used. `--recipe` cannot be combined with `--profiles`, `--category`, or `--all`.

## Existing pack commands still work

```bash
python install.py agency --list
python install.py council --list
python install.py academy --list
python install.py agency agency-backend-engineer agency-frontend-engineer
python install.py council --category growth
```

These commands delegate directly to the existing pack installers.

## Agent and script interface

Agents should not drive the interactive prompt. Discover the machine contract with:

```bash
python install.py --agent-help --json
```

Profile catalog:

```bash
python install.py --catalog --json
python install.py --catalog --pack council --json
```

Recipe catalog:

```bash
python install.py --list-recipes --json
```

Recommendation:

```bash
python install.py --recommend "build a web app" --json
python install.py --recommend "learn cybersecurity" --json
python install.py --recommend "improve my fitness and recovery" --json
```

For backward compatibility, `recommendations` remains the individual-profile result list. Recipe information is additive:

- `recipe_match` — the promoted recipe, or `null` when confidence is insufficient;
- `recipe_recommendations` — ranked recipe candidates;
- `recommendations` — the existing individual-profile candidates.

Recommendation mode is always read-only.

Exact profile dry-run/install:

```bash
python install.py \
  --profiles agency-backend-engineer agency-frontend-engineer \
  --dry-run --json

python install.py \
  --profiles agency-backend-engineer agency-frontend-engineer \
  --yes --json
```

Recipe dry-run/install:

```bash
python install.py \
  --recipe api-backend \
  --tier minimal \
  --dry-run --json

python install.py \
  --recipe api-backend \
  --tier minimal \
  --yes --json
```

Categories and full-pack selection still work:

```bash
python install.py --category council:growth --yes --json
python install.py --all --pack academy --yes --json
python install.py --all --yes --json
```

## Non-interactive safety rules

- `--catalog`, `--list-recipes`, and `--recommend` never install anything.
- `--dry-run` resolves the exact selection without changing Hermes.
- Non-interactive writes require `--yes`.
- `--json` never prompts.
- Unknown profiles, recipes, tiers, and invalid `PACK:CATEGORY` selectors fail closed.
- Explicit profile selections are deduplicated before installation.
- Recipe/profile/category/all selection modes are mutually exclusive where they would conflict.
- Installation continues to use each pack's existing native `hermes profile install` flow.

A safe agent pattern is:

1. inspect `--recommend --json`, `--list-recipes --json`, or `--catalog --json`;
2. choose an exact recipe/tier or profile set;
3. run `--dry-run --json`;
4. verify the returned exact plan;
5. repeat with `--yes --json`.

## Focused recipe CLI

`recipes.py` remains supported for callers who want a recipe-only surface:

```bash
python recipes.py --list
python recipes.py --recommend "build and ship a web app"
python recipes.py software-delivery --tier recommended --dry-run
```

Both entry points use the same shared recipe engine. `install.py` is the preferred general entry point; `recipes.py` is a focused convenience client.

## Recommendation implementation

Recommendations are local, deterministic, offline, and inspectable. Profile scoring uses names, categories, descriptions, roles, jobs, pack intent, and vocabulary expansion. Recipe scoring uses the same query vocabulary against recipe names, keywords, descriptions, and pack intent.

A recipe is advice, not authority. The user or calling agent still chooses the exact recipe/tier or profile selection to install.
