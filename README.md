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

Hermes Council currently contains 21 focused profiles and 84 purpose-built personal-life skills. Hermes Academy v0.2 contains 30 faculty profiles and 120 purpose-built teaching skills. Hermes Agency contains 109 professional specialists.

### Academy Continuing Education

Hermes Academy also includes an in-progress Continuing Education flow for profile-to-profile competency transfer. The merged implementation uses natural-language requests, Dean routing when needed, canonical Bot Chat, the generic `goal_manage` bridge into Hermes' native `/goal` state, `message_agent`, Academy instruction/transfer assessment, and native `/learn` into the learner's normal skill store. It adds no custom training runtime or Fleet dependency.

Implementation and deterministic/native-runtime validation are complete through the Phase 10–13 quality gate, and the Phase 14 controlled disposable-profile preflight has passed with learner-local persistence, fresh-session reuse, and a sealed A/B capability check. Phase 15 production-profile validation and Phase 16 release/whole-change review are still pending, so Continuing Education should not yet be described as production-validated. The current flow requires generic downstream Hermes support for Bot Chat `goal_manage`, profile-distribution `preload_skills`, and bounded goal-judge feedback propagation, merged in `Dadmin88/hermes-agent-downstream` PRs #24, #26, and #27. Every Agency distribution preloads `academy-continuing-education`, making the learner contract deterministic before the first model turn. Stock-install readiness remains a release gate until equivalent support is present in the normal Hermes release. See [`docs/CONTINUING_EDUCATION.md`](docs/CONTINUING_EDUCATION.md) and the normative [`docs/CONTINUING_EDUCATION_ARCHITECTURE.md`](docs/CONTINUING_EDUCATION_ARCHITECTURE.md).

## Start small with Team Recipes

You rarely need all 160 profiles. Team Recipes are validated compositions of existing profiles for common outcomes, with `minimal`, `recommended`, and `expanded` tiers.

The main installer understands them directly:

```bash
python install.py --list-recipes
python install.py --recommend "build and ship a web app"
python install.py --recipe software-delivery --tier minimal --dry-run
python install.py --recipe software-delivery --tier recommended --yes
```

Recommendation is confidence-aware. A recipe is promoted only when one formation is a strong, unambiguous fit; otherwise the installer falls back to individual profile matches instead of forcing a template.

Recipes are portable selection guidance only. They do not create memory, cron jobs, Bot groups, Kanban state, credentials, or other runtime state. Installation still uses the normal Profile Packs/Hermes distribution path.

See [`docs/TEAM_RECIPES.md`](docs/TEAM_RECIPES.md) and [`docs/FIRST_TEAM.md`](docs/FIRST_TEAM.md).

## Repository layout

```text
hermes-profile-packs/
├── hermes-agency/
├── hermes-council/
├── hermes-academy/
├── docs/
├── examples/
├── tests/
├── packs.json
├── recipes.json
├── recipe_catalog.py       # Shared recipe loading/scoring/confidence engine
├── install.py              # Canonical human + agent profile/recipe selector
├── recipes.py              # Focused recipe-only convenience client
└── validate.py
```

Runtime state is never distributed. Authentication material, `.env` files, logs, caches, databases, local paths, session history, and machine-specific configuration do not belong in this repository.

## Install

For most people, launch the selector:

```bash
python install.py
```

The wizard can recommend a validated Team Recipe when a goal maps cleanly to one, browse recipes directly, browse packs/categories, search exact profiles, or explicitly install everything. A recipe is never silently chosen: the user chooses its tier and sees the exact profile plan before final confirmation.

For agents and scripts:

```bash
python install.py --agent-help --json
python install.py --catalog --json
python install.py --list-recipes --json
python install.py --recommend "build a web app" --json
python install.py --recipe software-delivery --tier minimal --dry-run --json
python install.py --recipe software-delivery --tier recommended --yes --json
python install.py --profiles agency-backend-engineer agency-frontend-engineer --dry-run --json
python install.py --all --yes --json
```

`--catalog`, `--list-recipes`, and `--recommend` are read-only. Existing `--recommend --json` consumers keep the individual-profile `recommendations` array; recipe results are additive through `recipe_match` and `recipe_recommendations`.

Legacy pack-first commands remain supported.

See [`docs/INSTALLER.md`](docs/INSTALLER.md) for the full contract.

## Focused recipe client

`recipes.py` remains supported when a recipe-only surface is convenient:

```bash
python recipes.py --list
python recipes.py --recommend "learn cybersecurity"
python recipes.py cybersecurity-learning --tier recommended --dry-run
```

Both entry points use the same shared recipe engine.

## Operate the team

Use [`docs/OPERATING_PLAYBOOK.md`](docs/OPERATING_PLAYBOOK.md), [`docs/INSTALLATION_VERIFICATION.md`](docs/INSTALLATION_VERIFICATION.md), and [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

## Validate

```bash
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
```

This validates pack manifests, namespaces, distribution metadata, skills, portability, secret/path hygiene, team recipe references/tier invariants, and root selector behavior.

## Design principles

1. **Coherent teams, not prompt dumps.** Profiles have explicit ownership and clean handoffs.
2. **Namespace isolation.** `agency-*` is professional, `council-*` is personal, and `academy-*` is educational.
3. **Portable distributions only.** No runtime state, secrets, personal filesystem paths, or local caches.
4. **Specialists remain specialists.** Profiles hand off rather than silently absorbing unrelated domains.
5. **Smallest useful team.** Add profiles only for distinct expertise, independent review, or useful parallelism.
6. **Conservative recommendation.** A recipe is promoted only when the deterministic match is strong and unambiguous.
7. **Human agency stays central.** Council supports decisions and capability; it does not run a person's life.
8. **Safety beats role-play.** Profiles do not manufacture authority they do not possess.
9. **Academy teaches for transfer.** Teaching should make the learner progressively more capable.

See [`PACK_SPEC.md`](PACK_SPEC.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`SECURITY.md`](SECURITY.md).

## License

AGPL-3.0-only. See [`LICENSE`](LICENSE).
