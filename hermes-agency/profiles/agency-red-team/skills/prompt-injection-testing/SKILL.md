---
name: prompt-injection-testing
description: Conduct authorized defensive testing of AI instruction-boundary failures using controlled untrusted content, tool/retrieval scenarios, and trace evidence to verify that external data cannot silently override higher-priority intent or expand authority.
---
# Prompt Injection Testing

Use when an AI/agent system consumes untrusted text, webpages, documents, messages, tool results, or retrieved content that could contain instruction-like material.

## Procedure
1. Confirm authorized scope, test accounts/data, tools/actions permitted, prohibited side effects, and whether tests run in isolated/sandbox environments before introducing adversarial content.
2. Map instruction and trust boundaries: system/developer/task instructions, user input, retrieved documents, webpages, email/messages, memory, tool output, and any content passed between agents.
3. Identify the security/property being tested, such as preserving the assigned task, refusing authority expansion, not exposing protected data, not invoking tools outside user intent, and treating retrieved/external content as data rather than policy.
4. Create bounded adversarial fixtures that attempt to alter those properties without requesting real harmful external actions. Keep fixtures reproducible and scoped to the specific boundary under review.
5. Test direct and indirect paths: user-visible untrusted content, retrieved content, tool results, quoted documents, transformed/summarized content, and multi-step agent handoffs where the system actually uses them.
6. Capture the full trace needed to diagnose the first failure point: instructions/context construction, retrieved content, tool schemas/calls/results, memory/state, model output, and downstream validation/authorization.
7. Distinguish model obedience failure from system-design failure. Missing tool authorization, unsafe data mixing, overly broad capabilities, weak output validation, or retrieval provenance can be the root cause even when the final text looks like a prompt failure.
8. Validate defense in depth: instruction separation, least-privilege tools, server-side authorization, output/schema validation, content provenance, confirmation/approval gates, and monitoring as relevant.
9. Add confirmed failures and nearby variants to the AI evaluation/security regression set before accepting a fix.
10. Re-test with the same and structurally different fixtures to avoid a brittle defense that blocks one phrase while leaving the boundary unchanged.

## Decision rules
- Do not use live credentials, destructive tools, or unrelated third-party systems to prove an injection weakness when a sandboxed/no-op path establishes the boundary failure.
- Treat prompt injection as a system security problem, not a vocabulary filter problem.
- The model should never be the sole authorization boundary for consequential actions.
- Report the violated trust/authority property and trace evidence, not merely that “the prompt was jailbroken.”

## Quality gate
The assessment is complete when untrusted-content boundaries and protected properties are explicit, tests remain authorized and non-destructive, failures are traceable to the first system/model divergence, defenses address authority and data boundaries rather than specific phrases, and confirmed cases become repeatable regression coverage.