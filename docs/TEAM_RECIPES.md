# Team Recipes

Team recipes are validated, portable compositions of existing Hermes Profile Packs profiles. They answer a practical question: **which small set should I install for this kind of outcome?**

A recipe does not create a new agent type, scheduler, room, board, memory store, or runtime. It resolves stable profile identities and delegates installation to the existing Profile Packs installer.

## Browse and recommend

```bash
python recipes.py --list
python recipes.py --list --json
python recipes.py --recommend "build and ship a web app"
python recipes.py --recommend "learn cybersecurity" --json
```

## Tiers

Every recipe has three nested tiers:

- **minimal**: the smallest coherent set that can perform the core workflow;
- **recommended**: the default balance of expertise, review, and coordination;
- **expanded**: additional distinct specialties for larger or higher-risk work.

Bigger is not automatically better. Use the smallest tier that adds real expertise or independent verification.

## Inspect before installing

```bash
python recipes.py software-delivery --tier minimal
python recipes.py software-delivery --tier recommended --dry-run
python recipes.py security-review --tier recommended --dry-run --json
```

Without `--yes`, recipe selection is read-only. The plan shows exact profile names, source-payload estimates, workflow guidance, success criteria, and optional runtime ideas.

## Install

```bash
python recipes.py software-delivery --tier recommended --yes
python recipes.py api-backend --tier minimal --yes
python recipes.py personal-reset --tier minimal --yes
python recipes.py cybersecurity-learning --tier recommended --yes
```

Installation reuses the root installer and each pack's normal `hermes profile install` path. Recipe tooling does not maintain a second profile catalog.

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
