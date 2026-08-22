# Profile Selector & Installer

The root `install.py` is the recommended entry point for installing Hermes Profile Packs.

It has two surfaces backed by the same catalog:

- an interactive wizard for people;
- a deterministic non-interactive interface for agents and scripts.

The installer reads `packs.json`, each pack manifest, and existing profile distribution metadata. It does not maintain a second profile roster.

## Interactive wizard

Run:

```bash
python install.py
```

The wizard offers four paths:

1. **Recommend a small set for me** — describe what you want Hermes to help with and review the best matching profiles.
2. **Browse packs and categories** — choose a pack, category, and exact profiles.
3. **Search profiles directly** — search profile names, roles, jobs, and descriptions.
4. **Install everything** — explicitly install the complete catalog.

The default philosophy is sparse installation. Recommendations are intentionally bounded, and the wizard shows the exact plan before installation. It also estimates how much profile-distribution payload is selected versus skipped.

Nothing is installed until the final confirmation.

## Existing pack commands still work

The previous pack-first interface is preserved:

```bash
python install.py agency --list
python install.py council --list
python install.py academy --list
python install.py agency agency-backend-engineer agency-frontend-engineer
python install.py council --category growth
```

These commands delegate directly to the existing pack installers.

## Agent and script interface

Agents should not drive the interactive prompt. Use the machine-readable interface instead.

Discover the contract:

```bash
python install.py --agent-help --json
```

Inspect the full catalog:

```bash
python install.py --catalog --json
```

Limit discovery to one pack:

```bash
python install.py --catalog --pack council --json
```

Ask for deterministic recommendations without installing anything:

```bash
python install.py --recommend "build a web app" --json
python install.py --recommend "learn cybersecurity" --json
python install.py --recommend "improve my fitness and recovery" --json
```

Recommendations return exact profile names, scores, match reasons, pack/category metadata, and estimated source size. Recommendation mode is read-only.

Preview an exact selection:

```bash
python install.py \
  --profiles agency-backend-engineer agency-frontend-engineer \
  --dry-run \
  --json
```

Install an exact selection:

```bash
python install.py \
  --profiles agency-backend-engineer agency-frontend-engineer \
  --yes \
  --json
```

Install a category:

```bash
python install.py --category council:growth --yes --json
```

Install multiple categories:

```bash
python install.py \
  --category agency:engineering \
  --category agency:qa \
  --yes \
  --json
```

Install every profile in one pack:

```bash
python install.py --all --pack academy --yes --json
```

Install the entire repository:

```bash
python install.py --all --yes --json
```

## Non-interactive safety rules

- `--catalog` and `--recommend` never install anything.
- `--dry-run` resolves the exact selection without changing Hermes.
- Non-interactive writes require `--yes`.
- `--json` never prompts.
- Unknown profile names and invalid `PACK:CATEGORY` selectors fail closed with exit code `2`.
- Explicit profile selections are deduplicated before installation.
- Installation continues to use each pack's existing native `hermes profile install` flow.

A safe agent pattern is therefore:

1. `--catalog --json` or `--recommend ... --json`;
2. choose exact profile names;
3. `--dry-run --json`;
4. verify the returned plan;
5. repeat the exact selection with `--yes --json`.

## Recommendation behavior

Recommendations are local and deterministic. They score the existing catalog using profile names, display names, categories, descriptions, roles, jobs, pack intent, and a small vocabulary-expansion map for common terms such as web, API, security, fitness, finance, and learning.

This is deliberately not an LLM call. The selector remains fast, offline, inspectable, and predictable for both humans and agents.

The recommendation result is advice, not an installation decision. The user or calling agent still chooses the exact profiles to install.
