---
name: interface-design
description: Design durable software interfaces between components or services with explicit ownership, contracts, semantics, evolution, trust boundaries, and failure behavior.
---
# Interface Design

Use when two independently evolving parts of a system need a stable boundary such as an API, RPC, event, library interface, plugin contract, protocol, schema, or component boundary.

## Procedure
1. Identify the producer/provider, consumers, ownership boundaries, and the capability the interface must expose. Define what is intentionally hidden behind the boundary.
2. Model the contract in domain terms before choosing transport syntax. Specify operations or messages, inputs, outputs, identifiers, errors, state transitions, side effects, consistency expectations, and relevant timing/order semantics.
3. Minimize information leakage. Do not expose persistence layout, internal object graphs, implementation-specific errors, or incidental state that consumers do not need.
4. Define compatibility expectations: which behaviors can evolve additively, which require migration/versioning, how unknown fields/variants are handled, and whether producers/consumers may run different versions concurrently.
5. Define failure and retry semantics. State idempotency, duplicate delivery, timeout, cancellation, partial success, retryability, and how consumers distinguish permanent from transient failure where the interface requires it.
6. Define trust and authority at the boundary. Authentication context, authorization responsibility, validation, tenant scope, provenance, and untrusted external data should be explicit rather than inferred from call location.
7. Choose synchronous, asynchronous, streaming, or batch interaction based on latency, coupling, reliability, volume, and workflow needs rather than habit.
8. Record the interface using the ecosystem's executable or machine-readable mechanism where practical, plus examples for non-obvious semantics.
9. Validate risky assumptions with consumer/provider tests, prototypes, failure injection, or primary protocol documentation as appropriate.
10. Assign ownership for the contract and its evolution so changes do not become nobody's responsibility.

## Decision rules
- A good interface exposes capability and semantics, not internal structure.
- Use the simplest interaction model that satisfies the real reliability and latency needs.
- Compatibility is a consumer property, not merely a schema property.
- Do not invent a new protocol when an established project/platform contract fits.
- Cross-machine or distributed interfaces must make failure, replay, identity, and version mismatch explicit.

## Quality gate
The interface is ready when providers and consumers can implement independently from the same contract, ownership and trust are explicit, compatibility and failure semantics cover realistic deployment states, internal implementation details remain hidden, and the riskiest assumptions have evidence.