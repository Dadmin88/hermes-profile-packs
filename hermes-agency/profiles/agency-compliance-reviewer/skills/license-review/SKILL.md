---
name: license-review
description: Review source code, dependencies, assets, data, models, fonts, media, and other redistributed material for identified license terms, provenance, compatibility, notices, attribution, source obligations, and distribution constraints.
---
# License Review

Use when a product, repository, release, dependency, asset, or vendored skill includes third-party material whose redistribution/use obligations must be understood.

## Procedure
1. Define the distribution/use context and scope: source repository, binary/package, hosted service, embedded asset, documentation, model/data artifact, internal-only tool, or another relevant form.
2. Inventory third-party material and its provenance using manifests, lockfiles, vendored directories, asset metadata, headers, package registries, notices, source records, and build outputs as evidence.
3. Identify the exact license text/version for each material item from authoritative project/source metadata rather than relying only on a registry label or filename guess.
4. Map the obligations that are triggered by the intended use/distribution: attribution/notices, source availability, modification notices, reciprocal/copyleft scope, patent/trademark terms, redistribution of license text, or other explicit conditions.
5. Identify unclear, missing, conflicting, custom, dual-license, source-available, noncommercial, or no-license cases and escalate legal interpretation rather than inventing permission.
6. Check compatibility concerns where differently licensed components are combined or redistributed together. Distinguish factual packaging/linking/use structure from legal conclusions requiring qualified counsel.
7. Verify generated release artifacts include required notices/license files/attribution and do not accidentally contain material outside the reviewed inventory.
8. Record exact source/revision/package/version, license identifier/text source, intended distribution, evidence, obligations, and unresolved interpretation questions.
9. Re-run or update the inventory when dependencies/assets or distribution form changes materially.

## Decision rules
- Repository visibility or public availability is not a license grant.
- SPDX/package metadata is useful evidence but should be reconciled with the actual authoritative license when consequences matter.
- Do not declare legal compatibility where the answer depends on unsettled interpretation; state the facts and escalate.
- Vendored Agency skills must satisfy the repository's third-party skill provenance/redistribution rules in addition to general dependency review.

## Quality gate
The review is complete when third-party material and provenance are inventoried, exact license evidence is identified, triggered obligations and packaging requirements are mapped, ambiguous/custom/no-license cases are separated for escalation, and the actual distribution artifact can be checked against the recorded obligations without relying on memory.