# Team Recipes

Team Recipes are validated, portable compositions of existing Hermes Profile Packs profiles. They answer: **which small set should I install for this kind of outcome?**

A recipe does not create a new agent type, scheduler, room, board, memory store, or runtime. It resolves stable profile identities and delegates installation to the existing Profile Packs/Hermes distribution path.

## Recommended entry point

The root installer now understands recipes directly:

```bash
python install.py --list-recipes
python install.py --recommend "build and ship a web app"
python install.py --recipe software-delivery --tier minimal --dry-run
python install.py --recipe software-delivery --tier recommended --yes
```

The interactive wizard (`python install.py`) can also recommend a recipe, browse recipes, choose a tier, and show the exact final install plan.

## Confidence-aware promotion

The installer promotes a Team Recipe only when the match is both strong and unambiguous. A top-scoring recipe that is weak or nearly tied with another recipe is not presented as canonical.

This matters because recipes represent opinionated team formations. Ambiguity should fall back to individual profile discovery rather than forcing the user's goal into the wrong template.

`--recommend --json` exposes:

- `recipe_match`: one clear promoted recipe or `null`;
- `recipe_recommendations`: ranked recipe candidates;
- `recommendations`: individual profile candidates.

## Tiers

Every recipe has three nested tiers:

- **minimal**: smallest coherent set that can perform the core workflow;
- **recommended**: default balance of expertise, review, and coordination;
- **expanded**: additional distinct specialties for larger or higher-risk work.

Bigger is not automatically better. Use the smallest tier that adds real expertise, independent verification, or useful parallelism.

## Inspect before installing

```bash
python install.py --recipe software-delivery --tier minimal --dry-run
python install.py --recipe security-review --tier recommended --dry-run --json
```

Without `--yes`, the selection is read-only. The plan shows exact profile names, source-payload estimates, workflow guidance, success criteria, and optional runtime ideas.

## Focused recipe client

`recipes.py` remains available:

```bash
python recipes.py --list
python recipes.py --recommend "learn cybersecurity" --json
python recipes.py personal-reset --tier minimal --dry-run
```

It uses the same shared recipe engine as `install.py`; it does not maintain independent scoring or a second profile roster.

## Initial catalog

### Hermes Agency

- `software-delivery` — cross-functional software planning, implementation, review, QA, source control, and release.
- `api-backend` — APIs, services, persistence, security, performance, and backend quality.
- `security-review` — security review, threat modeling, privacy/compliance, QA, and authorized adversarial testing.
- `open-source-maintenance` — repository maintenance, review, QA, release hygiene, docs, and community-facing work.
- `product-launch` — product intent, launch sequencing, positioning, content, channels, analytics, and customer follow-through.
- `game-development` — game design, Godot implementation, levels/worlds, creative production, QA, and release.
- `research-analysis` — research, market/competitive evidence, data/business analysis, and decision-ready synthesis.

### Hermes Council

- `personal-reset` — clarity, resilience, attention, routines, and practical stabilization.
- `family-support` — parenting, communication, relationships, and household systems with privacy-aware routing.
- `fitness-recovery` — training, nutrition, sleep, recovery, and health-care navigation boundaries.

### Hermes Academy

- `technical-study` — computer science, systems, quantitative foundations, research methods, and adjacent faculty.
- `cybersecurity-learning` — defensive cybersecurity with prerequisite-aware computer science and systems teaching.

## Runtime boundary

Recipes may suggest useful routines, but never register them. They do not distribute memory, sessions, learned skills, group membership, Kanban state, credentials, or machine-specific configuration.

See `docs/OPERATING_PLAYBOOK.md` for how to run a selected team and `docs/INSTALLATION_VERIFICATION.md` for post-install checks.
