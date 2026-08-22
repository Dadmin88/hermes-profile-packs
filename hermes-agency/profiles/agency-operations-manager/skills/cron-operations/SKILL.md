---
name: cron-operations
description: Audit and operate scheduled Hermes work across profiles. Detect missed, failed, paused, degraded, or repeatedly unhealthy cron jobs; apply only bounded safe recovery; and route actionable evidence to the owning agent.
version: 1.0.0
author: Kyle French
license: AGPL-3.0-only
metadata:
  hermes:
    tags: [cron, operations, reliability, monitoring, incident-response]
---
# Cron Operations

## Overview

Use this skill to keep recurring Hermes work reliable across a roster of profiles. It provides an evidence-first workflow for inventorying cron jobs, checking durable run history, distinguishing real failures from intentional pauses or quiet schedules, applying narrowly safe recovery, and notifying the profile that owns the job.

The default mode is read-only. A cron job can publish, deploy, spend money, mutate data, contact people, or run privileged hooks; never assume that retrying or resuming it is harmless.

## When to Use

- Audit cron health across all Hermes profiles.
- Investigate a missed run, broken schedule, failed delivery, or recurring error.
- Prepare a scheduled-work reliability report.
- Determine whether a job should be retried, resumed, escalated, or left alone.
- Notify the owning profile about an actionable cron problem.

Do not use this skill to design new business workflows, silently rewrite job prompts, or bulk-enable old jobs. Use the owning specialty for workflow intent and obtain approval for consequential changes.

## Authoritative Commands

Always target the profile that owns the job. Do not assume the active profile's cron store represents the whole roster.

```bash
hermes profile list
hermes -p <profile> cron status
hermes -p <profile> cron list --all
hermes -p <profile> cron runs --limit 100
hermes -p <profile> cron runs <job_id> --limit 50
```

Bounded recovery commands exist, but they are mutations:

```bash
hermes -p <profile> cron run <job_id>
hermes -p <profile> cron pause <job_id>
hermes -p <profile> cron resume <job_id>
```

Never pass `--accept-hooks` merely to make an unattended recovery succeed. An unseen hook requires the same review and approval it would require outside this workflow.

## Audit Procedure

### 1. Establish scope and observation time

Record:

- profiles included;
- current local time and timezone;
- whether the audit is one-off or recurring;
- the run-history depth inspected;
- any profiles that could not be queried.

A profile omitted because of an error is unknown, not healthy.

### 2. Inventory profiles and jobs

Run `hermes profile list`, then inspect each in-scope profile with its explicit `-p` selector. For every job, capture:

- profile owner;
- job ID and name;
- enabled or paused state;
- schedule and expected cadence;
- last and next fire information when available;
- latest durable attempt and outcome;
- delivery target or conversational attachment when visible;
- whether the job uses a script, monitor, agent reasoning, or external side effects.

Do not read `.env`, auth stores, browser cookies, or credential values during a health audit.

### 3. Classify health from evidence

Use these states:

| State | Meaning |
|---|---|
| Healthy | Enabled and recent attempts match the expected cadence without actionable errors. |
| Intentionally paused | Disabled with evidence that the owner intentionally paused it. Do not resume. |
| Never run / insufficient history | No reliable baseline exists. Report separately; do not call it failed. |
| Missed or overdue | The expected fire window passed without a durable attempt and no documented pause explains it. |
| Transient failure | A bounded provider, network, timeout, or rate-limit failure with prior successful runs and no structural pattern. |
| Persistent failure | The same or related failure repeats, or retries do not recover. |
| Degraded result | The job completed but delivery, source coverage, output integrity, or downstream effect was incomplete. |
| Blocked on approval/configuration | The job requires a hook approval, credential, tool, destination, or owner decision. |
| Unknown | Evidence is missing, contradictory, stale, or inaccessible. |

A successful process exit does not prove delivery or semantic correctness. Inspect the durable attempt's result and delivery state where available.

### 4. Diagnose before changing state

For unhealthy jobs, determine the narrowest supported cause class:

- scheduler not running or profile inaccessible;
- job paused or disabled;
- invalid or surprising schedule;
- provider authentication or quota failure;
- tool, dependency, or hook approval failure;
- network timeout or temporary upstream outage;
- delivery target failure;
- prompt/runtime exception;
- monitor source or script failure;
- overlapping/long-running execution;
- repeated low-quality, empty, or partial output.

Do not infer a bad schedule from an unfamiliar cron expression. Check the actual next-fire behavior and timezone first.

### 5. Choose the response level

#### Observe only

