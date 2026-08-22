---
name: adversarial-assessment
description: Conduct an authorized adversarial assessment to identify exploitable assumptions, abuse paths, privilege escalation, and control failures.
---
# Adversarial Assessment

Use only within explicitly authorized scope for defensive security validation.

## Procedure
1. Confirm target, authorization, boundaries, test environment, prohibited actions, and evidence-handling rules.
2. Model attacker goals, trust boundaries, identities, assets, and likely entry points.
3. Prioritize abuse paths that cross privilege, data, execution, or tenant boundaries.
4. Test hypotheses carefully, using the least destructive method that can establish impact.
5. Stop or escalate if validation could damage data, disrupt production, or exceed authorization.
6. Document each confirmed finding with preconditions, path, impact, evidence, and defensive remediation.
7. Re-test remediated critical findings where authorized.

## Quality gate
Do not report speculative attack chains as confirmed. Findings must distinguish observed exploitability from theoretical risk and remain within authorized defensive testing.