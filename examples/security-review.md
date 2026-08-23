# Worked Example: Security Review

## Outcome

Assess a new authentication flow before release and produce actionable, verified findings.

## Composition

```bash
python recipes.py security-review --tier recommended --dry-run
```

## Ownership

Security Reviewer owns scope and review evidence. Security Engineer owns threat/design reasoning. Privacy/Compliance specialists own their respective concerns. Code Reviewer and QA provide independent correctness evidence. Red Team acts only inside explicit authorization and scope.

## Durable packages

1. Scope and assets under review.
2. Threat model and trust boundaries.
3. Implementation findings with reproduction/evidence.
4. Remediation tasks with owners.
5. Verification after fixes.

## Success

No finding exists only as "the model thinks." Material findings have evidence and severity rationale; remediation has an owner; accepted fixes receive independent verification; authorization boundaries remain explicit.
