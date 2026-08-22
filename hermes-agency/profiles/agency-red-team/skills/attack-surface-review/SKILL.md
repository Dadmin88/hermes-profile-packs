---
name: attack-surface-review
description: Map and prioritize a system's externally and internally reachable attack surface across identities, interfaces, data inputs, files, network paths, dependencies, automation, admin functions, agents/tools, and lifecycle operations for authorized defensive review.
---
# Attack Surface Review

Use before deeper adversarial testing or after architecture changes to identify which exposed boundaries deserve focused security validation.

## Procedure
1. Confirm system scope and authorization, then enumerate protected assets, sensitive operations, actors, trust levels, tenants, and administrative capabilities.
2. Inventory reachable interfaces: public/private APIs, web/app UI, CLI, RPC, webhooks, queues/events, file uploads/imports, plugins/extensions, remote management, support/admin tools, agent/tool endpoints, and service-to-service interfaces as relevant.
3. Map identity and trust transitions at each interface: unauthenticated to authenticated, user to admin, tenant to tenant, service/node to service/node, external provider to internal system, and untrusted content to AI/tool execution.
4. Trace accepted input types and parsers/transformations: text, structured data, URLs, archives/files/media, templates, code/config, serialized objects, database queries, model context, or provider events as relevant.
5. Inventory outbound authority and side effects available after each entry point: data access, filesystem, network, messaging, billing, provisioning, execution, secrets, credentials, profile/task routing, or administrative changes.
6. Identify shared dependencies and supply-chain surfaces whose compromise or misconfiguration could affect many components even without a public endpoint.
7. Include lifecycle/operational surfaces: install/update, migration, backup/restore, debug modes, diagnostics, recovery channels, feature flags, onboarding/invitations, and decommissioning.
8. Rank surfaces by reachability, privilege, data sensitivity, exploit preconditions, blast radius, historical weakness, and defense depth rather than endpoint count.
9. For the highest-risk surfaces, define focused defensive tests and owning specialist: authorization, injection/input handling, secret exposure, dependency risk, prompt injection, abuse cases, or infrastructure review.
10. Update the map after major interface, trust, node/Fleet capability, dependency, or administrative-workflow changes.

## Decision rules
- Attack surface includes trusted/internal interfaces when compromise or confused-deputy behavior can cross a meaningful boundary.
- The goal is prioritization and defensive coverage, not generating exploit instructions for systems outside authorized scope.
- A large surface is not automatically insecure; prioritize paths combining reachability, authority, and weak controls.
- Fleet/Keryx/Nodescale introduce distributed identity/transport/placement boundaries that belong in the map when reviewing that architecture, while Agency profiles themselves remain portable capability packages.

## Quality gate
The review is complete when meaningful entry points, identities/trust transitions, input types, outbound authority, dependencies, and lifecycle surfaces are mapped; high-risk combinations are prioritized with rationale; each priority has a defensive validation owner; and the map is specific enough to guide testing without drifting beyond the authorized system scope.