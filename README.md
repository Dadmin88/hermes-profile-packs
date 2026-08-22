# Hermes Profile Packs

Curated profile packs for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

This repository is the public upstream home for reusable Hermes profile distributions maintained as coherent teams rather than isolated prompts.

## Packs

| Pack | Namespace | Purpose |
| --- | --- | --- |
| **Hermes Agency** | `agency-*` | Professional specialists for engineering, product, design, QA, operations, marketing, content, and coordinated project work. |
| **Hermes Council** | `council-*` | Personal specialists for growth, health, fitness, parenting, relationships, communication, community, faith, finances, home stewardship, personal admin, career, learning, recreation, travel, nutrition, sleep, and preparedness. |
| **Hermes Academy** | `academy-*` | Professors and instructors for academic, technical, vocational, and professional learning. |

The packs deliberately separate durable context domains. Agency executes professional work, Council supports the person, and Academy teaches. A work profile should not need private life context, a personal profile should not inherit repository state merely because both run on Hermes, and a teaching profile should not silently become a production executor.

Hermes Council currently contains 21 focused profiles and 84 purpose-built personal-life skills. Hermes Academy v0.2 contains 30 faculty profiles and 120 purpose-built teaching skills.

## Repository layout

```text
hermes-profile-packs/
├── hermes-agency/          # Professional profile pack
│   ├── agency.json
│   └── profiles/
├── hermes-council/         # Personal-life profile pack
│   ├── council.json
│   └── profiles/
├── hermes-academy/         # Education profile pack
│   ├── academy.json
│   └── profiles/
├── docs/
├── tests/                  # Root installer/selector tests
├── packs.json
├── install.py              # Human wizard + agent-friendly selector
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

For most people, just launch the selector:

```bash
python install.py
```

The wizard can recommend a small set from a plain-language goal, let you browse packs/categories, search exact profiles, or explicitly install everything. It shows the exact plan before changing Hermes and is designed to avoid installing profiles you do not need.

The existing pack-first commands are still supported:

```bash
python install.py --list-packs
python install.py council --list
python install.py agency --list
python install.py academy --list
python install.py council council-life-coach council-fitness-coach
python install.py academy academy-cybersecurity-instructor academy-physics-professor
```

For agents and scripts, the same selector exposes a deterministic JSON interface:

```bash
python install.py --agent-help --json
python install.py --catalog --json
python install.py --recommend "build a web app" --json
python install.py --profiles agency-backend-engineer agency-frontend-engineer --dry-run --json
python install.py --profiles agency-backend-engineer agency-frontend-engineer --yes --json
python install.py --all --yes --json
```

`--catalog` and `--recommend` are read-only. Non-interactive installation requires `--yes`, and `--dry-run` resolves the exact plan first. Installation still delegates to each pack's native `hermes profile install` flow.

See [`docs/INSTALLER.md`](docs/INSTALLER.md) for the full wizard and agent contract.

## Validate

Run the full repository validation suite before publishing changes:

```bash
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
```

This validates all registered pack manifests, profile namespaces, distribution metadata, required profile files, skill frontmatter, portability, common secret/path leaks, and the root installer/selector behavior. Pack-specific validators and tests enforce additional contracts.

## Design principles

1. **Coherent teams, not prompt dumps.** Profiles have explicit ownership and clean handoffs.
2. **Namespace isolation.** `agency-*` is professional, `council-*` is personal, and `academy-*` is educational.
3. **Portable distributions only.** No runtime state, secrets, personal filesystem paths, or local caches.
4. **Specialists remain specialists.** Profiles should hand off rather than silently absorbing unrelated domains.
5. **Human agency stays central.** Council profiles support decisions and capability; they do not attempt to run a person's life.
6. **Safety beats role-play.** Profiles do not manufacture medical, legal, financial, spiritual, parental, credentialing, or other authority they do not possess.
7. **Academy teaches for transfer.** Explanations, examples, practice, feedback, and mastery checks should make the learner progressively more capable rather than merely dependent on answers.

See [`PACK_SPEC.md`](PACK_SPEC.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`SECURITY.md`](SECURITY.md) for repository standards.

## License

AGPL-3.0-only. See [`LICENSE`](LICENSE).
