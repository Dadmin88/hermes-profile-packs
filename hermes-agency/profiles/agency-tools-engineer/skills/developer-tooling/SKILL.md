---
name: developer-tooling
description: Build developer tooling that turns a repeated engineering workflow into a fast, safe, discoverable, scriptable, and diagnosable interface.
---
# Developer Tooling

Use for CLIs, code generators, local dev tools, linters, repository automation, and engineering utilities.

## Procedure
1. Observe the actual workflow and identify repeated friction, unsafe manual steps, or missing feedback.
2. Define the primary user and the smallest command/interface that removes that friction.
3. Make defaults safe and common usage obvious; expose advanced control without forcing it on every user.
4. Design stable input/output and exit behavior so the tool can be scripted and composed.
5. Provide actionable error messages with enough context to recover.
6. Avoid destructive behavior without explicit intent, previews, backups, or idempotent semantics where appropriate.
7. Test across representative environments and failure cases.
8. Document installation, examples, and troubleshooting close to the tool.

## Quality gate
The tool should reduce cognitive and operational load. A wrapper that merely hides errors or adds another mandatory step is not an improvement.