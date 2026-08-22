# Brooklyn Skills source audit

Canonical source: `https://github.com/OutThisLife/brooklyn-skills`

Reviewed revision: `f60ab3b43f422309c74dff5ed7dc53af042c2908`

Review date: 2026-08-10

Upstream author: Brooklyn Nicholson / OutThisLife

License: MIT

## Repository review

The reviewed revision contains 19 portable skill packages under `skills/`, plus `defaults.md`, README, and license material. The skill tree contains Markdown skill/reference files and no bundled executables, install scripts, hooks, credential files, or mutable runtime loaders. Hermes Agency does not use the upstream README's external-directory/`git pull` update model; selected content is pinned, adapted, and vendored into profile distributions instead.

## Approved imports

- `pr-ready` -> `agency-git-steward/skills/pr-ready`
- `stacked-pr` -> adapted as `agency-git-steward/skills/stacked-pr-management`
- `visual-verify` -> `agency-design-reviewer/skills/visual-verify`
- `research` -> adapted as `agency-software-architect/skills/technical-research`

Each vendored/adapted import includes a local `SOURCE.md` with revision, license, adaptations, and the upstream MIT notice.

## Incorporated concepts without vendoring the full skill

- `pr-update`: strengthened Agency `pr-preparation` with existing-PR detection, full-diff refresh, media preservation, and contributor provenance.
- `pr-triage`: strengthened Agency `repository-state-audit` with duplicate/sibling/stacked contribution discovery and cluster awareness without adopting the upstream three-verdict maintainer policy.
- `draft-tweet`: strengthened Social Media Manager `launch-post` with optional read-only sampling of recent original posts for voice-pattern matching without depending on `xurl` or another specific client.
- `ui-system`: strengthened `design-system-component` with existing-primitive/token discovery, variant-first reuse, and explicit resistance to parallel local UI kits.

## Reviewed but not imported

- `perf`: useful but substantially covered by Agency Performance Engineer's deeper profiling, bottleneck, measurement, and regression procedures.
- `runtime-debug`: useful logs-first guidance, but Agency Infrastructure Engineer already has broader runtime-layer and Fleet-relocation diagnosis.
- `work`: worktree/task-environment orchestration is not a professional Agency capability and should remain outside profile semantics.
- `ticket-ship`: tracker-to-ship workflow crosses into orchestration/project lifecycle rather than one specialist's professional capability.
- `cpr`: composition wrapper around other skills; Agency/Fleet orchestration should compose capabilities instead of storing unnecessary wrapper skills.
- `ui-only`: useful as an interactive workflow preference, but inappropriate as a default for autonomous distributed work because it intentionally delays normal validation/handoff steps.
- `free-disk-space`: narrowly macOS-specific; a future Infrastructure skill should be generalized around disk-pressure diagnosis and safe cleanup if needed.
- `notarize-mac`: useful specialist release procedure, but deferred until macOS signing/notarization is a recurring Agency/Fleet need.
- `clean`: good diff-polish principles but overlaps current code-review/Git Steward procedures.
- `audit-only`: good read-only behavior, but better represented by task authority and operating guardrails than a role-specific professional skill.
- `no-tropes`: objective is useful, but its bundled reference explicitly attributes a separate third-party source whose redistribution provenance was not independently reviewed here; Agency should author its own prose-quality procedure if needed rather than vendoring that reference.

## Security and portability decision

Approved imports are plain instruction documents and are adapted to avoid hard dependencies on one forge CLI, worktree layout, local hostname, provider, machine path, or live marketplace checkout. Fleet remains responsible for node placement and distributed execution; these skills define professional procedure only.