Use when the job is healthy, intentionally paused, new, unknown, or consequential to retry. Record evidence and leave state unchanged.

#### Safe one-time retry

A single retry is allowed without additional approval only when all of the following are true:

- the failure is clearly transient;
- the job previously completed successfully;
- no run for the same fire is active or already succeeded;
- the job is idempotent or read-only;
- it does not publish, deploy, purchase, message external people, mutate production data, rotate credentials, invoke privileged hooks, or trigger destructive cleanup;
- the retry cannot create duplicate external effects;
- the current assignment explicitly authorizes safe remediation.

Run once, then inspect the new durable attempt. Never loop retries.

#### Approval required

Obtain approval before:

- editing a schedule, prompt, delivery target, script, monitor, or toolset;
- resuming a paused job without explicit evidence that the pause was accidental;
- pausing a job except to contain an immediate, demonstrated harmful loop;
- removing a job;
- restarting a gateway or scheduler;
- accepting unseen hooks;
- changing credentials, models, provider configuration, permissions, or billing;
- rerunning any job with publishing, deployment, financial, messaging, production mutation, or destructive effects.

#### Emergency containment

If a job is actively repeating harmful external effects, pause only the exact job needed to stop the damage, preserve evidence, and notify the owner immediately. Do not broaden containment to unrelated profiles or jobs.

### 6. Verify every mutation

After any approved action:

1. Re-run `cron list --all` for the owning profile.
2. Inspect `cron runs <job_id>`.
3. Confirm the intended state transition or new attempt exists.
4. Check the actual result and delivery outcome.
5. Record what changed, who authorized it, and what remains unresolved.

Issuing a command is not proof of recovery.

### 7. Notify the owning profile

Use Bot Mode's agent handoff or Agent Inbox when available. Keep the message operational and evidence-based:

```text
Cron issue: <job name> (<job_id>)
Profile: <owner>
State: <classification>
Evidence: <latest attempts, timestamps, exact failure>
Action taken: <none | one safe retry | approved containment>
Result: <verified outcome>
Owner decision needed: <specific next action or none>
```

Do not send healthy-job noise. Notify immediately for harmful loops, repeated failures, missed critical runs, delivery failures, or blocked owner decisions. Aggregate lower-severity findings into a concise review.

## Recurring Review Pattern

A scheduled audit routine should:

1. inspect all profiles read-only;
2. compare against durable run history rather than chat claims;
3. emit nothing when there are no actionable changes, if the delivery surface supports silence;
4. retry at most one clearly safe transient failure;
5. notify the owning profile for unresolved problems;
6. maintain a stable summary so repeated unchanged failures do not create duplicate alerts.

Do not create a self-triggering repair loop. The audit routine must not schedule, edit, or recursively invoke itself.

## Reporting Format

Lead with actionable exceptions:

```text
Cron health: <healthy count> healthy, <actionable count> actionable, <unknown count> unknown

ACTIONABLE
- <profile> / <job>: <classification> - <evidence> - <next owner action>

REPAIRED
- <profile> / <job>: <bounded action> - <verified result>

UNKNOWN
- <profile>: <why it could not be assessed>
```

Omit empty sections. Include timestamps and job IDs when they materially aid follow-up.

## Common Pitfalls

1. **Auditing only the active profile.** Every profile has isolated cron state; use `hermes -p <profile>` for each owner.
2. **Treating disabled as broken.** A pause may be intentional. Require evidence before resuming.
3. **Retrying arbitrary jobs.** Cron jobs can have irreversible external effects. Apply the safe-retry gate first.
4. **Calling process success healthy.** Verify semantic result and delivery, not only exit status.
5. **Using `--accept-hooks` in automation.** This bypasses a meaningful approval boundary.
6. **Fixing symptoms repeatedly.** A second similar failure is persistent; stop retrying and escalate the root cause.
7. **Alerting on every healthy run.** Report changes and actionable exceptions, not heartbeat noise.
8. **Reading secrets to diagnose auth.** Report the missing/failed credential class without exposing values.

## Verification Checklist

- [ ] Every in-scope profile was queried explicitly.
- [ ] Disabled jobs were distinguished from failed jobs.
- [ ] Durable attempts and delivery outcomes were inspected.
- [ ] Unknown profiles/jobs were reported as unknown.
- [ ] Any retry passed the full safe-retry gate and occurred only once.
- [ ] No unseen hooks, credentials, schedules, prompts, or destructive actions were changed without approval.
- [ ] Every mutation was re-read and verified.
- [ ] Actionable findings were routed to the owning profile with evidence.
- [ ] The final report is concise and suppresses healthy-job noise.
