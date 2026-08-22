---
name: backend-service-implementation
description: Implement a backend service or API change from contract through domain logic, validation, persistence, failure handling, tests, and observability.
---
# Backend Service Implementation

Use for server-side application features, APIs, jobs, and domain behavior.

## Procedure
1. Read product acceptance criteria, architecture/interface decisions, existing conventions, and relevant data contracts.
2. Trace the current request/data path before editing.
3. Define or confirm inputs, authorization, validation, domain invariants, outputs, and error semantics.
4. Implement the smallest cohesive change while preserving compatibility unless a migration is explicitly approved.
5. Handle persistence boundaries, transactions, retries, and external dependencies deliberately.
6. Add tests at the cheapest layer that proves the changed behavior and important failures.
7. Run targeted checks and inspect logs/metrics or runtime behavior when applicable.
8. Hand off interface changes and migration implications to dependent specialists.

## Quality gate
The change is done when behavior is correct under normal and failure conditions, tests prove the relevant contract, and operationally important failures are diagnosable.