---
name: dependency-review
description: Independently review third-party software dependencies for provenance, necessity, maintenance, known security advisories, privilege/runtime reach, transitive exposure, update policy, and safe replacement or containment.
---
# Dependency Review

Use when a change adds, upgrades, vendors, enables, or materially increases reliance on a third-party package, library, image, plugin, SDK, tool, or service component.

## Procedure
1. Identify the exact dependency name/source, version or revision, package/artifact provenance, intended use, and whether it executes at build, development, runtime, privileged, or user-facing boundaries.
2. Verify the canonical project/source and integrity mechanism available through the ecosystem: lockfile/digest/signature/checksum/provenance metadata as applicable.
3. Determine whether the dependency is actually necessary or whether existing platform/standard-library functionality can meet the requirement with lower long-term surface.
4. Review current maintenance signals and published security advisories from authoritative project/ecosystem sources when the review requires current risk information.
5. Inspect the dependency's effective reach: filesystem/network access, native code, code generation, build scripts/install hooks, deserialization/parsing, credentials, sensitive data, plugin loading, or other privileged behavior relevant to the integration.
6. Review transitive dependencies and feature flags/default modules that materially expand attack surface beyond the direct package.
7. Evaluate update/pinning policy and how security fixes will be adopted. A permanent pin without monitoring can freeze known defects; an unreviewed floating source can introduce unexpected code.
8. Review fallback/removal cost and containment. Keep third-party semantics behind a boundary when practical so replacement or emergency disablement does not require broad product rewrites.
9. Confirm licensing/provenance questions are routed to `agency-compliance-reviewer` where appropriate and that vendored Agency skills follow their dedicated third-party review rules.
10. Record risk, evidence, mitigations, accepted residual exposure, and the trigger for re-review when versions or project status change.

## Decision rules
- Popularity and download count are not security review evidence.
- A vulnerability scanner finding requires context, but absence of known advisories is not proof a dependency is safe.
- Minimize dependency privilege and enabled surface, not merely dependency count.
- Current advisory/maintenance facts should be verified from authoritative sources at review time rather than frozen into this skill.

## Quality gate
The review is complete when the exact dependency/provenance and execution reach are understood, unnecessary surface is challenged, current known-risk information is checked when applicable, transitive/privileged behavior is considered, update/containment/removal have owners, and acceptance is based on concrete evidence rather than ecosystem reputation alone.