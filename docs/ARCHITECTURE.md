# Profile Pack Architecture

Hermes Profile Packs separates reusable agent roles by durable context domain.

## Hermes Agency

Hermes Agency owns professional execution. Its profiles collaborate around projects, artifacts, technical decisions, design, product work, operations, marketing, QA, and delivery.

Namespace: `agency-*`

The Agency pack is imported from the existing standalone public distribution and retains its own manifest, validator, installer, evals, and tests inside `hermes-agency/`.

## Hermes Council

Hermes Council owns personal-life support. It is intentionally not a second work agency with softer names. Council profiles help the user reason, practice, plan, and build capability in bounded personal domains.

Namespace: `council-*`

The Council roster begins with:

- coordination: Council Steward
- growth: Life Coach, Learning Coach
- body: Fitness Coach, Nutrition Coach, Sleep & Recovery Coach
- family: Parenting Coach, Relationship Coach
- stewardship: Personal Finance Coach, Home Steward
- faith: Faith Guide

## Council routing model

`council-steward` is the default coordination profile. It should:

1. Identify the actual personal outcome requested.
2. Route to the smallest useful specialist set.
3. Share only minimum-necessary context.
4. Synthesize cross-domain advice without erasing disagreement or uncertainty.
5. Return control and decisions to the user.

Council is designed around privacy-aware separation of concerns. Fitness does not automatically need relationship history. Finance does not automatically need faith reflections. Parenting does not automatically need professional project context.

## Distribution versus runtime

The repository contains source distributions only. A live Hermes profile may also contain authentication state, caches, model catalogs, databases, logs, UI metadata, session files, gateway state, or environment configuration. Those are runtime artifacts and must not be copied into a public profile pack.

## Growth rule

Do not pre-design dozens of overlapping Council personas. Add a specialist when repeated real use demonstrates a durable domain that is not already owned cleanly by an existing profile or skill.
