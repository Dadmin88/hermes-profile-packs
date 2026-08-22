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

Profile packs contain source artifacts only. Never commit tokens, passwords, credentials, `.env`, auth files, logs, caches, databases, process state, user-home paths, machine-specific mounts, or generated Hermes runtime state.

## Metadata and jobs

Pack manifests are the authoritative roster. A roster entry includes stable `name`, human-readable `display_name`, category, concise `role`, and `jobs` matching the profile's owned reusable skills. The manifest supports discovery and routing; `SOUL.md` remains the behavioral contract.

## Separation of concerns

Profiles own bounded domains. When a request materially belongs elsewhere, complete the owned part and hand off the rest with sufficient context.

Council profiles additionally share only minimum-necessary personal context across boundaries.

Academy profiles additionally teach rather than impersonate credentials or assessment authority. They should adapt to learner level and goal, distinguish instruction from professional advice, and verify current standards or facts when material.

## Versioning

Profile and pack versions use semantic versioning.

- Patch: wording, examples, or compatible skill improvements.
- Minor: new profiles, skills, or backward-compatible metadata.
- Major: renamed/removed profiles, incompatible distribution behavior, or semantic contract changes.
