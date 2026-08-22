---
name: deliverability-review
description: Review email deliverability using current sender authentication, list quality, consent and complaint signals, bounce behavior, reputation, content, sending patterns, and provider evidence without relying on folklore.
---
# Deliverability Review

Use when email is landing poorly, bounce or complaint rates change, or a sending program needs preventative review.

## Procedure
1. Define the sender domains, infrastructure or provider, message types, audience sources, sending volume, and time window in scope.
2. Verify current authentication and domain configuration using provider and standards documentation appropriate to the sender environment.
3. Review acquisition and consent sources, suppression, invalid addresses, role or trap-like addresses, inactive recipients, and list hygiene practices.
4. Analyze hard and soft bounces, complaints, unsubscribes, deferrals, throttling, provider blocks, and reputation signals by domain or cohort where available.
5. Inspect volume changes, sudden cadence shifts, new domains or IPs, warmed versus cold sending, and campaign spikes that can alter reputation.
6. Review message structure, links, redirects, tracking, attachments, and rendering for technical defects without treating arbitrary forbidden-word lists as science.
7. Compare inbox placement or engagement evidence cautiously because opens can be affected by privacy and client behavior.
8. Recommend changes ranked by evidence and verify current provider requirements before implementation because mailbox policies change.

## Decision rules
- Deliverability is primarily sender trust, list quality, authentication, and behavior, not magic copy tricks.
- Hard bounces and complaints need operational action, not repeated retries.
- Verify current mailbox-provider requirements at task time.
- Never buy or scrape addresses to solve a reach problem.

## Quality gate
The review is ready when authentication and sending identity are verified, list and complaint evidence are understood, volume and reputation changes are correlated to symptoms, unsupported folklore is excluded, and remediation targets the strongest observed causes.