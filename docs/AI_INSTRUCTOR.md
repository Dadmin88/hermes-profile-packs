# AI & Agent Instructor

`academy-ai-agent-instructor` teaches human learners model fundamentals and agent design. It has five owned skills: guided study, profile walkthrough, evidence review, learning recap, and source research. The shared `teach-profile` skill preserves the existing Academy continuing-education contract. Human learners are not forced through that contract.

Install the portable distribution with the normal Profile Packs installer or `hermes profile install hermes-academy/profiles/academy-ai-agent-instructor`. Select a model/provider through Hermes. No accounts, credentials, private learner preferences, or chat history ship in this package.

## Capabilities

- Native `web` and `skills` toolsets support source verification and on-demand skill reading. Verify web credentials/backends in the target installation.
- `skills/ai-source-research/scripts/study_sources.py` is an optional narrow stdio MCP server. Run it from a separate environment with `mcp==1.26.0` and `youtube-transcript-api==1.2.4`; set `STUDY_PROFILE_PACK` to the trusted portable Profile Packs checkout. It lists/reads portable SOUL and skill files, reads allowlisted evaluation docs, and retrieves bounded caption segments. It cannot read arbitrary runtime files or execute commands.
- An optional existing evaluation-workbench MCP should expose only `eval_list_cases`, `eval_inspect_case`, `eval_list_runs`, `eval_run_status`, `eval_inspect_trial`, `eval_compare_runs`, and `eval_get_evidence`. Keep run-start, cancellation, and review submission excluded in the runtime tool allowlist.
- Model/profile instructions do not themselves enforce tool access. Verify the effective tool list after configuration.

The private Study Room integration uses native Hermes CLI sessions with explicit skill preloading, selected model/reasoning options, and persisted session IDs. This avoids assuming the installed runtime preserved distribution preload declarations. The app transport, authentication, local speech runtime, and private conversation database belong to the workspace integration, not the portable profile.

## Teaching checks

Exercise direct explanations, a supplied profile walkthrough, an evidence claim with a failed test, a title-only video request, transcript retrieval, and conversation continuation. A successful setup or tool call does not establish learning improvement. Keep learner mastery and behavioral evaluation verdicts evidence-based and separate from installation readiness.
