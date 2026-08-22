# Profile Pack Architecture

Hermes Profile Packs separates reusable agent roles by durable context domain.

## Hermes Agency

Hermes Agency owns professional execution: projects, artifacts, technical decisions, design, product work, operations, marketing, QA, and delivery.

Namespace: `agency-*`

## Hermes Council

Hermes Council owns personal-life support. Council profiles help the user reason, practice, plan, recover, organize, and build capability in bounded personal domains while sharing only minimum-necessary private context.

Namespace: `council-*`

## Hermes Academy

Hermes Academy owns teaching and instruction. It provides a faculty of professors and instructors spanning academic disciplines, technical subjects, vocational learning, and professional foundations.

Namespace: `academy-*`

`academy-dean` coordinates the faculty. It identifies the learning goal and level, routes to the smallest useful specialist set, and synthesizes cross-disciplinary teaching when needed.

Academy is distinct from Agency: an Academy Computer Science Professor teaches algorithms, data structures, and systems concepts; an Agency engineer executes production engineering work. Academy is also distinct from Council Learning Coach, which helps manage the learner's personal learning process rather than serving as the subject-matter faculty.

## Academy teaching contract

Academy profiles should:

1. Establish the learner's goal and approximate level when material.
2. Explain concepts at an appropriate depth.
3. Use examples and guided practice.
4. Check understanding instead of assuming explanation equals learning.
5. Give actionable feedback and correct misconceptions clearly.
6. Distinguish source facts, inference, simplification, and uncertainty.
7. Verify current standards, software behavior, regulations, or industry practices when they materially affect instruction.
8. Avoid pretending to award credentials, grades, licenses, or professional authority.

## Distribution versus runtime

The repository contains source distributions only. Live Hermes profiles may contain authentication state, caches, databases, logs, UI metadata, session files, gateway state, or environment configuration; none belong in this public repository.

## Growth rule

Add a specialist when it owns a durable teaching domain that cannot be represented cleanly by an existing faculty profile. Broad initial chairs may later split into deeper departments such as physics, chemistry, biology, philosophy, law, cybersecurity, welding, nursing, or language-specific instructors.
