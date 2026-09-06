---
name: software-artifact-triage
description: Triage an authorized binary, application package, firmware image, or capture into a safe, evidence-preserving analysis plan.
---
# Software Artifact Triage

Use at the start of a reverse-engineering assignment or when an unfamiliar artifact must be identified before deeper static or dynamic analysis.

## Procedure

1. Confirm the analysis question, documented authority, allowed techniques, delivery expectations, and stop conditions. If authority or ownership is unclear, stop rather than infer permission.
2. Preserve the original artifact as read-only evidence. Record its source, filename, size, cryptographic hashes, acquisition time when known, and chain-of-custody notes when relevant.
3. Identify container, executable format, architecture, endianness, platform, signing state, packer or obfuscation indicators, and embedded components without executing the artifact.
4. Inventory metadata, sections or segments, imports, exports, resources, strings, manifests, certificates, dependencies, and nested payloads. Record the tool and version behind each derived result.
5. Classify handling risk. Treat unknown executables, firmware, documents with active content, and extracted scripts as untrusted until evidence supports a narrower classification.
6. Form a short hypothesis list tied to the requested question. Select the least invasive next method that can confirm or reject each hypothesis.
7. Define any required containment before dynamic work: disposable environment, no real credentials or user data, restricted or simulated networking, explicit resource limits, and a reset path.
8. Produce a triage brief containing artifact identity, observations, risks, hypotheses, proposed methods, expected evidence, and blockers.

## Quality gate

The triage is complete only when the original evidence remains unchanged, artifact identity is reproducible, authority and safety constraints are explicit, observations are separated from inference, and each proposed next step answers a stated question rather than performing open-ended execution.