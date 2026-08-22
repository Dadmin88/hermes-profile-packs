---
name: export-validation
description: Validate exported art assets for format, scale, orientation, pivots, naming, channels, transforms, animation, metadata, and target-tool import behavior before handoff.
---
# Asset Export Validation

Use when moving art from authoring tools into an engine, application, build pipeline, or another specialist's workspace.

## Procedure
1. Confirm the target application's import contract: format or version, coordinate system, units, scale, orientation, naming, materials, animation, and supported metadata.
2. Freeze or document the intended source revision and export selection so the artifact can be reproduced.
3. Normalize transforms, pivots or origins, hierarchy, and object naming according to project convention without destroying intentional local transforms.
4. Verify meshes or sprites, UVs, normals, vertex colors, material assignments, bones, animation clips, morphs, and custom attributes that the target workflow depends on.
5. Check exported texture paths and channels and whether dependencies are embedded, relative, or separately packaged.
6. Import the produced file into the actual target application and inspect warnings, scale, orientation, shading, animation, pivots, and missing references.
7. Compare the imported result to the approved source appearance and record any unavoidable conversion differences.
8. Deliver the exported artifact plus source revision and required import notes using portable paths rather than one machine's local layout.

## Decision rules
- An exporter reporting success is not proof the target importer interpreted the asset correctly.
- Validate in the receiving application, not only by reopening the export in the authoring tool.
- Do not bake absolute machine paths into portable asset packages.
- Source and export revisions must be traceable when distributed production spans multiple Fleet nodes.

## Quality gate
Export is complete when the target application imports the intended revision without missing dependencies or transform, material, or animation surprises, the result matches approved appearance within known conversion limits, and another node can reproduce the artifact from the documented source.