# Hermes Profile Packs

Curated profile packs for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

This repository is the public upstream home for reusable Hermes profile distributions maintained as coherent teams rather than isolated prompts.

## Packs

| Pack | Namespace | Purpose |
| --- | --- | --- |
| **Hermes Agency** | `agency-*` | Professional specialists for engineering, product, design, QA, operations, marketing, content, and coordinated project work. |
| **Hermes Council** | `council-*` | Personal specialists for growth, health, fitness, parenting, relationships, communication, community, faith, finances, home stewardship, personal admin, career, learning, recreation, travel, nutrition, sleep, and preparedness. |

The packs deliberately separate professional execution from personal-life support. A work profile should not need private life context, and a personal profile should not inherit project or repository state merely because both run on Hermes.

Hermes Council currently contains 21 focused profiles and 84 purpose-built personal-life skills.

## Repository layout

```text
hermes-profile-packs/
├── hermes-agency/          # Professional profile pack
│   ├── agency.json
│   └── profiles/
├── hermes-council/         # Personal-life profile pack
│   ├── council.json
│   └── profiles/
├── docs/
├── packs.json
├── install.py
└── validate.py
```

Each distributable profile follows the Hermes profile-distribution shape:

```text
profiles/<namespace-name>/
├── distribution.yaml
├── SOUL.md
├── .no-bundled-skills      # when the profile is intentionally isolated
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

Runtime state is never distributed. Authentication material, `.env` files, logs, caches, databases, local paths, session history, and machine-specific configuration do not belong in this repository.

## Install

```bash
python install.py --list-packs
python install.py council --list
python install.py agency --list
python install.py council
python install.py council council-life-coach council-fitness-coach
```

`install.py` delegates to the selected pack's installer, which uses Hermes' native `hermes profile install` distribution flow.

## Validate

Run the full repository validation suite before publishing changes:

```bash
python validate.py
```

This validates both pack manifests, profile namespaces, distribution metadata, required profile files, skill frontmatter, portability, and common secret/path leaks. The imported Agency pack also retains its original validation and tests.

## Design principles

1. **Coherent teams, not prompt dumps.** Profiles have explicit ownership and clean handoffs.
2. **Namespace isolation.** `agency-*` is professional; `council-*` is personal.
3. **Portable distributions only.** No runtime state, secrets, personal filesystem paths, or local caches.
4. **Specialists remain specialists.** Profiles should hand off rather than silently absorbing unrelated domains.
5. **Human agency stays central.** Council profiles support decisions and capability; they do not attempt to run a person's life.
6. **Safety beats role-play.** Personal profiles do not manufacture medical, legal, financial, spiritual, parental, or other authority they do not possess.

See [`PACK_SPEC.md`](PACK_SPEC.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`SECURITY.md`](SECURITY.md) for repository standards.

## License

AGPL-3.0-only. See [`LICENSE`](LICENSE).
