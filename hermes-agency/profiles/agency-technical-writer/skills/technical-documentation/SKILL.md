---
name: technical-documentation
description: Produce precise developer and operator documentation from verified implementation, interfaces, constraints, examples, and failure behavior.
---
# Technical Documentation

Use for READMEs, API docs, architecture explanations, runbooks, migration guides, developer setup, and integration docs.

## Procedure
1. Verify the current implementation, version, interfaces, and supported environments.
2. Identify the technical audience and the task or mental model they need.
3. Document prerequisites, contracts, invariants, configuration, and examples using exact names and commands.
4. Explain failure modes and recovery where operationally important.
5. Keep conceptual explanation separate from step-by-step procedures.
6. Run commands or examples where practical and ensure code samples are internally consistent.
7. Remove stale references and implementation archaeology that does not help a current user.

## Quality gate
A competent reader should be able to use or operate the system from the documentation without reverse-engineering the codebase first.