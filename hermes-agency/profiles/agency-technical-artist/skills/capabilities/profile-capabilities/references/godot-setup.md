# Godot MCP setup

Read `catalog.json` for the pinned checkout and this profile's tool list. The template starts disabled. The source build uses Godot 4, Node.js 20 or later and the checkout's pinned pnpm version.

1. Check out the exact commit from the catalog. Apply the packaged patch from the checkout with `git apply /path/to/godot-local.patch`.
2. Run `pnpm install --frozen-lockfile --ignore-scripts` and `pnpm run build`. Verify that the intended Godot binary is discoverable from the profile environment.
3. In the profile's supported configuration editor, merge only the `godot` entry from `mcp-servers.json`. Replace its argument with the absolute path to the patched `build/index.js`. Keep the profile's tool list, leave parallel calls disabled and explicitly enable the entry. Existing profile updates preserve the local configuration.
4. Check `hermes -p <profile> mcp test godot` in a fresh session. Use `get_godot_version`, then `get_project_info` against a trusted scratch project. Follow the project's editor version and renderer. If the bridge is unavailable, use the installed Godot CLI where it supports the task.

Use `run_interactive` only in a disposable project checkout. It starts a separate game process, temporarily changes `project.godot` and adds an input receiver. Use `stop_project` and check the checkout afterwards. Run one interactive test at a time on the host. The patched receiver binds only to loopback on port 9877 and is accessible to other local processes while it runs. The patch removes raw runtime evaluation and arbitrary method/property calls from both tool discovery and the TCP receiver. Editor tools that run a project execute that project's own code. Use trusted project copies, and keep project and output paths within the task's workspace.

Scene tools operate on saved project files. Save or close conflicting editor tabs before using write tools and verify that the expected file changed before reloading it in the editor.
