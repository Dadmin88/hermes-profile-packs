---
name: economy-design
description: Design a game economy around sources, sinks, currencies, resources, exchange, scarcity, pacing, player incentives, inflation, exploits, and recovery using explicit flow models.
---
# Economy Design

Use when a game has currencies, resources, crafting, shops, rewards, trading, repair, upgrading, or other systems that create value flows.

## Procedure
1. Define what each currency or resource represents, who can create or destroy it, and what player behavior the economy should encourage.
2. Map sources and sinks across the core loop with expected frequency, quantities, unlock timing, and player segments.
3. Model inventories or balances over representative sessions and progression stages to expose accumulation, starvation, or dead currencies.
4. Define exchange rates, price curves, rarity, caps, decay, transaction friction, and trade rules only where they support meaningful choices.
5. Identify inflation, hoarding, farming, arbitrage, duplication, pay-to-skip, and dominant conversion paths that can collapse intended scarcity.
6. Protect recovery from mistakes so an early purchase or loss does not unintentionally brick progression unless that consequence is deliberate.
7. Simulate or spreadsheet parameter ranges before tuning exact values, then validate them through telemetry and playtests.
8. Revisit the economy when content cadence, monetization, player population, or progression changes alter the flow assumptions.

## Decision rules
- Every source should be understood relative to its sinks.
- Scarcity should create choices, not merely waiting.
- A currency with no meaningful tradeoff is often unnecessary complexity.
- Never tune an economy only from average balances; cohort and progression position matter.

## Quality gate
The economy is ready when major value flows are modeled, currencies and resources have clear jobs, accumulation and scarcity behave plausibly across progression, obvious exploits and dead ends are addressed, and tuning assumptions can be checked against real player behavior.