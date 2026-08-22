---
name: agent-failure-analysis
description: Diagnose AI and agent failures from trace evidence by locating the first meaningful divergence across routing, instructions, context, retrieval, tools, state, model behavior, schemas, and runtime.
---
# Agent Failure Analysis

Use when an AI or agent workflow produces a wrong answer, wrong action, malformed output, tool failure, looping behavior, inconsistent result, unsafe behavior, or unexplained regression.

## Procedure
1. Capture the failing task exactly: user input, relevant system/developer instructions, model and configuration, prompt/context revision, retrieved evidence, tool definitions, tool calls/results, state or memory, output, timestamps, and environment needed to reproduce it.
2. Establish whether the failure is deterministic or probabilistic. Re-run the same case enough to distinguish a stable defect from variance without using repeated sampling as a substitute for diagnosis.
3. Build the execution trace in order and locate the first meaningful divergence from the intended path. Later bad output may be a consequence of an earlier routing, context, retrieval, or tool error.
4. Classify the failure by owning layer: task/routing, instructions, context construction, retrieval, tool selection, tool arguments, tool implementation/result, state or memory, model reasoning/instruction following, structured-output validation, safety policy, nondeterminism, latency/resource limits, or surrounding application/runtime.
5. Compare with a successful trace for a similar case when available. Identify the smallest changed input, evidence, prompt, tool result, state, model/configuration, or environment that predicts the failure.
6. Form a falsifiable hypothesis and test it with targeted counterexamples. Avoid changing prompt, model, retrieval, and tools simultaneously because a better result would not reveal which layer fixed the cause.
7. Repair the lowest layer that actually owns the defect. Examples: fix missing corpus data rather than prompting around it; fix a misleading tool schema rather than adding tool-selection prose; fix validation rather than asking the model to "always output valid JSON."
8. Add the failure and nearby variants to the evaluation set before accepting the fix. Check for regressions in cases that previously succeeded.
9. Measure the repair under the same configuration and task distribution. For probabilistic failures, compare rates with enough repetitions to support the claimed improvement.
10. Record the failure class, evidence, root cause, fix, evaluation impact, and remaining uncertainty so the case becomes reusable engineering knowledge rather than an anecdote.

## Decision rules
- The final wrong sentence is not automatically the root cause.
- Do not label every unexplained failure a hallucination; identify what information and control path the model actually had.
- Prompt changes are justified when instructions are the failing layer, not by default.
- A stronger model can mask a system defect without repairing it.
- If the trace shows the primary defect belongs to product logic, security, infrastructure, or another specialist, hand off the evidence rather than stretching the AI layer around it.

## Quality gate
The analysis is complete when the first meaningful failure point is supported by trace evidence, the owning layer is identified, the repair targets that cause, the failure is represented in evaluation coverage, and measured results show improvement without unacceptable regressions.