---
name: dependency-boundaries
description: Design and review dependency direction so components own clear responsibilities, depend on stable contracts, avoid cycles, and keep infrastructure or framework details from contaminating domain boundaries.
---
# Dependency Boundaries

Use when a system is becoming tightly coupled, a new component/service is being introduced, or an architectural change affects which modules are allowed to know about which others.

## Procedure
1. Map the current components/modules/services and the direction of their meaningful dependencies, including data schemas, shared libraries, events, runtime configuration, and generated code that can create hidden coupling.
2. Identify the concepts each boundary owns. A component should own a coherent set of decisions/data rather than exist merely because a directory or deployment unit exists.
3. Separate policy/domain behavior from delivery mechanisms and infrastructure details where that separation reduces change coupling. Framework objects, database records, transport payloads, and vendor SDKs should not become universal types by convenience.
4. Prefer dependencies toward stable abstractions owned by the capability provider. Consumers should not reach through another component to manipulate its storage or implementation internals.
5. Identify cycles and bidirectional knowledge. Break them by extracting the shared contract/concept, introducing an event or callback where appropriate, or re-evaluating whether the components are actually separate responsibilities.
6. Review shared libraries critically. A shared package is justified for a real stable cross-cutting contract or utility, not as a dumping ground that couples releases and ownership across unrelated components.
7. Define boundaries for data ownership. When multiple components need the same information, decide which is authoritative and how others receive/read it rather than allowing uncontrolled shared writes.
8. Consider deployment topology separately from code ownership. Two modules can share a process while retaining architectural boundaries; splitting them into services does not automatically improve the design.
9. Validate dependency rules with project conventions, module visibility, package boundaries, lint/static checks, or architectural tests where the ecosystem supports it.
10. Document exceptions that are intentionally accepted and the condition for revisiting them.

## Decision rules
- Avoid service boundaries that exist only to imitate an organizational chart or architecture trend.
- A dependency cycle often indicates confused ownership, but breaking every cycle mechanically can create worse indirection.
- Shared database access is a strong form of coupling and should be deliberate.
- Prefer clear data/control ownership over universal abstraction layers.
- Distributed deployment increases failure and operational cost; require a concrete reason before making a logical boundary a network boundary.

## Quality gate
The boundary design is ready when ownership and dependency direction are understandable, consumers use stable contracts rather than internals, data authority is explicit, cycles and shared-library coupling are justified or removed, and the structure reduces the number of places that must change together for ordinary evolution.