---
name: platform-capability
description: Design and deliver an internal platform capability with a clear consumer contract, paved path, self-service interface, reliability expectations, and operational ownership.
---
# Platform Capability

Use for shared developer/runtime capabilities consumed by multiple teams or services.

## Procedure
1. Identify platform consumers and the recurring problem that justifies centralization.
2. Define a stable contract and abstraction boundary that hides accidental complexity without blocking necessary control.
3. Design a paved path for common cases and explicit escape hatches for legitimate exceptions.
4. Address tenancy, quotas, identity, secrets, observability, reliability, versioning, and backward compatibility.
5. Provide self-service provisioning or clear automation where manual platform-team intervention would become a bottleneck.
6. Build usage documentation and examples as part of the capability.
7. Measure adoption, failure modes, support burden, and whether the platform actually reduces consumer complexity.

## Quality gate
A platform feature should make repeated work easier for consumers. Centralizing complexity without a good interface merely moves the problem.