---
name: mobile-permissions-native-apis
description: Integrate mobile permissions and device APIs with least privilege, contextual prompts, denied/restricted recovery, capability detection, and platform-specific behavior.
---
# Mobile Permissions Native Apis

Use when this procedure is the primary professional method needed for the assignment.

## Procedure
1. Confirm the decision or outcome this work must support, its scope, owner, constraints, and definition of success.
2. Establish the evidence baseline using device feature requirements, iOS/Android permission models, privacy requirements, UX states, and fallback behavior. Do not fill material gaps with assumptions when they can change the result.
3. Request only at point of value, separate capability availability from permission state, handle permanent denial, protect sensitive data, and test upgrade/settings transitions.
4. Exercise realistic edge, failure, transition, or exception cases that could invalidate the result; record unresolved uncertainty explicitly.
5. Validate the output against the original outcome and any neighboring professional contracts so this skill does not silently absorb another specialist's authority.
6. Record the resulting artifact, measurements, decisions, provenance, and handoff information needed for another owner to reproduce or continue the work.

## Quality gate
No feature assumes permission and every denial/restriction path leaves the user in a coherent recoverable state.
