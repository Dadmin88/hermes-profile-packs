---
name: localization-ready-dialogue
description: Prepare dialogue for localization by preserving meaning, context, speaker metadata, variables, gender or plurality constraints, line relationships, timing, and cultural clarity while avoiding source-language wordplay that cannot travel without annotation.
---
# Localization-Ready Dialogue

Use before dialogue is handed to translators or localization vendors.

## Procedure
1. Give every line a stable identifier plus speaker, addressee or scene context, emotional intent, and neighboring lines when meaning depends on them.
2. Expand ambiguous pronouns, subjects, references, abbreviations, or standalone fragments in translator notes when the line itself must remain natural.
3. Mark variables, placeholders, tags, markup, gender, plurality, grammatical choices, and runtime substitutions with clear constraints and examples.
4. Identify wordplay, idioms, rhyme, cultural references, invented terms, names, and jokes that require creative localization rather than literal translation.
5. Avoid concatenating sentence fragments or assuming English word order where runtime strings can be localized as complete units instead.
6. Define character voice and relationship context so translators can preserve status, formality, humor, and personality.
7. Record timing, subtitle length, UI width, lip-sync, audio, or branch constraints where the localized line must fit a technical boundary.
8. Validate imported localized samples in context and feed recurring ambiguity back into the source dialogue or localization notes.

## Decision rules
- Context is part of the translation source.
- Prefer full translatable units over runtime string concatenation.
- Do not force literal preservation of wordplay when equivalent effect is the real requirement.
- Stable line IDs matter more than file order in distributed production.

## Quality gate
Dialogue is localization-ready when every line has enough context and metadata to translate meaning and voice, variables and technical constraints are explicit, language-specific traps are annotated, and localized samples can be imported without reconstructing intent from the original writer.