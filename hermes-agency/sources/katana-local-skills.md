# Katana local skill enrichment

- Source: Kyle French's local Katana Hermes profile skill library
- Source inventory: 213 complete skills reviewed
- Review date: 2026-08-13
- License gate: only skills declaring MIT were imported
- Portability gate: private topology, credentials, machine-specific operations, personal profile administration, and destructive deployment workflows were excluded
- Curation gate: each imported skill adds a distinct procedure beyond the profile's baseline bundle

Imported skills:

| Profile | Skill | Local adaptation |
|---|---|---|
| `agency-code-reviewer` | `contract-value-object-review` | None |
| `agency-design-systems-designer` | `design-md` | None |
| `agency-editor-in-chief` | `humanizer` | None |
| `agency-market-researcher` | `grounded-citations` | Removed generated Python bytecode caches |
| `agency-social-media-manager` | `x-builder-content-operator` | Generalized builder-specific wording and removed account-specific research notes |
| `agency-systems-architect` | `architecture-diagram` | None |

The source skills were copied as complete directories, including their useful references, templates, and scripts. They are vendored distribution content; installed profiles do not fetch them from the local Katana profile at runtime.
