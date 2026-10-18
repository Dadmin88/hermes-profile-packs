---
name: vehicle-records
description: Organize per-vehicle mileage and service history with supporting evidence and explicit distinctions between proposed, booked, reported, and documented work.
---
# Vehicle Records

Use when the user wants a reliable history of a vehicle or a service event.

## Procedure

1. Identify the vehicle by year, make, model, and relevant variant. Use a short alias when enough; request sensitive VIN or plate details only if needed for a specific authorized check.
2. Record odometer readings with dates and units. Convert units only when explicitly identified; preserve originals.
3. Enter each task with a state: recommended, estimated, booked, reportedly completed, documented completed, or unknown. Never infer completed service from a quote, appointment, memory alone, or a suggested interval.
4. Attach the provenance of each claim: manual section, dated invoice or receipt, service record, or owner report. Distinguish documents from recollection and keep conflicting accounts visible.
5. Produce a concise history and missing-evidence list. Avoid storing personal identifiers beyond the task's needs.

## Output standard

Return a vehicle-specific service ledger with dates, readings, task/state, evidence, and unresolved gaps. If the user requests persistence, use only the ordinary authorized Hermes profile storage or files available in that installation; do not invent a new database or claim a file was saved unless it was.
