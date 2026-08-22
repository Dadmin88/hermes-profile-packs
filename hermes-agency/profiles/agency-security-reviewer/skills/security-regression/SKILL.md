---
name: security-regression
description: Review and validate changes for regression of previously enforced security boundaries, fixed vulnerabilities, hardening controls, negative tests, and assumptions that may be weakened by refactoring, migration, dependency, or configuration changes.
---
# Security Regression Review

Use when a change touches code or configuration near a prior security finding, trust boundary, auth control, sensitive parser/input path, secret handling, or defense-in-depth mechanism.

## Procedure
1. Identify the security properties that must remain true and gather the prior finding, threat model, incident, test, architecture decision, or control that established them.
2. Map the current change to those properties: enforcement functions, middleware/policy, schemas/validators, dependency versions, configuration defaults, database filters, infrastructure policy, tool capabilities, and error/log behavior as relevant.
3. Review whether the change bypasses, duplicates, moves, weakens, or makes the control conditional on a new path or default.
4. Re-run the original security regression/negative test when one exists and confirm it exercises the current authoritative boundary rather than an obsolete implementation path.
5. Add nearby variants when the refactor introduced new endpoints, alternate resource identifiers, bulk operations, async jobs, provider adapters, AI tools, or distributed execution routes that could reach the same authority differently.
6. Check secure defaults and configuration migration. A control that remains in code but defaults off or is omitted on new nodes/environments can still regress.
7. Review compatibility/fallback paths so old clients, rolling versions, degraded modes, or provider fallback do not silently use weaker enforcement.
8. Verify monitoring/detection added for the original problem still observes the new path and does not depend on removed log/event fields.
9. Classify evidence as regression confirmed, property preserved, or insufficient evidence; do not infer preservation merely because the original exploit string/path no longer works.
10. Update durable regression coverage and security documentation/control references so the next refactor tests the security property rather than one historical implementation detail.

## Decision rules
- Security regression tests should encode the protected property, not a brittle exploit payload alone.
- Refactoring can move enforcement safely, but every reachable path still needs the same authoritative property.
- “The old bug does not reproduce” is weaker evidence than demonstrating why the forbidden action is still impossible.
- When Fleet adds new placement/transport paths, re-evaluate security properties at those boundaries without moving application authorization into Fleet by accident.

## Quality gate
The review is complete when the original security property is explicit, the changed and alternate paths are traced to current enforcement, regression/negative evidence covers the property, configuration/mixed-version/degraded paths do not weaken it, monitoring still observes relevant failures, and any gap is reported as a concrete boundary risk.