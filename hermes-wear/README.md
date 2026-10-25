# Hermes Wear

Portable **Wear OS wrist assistant** profile, independent of Hermes Agency, Council, Academy, any particular owner, and any single watch application. Designed for a Galaxy Watch6-class device, but with no device ID or personal configuration bundled.

## Installation
From a checkout of this repository:

```sh
hermes profile install ./hermes-wear --name hermes-wear
```

Review changes before updating an existing installed profile. Select and authenticate a model through the installed Hermes release. No provider, endpoint, API credential, personal history, pairing state, log or database is distributed. Installing this source **does not** change the running watch instance until its backend is configured/updated to use it.

## What it contains

| Skill | Function |
| --- | --- |
| `wrist-interactions` | Route watch requests to the right workflow |
| `glanceable-answers` | Short, accurate, spoken-friendly answers |
| `voice-transcript-repair` | Recognize risky speech ambiguity and language mistakes |
| `quick-capture` | Capture notes, ideas and tasks with truthful save status |
| `reminders-and-time` | Interpret times and conditionally schedule alerts |
| `action-confirmations` | Verify parameters, permissions and external outcomes |
| `background-task-tracking` | Check running jobs and approval states |
| `reconnection-recovery` | Recover from stalls, disconnects and voice failures |
| `wear-memory-privacy` | Keep memory minimal, private and isolated |
| `watch-context-safety` | Public speech, limited attention and urgent situations |

The distributed toolsets are memory, session search, skills and read-oriented web lookup (only when supported/configured). The older profile shipped skills but **disabled its skills toolset**. Version 1.1.0 allows native skills lookup, while keeping terminal, file, browser, code execution, delegation, cron, computer-use, image generation and server-side TTS disabled. The skills toolset may expose native skill management; enforce normal Hermes write approvals and an OS-level restricted runtime identity.

**Capability ≠ instruction.** Watch notifications, timers, GPS, calls, texting, sensors, microphone/STT, audio playback, persistent backend runs, and structured approvals require separate integrations. This profile does not pretend they exist. Consequential actions additionally require actual backend permission enforcement.

## Watch acceptance tests
1. Confirm the watch backend actually selects the independent `hermes-wear` profile.
2. List skills/toolsets from the authenticated backend; check the expected ten skills are available.
3. Ask a fast fact, a long explanation, and an ambiguous dictated command.
4. Request a note and a reminder with no destination integration: it must explicitly disclose that nothing was saved/scheduled.
5. When narrow action integrations exist, verify confirmed/denied/expired approval and exact targeting.
6. Disconnect or time out during a job and reconnect: original status should be checked before any retry.
7. Verify text completion independently of actual audible output on the watch.
8. Verify private profile memory and no cross-profile information leak.

Repo checks:

```sh
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
```

The profile source alone cannot certify the installed watch app, backend, voice model, scheduler or notification path.
