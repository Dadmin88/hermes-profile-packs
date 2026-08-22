# Hermes Profile Packs

Curated profile packs for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

This repository is the public upstream home for reusable Hermes profile distributions maintained as coherent teams rather than isolated prompts.

## Packs

| Pack | Namespace | Purpose |
| --- | --- | --- |
| **Hermes Agency** | `agency-*` | Professional specialists for engineering, product, design, QA, operations, marketing, content, and coordinated project work. |
| **Hermes Council** | `council-*` | Personal specialists for life support, growth, health, family, stewardship, connection, recreation, and planning. |
| **Hermes Academy** | `academy-*` | Professors and instructors for academic, technical, vocational, and professional learning. |

The packs separate durable context domains: Agency executes professional work, Council supports the person, and Academy teaches.

## Repository layout

```text
hermes-profile-packs/
├── hermes-agency/
├── hermes-council/
├── hermes-academy/
├── docs/
├── packs.json
├── install.py
└── validate.py
```

Every distributable profile uses Hermes' native profile-distribution shape with `distribution.yaml`, `SOUL.md`, and purpose-built `skills/*/SKILL.md`. Runtime state, authentication material, local paths, caches, databases, logs, and sessions are never distributed.

## Install

```bash
python install.py --list-packs
python install.py academy --list
python install.py academy
python install.py academy academy-mathematics-professor academy-skilled-trades-instructor
```

## Validate

```bash
python validate.py
```

## Design principles

1. Coherent teams, not prompt dumps.
2. Stable namespace isolation.
3. Portable source distributions only.
4. Specialists hand off instead of silently swallowing unrelated domains.
5. Human agency stays central.
6. Safety beats role-play or invented authority.
7. Academy optimizes for understanding, practice, feedback, and transferable capability rather than answer dumping.

See `PACK_SPEC.md`, `CONTRIBUTING.md`, and `SECURITY.md` for repository standards.

## License

AGPL-3.0-only. See `LICENSE`.
