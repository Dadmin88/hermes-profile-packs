---
name: hermes-config-inventory
description: Inventory installed Hermes profiles, configuration scope, effective values, provider status, and authoritative selection metadata without changing state.
---
# Hermes Configuration Inventory

Use before changing Hermes settings, selecting profiles by criteria, comparing model assignments, or diagnosing configuration drift.

## Procedure

1. Resolve the active Hermes installation and inspect the running CLI's help for the relevant `profile`, `config`, `auth`, and `model` commands. Do not assume flags from another Hermes version.
2. List installed profiles through the supported profile interface. Record exact profile identity, active/default status, configured model when exposed, distribution identity, and gateway/activity indicators relevant to safe rollout.
3. For each candidate profile, use profile-scoped supported commands to locate configuration and read the requested keys. Distinguish an explicit local value from an inherited global value, a missing key, and a command/read failure.
4. Obtain category and role metadata from an authoritative installed catalog, registered profile description, or matching pinned pack manifest when available. Record the metadata source and revision. Never infer a side-effect target solely from substrings in a profile name.
5. If the requested selector depends on metadata that is absent, stale, or conflicting, identify the affected profiles and require user confirmation rather than silently classifying them.
6. For provider/model work, inspect provider authentication status and model availability using supported Hermes interfaces. Report only status, labels, identifiers, and capability—not credential contents.
7. Produce an inventory table with profile, selection metadata, configuration scope, effective value, explicit/inherited status, provider readiness, active-session impact, and any uncertainty.

## Safety rules

- Inventory is read-only. Do not call `config set`, `config unset`, credential-add/remove/logout, profile deletion, or gateway mutation.
- Do not read `.env`, `auth.json`, credential databases, browser stores, or secret-manager values to prove availability.
- Redact sensitive-looking values if an unexpected command exposes them; stop and report the exposure path without repeating the value.

## Quality gate

The inventory is complete when every candidate profile has an exact identity, the requested value is classified as explicit/inherited/absent/error, selector metadata has a cited source, provider readiness is known without secret access, and unresolved classification uncertainty is presented for user confirmation.