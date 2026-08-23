# Team Operating Layer Implementation Plan

Status: implemented on the `feat/team-recipes-operating-layer` branch.

## Purpose

Hermes Profile Packs already provides the reusable people: namespaced Hermes profiles, SOUL contracts, bundled skills, manifests, installers, validators, and tests. This program adds the missing adoption and operating layer without turning the repository into a runtime framework.

The new layer answers four questions:

1. Which small group of profiles should I install for a common outcome?
2. How should those profiles divide work without creating coordination overhead?
3. What does a healthy first run look like after installation?
4. How can an operator adopt useful routines while keeping runtime state owned by Hermes rather than by Profile Packs?

## Architectural boundary

Profile Packs remains a source-distribution repository.

It may ship:

- team recipes that reference stable profile identities;
- operating guidance and worked examples;
- verification checklists;
- optional routine suggestions;
- reusable profile skills that improve coordination judgment.

It does not own or distribute:

- live memory, STATE files, session history, or user vault contents;
- cron registrations;
- Bot/group membership;
- Kanban boards or tasks;
- learned local skills;
- model credentials or provider configuration;
- Fleet placement, transport, or node state.

A recipe is advice plus a deterministic profile selection. It never grants authority and never creates runtime state by itself.

## Phase 1: Recipe schema and registry

Create `recipes.json` as the canonical machine-readable roster for proven team formations.

Each recipe contains:

- stable `id`;
- `display_name`;
- owning `pack`;
- short `description` and `when_to_use` guidance;
- search `keywords`;
- `minimal`, `recommended`, and `expanded` profile tiers;
- a concise workflow;
- observable success criteria;
- optional runtime routine suggestions.

Rules:

- Recipes reference existing profile identities only.
- A recipe belongs to one durable context domain: Agency, Council, or Academy.
- `minimal` must be a subset of `recommended`; `recommended` must be a subset of `expanded`.
- Bigger tiers add distinct expertise, review, or useful parallelism. They are not prestige levels.
- No recipe installs every profile by default.
- Optional routines are documentation only and are never registered automatically.

Initial catalog covers software delivery, API/backend work, security review, open-source maintenance, product launches, game development, research/analysis, personal reset, family support, fitness/recovery, technical study, and cybersecurity learning.

Acceptance:

- Every referenced profile exists.
- Every profile belongs to the recipe's owning pack.
- Tier nesting is deterministic and validated.
- Registry passes repository validation and unit tests.

## Phase 2: Deterministic recipe selector

Add `recipes.py` as an additive companion to the existing profile-level `install.py`.

Design rule: do not create a second installer or profile catalog.

`recipes.py` imports and reuses the existing root installer for:

- profile catalog loading;
- source-size accounting;
- profile installation;
- JSON output conventions;
- Hermes-native pack installer delegation.

Supported flows:

```bash
python recipes.py --list
python recipes.py --recommend "build and ship a web app"
python recipes.py software-delivery --tier minimal --dry-run
python recipes.py software-delivery --tier recommended --dry-run --json
python recipes.py software-delivery --tier recommended --yes
```

Safety:

- Listing, recommendation, recipe inspection, and dry-run are read-only.
- Writes require explicit `--yes`.
- JSON mode never prompts.
- Unknown recipes and tiers fail closed.
- The resulting install still uses each pack's native `hermes profile install` flow through the existing root installer.

Acceptance:

- Recipe selection resolves exact profile names deterministically.
- Dry-run reports exact profiles and catalog payload statistics.
- Agent/script callers can use JSON.
- No duplicated installation implementation exists.

## Phase 3: First useful team onboarding

Add `docs/FIRST_TEAM.md`.

The guide deliberately avoids the "install everything" trap. It provides one short proof path for each pack:

- Agency: install a small delivery team, complete one bounded multi-profile workflow, and capture one independent review.
- Council: install Steward plus the smallest relevant personal-support set, preserve minimum-necessary context, and complete one practical plan.
- Academy: install Dean plus relevant faculty, complete one lesson/practice loop, and verify transfer rather than mere explanation.

