# CLI and case contracts

Requires Python 3.10+. Intake, prompts, integrity checks and the fal adapter use the standard library. Install `scripts/requirements.txt` for image tools. `inspect` uses `ffmpeg` and `ffprobe` for audio/video. The runtime helpers use standard ES modules and can be tested with Node 20+.

```bash
python3 scripts/r2g.py init /tmp/my-game --input /path/to/concept.png --input /path/to/motion.mp4 --brief "Make this playable"
python3 scripts/r2g.py init /tmp/text-game --brief "An ink-drawn railway mystery" --engine godot
python3 scripts/r2g.py inspect /tmp/my-game --frames 6
python3 scripts/r2g.py prompt /tmp/my-game --out /tmp/my-game/IMPLEMENT.txt
python3 scripts/r2g.py install-core /tmp/my-game
python3 scripts/r2g.py validate /tmp/my-game
python3 scripts/r2g.py review-page /tmp/my-game
```

Commands refuse to overwrite an existing case. `install-core` refuses an existing destination. All CLI outputs are JSON except the handoff prompt. Exit 0 is success, 1 is failed validation, 2 is a usage/data error. An inspection can partially succeed: review the per-reference `error` and `inspection` fields.

## Files

- `case.json`: schema version 1, title, engine, brief, references and generation policy. Reference IDs are unique; local paths are case-relative and hashed. URLs remain `link-only` until the agent opens them. Priorities are proposed intake order, not inferred artistic authority.
- `style.json`: draft/locked, anchors (`reference_id`, notes), palette (`role`, hex, reference_id or null), identity, materials, lighting, camera, UI, motion, nonnegotiables, avoid and deliberate changes. Add structured detail when useful.
- `game.json`: draft/ready, premise, actions, loop (`goal`, `success`, `failure_or_pressure`, `restart`), mechanics, invariants, levels and assumptions. Distinguish observations from authored rules in each mechanic.
- `assets.json`: items with unique IDs, references, representation, status and optional runtime_path. Release accepts statuses accepted/rejected/deferred; accepted items require an existing runtime_path.
- `review.json`: source fingerprint and six independent checks with status, notes and hashed evidence. Review is an author attestation with inspectable artifacts, not an automatic aesthetic grade.
- `analysis/`: inspection output and extracted frames. `production/`: asset work and private fal job records. `review/`: comparisons, test results, traces and recordings. `app/`: game source.

## Semantic palette and comparison

Create `points.json`: `[ {"role":"hero accent", "uv":[0.4,0.6], "radius":2, "reference_id":"ref-001"} ]`.

```bash
python3 scripts/r2g.py palette reference.png --points points.json --out sampled.json
python3 scripts/r2g.py compare reference.png capture.png --out review/comparison.png
```

Sampling uses oriented pixels and median RGB, ignores mostly transparent pixels and records source hashes. It does not perform ICC conversion or infer semantic roles. Normalize unusual color profiles in a documented derivative before using values as a style authority. Compare letterboxes instead of stretching; it does not register views or output a misleading universal similarity score.

Video extraction records requested timestamps, not a per-frame presentation-timestamp motion analysis. ffprobe metadata preserves frame-rate, SAR and rotation information. For exact timing work, inspect actual decoded frame timestamps and event boundaries separately.

## Review and generation

```bash
python3 scripts/r2g.py freeze /tmp/my-game
python3 scripts/r2g.py evidence /tmp/my-game style --file review/comparison.png --notes "Reviewed focal silhouette and palette; remaining gap recorded."
python3 scripts/r2g.py validate /tmp/my-game --release
python3 scripts/r2g.py fal-submit /tmp/my-game --asset hero --endpoint provider/model/edit --input request.json --estimate 0.20
# Add --execute only for an authorized real submission. The dry run above is offline.
python3 scripts/r2g.py fal-status /tmp/my-game JOB_ID
```

Endpoint names above are placeholders for a schema-verified endpoint, not working model recommendations. Every generation estimate is an estimate; failed or ambiguous jobs continue reserving budget conservatively. `fal-status` polls once so a caller can choose its own bounded wait policy.
