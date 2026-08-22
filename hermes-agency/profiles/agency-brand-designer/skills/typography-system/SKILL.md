---
name: typography-system
description: Define a brand typography system with role hierarchy, typeface rationale, scale, weights, spacing, fallback, language coverage, accessibility, and cross-medium behavior.
---
# Typography System

Use when a brand needs durable typographic rules across product, marketing, documents, and other channels.

## Procedure
1. Inventory content roles across intended media: display, heading, body, UI, labels, data, captions, editorial, or other brand-specific needs.
2. Select or confirm typefaces based on personality, readability, licensing, language or glyph coverage, performance, and production availability.
3. Define hierarchy using a limited set of sizes, weights, line heights, letter spacing, and casing conventions tied to semantic roles rather than arbitrary visual presets.
4. Test body and UI text at realistic sizes, densities, contrast, and viewport widths for readability and accessibility.
5. Define fallback stacks and behavior when the primary font is unavailable or lacks a glyph or script.
6. Address responsive scaling, long translations, numerals, tables or data, punctuation, and mixed-script content where relevant.
7. Document cross-medium differences such as print versus web rendering without fragmenting the brand into unrelated typography systems.
8. Validate licensing and packaging requirements before distributing or embedding fonts.

## Decision rules
- Typography hierarchy should communicate content structure before decoration.
- Do not choose a typeface solely from a brand mood if it fails readability, language, or licensing needs.
- Fallback behavior is part of the system.
- Never redistribute font files unless the license permits it.

## Quality gate
The typography system is ready when semantic roles map to a coherent hierarchy, real content remains readable across required sizes, languages, and media, fallback and responsive behavior are defined, licensing is understood, and teams can apply the system consistently without inventing new text styles.