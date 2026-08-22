# cron-operations skill enrichment

- Source: authored for Hermes Agency
- Review date: 2026-08-13
- License: AGPL-3.0-only
- Assignment count: 1
- Profile: `agency-operations-manager`

## Why this profile

The Operations Manager already owns recurring operational work, service levels, reliability, incident coordination, and cross-team follow-through. Cross-profile cron health is therefore an operating-reliability responsibility, not a reason to create a second overlapping bot profile.

## Capability

`cron-operations` provides an evidence-first procedure to inventory cron state across isolated Hermes profiles, inspect durable run history, classify missed, failed, paused, degraded, blocked, and unknown jobs, apply at most one narrowly safe transient retry, verify every mutation, and notify the owning profile through Bot Mode handoffs or its Agent Inbox.

## Safety boundary

The skill is read-only by default. It requires approval for schedule or prompt edits, resume/pause operations outside immediate harmful-loop containment, job removal, gateway or scheduler restart, unseen hook acceptance, credential/model/provider changes, and retries involving publishing, deployment, payments, external messaging, production mutation, or destructive work. It forbids retry loops and requires post-action durable-run verification.
