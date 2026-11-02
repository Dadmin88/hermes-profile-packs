# Authentication and object authorization: Worked reasoning

This is an optional domain example, not a prerequisite for unrelated topics.

### Worked example

Use a paper-only toy policy: users Alice and Bob; D.owner = Bob; allow read only when actor.id = D.owner. Alice passes authentication but fails the object check; Bob passes both. Enforce the check at the resource boundary for each request. Keep denial evidence minimal and avoid logging document contents or credentials. This example does not implement production authentication.

### Requested depth and early exit

Direct-answer example: No. A successful login does not grant access to every document; object-level authorization is required.

Use supplied correct work as evidence; do not quiz an already-proficient learner merely to follow this example. Offer a different challenge only when useful and wanted. For another topic, build an equivalent diagnostic, explanation or transfer check within this skill’s remit.
