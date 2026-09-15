# AI Music Production Templates

Use stable project, reference, take, edit, and artifact IDs. Write `not-applicable`, `unsupported`, or `unresolved` instead of silently omitting a required decision. Rights labels must identify their basis: `user-confirmed`, `provider-stated`, `independently-verified`, or `unresolved`.

## Creative brief

```markdown
# Creative brief — <project-id>
- Project ID:
- Requester:
- Decision owner:
- Audience:
- Intended use:
- Commercial status: commercial | non-commercial | unresolved
- Emotional function and narrative:
- Themes or supplied lyrics:
- Requested duration and structure:
- Genre and era attributes:
- Instrumentation and texture:
- Non-identifying vocal characteristics:
- Production and mix direction:
- Required outputs and formats:
- Conditional/optional outputs:
- Deadline:
- Review points and owners:
- Privacy and upload constraints:
- Selected provider or tool: undecided | <name>
- Paid-generation authorization: not-authorized | authorized
- Numeric cap and currency:
- Prohibited outcomes:
- Acceptance criteria:
```

## Reference and permission ledger

```markdown
| Reference ID | Source/citation | Media owner | Useful high-level traits | Intended operation | Permission status | Basis/evidence | Upload allowed? | Commercial use allowed? | Restrictions | Verification owner | Verified/access date |
|---|---|---|---|---|---|---|---|---|---|---|---|
| REF-001 | | | | listen-only / analyze / upload / condition / remix / distribute | user-confirmed / licensed / public-domain / otherwise-authorized / unresolved | | yes / no / unresolved | yes / no / unresolved | | | |
```

Record the user's statement as a claim, not independent legal clearance. Do not perform an operation whose required permission is `unresolved`.

## Reference-feature analysis

```markdown
| Reference ID | Feature | Finding | Evidence class | Method/tool | Confidence/precision | Production implication |
|---|---|---|---|---|---|---|
| REF-001 | tempo/meter | | observed / measured / interpretation | | | |
| REF-001 | key/mode/harmony | | | | | |
| REF-001 | rhythm/groove | | | | | |
| REF-001 | instrumentation/texture | | | | | |
| REF-001 | structure/arrangement | | | | | |
| REF-001 | energy/dynamics | | | | | |
| REF-001 | non-identifying vocal traits | | | | | |
| REF-001 | lyrics/prosody | | | | | |
| REF-001 | production/space/mix | | | | | |
```

## Originality brief

```markdown
# Originality brief — <project-id>
- Functional goal:
- Attribute-level influence to retain:
- Purpose of each retained influence:
- Original melodic vocabulary:
- Original harmonic route and chord rhythm:
- Original rhythm and groove:
- Form and energy differences:
- Instrumentation and timbre differences:
- Vocal identity boundaries:
- Lyrical premise and phrase boundaries:
- Production-space differences:
- Explicit exclusions:
- Comparison red flags:
- Named identities removed from generation instructions: yes / no
- Approval owner:
- Approval date:
- Status: draft | approved | revision-required
```

## Synthetic-artist identity brief

```markdown
# Synthetic artist — <artist-id>
- Project/artist name:
- Audience:
- Artistic point of view:
- Themes and emotional range:
- Catalog promise:
- Original melodic vocabulary:
- Harmonic tendencies:
- Rhythmic tendencies:
- Lyrical vocabulary and perspective:
- Non-identifying vocal direction:
- Instrumentation palette:
- Production signatures:
- Catalog-coherence rules:
- Intentional creative exclusions:
- Identity/affiliation confusion safeguards:
- Track-specific experiments kept separate:
```

## Provider capability and terms check

```markdown
# Provider check — <provider/tool> — <access-date>
- Provider/tool:
- Exposed model/version:
- Access date:
- Evidence source URL/document/revision:
- Account/tier constraints:

| Capability or term | Supported/status | Evidence class | Constraint | Workflow response |
|---|---|---|---|---|
| Reference upload/conditioning | yes / no / unclear | provider-stated / independently-verified / unresolved | | |
| Lyrics conditioning | | | | |
| Vocals and voice controls | | | | |
| Instrumental-only output | | | | |
| Stem export | | | | |
| Editing | | | | |
| Extension | | | | |
| Remixing | | | | |
| Seeds/reproducibility | | | | |
| Export formats | | | | |
| API automation | | | | |
| Metadata support | | | | |
| Ownership/commercial use | | | | |
| Retention/privacy | | | | |
| Attribution/disclosure | | | | |

- Technical capability is permission: false
- Upload allowed by reference ledger:
- Commercial workflow allowed:
- Unsupported deliverables:
- Required redesign:
```

