# Hermes Wear device awareness v1

**Status: design and profile behavior, not a live integration.** The currently inspected Kotlin watch app, phone bridge and Node relay send chat, approvals, voice and run status, but they do not offer live GPS or a dedicated Hermes device tool catalog. The Wear app Android manifest presently has no location permission.

## Architecture

```text
Hermes Wear (dedicated profile)
  → authenticated read-only wear tool adapter (not yet implemented)
  → existing device-scoped relay / transport extension
  → Wear OS app, with phone companion fallback when explicitly allowed
  → versioned response with provenance, timestamp, accuracy, status
  → Hermes converts verified result into a concise response
```

Do **not** silently prepend a huge device dump to each prompt. Capability discovery is lightweight; measurements are on demand. The existing relay takes only plain text `input` in its native Runs API call, so the device adapter and reverse request/response channel are required before these can become genuine Hermes tools.

## Proposed tool inventory (none is automatically installed)

| Tool | Response | Default |
| --- | --- | --- |
| `watch.capabilities.list` | Supported/permission/available/source for each capability | Metadata read |
| `watch.device.snapshot` | OS/app identity, battery and connectivity summary | On demand |
| `watch.battery.status` | Percentage, charging, time, source | On demand |
| `watch.connection.status` | Watch network and phone-link status separately | On demand |
| `watch.location.current` | Position, precision, accuracy, time and source | Explicit on-demand foreground permission |
| `watch.notifications.capabilities` | Permission and delivery support, not delivered notification | Metadata only |
| `watch.health.capabilities` | Which sensors or Health Services types could be used | Metadata only; no readings by default |

Later `watch.health.*` readings and `watch.action.*` actions need independent user opt-in, Android permissions and backend authorization. No generic shell/browser tool or device admin access.

## Versioned response requirements

Capability manifest `schema: hermes-wear.capabilities.v1` includes `issued_at`, `device` and `capabilities`. Each capability has `id`, `supported` (OS/hardware), `permission` (`not_required`, `granted`, `prompt`, `denied`, `unknown`), `available` (working integration now), `source` (`watch`, `phone`, `relay`), and optional `reason`.

Tool result `schema: hermes-wear.tool-result.v1` includes `tool`, opaque `request_id`, `status`, `source`, `observed_at`, `data` on success and `error` on failure. Status is `ok`, `permission_required`, `permission_denied`, `temporarily_unavailable`, `unsupported`, `timeout`, or `error`. Validate result source and IDs against the currently authenticated device and Hermes session/run, not values supplied by a user message.

Location `data` must include latitude (-90..90), longitude (-180..180), nonnegative finite `accuracy_m` and `precision` (`coarse` or `fine`). `observed_at` is the **measurement timestamp**, not relay arrival. Values older than the caller's maximum age are **last known**, not current. When a location is fused with a phone and the source is ambiguous, say so. All JSON examples under `examples/` are **synthetic**.

## Safety, privacy and power

- Default to **location on request**, foreground only, no ongoing monitoring. The watch app must declare foreground coarse/fine permissions and request OS approval in context; a profile prompt cannot request them directly.
- A Wear OS fused location fix can originate from the phone. Use an actual source/accuracy result rather than guessing which GPS chip supplied it.
- Minimize precise locations; coarse is often enough for weather or neighbourhood questions. Request fine only when necessary and granted.
- **Never persist raw position or health sensor readings in profile memory, logs, relay SQLite or analytics by default.** The user may explicitly request a separately authorized saved-place operation.
- Immediately honor revoked permissions. A normal one-time location request does not authorize background location or health collection.
- Typed payloads must have size, expiry, rate, device/session and concurrency limits, with fail-closed errors. Do not inject JSON as privileged assistant instructions.
- Treat public audio and watch attention as privacy and safety constraints.

## Implementation and acceptance

1. Inspect Android APIs in the actual installed Watch6 version. Add a capability collector for no-permission battery/network/connected-node metadata, with explicit source and timestamps.
2. Add a bounded request/response path using existing authenticated device-scoped relay identities and the phone bridge, with opaque request IDs, timeouts, cancellation and no duplicate execution.
3. Add `watch.location.current` using Android on-demand foreground location (Fused Location Provider or suitable equivalent); prompt for OS permission, handle approximate, denial, null fix, timeout, stale cache, phone fallback and offline watch.
4. Register actual read-only named tools inside the isolated Hermes Wear runtime once its installed extension/tool API has been verified. Device and run binding must be checked **server-side**.
5. Unit/integration test valid data, unsupported/denied, stale and inaccurate data, two paired devices, mismatched request IDs, disconnects and duplicate requests. Test live on the physical watch: "Where am I?", "What's my watch battery?", and "Is my phone connected?".
6. Expand only after the minimal read-only path passes end-to-end. Health Services permissions depend on Wear OS/API target; health readings require separate consent.

The profile distribution does **not** implement phone call, messaging, GPS, sensor or notification hardware access by itself. This contract tells Hermes how to understand those capabilities when a genuine bridge is installed.
