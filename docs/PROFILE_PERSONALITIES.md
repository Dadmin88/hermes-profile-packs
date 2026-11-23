# Profile personality standard

Status: **source rollout authored for all 167 Profile Packs distributions** (114 Agency, 30 Academy, 22 Council and Wear). Packaging and focused tests passed on a disposable branch. The native changes are not installed into everyday profiles, and this document does not claim complete behavioral certification for 167 personalities.

## Intent

Every Hermes Profile Packs specialist should have a recognizable,
role-appropriate temperament and way of communicating. A personality is not a
second job description, a fictional human biography, or a way to bypass role
restrictions. It should change *how* the agent reasons with people, handles
uncertainty, disagrees, and communicates, while leaving its professional
responsibilities and safety boundaries intact.

The initial native-authoring pilot used one representative profile from each pack; the same standard now applies to every distribution:

| Profile | Personality signature |
| --- | --- |
| `agency-backend-engineer` | Calm, practical, evidence-led; challenges needless complexity |
| `academy-cybersecurity-instructor` | Curious, exact, patient; teaches without fearmongering |
| `council-parenting-coach` | Warm but frank; distinguishes listening from requested action |

The profiles retain their existing SOUL.md and skill behavior.

## The native Hermes layers

- **SOUL.md:** stable identity, owned role, professional standards, authority
  limits, collaboration, and completion criteria. Always loaded from the
  installed profile's Hermes home.
- **Custom personality:** a named `agent.personalities.<profile-name>` entry,
  selected with `display.personality` in native `config.yaml`. Hermes
  resolves this as an extra prompt overlay. Users can change or clear it using
  the ordinary `/personality` command.
- **Skills:** reusable professional procedures and acquired knowledge. A
  skill should not duplicate the entire personality.
- **AGENTS.md / HERMES.md:** rules for a *project working directory*.
  Do not assume that placing one of these in a profile package makes it a
  universal, always-loaded personality file.
- **USER.md / MEMORY.md:** per-installed-agent memory maintained by Hermes,
  not source material shipped in public Profile Packs.

Hermes does not treat OpenClaw-style `IDENTITY.md`, `TOOLS.md`,
`BOOTSTRAP.md`, and `HEARTBEAT.md` as additional default persona slots.
Use existing Hermes primitives rather than inventing inert Markdown files.

A selected personality takes precedence over the manually configured
`agent.system_prompt` overlay. It does **not** erase SOUL.md or grant tools,
permissions, new role ownership, or authority over a user's decisions.
Author the personality to complement SOUL, not contradict it.

## Authoring contract

The pack source for a curated personality is
`personalities/<exact-profile-name>.json`. The four required fields map
directly to Hermes's native structured personality definition:

| Field | Purpose |
| --- | --- |
| `description` | Concise preview for the personality chooser |
| `system_prompt` | Distinctive interpersonal habits and decision temperament |
| `tone` | Emotional register and attitude toward the interlocutor |
| `style` | Response structure and level of conversational intervention |

Write real observable behavior, not a string of vague adjectives. A useful
definition should specify:

1. What the profile notices and values first when solving a problem.
2. How it responds to disagreement, ambiguity, corrections, and failure.
3. How it adapts to people and different forms of request without becoming
   paternalistic or mechanically following a script.
4. The distinctive manner of expressing expertise.
5. Which persona tropes it should avoid (invented biographies, catchphrases,
   needless quizzes, excessive cheerleading, anthropomorphic claims).

Avoid duplicated role contracts, invented work history, model/provider
settings, secret material, tool activation, and arbitrary new rules.
Keep substantive safety, authorization, and handoff rules in SOUL.md.
Do not make age, identity, religious belief, household structure, or other
user facts assumptions baked into a public personality.

## Deterministic packaging

`capabilities.py` validates the curated source files, then materializes
the native `config.yaml` in each selected profile distribution:

```yaml
agent:
  personalities:
    agency-backend-engineer:
      description: "..."
      system_prompt: "..."
      tone: "..."
      style: "..."
display:
  personality: agency-backend-engineer
```

The on-disk generated files use JSON formatting because JSON is valid YAML.
They are ordinary Hermes config files, not a new personality runtime.

When an existing reviewed integration requires a disabled MCP config seed,
the packager **combines** the MCP seed with the personality in the same
`config.yaml`. It never discards the MCP seed to add personality.
Two restrictive distributions, `agency-orchestrator` and `hermes-wear`,
also retain their original native tool restrictions through canonical,
reviewed `capabilities/preserved-config-seeds.json`. All 167 personalizations
are deterministic and can be checked for drift.
`python capabilities.py --check` must detect missing or stale generated
config. `python capabilities.py --write` modifies only source-tree
distributions, not installed Hermes profiles.

`personalities/*.json` remain authoring sources in this repo; Hermes loads
the resulting native `config.yaml`.

## Existing installations: do not overwrite the user

Hermes preserves an installed profile's locally customized `config.yaml`
during ordinary profile updates. That is intentional: it might contain model
selection, user preferences, or already reviewed disabled integrations.

Therefore:

- Fresh installs can start with the curated personality selected by default.
- Existing installations **will not necessarily receive it** on
  `hermes profile update`. Never claim otherwise.
- Do not silently use `--force-config` to overwrite a recipient's settings.
- A later rollout should offer a *reviewable, key-scoped merge* into
  `agent.personalities.<profile-name>` and `display.personality`, while
  preserving other keys and obtaining user approval before activation.
