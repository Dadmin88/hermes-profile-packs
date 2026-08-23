# Hermes Profile Pack Specification

## Namespaces

A pack owns a stable prefix. Every profile directory and `distribution.yaml` name must begin with that prefix.

- Hermes Agency: `agency-*`
- Hermes Council: `council-*`
- Hermes Academy: `academy-*`

Names use lowercase kebab-case and are treated as public API once released.

## Required profile files

Every profile must contain:

- `distribution.yaml` with `name`, `version`, `description`, `author`, and `license`.
- `SOUL.md` defining role, responsibilities, working standard, collaboration boundaries, communication, and completion criteria.
- At least one profile-specific `skills/<skill>/SKILL.md`.

A skill file begins with YAML frontmatter containing a matching `name` and useful `description`, followed by a concrete procedure or operating guidance.

## Portable versus runtime state

Profile packs contain source artifacts only. Never commit:

- tokens, passwords, cookies, API keys, OAuth credentials, or private keys
- `.env` or authentication files
- logs, caches, databases, process IDs, sockets, or session history
- absolute user-home paths or machine-specific mount paths
- generated Hermes runtime state

## Metadata and jobs

Pack manifests are the authoritative roster. A roster entry includes:

- stable profile `name`
- human-readable `display_name`
- category
- concise `role`
- `jobs`, which map to the profile's owned reusable skills

The manifest is designed for discovery and routing; `SOUL.md` remains the behavioral contract.

## Team recipes

`recipes.json` is the authoritative registry for portable team compositions.

A recipe is not a new runtime primitive. It references existing released profile identities and describes a useful formation for a common outcome.

Every recipe must contain:

- stable lowercase kebab-case `id`;
- `display_name`;
- one owning `pack` (`agency`, `council`, or `academy`);
- `description` and `when_to_use`;
- non-empty search `keywords`;
- `minimal`, `recommended`, and `expanded` tiers;
- a non-empty `workflow`;
- non-empty observable `success_criteria`;
- optional runtime routine suggestions.

Tier rules:

- every profile reference must exist in the owning pack;
- no cross-pack profile references are allowed inside a single recipe;
- `minimal` must be a subset of `recommended`;
- `recommended` must be a subset of `expanded`;
- larger tiers should add distinct expertise, independent review, or useful parallelism rather than status or duplication.

Recipe installation must reuse the normal Profile Packs/Hermes distribution path. Recipes may suggest runtime routines, but must never create cron jobs, memory, sessions, groups, Kanban state, credentials, or other live state during installation.

## Separation of concerns

Profiles should own a bounded domain. When a request materially belongs elsewhere, complete the part owned by the current profile and hand off the rest with sufficient context.

Council profiles have an additional privacy rule: only the minimum personal context needed for the task should cross profile boundaries.

Academy profiles have an additional teaching rule: adapt instruction to the learner's goal and level, teach reasoning and transferable skill rather than merely dumping answers, distinguish education from professional execution or advice, and verify current standards or facts when material.

## Versioning

Profile and pack versions use semantic versioning.

- Patch: wording, examples, or compatible skill improvements.
- Minor: new profiles, skills, recipes, or backward-compatible metadata.
- Major: renamed/removed profiles or recipes, incompatible distribution behavior, or semantic contract changes.
