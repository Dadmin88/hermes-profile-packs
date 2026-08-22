---
name: source-of-truth-audit
description: Audit organizational sources of truth by identifying authoritative systems, duplicated facts, conflicting records, ownership, freshness, synchronization, access, and downstream consumers.
---
# Source-of-Truth Audit

Use when teams disagree about which document, database, repository, dashboard, or system is authoritative for an important fact.

## Procedure
1. Define the information domain and decisions affected, such as product configuration, customer state, policy, pricing, architecture, inventory, contracts, or process status.
2. Inventory every system or document currently treated as authoritative or commonly copied for that information.
3. For each source, record owner, update mechanism, freshness, permissions, versioning, consumers, and whether it stores original or derived data.
4. Compare conflicting records and trace how each is created, synchronized, transformed, cached, or manually copied.
5. Designate the authoritative source for each fact or clearly define precedence when several sources have legitimate distinct scopes.
6. Replace duplicated mutable facts with links, generated views, or synchronization where practical rather than relying on manual multi-source updates.
7. Identify downstream automations, reports, docs, and Fleet workflows that will be affected by source or precedence changes.
8. Document ownership and correction path so future discrepancies can be resolved without repeating the audit.

## Decision rules
- One organization can have several sources of truth for different facts; the problem is ambiguous authority for the same fact.
- Derived views should reveal their upstream source.
- Copying volatile values into documents creates drift risk.
- A source is not authoritative merely because it is old or widely referenced.

## Quality gate
The audit is complete when each material fact has clear authority or precedence, conflicting sources have an explained resolution path, duplicated mutable data is reduced or synchronized, owners and freshness are visible, and downstream consumers can migrate without hidden assumptions.