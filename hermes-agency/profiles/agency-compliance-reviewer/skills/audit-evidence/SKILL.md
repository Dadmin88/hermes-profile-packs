---
name: audit-evidence
description: Collect and evaluate review evidence with clear provenance, scope, time period, completeness, integrity, ownership, sampling, and traceability to the requirement or control it is intended to demonstrate.
---
# Audit Evidence

Use when a compliance or control review needs durable evidence rather than conclusions based on screenshots, memory, or informal assertions.

## Procedure
1. Define the requirement/control, system/process scope, review period, and exact question the evidence must answer before collecting artifacts.
2. Prefer evidence from the authoritative system of record or reproducible query/configuration over manually recreated screenshots or summaries when both are available.
3. Record provenance for each artifact: source system, owner, collection date/time, environment/tenant/project, relevant version/revision, query/filter, and collector when material.
4. Assess whether evidence shows control design, one-time implementation, or recurring operation during the required period. Do not treat one current-state snapshot as proof of historical operation.
5. When sampling records, define the population and selection method, capture sample identifiers safely, and make clear what the sample can and cannot support.
6. Check completeness and internal consistency across related evidence. Missing periods, contradictory timestamps, unaccounted exceptions, or unexplained gaps should remain visible.
7. Preserve evidence integrity using stable exports, immutable records, versioned documents, checksums, or repository history when the review process requires durable proof.
8. Minimize sensitive content. Collect only fields necessary to demonstrate the control and handle access/storage/retention according to the evidence-handling process.
9. Tie each artifact to the exact control/requirement and record reviewer conclusion separately so raw evidence is not altered to fit the conclusion.
10. Identify stale evidence and define what must be recollected when configuration, ownership, system version, or review period changes.

## Decision rules
- Evidence should be sufficient for another reviewer to understand what was observed without trusting the collector's memory.
- Screenshots are useful for some UI/config states but weak when a structured export or query can demonstrate the same fact more completely.
- Current state does not prove continuous historical operation.
- Do not collect broad sensitive datasets merely because they might become useful later.

## Quality gate
Evidence is review-ready when it traces to a scoped requirement/control, provenance and period are clear, completeness and sampling limits are explicit, sensitive content is minimized, artifacts are durable enough for the review purpose, and the reviewer conclusion can be independently checked against the recorded source material.