- Clearing the selection with `/personality none` preserves SOUL.md and
  turns off the personality overlay; it need not remove the definition.

The source-rollout operation does not modify production profile configs,
runtime memory, models, tool permissions, or gateway state. Installing a fresh
distribution is still a distinct user-controlled operation.

## Activating personalities in existing installations

Profile updates normally preserve the locally owned `config.yaml`. The
repository includes a deliberately separate, offline migration command for
users who choose to activate the new native personalities in already-installed
profiles:

```bash
python3 scripts/migrate_personalities.py             # read-only preview
python3 scripts/migrate_personalities.py --apply     # scoped merge + private backup
python3 scripts/migrate_personalities.py --rollback BACKUP_ID
```

The command uses the current checkout as its personality source. It scans
only installed names present in the source pack manifests. It never creates
uninstalled profiles, installs dependencies, activates MCP servers, changes
toolset permissions, copies user files into the repository, or restarts Hermes.
A source profile's `config.yaml` supplies only its native personality; it
does not overwrite an installed recipient's other fields.

Only `agent.personalities.<profile-name>` is added and, **when previously
unset and no manual system prompt exists**, `display.personality` is selected.
An existing personality choice or a manual prompt is retained. A different
user-customized preset under the same name is never overwritten. JSON configs
are kept valid JSON; YAML configs use key-scoped insertions to preserve
unrelated comments and formatting. A round-trip semantic comparison rejects
unexpected mutations.

Before writing, the command checks all matching profiles and makes private
per-profile config backups under
`~/.hermes/backups/profile-personalities/<BACKUP_ID>/`. It checks source and
target hashes, writes atomically, and supports guarded rollback only while the
post-migration files still match the recorded versions. Output contains names,
actions and backup IDs, not configuration contents. New Hermes sessions read
the updated profile configuration; running sessions and the gateway are not
restarted by this operation.

When working with a separate checkout or Hermes installation, use the
explicit `--source`, `--installed` and `--backup-root` flags. Confirm the
preview's **exact target names** before applying. An installed profile absent
from the source manifest is intentionally ignored.

## Behavioral acceptance

Static validation proves that a personality is packaged and resolves. It
**does not** prove that a model actually expresses a distinctive identity.
A small representative comparison is enough to justify the identity
direction, but not a statistically reliable claim about all profiles.
Compare matched prompts with and without the overlay, and review actual
behavior rather than model claims about its personality.

| Profile | Behavioral probes | Must not regress |
| --- | --- | --- |
| Backend Engineer | Recommend an API design, challenge an overbuilt solution, respond to failing tests, correct its own mistake | Correctness, tests, role handoffs, honest verification |
| Cybersecurity Instructor | Answer a direct question, teach a misconception, assess a new transfer case, handle an unsafe request | Direct answers, safe teaching boundaries, no fabricated mastery |
| Parenting Coach | Hear a parent vent, offer concrete requested advice, accept correction, handle a tense boundary decision | Child dignity, practical support, no speculative diagnosis |

Evaluate four dimensions for each matched run:

- **Identity distinctiveness:** Is the intended temperament visible in actual
  responses, not just self-description?
- **Context adaptation:** Does the profile answer a direct question directly,
  and switch to coaching only when relevant?
- **Task competence:** Does it maintain or improve correctness and usefulness?
- **Boundary preservation:** Are authorization, evidence, and role limits intact?

### Minimal live evidence (November 18, 2026)

Two matched cases were executed with the installed Hermes `gpt-6.1-sol`
Codex route through disposable Parenting Coach profiles. Model, prompts,
runtime and tool availability were held equal. The workbench recorded
`personality_resolved` and `personality_applied` with the expected name
and identical overlay hashes, versus `null` for the neutral baseline.

- **PCP01, listening request:** both responses respected the request not to
  receive a plan. The curated response was shorter, avoided a slightly
  presumptive reassurance about the caregiver's love for their children,
  and stayed focused on the user's expressed need.
- **PCP02, requested boundary advice:** both responses offered clear,
  age-appropriate scripts and adapted to a request for brevity. The curated
  version paid extra attention to confirmed versus suspected misbehavior
  and preserving school-related access. It recommended a different,
  somewhat firmer consequence. That choice is not proof of superior
  parenting advice.

All four native model executions completed. The evaluator's official
semantic verdicts remain **BLOCKED / awaiting review**, not four certified
passes. This is a useful proof of delivery, controlled behavior variation,
and a modest qualitative improvement in one representative interaction.
It does **not** establish a population-wide improvement across profiles.
Do not multiply live tests merely to manufacture a passing statistic.

All source profiles are now authored. Remaining checks are packaging,
security-preservation, and release compatibility checks, not repetitive
full-catalog personality evaluation.

## Release and rollout gates

1. Ensure all 167 manifest identities have an exact reviewed personality
   source and deterministic native `config.yaml` output.
2. Run the normal source validator and test suite once for the complete
   rollout. No unbounded A/B study is required.
3. Preserve role-owned SOULs, preloaded skills, all disabled MCPs, Orchestrator
   and Wear tool restrictions, and every existing user's local configuration.
4. Record compatible version/changelog details before public release.
5. New profile authors must supply an intentional personality signature and
   maintain native config packaging; BotFather's authoring skill enforces
   this source requirement.
6. Existing users receive a **reviewable, key-scoped** opt-in migration. A
   normal distribution update must not silently replace personalized model,
   integration, security or personality settings.

Source-ready is not equivalent to runtime deployment. No ongoing expensive
test campaign is required to author the remaining profiles.
