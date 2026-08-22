# AGENTS.md

## Repository purpose

Hermes Agency is a curated collection of professional Hermes Agent profiles and the bundled skills that make those profiles useful.

Repository changes should improve one or more of these areas:

- profile quality;
- skill quality;
- routing clarity;
- collaboration behavior;
- profile packaging and installation;
- static interoperability contracts;
- validation, evaluation, and production documentation.

## Scope boundary

Hermes Agency owns portable professional capability definitions. It does not own the distributed runtime that executes them.

This repository may define:

- professional profile identities and routing descriptions;
- profile `SOUL.md` behavior;
- bundled skills and their supporting files;
- Hermes profile distribution metadata;
- installer behavior built on Hermes profile commands;
- deterministic profile content identity;
- static catalog and routing metadata for external consumers;
- routing evaluation cases and repository validation.

Do not add live node registries, peer discovery, membership, scheduling, placement engines, capacity management, transport protocols, remote-execution services, task daemons, runtime databases, dashboards, deployment services, or custom orchestration runtimes here.

In the wider Hermes ecosystem, Fleet may place and route profiles, Nodescale may provide node identity and membership, and Keryx may provide authenticated transport. Those systems consume Agency identities and packages; their implementations remain in their own repositories.

## Sources of truth

- `agency.json` is the machine-readable profile roster and static routing contract.
- `profiles/<name>/distribution.yaml` defines distribution metadata for a profile.
- `profiles/<name>/SOUL.md` defines the professional behavior of a profile.
- `profiles/<name>/skills/` is the canonical capability set bundled with that profile.
- `AGENCY.md` defines the shared collaboration model.
- `catalog.py` emits the deterministic runtime-facing profile catalog from the real profile tree.
- `runtime-contract.json` describes the small static source contract used by external consumers.
- `evals/routing.json` contains routing evaluation cases.
- `README.md` is the newcomer-facing product documentation.

Do not introduce a second maintained skill registry. Capability names are derived from the actual `profiles/<name>/skills/*/SKILL.md` directories.

## Profile structure

Every profile must include:

```text
profiles/<profile-name>/
├── distribution.yaml
├── SOUL.md
└── skills/
    └── <skill-name>/
        └── SKILL.md
```

Every profile must ship with at least one useful role-specific skill. Additional Hermes configuration, references, or skill helper scripts may be added when they materially improve the specialty.

Profile names use the `agency-` prefix and lowercase kebab case.

## Profile quality standard

A profile must represent a meaningful professional specialization.

Its routing description should make clear:

- what class of work the profile owns;
- what deliverables it is expected to produce;
- how it differs from nearby specialties.

Its `SOUL.md` should define:

- role and specialty;
- core responsibilities;
- authority and handoff boundaries;
- operating standards;
- common collaborators;
- communication expectations;
- definition of done.

Profiles should exercise independent professional judgment inside their domain. Avoid generic instructions that could be copied unchanged across roles without affecting behavior.

## Skill quality standard

Skills are procedural capability, not alternate personas.

A useful skill should define a repeatable method for a recognizable class of work within the profile's specialty. It should explain when to use the procedure, what evidence or inputs matter, how to perform the work, and how to judge completion.

Skills should:

- solve a real recurring task;
- contain concrete professional procedure rather than generic advice;
- complement the profile's `SOUL.md` instead of repeating it;
- state important validation or quality gates;
- use supporting references or scripts only when they materially improve the workflow;
- avoid unnecessary tool, provider, framework, platform, or machine assumptions unless the skill is intentionally specific to them.

Prefer a smaller set of strong, distinct procedures over overlapping prompts.

## Third-party skill sourcing

Public skill directories and marketplaces are discovery sources, not runtime dependencies.

Before adding third-party skill content:

