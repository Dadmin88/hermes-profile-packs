---
name: developer-experience
description: Improve developer experience by measuring the path from intent to working change, locating friction, reducing unnecessary cognitive load, and validating improvements with real users and delivery evidence.
---
# Developer Experience

Use when engineers lose time to setup, discovery, local environments, builds, tests, deployment, debugging, platform interfaces, or unclear ownership.

## Procedure
1. Define the developer population and the job they are trying to complete. Measure the actual path from starting intent to useful outcome instead of optimizing an isolated tool in a vacuum.
2. Gather evidence from task timing, failed attempts, support requests, onboarding sessions, build/test/deploy telemetry, interviews, and repeated workaround patterns.
3. Map friction by stage: discovery, access, environment setup, code navigation, feedback loop, testing, dependencies, platform usage, deployment, observability, and recovery.
4. Distinguish unavoidable domain complexity from accidental platform/tooling complexity. The platform should absorb repetitive mechanics while keeping important system behavior understandable.
5. Prioritize bottlenecks by frequency, time lost, error risk, and population affected. Do not chase cosmetic polish while a slow or unreliable core loop dominates the experience.
6. Improve the default path using automation, clearer contracts, faster feedback, better errors, discoverable docs/examples, sensible defaults, and self-service access where appropriate.
7. Keep escape hatches and diagnostics available. A paved path that hides all underlying state can make unusual failures harder to solve.
8. Validate changes with representative developers performing real tasks. Measure before/after completion time, success rate, retries, support burden, or another relevant outcome.
9. Instrument the experience enough to detect regressions as the platform evolves.

## Decision rules
- Developer experience is the usability of the engineering system, not the number of internal tools.
- Faster local commands do not help if access, CI, deployment, or diagnosis remains the real bottleneck.
- Good defaults reduce decisions; they should not remove required control from advanced cases.
- Documentation should support the workflow, but recurring mechanical confusion may indicate a product/platform defect rather than a documentation defect.

## Quality gate
The improvement is done when a real developer workflow becomes measurably easier or more reliable, the dominant friction is reduced rather than relocated, exceptional cases remain diagnosable, and telemetry or feedback can reveal future regression.