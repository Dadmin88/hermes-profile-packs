---
name: service-template
description: Design a maintainable service or workload template that captures approved defaults without freezing consumers to stale generated code, hidden infrastructure assumptions, or unsafe credentials.
---
# Service Template

Use when a platform needs repeatable starting artifacts for a common service, worker, application, or integration pattern.

## Procedure
1. Define the workload class, supported runtimes/stacks, and which concerns the template should solve versus leave to the application team.
2. Inventory the minimum approved defaults: project layout, build/test entry points, configuration contract, health behavior, identity, telemetry, deployment metadata, ownership, and documentation.
3. Keep generated code minimal and ordinary. Prefer platform-provided reusable capabilities for evolving behavior rather than copying large framework/platform internals into every repository.
4. Do not embed credentials, node addresses, environment-specific secrets, mutable resource IDs, or assumptions about one deployment target. Resolve environment/runtime details through accepted configuration and platform contracts.
5. Make parameters explicit and validate them before generation. Avoid a combinatorial template with switches for every historical exception.
6. Define how dependencies and versions are selected, pinned, upgraded, and audited. Template creation should produce a reproducible starting state.
7. Include a small executable example or smoke path that proves the generated project can build/test/run using the supported workflow.
8. Define template evolution. Separate fixes that should reach existing services through shared tooling/dependencies from changes that only affect newly generated projects; provide migrations when existing consumers need updates.
9. Test generation from a clean environment and validate the result as a consumer would, including CI/deployment integration where practical.

## Decision rules
- A template is a starting point, not a control plane.
- Avoid copying logic into every service when a maintained shared capability can enforce or deliver it centrally.
- Do not add options until real consumers demonstrate distinct needs.
- Fleet-compatible workloads should remain portable; placement-specific state belongs to Fleet/node runtime metadata, not the template.

## Quality gate
The template is ready when clean generation produces a small understandable project with approved defaults, no machine-specific or secret state is embedded, versions are reproducible, the supported workflow succeeds from scratch, and there is a clear strategy for future platform changes affecting existing consumers.