# Worked Example: Software Delivery

## Outcome

Add a small authenticated API feature with a usable UI and release it safely.

## Composition

Start with:

```bash
python recipes.py software-delivery --tier minimal --dry-run
```

## Ownership

- Product Manager: behavior and acceptance criteria.
- Software Architect: only material system/interface boundaries.
- Full-Stack Engineer: primary implementation owner.
- Code Reviewer: independent implementation review.
- QA Tester: end-to-end behavior/regression evidence.
- Git Steward: branch/commit/PR integration state.

## Durable work

Create separate tasks only where ownership is distinct. Keep implementation coherent under one owner unless the API/UI seam can genuinely be split and independently validated.

## Handoffs

Implementation -> Code Reviewer: artifact, commands/tests run, assumptions, known risks.

Implementation/review -> QA: expected user behavior, setup, edge cases, build under test.

QA/review -> Git Steward: exact accepted revision and remaining blockers.

## Success

The feature satisfies explicit acceptance criteria; review and QA are independent; source-control state is clear; the final result can be understood without replaying the conversation history.
