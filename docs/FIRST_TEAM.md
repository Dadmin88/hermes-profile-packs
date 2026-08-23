# Your First Useful Team

The fastest way to understand Profile Packs is not to install all 160 profiles. Start with one real outcome, choose the smallest useful recipe, prove the profiles work, then expand only when another specialty earns its seat.

## 1. Pick an outcome

Examples:

- "Build and ship a small web feature."
- "Help me reset my routines and priorities."
- "Teach me defensive cybersecurity."

Ask the main installer:

```bash
python install.py --recommend "build and ship a web feature"
```

If one Team Recipe is a strong, unambiguous match, the installer promotes it. If the goal is broad or several recipes are plausible, it keeps the recommendation at the individual-profile level instead of forcing a formation.

Inspect the recipe before installing:

```bash
python install.py --recipe software-delivery --tier minimal --dry-run
```

## 2. Install the smallest coherent tier

```bash
python install.py --recipe software-delivery --tier minimal --yes
```

Do not upgrade to `recommended` or `expanded` because the names look useful. Add roles when the work actually crosses into their specialty, when independent review is justified, or when a clean parallel seam exists.

You can also run `python install.py` and use the interactive recipe-aware wizard.

## 3. Prove one real workflow

### Agency proof

Give the team one bounded software outcome with checkable acceptance criteria.

A healthy flow looks roughly like:

Product intent -> architecture only if needed -> one implementation owner -> independent review/QA -> Git/release closure.

Success means you can point to the deliverable, owner, evidence, and next state without reconstructing a long chat transcript.

### Council proof

Start with the minimal `personal-reset` or another relevant Council recipe. Let `council-steward` identify the smallest domains that matter. Share only the context each specialist needs.

Success means you leave with a small practical plan, specialists did not absorb unrelated private context, and the user remains the decision-maker.

### Academy proof

Start with `cybersecurity-learning` or `technical-study`. Let `academy-dean` route to the narrowest useful faculty.

Success means the learner can apply the material to a different example, not merely repeat the explanation.

## 4. Verify in fresh sessions

After installation, open the installed profiles through the normal Hermes profile/alias surface and verify:

- the profile identifies the correct role;
- its boundaries match the shipped SOUL;
- relevant bundled skills are available;
- a multi-profile recipe produces at least one clean handoff or independent review where expected.

See `docs/INSTALLATION_VERIFICATION.md`.

## 5. Expand only for a reason

Move from minimal -> recommended -> expanded when at least one is true:

- a new specialty owns a material decision;
- independent review is worth its cost;
- work can be split into independently verifiable packages;
- the critical path genuinely benefits from parallelism;
- a recurring operational need justifies another specialist.

If you cannot explain what the new profile uniquely owns, do not add it yet.

## What success looks like

You installed a small set rather than the whole catalog, completed a real outcome, saw correct role boundaries and at least one useful handoff/review, and can name exactly why you would add the next profile.
