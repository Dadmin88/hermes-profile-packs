---
name: editor-integration
description: Integrate engineering capabilities into editors/IDEs with explicit protocol boundaries, workspace awareness, incremental updates, cancellation, diagnostics, compatibility, and fallback behavior.
---
# Editor Integration

Use when a CLI, language/tooling service, generator, formatter, debugger, or platform capability needs a first-class editor/IDE experience.

## Procedure
1. Define the editor user task and decide what belongs in the editor versus an underlying reusable CLI/service/library. Keep core behavior usable outside one editor where practical.
2. Identify the editor APIs/protocols and versions involved, workspace/project discovery rules, configuration scope, and supported platforms/editors.
3. Design requests/events around stable capability boundaries. Prefer standard protocols such as language/debug protocols when they genuinely match the feature rather than inventing a private transport unnecessarily.
4. Handle workspace lifecycle: open/close, multiple roots, file create/rename/delete, configuration changes, branch/worktree changes, project reload, and partial/untrusted workspaces as relevant.
5. Keep interactive latency bounded using incremental computation, debouncing, cancellation, background work, caching, and stale-result rejection where appropriate.
6. Report diagnostics/actions with precise locations, severity, message, and actionable recovery. Do not flood the editor with repeated or non-actionable findings.
7. Treat code edits/fixes as user-visible mutations: generate minimal edits, account for concurrent document versions, and fail safely when the buffer changed underneath the operation.
8. Define failure/offline/fallback behavior when the backing service, toolchain, network, or remote node is unavailable. Preserve useful local functionality when possible.
9. Test representative workspace layouts, large projects, unsaved edits, rapid changes/cancellation, multi-root/worktree behavior, unsupported versions, and editor restart/reconnect.
10. Document installation, configuration, supported versions, troubleshooting, and how to invoke the underlying non-editor interface when the extension fails.

## Decision rules
- The editor extension should be an interface to engineering capability, not the only place the capability exists unless the task is inherently editor-specific.
- Never apply stale edits to a newer buffer silently.
- Remote Fleet execution should be surfaced as a normal capability boundary/status, not encoded as a permanent connection to one node.
- Verify version-specific editor APIs against current official documentation when implementing a concrete integration.

## Quality gate
The integration is ready when the editor workflow is responsive and workspace-aware, core operations have stable underlying boundaries, stale/cancelled work cannot overwrite newer state, failures degrade predictably, supported-version behavior is tested, and users can diagnose or bypass the editor layer when necessary.