1. Follow the listing to the canonical source repository or author.
2. Review the complete skill directory, including instructions, scripts, references, assets, and install behavior.
3. Verify that the license permits redistribution and preserve required attribution.
4. Pin the reviewed source revision rather than depending on a moving target.
5. Reject content that requests unnecessary credentials, secret discovery, persistence, broad filesystem access, arbitrary remote code execution, opaque installers, or unrelated network access.
6. Adapt agent-specific instructions only when the adaptation preserves intent and license requirements.
7. Vendor reviewed files into the appropriate profile. Installation must not fetch mutable marketplace content.
8. Preserve provenance either in the vendored skill itself or in a repository source record when the original package structure makes a per-skill provenance file impractical.

Popularity and marketplace ranking are not substitutes for review.

## Fleet interoperability

Agency profile names are stable professional identities across eligible Hermes nodes.

The Agency side of the interoperability contract is static and portable:

- profile `name` is the stable identity;
- `agency.json` exposes the roster and distribution layout;
- every profile is independently installable;
- the same profile package should behave consistently on any eligible node;
- profiles and skills must not bake in node IDs, hostnames, IP addresses, machine-specific absolute paths, local credentials, or assumptions about a particular placement;
- model/provider/runtime requirements should only be declared when the professional capability genuinely depends on them.

Live presence and placement are not stored here. External orchestration may discover, place, and route Agency profiles using current node health, capacity, policy, and availability.

## Routing quality

Routing is based on professional responsibility, not keyword matching.

When adding or editing a role, compare it with neighboring profiles. Overlap is acceptable when the professions are genuinely distinct, but the ownership boundary must remain clear enough for an orchestrator to choose between them.

Examples:

- Product Manager defines product behavior; Technical Lead coordinates engineering execution.
- Software Architect defines durable software structure; Backend Engineer implements backend behavior.
- Product Designer defines product experience; Frontend Engineer implements the interface.
- Code Reviewer reviews implementation; QA Tester validates behavior.
- Marketing Strategist defines marketing direction; Copywriter produces persuasive copy.
- Market Researcher studies the market; User Researcher studies users.

## Collaboration standard

Profiles should work as a team without becoming interchangeable.

Shared expectations:

- inspect relevant context before acting;
- keep ownership explicit;
- use the smallest capable specialist set;
- preserve unrelated work;
- validate deliverables before completion;
- use independent review where it adds meaningful confidence;
- hand off outcome, artifacts, evidence, risks, and next action;
- escalate decisions to the role that owns them.

## Distribution metadata

Each `distribution.yaml` should include at least:

```yaml
name: agency-example
version: 0.1.0
description: "Clear routing description"
author: "Kyle French"
license: "AGPL-3.0-only"
```

Do not pin a model or provider unless the profile genuinely depends on one.

## Roster changes

When adding, renaming, or removing a profile:

1. Update the profile directory.
2. Update `agency.json` and category counts.
3. Update the README roster.
4. Check handoff references in related profiles.
5. Add or update the role's bundled skills.
6. Update `backbone_profiles` in `agency.json` only when the role is part of the core routing backbone.
7. Add or update routing evaluations when a new ownership boundary matters.
8. Confirm `python validate.py`, `python catalog.py`, and the test suite pass.

Profile names are distributed identities. Treat renames as compatibility changes rather than cosmetic edits.

## Installer and catalog

Keep `install.py` small and dependency-free. It should rely on Hermes profile commands rather than reimplementing profile management or skill loading.

`catalog.py` must derive capabilities from the actual profile directories, fail closed on malformed distributions, and preserve deterministic profile content digests. Do not add a mutable registry or live orchestration behavior to the catalog.

## Security and repository hygiene

Never commit credentials, API keys, `.env` files, `auth.json`, memories, sessions, runtime databases, caches, logs, user workspaces, generated runtime state, or deployment secrets.

Treat third-party skills as executable agent instructions with meaningful access to the profile's tools and environment. Review them accordingly before vendoring.

Keep examples generic and safe for a public repository.

## Documentation style

Write documentation for someone encountering Hermes Agency for the first time. Explain the current product directly: what it is, why someone would use it, how to install it, how profiles and skills are organized, and how to contribute.

Use normal production documentation. Do not add migration diaries, superseded architecture descriptions, historical implementation notes, or commentary about responsibilities that used to live in this repository.
