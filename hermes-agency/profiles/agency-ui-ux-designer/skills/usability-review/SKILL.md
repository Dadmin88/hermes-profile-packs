---
name: usability-review
description: Review an interface against user goals, clarity, feedback, error prevention and recovery, consistency, cognitive load, accessibility, and likely task friction using evidence and realistic flows.
---
# Usability Review

Use when an existing or proposed interface needs expert usability evaluation before or alongside user testing.

## Procedure
1. Define target users, critical tasks, environment, constraints, and known research or analytics before reviewing screens.
2. Walk each critical flow from a realistic starting point, including loading, empty, error, permission, interruption, and recovery states.
3. Evaluate discoverability, terminology, hierarchy, control affordance, feedback, system status, defaults, and whether actions match user expectations.
4. Look for unnecessary memory burden, repeated decisions, hidden prerequisites, destructive ambiguity, and places where users must understand implementation concepts.
5. Check consistency with existing product patterns unless a deliberate change improves the task.
6. Include accessibility and input-method implications where they materially affect usability, while routing formal accessibility conformance to Accessibility Reviewer.
7. Rank findings by task impact, frequency, severity, and confidence; distinguish observed evidence from heuristic inference.
8. Recommend the smallest design change that addresses the underlying user problem and identify where user research or testing is needed to resolve uncertainty.

## Decision rules
- Expert review is not a substitute for watching real users when the risk or uncertainty warrants research.
- Consistency is valuable until the existing pattern itself is the usability problem.
- Do not hide subjective taste inside usability language.
- Error recovery matters as much as happy-path efficiency for consequential tasks.

## Quality gate
The review is complete when critical flows and failure states have been examined, findings connect to user-task consequences, evidence and inference are separated, priorities are clear, and recommended changes address causes rather than merely rearranging pixels.