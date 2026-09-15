---
name: ai-music-production
description: Produce original AI-assisted music and synthetic-artist projects from authorized references through rights-aware analysis, controlled generation, audio QC, provenance, and release handoff.
---
# AI Music Production

Use for recurring original song, instrumental, alternate-version, or synthetic-artist production where AI tools may assist composition, performance, editing, mixing, or mastering.

Use the templates in [references/production-templates.md](references/production-templates.md). Complete only fields relevant to the assignment, but do not omit rights, provider, spending, lineage, originality, QC, or handoff evidence when those stages apply.

## Evidence vocabulary

Label material claims consistently:

- **Observed:** directly perceived in supplied material.
- **Measured:** produced by a named tool with stated method or precision.
- **Interpretation:** professional analysis that is plausible but not directly measured.
- **Creative decision:** an intentional choice for the new work.
- **User-confirmed:** the user's recorded rights or permission claim; not independent legal clearance.
- **Provider-stated:** a capability or term stated by the provider at the cited source and access date.
- **Independently verified:** checked against authoritative evidence by the responsible owner.
- **Unresolved:** not established sufficiently to rely on.

Never convert one category into another silently.

## Workflow

### 1. Creative intake

Create the Creative Brief. Establish project ID, decision owner, audience, intended and commercial use, emotional/narrative function, supplied themes or lyrics, duration, structure, high-level genre/era attributes, instrumentation, non-identifying vocal direction, production intent, deliverables/formats, deadline, review points, privacy/upload constraints, prohibited outcomes, and acceptance criteria.

Identify which deliverables are mandatory, optional, or conditional on provider capability. Do not promise stems, vocal identity controls, reference conditioning, automation, or commercial rights before the relevant gate.

### 2. Rights and provenance check

Give every input a stable reference ID and complete the Reference and Permission Ledger.

For each reference, record source/citation, asserted owner, useful high-level traits, intended operation, permission status and basis, upload permission, commercial-use permission, restrictions, verification owner, and date. Allowed recorded statuses are `user-confirmed`, `licensed`, `public-domain`, `otherwise-authorized`, and `unresolved`.

A user statement is evidence of the user's claim only. It is not independent legal clearance. Do not upload, condition on, remix, or commercially exploit material while the required permission remains unresolved. Route unresolved licensing, voice consent, publicity, ownership, provider-terms, or release-rights questions to `agency-legal-ops` or qualified counsel.

Never continue lyrics provided only as copyrighted reference text. Do not place reference media, copyrighted lyrics, credentials, or private files in reusable profile artifacts.

### 3. Reference-feature analysis

Analyze only authorized, available references. Record source and confidence for each finding.

Cover, where supported:

- approximate tempo and meter;
- key, mode, harmony, cadence, chord rhythm, and harmonic movement;
- rhythm, pocket, subdivision, syncopation, and groove;
- instrumentation, register, density, texture, and timbre;
- arrangement, sections, transitions, repetition, and structure;
- energy curve, dynamics, tension, and release;
- non-identifying vocal range, register, articulation, density, delivery energy, ensemble role, and treatment;
- lyrical theme, perspective, image system, rhyme, phrasing, prosody, and narrative movement;
- production space, tonal balance, saturation, transients, stereo behavior, depth, effects, and mix priorities.

Do not claim exact BPM, key, tuning, loudness, or other measurements without an actual capable measurement. Mark unsupported precision as interpretation or unknown.

### 4. Originality and differentiation brief

Convert influence into function and attributes. Never pass a named artist, track, or voice identity to a generation prompt.

For every influence, state: the functional goal; high-level trait worth retaining; and the new work's meaningful difference. Define an original melodic vocabulary, harmonic route, chord rhythm, groove, form, energy curve, instrumentation/timbre, vocal boundary, lyrical premise, arrangement, and production space.

List explicit exclusions and comparison red flags, including recognizable melodic contour, hook rhythm, distinctive lyric phrases, signature arrangement events, identifiable vocal imitation, deceptive title/marketing, or source confusion. Obtain the decision owner's approval before generation.

### 5. Synthetic-artist concept and sonic identity

When the assignment includes an artist project, document a durable identity separate from track experiments:

- project/artist name and audience;
- artistic point of view, themes, emotional range, and catalog promise;
- original melodic, harmonic, rhythmic, lyrical, instrumental, and production vocabulary;
- non-identifying vocal direction;
- production signatures and catalog-coherence rules;
- intentional exclusions and identity-confusion safeguards.

A synthetic identity must not imply a real artist's participation, affiliation, endorsement, archive, lost work, or unreleased material.

### 6. Lyrics, composition, and arrangement

Compose deliberately before broad generation. Develop the premise, point of view, hooks, lyric architecture, melody, harmony, chord rhythm, groove, meter, form, arrangement, transitions, dynamics, and production arc.

