# Reviewed profile source sync

Use this when an installed Hermes profile has local SOUL or skill changes that a
normal `hermes profile update` might overwrite.

**This is intentionally narrower than Hermes's native updater.** It syncs only
individually reviewed `SOUL.md` and `skills/<skill-name>` source packages. It does
not change an installed profile's `config.yaml`, model selection, personality,
credentials, memories, sessions, cron jobs, `distribution.yaml`, version,
profile metadata, or locally added skills. It never deletes files.

## Why a separate workflow?

Hermes's native update generally preserves user `config.yaml`, but it replaces
distribution-owned SOUL and skill files. A changed file may be a custom local
improvement, an older upstream version, or a combination. Without a trusted
three-way base, the safe default is to **show a difference and require explicit
approval**, not guess which side should win.

This script is for a trusted, local Profile Packs checkout and **only** for
installed profiles whose recorded `distribution.yaml` source matches that exact
checkout's profile directory. Missing manifests, unrelated installed profiles,
external sources, and mismatched paths are skipped in the catalog overview or
blocked in an explicitly requested profile.

## 1. Preview

From your maintained checkout:

```bash
python3 scripts/reviewed_profile_sync.py
python3 scripts/reviewed_profile_sync.py --profile agency-botfather
```

The read-only output counts unchanged, differing and source-new files. The
overview lists only changed source units and caps the list size. Locally added
skill packages that are absent from source are never candidates for deletion.

To inspect one exact SOUL or skill package, including a bounded text diff:

```bash
python3 scripts/reviewed_profile_sync.py \
  --profile agency-botfather --unit SOUL.md --diff

python3 scripts/reviewed_profile_sync.py \
  --profile agency-botfather --unit skills/academy-continuing-education --diff
```

The second command selects the **complete skill package**, including any
references or scripts it ships. The output includes a `plan_sha256` bound to
the exact source bytes, installed bytes and distribution metadata observed.
Inspect the diff and source before approving it.

## 2. Apply only explicitly selected changes

Copy the exact plan hash returned by the scoped preview:

```bash
python3 scripts/reviewed_profile_sync.py \
  --profile agency-botfather \
  --unit skills/academy-continuing-education \
  --apply --approve-plan YOUR_REVIEWED_PLAN_SHA256
```

The tool rechecks the source and installed files before writing. If either
changed since preview, it refuses the approval and requires another preview.

The apply writes only changed source files in approved units and retains extra
installed files even inside those skill directories. It uses atomic writes and
private, mode-preserving backups under
`~/.hermes/backups/reviewed-profile-sync/<backup-id>/`.

You can repeat `--unit` for a small set of packages in one approved plan.
There is no wildcard `--apply`, no automatic all-profile upgrade, and no
unattended change to an existing SOUL.

## 3. Roll back if needed

```bash
python3 scripts/reviewed_profile_sync.py --rollback BACKUP_ID
```

Rollback verifies the recorded post-update hashes before restoring earlier
bytes or deleting files that the selected sync had newly created. It fails
closed if a file changed again after synchronization, rather than overwriting
a newer local edit.

Backups may contain user-specific local SOUL or skill content and must remain
private. Never commit them to the public Profile Packs repository.

## Boundaries

- This is **content sync**, not a full profile distribution update. It does
  not bump an installed profile's recorded version or claim the entire
  distribution now matches the latest source.
- It does not edit native personality or model configuration, install or enable
  MCP tools, update runtime permissions, or touch other operational state.
- Skill contents are files, not executed by the sync tool. Approving a skill
  can still change an agent's future behavior; review it before applying.
- If a source cannot be matched, repair its recorded distribution source first
  using a separately reviewed, backup-backed process. Do not force an install.
- A 24-profile group on the historical Psalmbox deployment lacks native
  distribution manifests; that is a different provenance/adoption problem, not
  something this script should silently repair.
- New Hermes sessions may see approved SOUL or skill changes after syncing.
  Running sessions are not restarted, and this script does not prove a
  behavioral improvement.
