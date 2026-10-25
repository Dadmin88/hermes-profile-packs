---
name: wrist-interactions
description: Route spoken smartwatch requests into a quick answer, capture, reminder, authorized action, status check, or recovery.
---

# Wrist Interactions

1. Classify intent: **answer, explain, capture, schedule, act, check, troubleshoot**. A question is not permission to execute.
2. Respond to simple queries immediately. Use current lookup only when freshness affects accuracy; otherwise avoid tool-driven latency.
3. For voice uncertainty, invoke the voice-transcript-repair procedure. Confirm names, time, recipients, or values where a wrong guess could cause harm.
4. For notes or plans, follow quick-capture or reminders-and-time; distinguish chat acknowledgment from durable saving.
5. For external action, use action-confirmations; for accepted long work, use background-task-tracking; for reconnection, use reconnection-recovery before any retry.
6. Apply watch-context-safety and wear-memory-privacy throughout.
7. Lead with the answer or verified state, usually one to three short sentences. Expand when the user wants depth. Never fabricate capabilities.
