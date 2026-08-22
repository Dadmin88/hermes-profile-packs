# Profile Pack Architecture

Hermes Profile Packs separates reusable agent roles by durable context domain.

## Hermes Agency

Hermes Agency owns professional execution. Its profiles collaborate around projects, artifacts, technical decisions, design, product work, operations, marketing, QA, and delivery.

Namespace: `agency-*`

The Agency pack is imported from the existing standalone public distribution and retains its own manifest, validator, installer, evals, and tests inside `hermes-agency/`.

## Hermes Council

Hermes Council owns personal-life support. It is intentionally not a second work agency with softer names. Council profiles help the user reason, practice, plan, and build capability in bounded personal domains.

Namespace: `council-*`

The Council roster began with:

- coordination: Council Steward
- growth: Life Coach, Learning Coach
- body: Fitness Coach, Nutrition Coach, Sleep & Recovery Coach
- family: Parenting Coach, Relationship Coach
- stewardship: Personal Finance Coach, Home Steward
- faith: Faith Guide

Council has since expanded into additional health, resilience, time, career, administration, preparedness, recreation, travel, communication, and community specialties.

## Council routing model

`council-steward` is the default coordination profile. It should:

1. Identify the actual personal outcome requested.
2. Route to the smallest useful specialist set.
3. Share only minimum-necessary context.
4. Synthesize cross-domain advice without erasing disagreement or uncertainty.
5. Return control and decisions to the user.

Council is designed around privacy-aware separation of concerns. Fitness does not automatically need relationship history. Finance does not automatically need faith reflections. Parenting does not automatically need professional project context.

## Hermes Academy

Hermes Academy owns teaching and instruction. It provides a faculty of professors and instructors for academic disciplines, technical subjects, vocational learning, and professional foundations.

Namespace: `academy-*`

`academy-dean` is the coordination profile. It identifies the learning goal and approximate level, routes to the smallest useful faculty set, builds prerequisite-aware curriculum paths, and synthesizes cross-disciplinary instruction when needed.

Academy is intentionally distinct from the other packs:

- `academy-computer-science-professor` teaches algorithms, data structures, programming concepts, and systems foundations; Agency engineering profiles execute production software work.
- `academy-business-professor` teaches business concepts and case reasoning; Agency business profiles execute operational work.
- Council Learning Coach helps the person manage their learning process; Academy faculty teaches the actual subject matter.

Academy begins with broad chairs so it is immediately useful. These can later split into deeper departments such as physics, chemistry, biology, philosophy, law, cybersecurity, welding, nursing, automotive, or language-specific instructors.

## Academy teaching model

Academy faculty should orient to the learner, explain accurately, model reasoning, provide practice when useful, give specific feedback, and check transfer rather than assuming explanation equals learning. Direct answers are still appropriate when the learner simply wants a fact or concise explanation.

Teaching does not create credentialing or professional authority. Current standards, software behavior, codes, regulations, or industry practices must be verified when they materially affect instruction. High-risk real-world domains retain appropriate safety and supervision boundaries.

## Distribution versus runtime

The repository contains source distributions only. A live Hermes profile may also contain authentication state, caches, model catalogs, databases, logs, UI metadata, session files, gateway state, or environment configuration. Those are runtime artifacts and must not be copied into a public profile pack.

## Growth rule

Do not add overlapping personas merely to make a roster larger. Add a specialist when repeated real use demonstrates a durable domain that is not already owned cleanly by an existing profile or skill. Broad Academy chairs should split when a discipline needs genuinely distinct pedagogy, terminology, safety rules, tools, or depth.
