---
name: security-review
description: Review a proposed or implemented change for security boundary violations, unsafe data handling, auth flaws, secret exposure, injection, and abuse risk.
---
# Security Review

Use for changes that affect authentication, authorization, sensitive data, external input, execution, networking, secrets, or trust boundaries.

## Procedure
1. Establish assets, actors, privileges, data sensitivity, and trust boundaries affected by the change.
2. Trace untrusted input and authority decisions through the implementation.
3. Review authentication, authorization, tenant isolation, validation/encoding, secret handling, cryptographic use, logging, dependencies, and failure behavior as relevant.
4. Look for confused-deputy behavior, privilege escalation, unsafe defaults, bypass paths, and information leakage.
5. Rank findings by realistic exploitability and impact.
6. Provide concrete remediation and validation steps.

## Quality gate
Every blocking security finding should identify the violated boundary or control and a plausible impact. Avoid generic hardening advice disconnected from the change.