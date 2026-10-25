# Hermes Wear

Standalone, portable Hermes profile distribution for a Wear OS wrist assistant. This distribution is separate from the Agency, Council, and Academy team catalogs.

From this repository checkout:

```sh
hermes profile install ./hermes-wear --name hermes-wear
```

Use a fresh profile or review an existing profile before updating it. Select a model and authenticate its provider independently through the installed Hermes version's native commands. No provider, deployment address, private preferences, or server-specific configuration is included.

Only identity, reusable behavior, minimal tool configuration, and one interaction skill are distributed. Personal data, memories, history, authentication material, databases, logs, pairing state, and device credentials are excluded. Publishing this template does not modify the running device profile.

The watch application, relay, background execution, notifications, speech, and structured approvals require separately configured integrations. This template does not claim those capabilities are installed. Configured tool limits should be combined with a restricted runtime user and filesystem boundary. An operator must enforce consequential-action authorization outside the prompt.
