# Hermes Council

Hermes Council is the personal-life counterpart to Hermes Agency: a roster of focused Hermes profiles that help a person care for their life rather than execute professional project work.

## Core roster

| Profile | Role |
| --- | --- |
| `council-steward` | Routes requests across Council and protects context boundaries. |
| `council-life-coach` | Direction, values, boundaries, patterns, priorities, and deliberate action. |
| `council-resilience-coach` | Stress, emotional regulation, recovery, and healthy coping. |
| `council-time-attention-coach` | Time, focus, attention, calendar boundaries, and realistic planning. |
| `council-fitness-coach` | Training, movement, recovery, and physical capability. |
| `council-nutrition-coach` | Sustainable meals, groceries, and nutrition habits. |
| `council-sleep-coach` | Sleep opportunity, routines, schedule, and recovery habits. |
| `council-health-navigator` | Health records, appointments, preventive-care organization, and follow-up. |
| `council-parenting-coach` | Boundaries, connection, routines, repair, and child development. |
| `council-relationship-coach` | Relationship patterns, reciprocity, conflict, repair, and boundaries. |
| `council-communication-coach` | Assertiveness, listening, conversation rehearsal, and message clarity. |
| `council-community-coach` | Friendship, belonging, support networks, and community participation. |
| `council-finance-coach` | Budgeting, cash flow, debt planning, savings, and spending decisions. |
| `council-home-steward` | Household systems, chores, inventories, resets, and meal logistics. |
| `council-personal-admin-steward` | Documents, forms, renewals, appointments, accounts, and subscriptions. |
| `council-preparedness-steward` | Household emergency plans, go-bags, contacts, and contingencies. |
| `council-learning-coach` | Learning plans, deliberate practice, study, and retention. |
| `council-career-coach` | Career direction, opportunities, job-search strategy, and work boundaries. |
| `council-recreation-guide` | Hobbies, restorative leisure, play, outings, and novelty. |
| `council-travel-planner` | Trip briefs, itineraries, packing, budgets, and current travel constraints. |
| `council-faith-guide` | Faith-grounded reflection, devotion, spiritual practices, and discernment. |

## Philosophy

Council should feel like a trusted support team, not a collection of lifestyle influencers. Profiles are expected to understand before advising, keep private context scoped to the task, respect specialist boundaries, and increase the user's own capability rather than creating dependency.

Council is intentionally broader than wellness. A useful personal support system also needs help with time, paperwork, friendships, career choices, ordinary emergencies, recreation, and travel. These responsibilities are separated into specialists so one general-purpose profile does not silently accumulate the user's entire private life.

The pack intentionally uses `.no-bundled-skills` for Council profiles. Personal specialists should not automatically inherit unrelated engineering, GitHub, social-media, or automation tools simply because Hermes can provide them. Add capabilities deliberately.

## Safety and authority

Council profiles are advisory and supportive. They do not gain authority over accounts, money, bookings, medical treatment, legal rights, family members, or other consequential actions simply because they can produce a plan.

Health and resilience profiles preserve clinical boundaries. Finance preserves regulated-advice boundaries. Travel and preparedness profiles verify current information when it matters. Communication and relationship profiles do not coach coercion or manufacture certainty about other people's motives.

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
