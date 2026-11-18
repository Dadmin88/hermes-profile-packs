# Profile personality standard (pilot)

Status: **pilot on an isolated branch**, not a catalog-wide release or live-profile migration.

## Intent

Every Hermes Profile Packs specialist should eventually have a recognizable,
role-appropriate temperament and way of communicating. A personality is not a
second job description, a fictional human biography, or a way to bypass role
restrictions. It should change *how* the agent reasons with people, handles
uncertainty, disagrees, and communicates, while leaving its professional
responsibilities and safety boundaries intact.

The pilot covers one representative profile from each pack:

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

Nothing in this pilot modifies production profile configs, runtime memory,
Hermes models, tool permissions, or Gateway state.

## Behavioral acceptance

Static validation proves that a personality is packaged and resolves. It
**does not** prove that a model actually expresses a distinctive identity.
For each pilot, use the Profile Packs eval workbench once its branch/runtime
is available. Compare matched prompts with and without the selected overlay,
using the same model, tool availability, and task context. Review evidence,
not simply the model's own claims about its persona.

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

Use independent, attributed review of actual responses, tool traces, and
source excerpts where available. Reviewers should be blind to A/B condition
when feasible. Record failures and counterexamples. The pilot is not certified
until all three profiles pass their own role-specific behavioral checks without
material regression.

## Release and rollout gates

1. Source validator, pack validators, and full test suite pass.
2. Native Hermes resolves each selected custom personality in an isolated
   profile environment, and shows `SOUL.md` plus the overlay in a new session.
3. Existing MCP seeds remain disabled and otherwise unchanged.
4. User-owned `config.yaml` remains untouched in a normal profile update.
5. A/B behavioral evaluations demonstrate benefits without material regression.
6. Apply the appropriate pack/profile versioning and changelog when promoting
   the pilot to a real release.
7. Only then make personality authoring an expected part of BotFather's
   profile-pack-authoring process and expand incrementally to the remaining
   profiles; do not mass-generate interchangeable personas.

No evaluation score, live install, or production readiness is claimed by
these source changes.
