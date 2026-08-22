---
name: test-fixture-engineering
description: Build deterministic fixtures and test data with explicit lifecycle, ownership, isolation, and cleanup across parallel test execution.
---
# Test Fixture Engineering

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using schema, factories, external-service constraints, parallelism model, and cleanup behavior. Do not fill material gaps with assumptions when they can change the result.
3. Model fixture dependencies, generate minimal representative data, isolate mutable state, make cleanup idempotent, and detect leaked state.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Tests can run repeatedly and concurrently without order dependence or hidden shared state.
