# Installation Verification

Repository CI proves that Profile Packs source distributions are valid. This checklist answers a different question: **did the profiles actually install and behave correctly in this Hermes environment?**

No undocumented Hermes flags are required by this guide.

## 1. Installer result

The selected pack installer must finish without an error. If recipe installation is used, inspect the exact plan first:

```bash
python install.py --recipe software-delivery --tier minimal --dry-run
```

Then install that exact tier with `--yes`:

```bash
python install.py --recipe software-delivery --tier minimal --yes
```

## 2. Presence

Use the normal Hermes profile or generated alias surface you already use for installed profiles. Confirm every profile named in the recipe plan is available.

Do not treat a source directory in this Git checkout as proof of installation.

## 3. Fresh-session identity

Open a fresh session with one installed profile and ask it to state:

- its role;
- what it owns;
- what it should hand off;
- what completion means for its work.

The answer should match the shipped SOUL contract rather than a generic assistant identity.

## 4. Skill availability

Give the profile a task that should naturally call for one of its bundled skills. Confirm the procedure/behavior matches that specialty.

You do not need to force every skill into context. The proof is that relevant bundled capability is available when the matching task occurs.

## 5. Recipe interaction proof

For a multi-profile recipe, run one real handoff or independent review.

Examples:

- Backend Engineer -> Code Reviewer with artifact and evidence.
- Security Engineer -> Security Reviewer/Red Team within explicit authorized scope.
- Council Steward -> one personal specialist with minimum-necessary context.
- Academy Dean -> the most specific faculty member for a learning objective.

## 6. Source/runtime separation

Verify that normal use did not write runtime state back into this repository. Profile Packs source should remain free of credentials, sessions, logs, local memory, databases, and machine-specific state.

## 7. Evidence to keep

For a useful smoke proof, keep only what is needed:

- recipe id and tier;
- exact installed profile list;
- one fresh-session identity result;
- one handoff/review or teaching transfer result;
- any failure and its resolution.

Do not commit private runtime evidence into the public source pack.
