---
name: dependency-risk
description: Assess software dependency and supply-chain risk using inventory, provenance, advisories, reachability, install/build behavior, maintenance signals, update impact, and compensating controls.
---
# Dependency Risk

Use when adding or updating a dependency, reviewing a release, investigating a vulnerable package, or assessing software supply-chain exposure.

## Procedure
1. Identify the exact dependency graph relevant to the shipped artifact, including direct and transitive packages, versions, lockfiles, build-time dependencies, plugins, container/base-image components, generated binaries, and platform packages where applicable.
2. Establish provenance for high-impact dependencies: canonical source, expected publisher or maintainer, package registry identity, release/tag relationship, checksums/signatures/attestations when the ecosystem provides them, and whether the package name could be confused with another project.
3. Review known vulnerability information from authoritative advisories and the affected project's own security information where available. Record the exact affected versions and conditions rather than assuming every advisory applies equally.
4. Determine reachability and exploit conditions in this system. Identify whether the vulnerable feature, parser, protocol, permission, platform, or code path is actually present and what attacker control is required.
5. Review install and build behavior for scripts, native compilation, downloaded binaries, code generation, network fetches, post-install hooks, or other execution that expands the trust granted merely by installing the package.
6. Review runtime privilege and exposure. A small transitive dependency reachable from untrusted network input or privileged build credentials may deserve more attention than a high-scoring issue in unreachable tooling.
7. Review project health relevant to risk: release cadence, security response, maintainer continuity, ownership changes, repository/package mismatch, unexpected version jumps, and whether the dependency has become unnecessary or replaceable by standard-library/project code.
8. Evaluate remediation options in order of reliable risk reduction: remove the dependency, upgrade to a fixed version, disable or isolate the vulnerable feature, narrow privileges/exposure, apply an upstream-supported patch, or document a time-bounded compensating control.
9. Test upgrades against the real integration and review lockfile/graph changes for unexpected new dependencies or build behavior. Preserve a rollback path for consequential updates.
10. Record residual risk, evidence, affected artifact versions, and the trigger for re-evaluation. Do not treat a scanner's severity number as the complete risk decision.

## Decision rules
- Dependency count is attack surface; add a package when its value justifies the trust and maintenance cost.
- Vulnerability severity and system risk are related but not identical. Reachability, attacker control, privilege, and compensating controls matter.
- Avoid unreviewed installers or commands copied from package documentation when the same change can be inspected and pinned explicitly.
- Pinning prevents surprise movement but also preserves known vulnerabilities; updates still require a deliberate process.

## Quality gate
The assessment is complete when the shipped dependency graph and provenance are understood, relevant advisories are evaluated in system context, risky install/runtime behavior is explicit, remediation is tested, and residual supply-chain risk has an owner and re-evaluation trigger.