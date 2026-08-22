---
name: lifecycle-email
description: Design lifecycle email journeys around user state, trigger, value, timing, frequency, suppression, personalization, action, and measurable downstream behavior.
---
# Lifecycle Email

Use when email should respond to a user's or account's lifecycle state rather than a one-time campaign calendar.

## Procedure
1. Define the lifecycle state, audience eligibility, trigger, desired user outcome, and authoritative data that determines entry.
2. Map where email adds value relative to in-product messaging, support, sales, or no message at all.
3. Define sequence, timing, waiting periods, exit conditions, suppression, frequency caps, and behavior when the user advances before the next message.
4. Write each message around one useful job and action, using current product state rather than generic personalization tokens where possible.
5. Handle missing data, inactive accounts, plan or permission differences, time zones, and localization as relevant.
6. Coordinate unsubscribe, consent, transactional versus marketing classification, and current legal requirements with the appropriate compliance owner.
7. Instrument delivery, engagement, downstream product behavior, conversion, and negative signals such as complaints or unsubscribes.
8. Test the journey from trigger through exit using real lifecycle states before broad activation.

## Decision rules
- Lifecycle email should respond to meaningful state, not merely elapsed time.
- Stop messaging when the user has already completed the intended action.
- Open rates alone do not prove product value.
- Verify current deliverability and regulatory requirements at execution time.

## Quality gate
The journey is ready when entry and exit state are deterministic, timing and suppression prevent irrelevant messages, each email has one useful role, downstream outcomes and negative signals are measurable, and compliance or deliverability requirements are owned and verified.