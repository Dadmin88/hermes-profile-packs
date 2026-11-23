# Separate the verdicts

| Dimension | Evidence | A failure that must remain visible |
|---|---|---|
| Style | Matched-camera reference comparison, focal crops, HUD on/off, later gameplay moments | Wrong palette relationships, generic material, lost silhouette or mismatched typography |
| Playability | Input-driven session with a real goal, failure/recovery where relevant, result and restart | Static showcase, prerecorded game, unreachable goal, decorative controls |
| State and restart | Boundary tests and repeat-action traces | Double rewards, stale UI, duplicated entities, leaking listeners/audio, broken saves |
| Build | Clean install and production build/preview logs | Dev-only routes, missing assets, exposed keys, unavailable dependencies |
| Performance | Named hardware/browser/resolution, frame time and resource counts, high/low comparison | FPS claims without measurement or a low mode that destroys visual identity |
| Assets | Provenance, accepted/rejected outputs, runtime integration captures | Pretty raw assets that do not work at gameplay scale |

## Exercise actual interaction

Drive keyboard, pointer or touch events through the public game controls. Read-only state hooks may help diagnose or choose an action; mutation hooks or solved fixtures cannot stand in for a full playthrough. Unit tests may load fixtures to verify rules, and those results must be labelled separately. Record input traces and game footage. Include pause, resize, blur, restart, save reload, repeated rewards and relevant failure paths. Report what was and was not exercised.

Use quality controls that are sensitive to known failures. Deliberately try a missed gate, a duplicate pickup, an empty inventory, a wrong machine port, a blocked route or a paused timer. A test that always succeeds is not evidence of a working rule. Visual review should inspect both a matched opening and later states where a generated asset or camera can drift.

## Source-bound review

`freeze CASE` fingerprints the contracts and app sources (excluding dependencies, build output and review folders), writes `review/source-snapshot.json` and resets signoffs. It does not create an immutable source copy or build anything. Keep a Git commit or archive for immutable recovery; include a build-artifact hash in build evidence when needed.

After a check is genuinely completed, `evidence CASE style --file review/comparison.png --notes '...'` attaches local hashes and records an author's passed attestation. Each other category needs evidence too. `validate --release` refuses missing/incomplete contracts, changed references, stale source fingerprints and missing/changed evidence. It cannot determine that a screenshot looks good, that a log tells the truth or that an arbitrary file proves a category. An external reviewer must inspect the evidence.

Use explicit limitations. State “tested in Chrome on M4 at 1080p” rather than “runs at 60 fps everywhere.” Mark a generated recording as a motion reference and an input-driven recording as gameplay. Successful case studies are demonstrations, not a controlled estimate of skill effectiveness.
