---
name: data-handling-review
description: Review how a system collects, receives, uses, stores, shares, logs, retains, exports, and deletes data against explicitly identified policy, contractual, regulatory, and product requirements.
---
# Data Handling Review

Use when a change touches personal, customer, confidential, regulated, credential, telemetry, model, or other data with explicit handling requirements.

## Procedure
1. Identify the exact data categories and requirement sources in scope. Record jurisdiction/contract/policy/version when relevant instead of assuming a regime from the data name alone.
2. Trace data end to end: collection or inbound source, purpose/use, validation/transformation, storage, caches, logs/telemetry, backups, analytics, third-party processors, exports, support/admin access, and deletion/retention paths.
3. Map who or what can access each form of the data and under which identity/role/tenant boundary. Separate application authorization from infrastructure/operator access.
4. Review minimization and purpose alignment against the stated requirement: collect, retain, expose, and log only what the approved use actually needs.
5. Review storage/transmission and secret/sensitive-field protections required by the applicable control set, including masking/redaction and test/development data handling where relevant.
6. Review retention and deletion semantics across primary stores, replicas, caches, derived data, exports, logs, and backups according to the identified requirement. Do not promise immediate deletion from systems whose approved retention model differs.
7. Review data sharing and external processors/integrations for approved destination, scope, purpose, contract/policy coverage, and fields actually transmitted.
8. Review user/operator transparency and control requirements such as notices, consent/preferences, access/export/correction/deletion workflows only when they are part of the identified requirement set.
9. Record conforming evidence, gaps, uncertain interpretation, affected data flow, consequence, and owning remediation role separately.
10. Re-test the actual implemented flow or configuration after remediation; design intent alone is not handling evidence.

## Decision rules
- Start from explicit requirements and observed data flows, not generic privacy checklists detached from the product.
- Logs, backups, analytics, and exports are data stores/flows too.
- A compliance reviewer can establish factual handling and requirement mapping but should escalate legal interpretation beyond available authority.
- Data location on a Fleet node is dynamic runtime state; requirements should be expressed as policy/eligibility constraints for Fleet rather than hardcoded host selection in Agency.

## Quality gate
The review is complete when scoped data categories and requirement sources are explicit, the full data lifecycle is traced with access and external-sharing boundaries, retention/deletion and telemetry are included, conforming evidence and gaps are separated, and any interpretation-dependent conclusion is clearly escalated rather than overstated.