Acceptance:

- A newcomer can reach a useful result without understanding the full 160-profile catalog.
- The guide uses existing Hermes/Profile Packs primitives only.

## Phase 4: Operating playbook

Add `docs/OPERATING_PLAYBOOK.md` with shared rules that apply after installation.

Core decision model:

1. Prefer one clear owner when one specialty can complete the work coherently.
2. Add a second specialist only for distinct expertise, independent review, or a clean parallel seam.
3. Use larger teams only when work packages can be independently owned and verified.
4. If the seam cannot be stated clearly, do not split the work merely to create activity.
5. Prefer independent review over multiple implementers when correctness is the main reason for adding another profile.

Durability rule:

- Chat/group rooms deliberate.
- Kanban or another operator-selected durable work system records commitments, ownership, dependencies, decisions, and completion evidence.

Acceptance:

- The guidance reduces unnecessary delegation rather than encouraging swarm-by-default behavior.
- It preserves the existing Agency handoff/evidence contract.

## Phase 5: Orchestrator coordination judgment

Add a new Agency Orchestrator skill, `coordination-pattern-selection`.

The skill makes the Orchestrator explicitly decide among:

- solo ownership;
- paired execution/review;
- multi-specialist decomposition.

It evaluates domain count, ownership clarity, dependency seams, review needs, critical-path benefit, context-transfer cost, and synthesis risk before decomposing work.

Update the Orchestrator SOUL so delegation is not treated as success by itself.

Acceptance:

- Simple single-domain work stays with one specialist.
- Independent review is selected when review is the actual need.
- Multi-profile work has explicit seams and owners.

## Phase 6: Runtime verification guidance

Add `docs/INSTALLATION_VERIFICATION.md`.

The checklist distinguishes repository validation from user-install verification.

Repository validation proves the source distribution is internally valid.
Runtime verification asks the operator to prove that an installed profile actually behaves as intended in a fresh Hermes session.

Checks include:

- installation completed without pack-installer failure;
- expected aliases/profiles are present through the normal Hermes surface;
- the profile identifies the correct role and boundaries in a fresh session;
- bundled skills are available when relevant;
- one handoff or review works when the recipe requires multiple profiles;
- no source repository files are used as runtime state.

No undocumented Hermes CLI flags are invented merely to automate this.

## Phase 7: Worked examples

Add sanitized examples showing the lifecycle rather than fake transcripts:

- software delivery;
- security review;
- Council personal reset;
- Academy technical study.

Each example shows:

user outcome -> recipe/tier -> ownership -> durable task split -> handoffs/review -> observable success.

Examples contain no runtime credentials, user memory, or machine-specific paths.

## Phase 8: Troubleshooting and routines

Add `docs/TROUBLESHOOTING.md` for common adoption failures and include optional routine patterns in the operating documentation.

Routine principles:

- Profile Packs may suggest a routine and its intended owner.
- The user explicitly creates runtime schedules in Hermes if desired.
- Profile Packs never registers cron jobs during profile/recipe installation.
- Routines must produce useful artifacts or decisions, not status noise.

Examples include Chief of Staff board review, Security Operations advisory review, Open Source Maintainer upstream review, and Academy study-plan review.

## Phase 9: Validation, CI, and release gate

Extend `validate.py` to validate `recipes.json`.

Add root unit tests for:

- recipe loading;
- tier monotonicity;
- profile resolution;
- deterministic recommendations;
- JSON dry-run planning.

Existing GitHub Actions already runs `python validate.py` and root unit tests, so the new layer enters the normal repository gate automatically.

Release acceptance:

```bash
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
python -m unittest discover -s hermes-agency/tests -p 'test_*.py'
python -m unittest discover -s hermes-council/tests -p 'test_*.py'
python -m unittest discover -s hermes-academy/tests -p 'test_*.py'
```

The branch must pass CI before merge.
