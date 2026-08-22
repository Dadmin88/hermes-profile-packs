---
name: tutorial-writing
description: Write a tutorial that teaches a new user to accomplish one meaningful outcome through a verified sequence, explanatory context, checkpoints, troubleshooting, and final proof rather than documenting every option.
---
# Tutorial Writing

Use when a newcomer needs a guided learning path through a product or workflow.

## Procedure
1. Define the learner, starting knowledge, prerequisites, environment, and one concrete outcome they will achieve.
2. Verify the entire workflow on the current supported product or version before writing steps.
3. Introduce only the concepts needed for the next action and explain why they matter at the moment they become useful.
4. Provide exact commands, labels, paths, examples, or screenshots where ambiguity would cause failure.
5. Add checkpoints after meaningful stages so readers can verify they are on track before continuing.
6. Include common failure recovery near the step where the problem occurs rather than collecting all troubleshooting at the end.
7. Keep optional alternatives out of the main path unless the learner must choose between them.
8. Finish by proving the intended outcome and pointing to deeper reference or how-to material for next steps.

## Decision rules
- A tutorial teaches through doing; it is not an exhaustive reference page.
- One reliable happy path is better than presenting every possible setup to a beginner.
- Commands and UI labels must be verified against the current version.
- Explain concepts when the learner needs them.

## Quality gate
The tutorial is ready when a target learner can start from documented prerequisites, follow a verified path without hidden steps, check progress along the way, recover from common failures, and end with observable proof of the promised outcome.