## Generation log

```markdown
| Take ID | Parent take ID | Tool/provider | Model/version | Prompt reference or text | Negative constraints | Settings | Seed/job ID | Input reference IDs | Output artifact ID/checksum | Cost | Result/defects | Decision/rationale | Authorized cap | Cumulative spending | Remaining spending | Cap-change approval |
|---|---|---|---|---|---|---|---|---|---|---:|---|---|---:|---:|---:|---|
| TAKE-001 | none | | | | | | unavailable | | | | | | | | | none |
```

Use a new child ID for every extension, remix, edit, comp, mix, master, or alternate. Do not reuse IDs after failed generations.

## Selection record

```markdown
| Candidate ID | Brief fit | Originality | Musical coherence | Lyrics/prosody | Performance | Defects | Editability | Comparison risk | Decision | Human decision owner | Rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|
```

## Track manifest

```markdown
# Track manifest — <project-or-track-id>
- Project/track ID:
- Public title and version:
- Synthetic artist:
- Writers and contributors:
- Production owner:
- Source reference IDs:
- Selected take and edit lineage:
- Tool/provider and model versions:
- Master artifact and checksum:
- Alternate artifacts and checksums:
- Stem artifacts and checksums: unsupported | <list>
- Duration:
- Sample rate:
- Bit depth:
- Channel layout:
- Integrated loudness and method:
- True peak and method:
- Tempo and evidence class:
- Key/mode and evidence class:
- Explicit/clean status:
- Identifier fields (ISRC/catalog/etc.):
- Artwork status and owner:
- Provider terms source/revision/date:
- Rights and consent status:
- Attribution/disclosure requirements:
- Commercial-use status:
- Remaining restrictions:
```

## Audio and export QC checklist

Record `pass`, `fail`, `not-tested`, `not-applicable`, or `unsupported`, plus evidence.

```markdown
| Check | Status | Method/tool/listening system | Evidence/result | Owner/date |
|---|---|---|---|---|
| Creative-brief fit | | | | |
| Originality comparison | | | | |
| Melody overlap review | | | | |
| Lyric overlap review | | | | |
| Real-artist identity/affiliation review | | | | |
| Voice-consent review | | | | |
| Clipping/clicks/dropouts/noise/tails/exposed edits | | | | |
| Synthetic artifacts | | | | |
| Timing and tuning | | | | |
| Transitions | | | | |
| Low-end behavior | | | | |
| Vocal intelligibility | | | | |
| Masking | | | | |
| Stereo image | | | | |
| Dynamics | | | | |
| Listening-system translation | | | | |
| Peak/integrated loudness/true peak/noise floor | | | | |
| File format/sample rate/bit depth/channels | | | | |
| Duration/silence/loop behavior | | | | |
| Independent decode/playback | | | | |
| Stem synchronization/start/tails/polarity/sum | | | | |
| Provider capability and terms | | | | |
| Generation and edit lineage | | | | |
| Metadata accuracy | | | | |
| Legal/consent/brand/distribution/release approvals | | | | |
```

## Originality comparison review

```markdown
# Originality comparison — <selected-artifact-id>
- Reviewer and date:
- References compared:
- Method and tools:
- Melody/hook contour and rhythm:
- Harmony/chord-rhythm comparison:
- Groove comparison:
- Form/signature-event comparison:
- Lyric-phrase comparison:
- Vocal identity comparison:
- Title/marketing/affiliation confusion:
- Material overlap found:
- Required quarantine/revision/escalation:
- Decision: pass | revise | quarantine | unresolved
- Decision evidence:
```

## Release handoff

```markdown
# Release handoff — <project-id>
- Outcome and approved brief:
- Delivered files, versions, locations, and checksums:
- Selected take and edit lineage:
- Listening evidence:
- Measurement evidence:
- Originality comparison summary:
- Source-permission summary:
- Provider/tool and model/version:
- Provider terms source, revision, and constraints:
- Authorized cap and currency:
- Actual cumulative spending:
- Metadata status:
- Attribution/disclosure requirements:
- Unsupported or omitted deliverables:
- Unresolved rights/consent risks:
- Unresolved quality risks:
- Unresolved distribution/release risks:
- Hold or release decision:
- Decision owner:
- Decision date:
- Next owner:
- Exact next action:
```
