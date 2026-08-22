# Hermes Council

Hermes Council is the personal-life counterpart to Hermes Agency: a roster of focused Hermes profiles that help a person care for their life rather than execute professional project work.

## Core roster

| Profile | Role |
| --- | --- |
| `council-steward` | Routes requests across Council and protects context boundaries. |
| `council-life-coach` | Direction, values, boundaries, patterns, priorities, and deliberate action. |
| `council-fitness-coach` | Training, movement, recovery, and physical capability. |
| `council-nutrition-coach` | Sustainable meals, groceries, and nutrition habits. |
| `council-sleep-coach` | Sleep opportunity, routines, schedule, and recovery habits. |
| `council-parenting-coach` | Boundaries, connection, routines, repair, and child development. |
| `council-relationship-coach` | Communication, reciprocity, conflict, repair, and boundaries. |
| `council-finance-coach` | Budgeting, cash flow, debt planning, savings, and spending decisions. |
| `council-home-steward` | Household systems, chores, inventories, resets, and meal logistics. |
| `council-learning-coach` | Learning plans, deliberate practice, study, and retention. |
| `council-faith-guide` | Faith-grounded reflection, devotion, spiritual practices, and discernment. |

## Philosophy

Council should feel like a trusted support team, not a collection of lifestyle influencers. Profiles are expected to understand before advising, keep private context scoped to the task, respect specialist boundaries, and increase the user's own capability rather than creating dependency.

The pack intentionally uses `.no-bundled-skills` for Council profiles. Personal specialists should not automatically inherit unrelated engineering, GitHub, social-media, or automation tools simply because Hermes can provide them. Add capabilities deliberately.

## Install

```bash
python install.py --list
python install.py council-life-coach council-fitness-coach
python install.py
```

The installer uses Hermes' native profile distribution command and sets the profile description from `distribution.yaml`.

## Adding a profile

A Council profile needs:

- a `council-*` name
- a distinct role that does not duplicate an existing specialist
- `distribution.yaml`
- `SOUL.md`
- one or more purpose-built skills
- a roster entry in `council.json` whose `jobs` correspond to installed skills

Do not commit live profile directories wholesale. Runtime profile folders contain authentication state, databases, caches, logs, and other private material that do not belong in a distribution.
