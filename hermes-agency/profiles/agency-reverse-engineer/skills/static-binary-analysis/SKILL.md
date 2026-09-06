---
name: static-binary-analysis
description: Reconstruct program structure and behavior from an authorized compiled artifact without executing it.
---
# Static Binary Analysis

Use when a compiled executable, library, application bundle, or firmware component must be understood through its bytes, metadata, and recovered code structure.

## Procedure

1. Start from an identified working copy and preserve the original hash. Record the architecture, format, base-address assumptions, and analysis-tool versions.
2. Map sections, segments, entry points, imports, exports, relocations, symbols, resources, exception metadata, and embedded payloads before interpreting decompiled code.
3. Locate behavior relevant to the analysis question using multiple signals: callers and callees, constants, strings, cross-references, imports, data structures, and control-flow shape.
4. Rename functions, variables, and structures as hypotheses, using confidence markers when meaning is not confirmed. Preserve original addresses or offsets alongside analyst labels.
5. Recover important control flow, data flow, state transitions, serialization logic, cryptographic or compression boundaries, and external effects. Trace inputs to outputs rather than reading isolated pseudocode.
6. Corroborate decompiler output against disassembly and binary metadata, especially around indirect calls, optimized code, exception paths, type recovery, and compiler-generated constructs.
7. Record anti-analysis, packing, stripping, or obfuscation effects as limitations. Do not claim semantic certainty where the available representation cannot support it.
8. Produce a concise behavior map with evidence references, confirmed conclusions, open hypotheses, and the smallest dynamic experiment needed for unresolved questions.

## Quality gate

Every material conclusion must cite reproducible evidence such as an address, offset, symbol, cross-reference, byte pattern, or recovered call/data path. Decompiler pseudocode alone is not proof, and analyst-assigned names must never be presented as original symbols.