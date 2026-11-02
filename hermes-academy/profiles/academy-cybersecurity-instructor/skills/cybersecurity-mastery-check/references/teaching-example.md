# Authentication and object authorization: Transfer and feedback

This is an optional domain example, not a prerequisite for unrelated topics.

### Transfer task

A fictional photo service lets a signed-in user change photo IDs in a request. Ask what rule and two paper-only tests would protect private photos without trying any real service.

### Instructor key — withhold during an unaided attempt

Server checks authenticated actor permission for the requested photo. Owner allowed and different actor denied are required; add unauthenticated denial. IDs being hard to guess is not sufficient.

### Feedback

If identity is understood, teach only object permission. For a name slip, ask to reread actor/owner. For a UI-only control, explain the trust boundary and require a server-side check.

### Requested depth and early exit

Direct-answer example: No. A successful login does not grant access to every document; object-level authorization is required.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
