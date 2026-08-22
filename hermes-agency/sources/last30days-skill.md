# last30days skill enrichment

- Source: `mvanhorn/last30days-skill`
- Repository: https://github.com/mvanhorn/last30days-skill
- Revision: `e93c8249d8ba073e8e88c388ed1f0fc403ffd86e`
- Skill version: `3.18.4`
- License: MIT
- Review date: 2026-08-13
- Imported assignment count: 2
- Imported profiles:
  - `agency-market-researcher`
  - `agency-competitive-analyst`

## Why these profiles

`last30days` provides fresh, engagement-weighted research across public web and social sources, including comparison, competitor discovery, trend discovery, hiring signals, and cited brief generation. Market Researcher is the primary fit; Competitive Analyst directly benefits from the engine's comparison and competitor workflows.

The skill was not duplicated into adjacent content or social roles. Those profiles can consume specialist research outputs without inheriting this engine's broader network, credential, persistence, setup, and optional publishing surface.

## Audit and import boundary

- Reviewed the repository guidance, canonical `skills/last30days/SKILL.md`, runtime tree, packaging rules, dependency manifest, credential flows, file writes, subprocess/network surfaces, publishing/watchlist behavior, and vendored X-search client boundary.
- Ran the upstream focused Hermes, security, secret-hygiene, runtime-preflight, metadata, and version-consistency tests before import.
- Imported only the tracked canonical `skills/last30days/` tree from the pinned revision, not repository tests, fixtures, CI, MCP code, release media, or development documentation.
- Added the upstream MIT `LICENSE` to each distributed profile copy so the copyright and permission notice travel with the substantial redistributed runtime.
- Preserved the upstream skill content and runtime files without functional modification. The distributed copies only normalize trailing whitespace and the final newline in three upstream Python files so the Agency repository passes `git diff --check`.

## Operating risks

The skill can make network requests, read optional browser cookies only after consent, consume optional API credentials, install optional tools during consent-driven setup, write local research state, deliver watchlist webhooks, and publish HTML only when explicitly requested. Normal Hermes approval and secret-handling rules remain in force; installing the skill does not authorize those actions.
