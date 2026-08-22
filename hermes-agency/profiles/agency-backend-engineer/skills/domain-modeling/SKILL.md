---
name: domain-modeling
description: Model backend business behavior with explicit terminology, invariants, state transitions, ownership boundaries, persistence mapping, and concurrency rules.
---
# Domain Modeling

Use when backend behavior has meaningful business rules, lifecycle states, ownership, or invariants that should not be scattered across handlers and persistence code.

## Procedure
1. Extract the domain language from accepted requirements, existing behavior, data, and user-facing terminology. Resolve materially conflicting terms before encoding them.
2. Identify the concepts with identity, the values without identity, the relationships between them, and the state transitions the system must permit or reject. Use entities, value objects, aggregates, or simpler structures only when those concepts actually clarify the model.
3. Write the invariants in plain language before implementing them. Examples include uniqueness, ownership, allowed transitions, quantity limits, ordering constraints, and conditions that must hold atomically.
4. Put rules near the model that owns them instead of duplicating them across routes, jobs, and controllers. Keep transport validation separate from domain invariants.
5. Define transaction and concurrency boundaries. Decide what must change atomically, what can tolerate stale reads, and what conflicts require optimistic locking, serialization, retries, or another explicit strategy.
6. Map the domain to persistence deliberately. Database tables, ORM records, external schemas, and cache representations may differ from the domain model; add translation where that separation protects the business rules.
7. Make lifecycle and failure states explicit. Avoid impossible or ambiguous combinations of flags when a finite state or structured type would represent the rules more clearly.
8. Test invariants and transitions directly, including invalid transitions, boundary values, duplicate/replayed operations, and concurrent behavior where relevant.
9. If modeling reveals a durable service or bounded-context boundary change, hand that architectural decision to `agency-software-architect` rather than silently redefining the system.

## Decision rules
- Prefer the simplest model that makes invalid behavior difficult to represent.
- Do not apply Domain-Driven Design vocabulary ceremonially. A plain function or data structure is correct when the domain is simple.
- Do not let framework, ORM, or API conventions dictate business rules.
- Preserve existing accepted semantics unless a product or architecture owner approves a change.

## Quality gate
The model is done when important business rules have one clear home, valid and invalid transitions are understandable, persistence and concurrency behavior preserve the invariants, and tests prove the rules rather than just the implementation shape.