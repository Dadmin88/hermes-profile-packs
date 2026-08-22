---
name: threat-modeling
description: Threat-model a system or change by identifying assets, actors, trust boundaries, entry points, abuse cases, controls, and prioritized mitigations.
---
# Threat Modeling

Use early in security-sensitive design and whenever a change creates a new trust boundary, privilege, data flow, or external exposure.

## Procedure
1. Define system scope, assets, sensitive operations, actors, and assumed trust.
2. Draw or describe data/control flows and mark trust boundaries.
3. Enumerate entry points and attacker goals, including compromised internal actors or dependencies where relevant.
4. Generate abuse cases around authentication, authorization, spoofing, tampering, disclosure, denial of service, privilege escalation, supply chain, and unsafe automation as applicable.
5. Review existing controls and identify where assumptions are not enforced.
6. Prioritize threats by plausible impact and exploitability rather than theoretical completeness.
7. Recommend design mitigations, validation, monitoring, and residual-risk owners.
8. Revisit the model when architecture materially changes.

## Quality gate
The model should change a design, test, control, or risk decision. A long threat list with no prioritized action is not useful.