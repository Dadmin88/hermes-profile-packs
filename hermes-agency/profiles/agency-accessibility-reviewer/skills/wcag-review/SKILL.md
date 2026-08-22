---
name: wcag-review
description: Review a product flow or implementation against an explicitly identified WCAG version and conformance target by mapping applicable success criteria to reproducible evidence without reducing conformance to scanner output.
---
# WCAG Review

Use when accessibility work must be evaluated against a specific WCAG requirement set for design, implementation, release, procurement, or compliance evidence.

## Procedure
1. Identify the exact WCAG version, conformance level, product surface, technologies, platforms, and scope of pages/screens/flows being reviewed. Verify the current normative requirement source when the engagement depends on formal conformance.
2. Build a review matrix of success criteria applicable to the scoped experience and the testing method needed for each: inspection, keyboard/manual interaction, contrast/visual measurement, responsive/reflow test, assistive technology, media review, timing/motion test, or automated detector.
3. Evaluate semantic structure, text alternatives, adaptability, distinguishability, keyboard operation, timing/seizure/motion considerations, navigation, input assistance, compatibility, and other applicable criteria against actual user flows rather than isolated components only.
4. Record objective evidence for each tested criterion: location, environment, steps, observed behavior, measurement/tool where relevant, and pass/fail/not-applicable/not-tested status.
5. Treat automated scanners as one evidence source. Manually verify their findings and test criteria they cannot evaluate reliably.
6. Distinguish a criterion failure from broader usability concerns that may still affect disabled users but are not proven violations of the selected requirement.
7. For component patterns reused widely, sample enough instances to validate the shared implementation while separately checking context-specific behavior such as labels, errors, focus, and content order.
8. Trace failures to the user consequence and recommend remediation aligned with the criterion without prescribing unnecessary implementation details.
9. Re-test remediated failures and update the evidence matrix rather than marking them closed from code review alone.
10. State scope and limitations clearly. Do not generalize reviewed samples into whole-product conformance beyond the evidence collected.

## Decision rules
- Formal conformance statements require the exact applicable normative criteria and scope; do not infer them from memory when current source verification is required.
- Passing automated checks is not proof of WCAG conformance.
- WCAG criteria are a minimum requirement framework, not the complete definition of accessible usability.
- Record untested criteria honestly rather than converting missing evidence into a pass.

## Quality gate
The review is ready when the conformance target and scope are explicit, applicable criteria map to appropriate manual/automated evidence, failures are reproducible and criterion-linked, remediation is re-tested, and the final statement accurately distinguishes tested evidence, limitations, and any broader accessibility risks outside the formal criterion set.