Check lyric originality, singability, stress/prosody, section function, cliché density, perspective consistency, and fit with the approved identity. Check melody and harmony as musical material, not merely text prompts. Never reproduce or continue protected reference lyrics or recognizable reference melodies.

Create a controlled generation plan identifying fixed variables, the one or few variables changed per round, evaluation criteria, maximum takes, and stop conditions.

### 7. Provider capability, terms, privacy, and spending gate

Before using any selected tool or provider, complete the Provider Capability and Terms Check with an access date and evidence source. Verify actual support for reference upload/conditioning, lyrics conditioning, vocal controls, instrumental output, stems, editing, extension, remixing, seeds/reproducibility, export formats, API automation, metadata, ownership/commercial use, retention/privacy, and attribution/disclosure.

Treat technical capability and legal permission as separate gates. If a capability is unavailable, redesign the workflow or label the deliverable `unsupported`; never simulate stems, permissions, provenance, measurements, or exports.

Do not make a paid call without explicit authorization for a numeric total cap and currency. Record the cap, cumulative cost, remaining amount, and any later cap-change approval. Stop before exceeding the cap.

### 8. Controlled generation and versioning

Assign every generation or manual production state a stable take ID. Record parent take ID, tool/provider, exposed model/version, prompt, negative constraints, settings, seed/job ID when available, input reference IDs, output artifact ID or checksum, cost, result, defects, selection decision, and rationale.

Change major variables controllably. Preserve parent-child lineage for extension, remix, edit, comp, mix, master, and alternate versions. Never overwrite the only traceable selected source. Reject provider outputs that violate the originality brief, identity safeguards, rights gate, or technical constraints.

### 9. Selection, editing, and comping

Use explicit criteria: brief fit, musical identity, hook strength, melodic/harmonic originality, groove, structure, lyric/prosody quality, performance, absence of synthetic defects, editability, production potential, and comparison risk.

Provider scores may inform triage but cannot make the final creative decision. A human decision owner must approve the selected direction. Record rejected takes and concise reasons so later iterations do not repeat known failures.

Build edits and comps with traceable source take IDs, time ranges or section labels, processing decisions, and new child IDs. Listen across transitions and exposed edit points.

### 10. Mixing, mastering, and export

Mix and master only to the assignment's intended use and actual tool capability. Check applicable clipping, clicks, dropouts, noise, abrupt tails, exposed edits, synthetic artifacts, timing, tuning, transitions, low-end balance, vocal intelligibility, masking, stereo image, dynamics, and listening-system translation.

Measure applicable peak level, integrated loudness, true peak, noise floor, sample rate, bit depth, channel layout, duration, silence, and loop behavior with identified tools. Do not claim a measurement that was not performed.

Verify every requested export independently by opening or decoding it and checking file integrity, duration, format, and playback. For stems, verify common start time, expected tails, synchronization, polarity, silence, channel layout, and summed behavior. Mark stems `unsupported` when the provider did not supply genuine separations.

### 11. Originality comparison review

Compare the selected result with references at the attribute and protected-expression level. Review melody, hook contour/rhythm, harmony and chord rhythm, groove, form, signature events, lyric phrases, vocal identity, title/marketing, and overall source/affiliation confusion.

A high-level genre resemblance is not itself a failure; recognizable protected expression or identity confusion is. Quarantine the candidate when overlap is plausible and material. Revise it or escalate uncertain rights and release implications. Record reviewer, method, evidence, and decision.

### 12. Metadata, provenance, and release handoff

Complete the Track Manifest, Audio and Export QC Checklist, and Release Handoff. Record selected take/edit lineage, tool and model versions, artifact locations and checksums, reference IDs, writers/contributors, technical metadata, provider terms revision, rights/consent status, attribution/disclosure, commercial-use status, artwork owner/status, restrictions, unsupported outputs, and next action.

The release decision belongs to the named decision owner after required creative, legal/consent, brand, distribution, and release approvals. Never label unresolved clearance as approved.

## Completion gates

Complete the assignment only when:

- the requested original deliverables exist in formats the selected tools genuinely support;
- permission claims, reference operations, provider capability/terms/privacy, and commercial constraints are recorded;
- the originality direction was approved before generation and the selected result is meaningfully differentiated;
- every paid call stayed within explicit authorization and the numeric cap;
- take, edit, comp, mix, master, alternate, and stem lineage is traceable;
- human judgment selected the final creative direction;
- requested exports were independently opened or decoded and applicable audio/metadata checks have evidence;
- no unresolved impersonation, unauthorized identifiable voice cloning, recognizable lyric reproduction, recognizable melody reproduction, deceptive affiliation, or source confusion remains;
- the release handoff lists artifacts, checks, provenance, costs, constraints, unsupported items, risks, decision owner, next owner, and exact next action.
