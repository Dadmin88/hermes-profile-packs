---
name: desktop-packaging-signing
description: Build reproducible desktop packages with correct assets, native dependencies, permissions, signing/notarization inputs, architecture targets, and install/uninstall behavior.
---
# Desktop Packaging Signing

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using build inputs, target OS/architectures, certificates via approved secret handling, assets, native deps, and release version. Do not fill material gaps with assumptions when they can change the result.
3. Pin toolchain, build from clean state, verify bundled resources/native libraries, produce per-platform artifacts, sign where required, and test install/launch/uninstall on clean hosts.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
Artifacts install and launch on clean target systems and can be traced to exact source/build inputs.
