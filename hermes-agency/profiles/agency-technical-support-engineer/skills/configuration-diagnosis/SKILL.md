---
name: configuration-diagnosis
description: Diagnose configuration failures by comparing effective values, precedence, environment, defaults, validation, and version compatibility rather than assuming the visible file is authoritative.
---
# Configuration Diagnosis

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using config files, environment variables, CLI flags, defaults, runtime introspection, and version docs. Do not fill material gaps with assumptions when they can change the result.
3. Identify all config sources and precedence, inspect effective runtime state, compare known-good baseline, validate schema/version, and test the minimal change.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
The fix targets the effective misconfiguration and does not require exposing secrets.
