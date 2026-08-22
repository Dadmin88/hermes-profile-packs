---
name: spatial-blockout
description: Create a low-cost playable blockout that proves scale, traversal, sightlines, routes, encounter spaces, gating, and camera behavior before art production.
---
# Spatial Blockout

Use when a new level or major area needs spatial validation before visual production.

## Procedure
1. Start from gameplay goals, player or camera dimensions, movement metrics, encounter needs, and required landmarks or connections.
2. Build with simple primitives and clear functional labels so geometry can change quickly.
3. Set real gameplay scale early: doorways, cover, stairs, corridors, jumps, vertical transitions, and interaction distances.
4. Establish critical path, optional routes, sightlines, chokepoints, arenas, safe spaces, and transition volumes.
5. Test camera collision, visibility, navigation, AI movement, traversal abilities, and multiplayer spacing where relevant.
6. Use temporary lighting or color only to communicate function and route, not to conceal spatial problems with presentation.
7. Run repeated playthroughs from the player's perspective and measure travel or encounter timing where pacing matters.
8. Lock only the spaces proven by gameplay; document unresolved areas before environment art begins.

## Decision rules
- Blockout should be cheap to delete.
- Correct scale is a gameplay requirement, not an art-polish detail.
- Do not let temporary blockout shapes become permanent by inertia.
- Art production should not begin on spaces whose core traversal or encounter geometry is still unproven.

## Quality gate
The blockout is ready for art when player scale and movement feel correct, required routes, encounters, and camera behavior are playable, major visibility or navigation issues are resolved, pacing is plausible, and remaining spatial uncertainty is explicitly documented.