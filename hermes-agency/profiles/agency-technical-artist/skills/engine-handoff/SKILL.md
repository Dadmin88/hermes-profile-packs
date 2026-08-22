---
name: engine-handoff
description: Define and validate the art-to-engine contract for formats, scale, naming, materials, rigs, animation, metadata, import settings, automation, and ownership across distributed production.
---
# Art-to-Engine Handoff

Use when art production and engine implementation need a reliable shared pipeline.

## Procedure
1. Map the complete path from source DCC or design tool through export, version control or storage, import, processing, runtime asset, and final scene use.
2. Define source and export ownership, canonical formats, scale or axis, naming, folder or package structure, metadata, and versioning.
3. Specify material or shader conventions, texture channels, rig or skeleton expectations, animation clip or event conventions, LOD or collision, and other asset-class requirements.
4. Automate repetitive import validation or conversion where it materially reduces drift, while preserving useful warnings and artist control.
5. Make import settings reproducible from versioned metadata or configuration rather than one person's editor state when possible.
6. Provide validation that catches missing references, wrong scale, unsupported features, bad pivots, channel mistakes, oversized assets, or incompatible rig or material data.
7. Test the handoff from a clean workspace or another eligible node to expose machine-local dependencies.
8. Define who owns fixing source defects, exporter defects, importer defects, and engine integration defects so failures do not bounce indefinitely.

## Decision rules
- A handoff is a contract between tools and teams, not an instruction to export and hope.
- Machine-local editor settings are fragile pipeline state.
- Validation should fail with actionable messages at the earliest useful boundary.
- Keep source-of-truth and generated outputs distinguishable.

## Quality gate
The pipeline is ready when a clean node can reproduce import behavior from versioned source and configuration, asset-class contracts are explicit, common defects are caught early, ownership for failures is clear, and artists and engineers can exchange work without hidden machine-specific ritual.