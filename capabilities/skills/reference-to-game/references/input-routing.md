# Intake by modality

| Input | Inspect | What it can establish | What remains a design decision |
|---|---|---|---|
| Screenshot / illustration / sketch | Full frame, focal crops, geometry, composition, annotations | Appearance, proportions, camera hints, visible interface | Hidden surfaces, level connectivity, rules, animation |
| Sheet / mood board / atlas | Whole sheet first, then named regions with coordinates | Asset vocabulary, variants, relationships | Whether panels are alternatives, sequence, or simultaneous state |
| Gameplay / generated video | Representative timestamps, cuts, action boundaries, background motion | Motion language, camera behavior, demonstrated interactions | Consistent physics, persistent counts, unseen controls |
| Real footage | Camera versus object motion, lighting, scale clues | Movement and material evidence | Playable abstraction, controls, pacing |
| GLB / model / scene | Open in a viewer, bounds, axes, topology, materials, pivots and rigs | Reusable geometry and animation | Camera, gameplay, art integration |
| Audio / music | Listen; examine duration, loop seam, dynamics | Mood, rhythm, impact character | Visual identity unless the user specifies it |
| PDF / design document | Render relevant pages; read headings and diagrams | Explicit requirements, labels, layout | Missing production details |
| URL | Resolve with browser or connector; retain stable source and local authorized evidence | Whatever the destination actually contains | Anything behind inaccessible pages; never fabricate inspection |
| Text only | Extract constraints, preferences and core action | Intended mood and game concept | Palette, composition and assets must be designed and labelled |
| Mixed folder | Inventory first; deduplicate; identify originals, revisions and finals | Cross-modal constraints | Authority when sources disagree |

`init --input` accepts repeated paths and HTTP(S) links. Directories include common media/document extensions, skip hidden/dependency folders and symlinks, and enforce intake limits. A directly supplied unknown file is preserved as `other`; it is not decoded. PDF, HEIC, SVG, FBX and similar formats may need external viewers. Do not promise universal file decoding.

The generated inventory stores content hashes and case-relative filenames, so moving the package does not break it. It does not rewrite originals, fetch URLs, execute scripts or recursively unpack archives. Keep reference archives outside the client bundle.

## Authority and uncertainty

Use each reference's `role`, `authority` array, `priority` and `notes`. Authority values can be `style`, `identity`, `mechanics`, `motion`, `ui`, `audio` or `historical`. Priority resolves ties only within the same dimension. Explicit user corrections take precedence.

A source observation should name a file/frame/region: “ref-002 at 3.4 s: vehicle tilts outward on landing.” An inference records uncertainty: “likely a chase camera; orbit is unobserved.” An authored rule records intention: “checkpoint resets speed and adds a penalty.” Do not turn UI decoration, impossible joints, morphing entities or duplicated pickups in generated video into invariants.

For sheets, identify panel boundaries from content. Do not force 2×2 or 3×3 layouts. If extracting a region, retain the source hash, normalized crop rectangle and purpose. A whole sheet can remain the visual authority even when production uses isolated crops.
