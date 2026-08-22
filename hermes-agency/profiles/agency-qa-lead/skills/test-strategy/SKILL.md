---
name: test-strategy
description: Design a risk-based test strategy that maps product and technical risks to appropriate validation layers and release evidence.
---
# Test Strategy

Use for significant features, releases, migrations, or changes where ad hoc testing is insufficient.

## Procedure
1. Identify critical user outcomes, system invariants, failure consequences, and changed surfaces.
2. Rank risks by likelihood and impact.
3. Map each risk to the cheapest reliable validation layer: static checks, unit, integration, contract, E2E, performance, security, exploratory, or manual operational proof.
4. Define environments, data, fixtures, and observability required to make failures diagnosable.
5. Specify entry/exit criteria and the evidence required for release confidence.
6. Avoid duplicate tests that prove the same thing at more expensive layers unless defense in depth is justified.
7. Update the strategy when defects reveal unmodeled risk.

## Quality gate
The strategy must explain what can break, how it will be detected, and why the chosen tests are sufficient.