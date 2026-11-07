# Local editor setup

Both MCP entries ship disabled. Use the active profile's `profile-capabilities` catalog for the exact Git revisions and allowlists. The server and editor must run on the same machine. Use a dedicated scratch project for verification.

## Pixelorama

1. Use Pixelorama 1.2, Node.js 22.13 or later and Godot 4.6 or later for packaging. Check out the catalog's pinned TeeboBaggens revision in a clean local tools directory. Apply [the reviewed patch](pixelorama-local.patch) from that checkout with `git apply /path/to/pixelorama-local.patch`. Use the patched checkout for both components.
2. In `mcp-server`, run `npm ci --ignore-scripts` followed by `npm run build`. From the repository root, run `godot --headless --script pack.gd` to build `PixMcpBridge.pck`. For GIF support, set `PIXELORAMA_SRC` to the corresponding official Pixelorama source checkout before packaging so the build can include its GIF shaders. Skeletor is optional and needed only for rig tools.
3. In Pixelorama Preferences → Extensions, disable any old **pix-MCP Bridge** extension, import the source-built PCK and enable it. The patched build binds loopback port 7374, rejects browser-origin requests, and unregisters raw GDScript execution on both ends. Other local processes can still reach it. Keep it on a trusted workstation and disable it when finished. Keep private or unrelated tabs out of the active editor session.
4. Point the disabled Hermes `pixelorama` entry at the absolute path to `mcp-server/dist/index.js`. Enable it as described below. Check `hermes -p agency-pixel-artist mcp test pixelorama` and use `get_canvas_info` on an empty tab. In scratch, create a canvas, draw a small patch, add a frame and export a PNG. Read tool schemas for index conventions, especially when switching between frame indexes and tagged animation exports.

## Aseprite

1. Use Aseprite 1.3 with its native Lua `json.decode` API and Node.js 22 or later. Check out the catalog's pinned Vollkorn Games revision. From the checkout, apply [the reviewed patch](aseprite-local.patch) with `git apply /path/to/aseprite-local.patch`. The patch requires native JSON parsing and rejects flag-shaped paths.
2. Run `pnpm install --frozen-lockfile --ignore-scripts` followed by `pnpm run build` using the checkout's pinned pnpm version. Make sure the intended Aseprite binary is discoverable and `MCP_TRANSPORT` is unset or `stdio`. Use stdio only.
3. Point the disabled Hermes `aseprite` entry at the absolute path to `build/index.js`. Enable it as described below. Check `hermes -p agency-pixel-artist mcp test aseprite`, then create and export a small sprite in scratch. Batch calls act on files and can overwrite a target. Use working copies and serialize edits.
4. If MCP is unavailable, a locally installed Aseprite can still export from a working copy. For example, `aseprite -b sprite.aseprite --list-tags --data sprite.json --sheet sprite.png` writes an atlas and metadata. Check local CLI help and validate the resulting sheet layout and frame tags.

## Enable and verify

Use the profile's supported configuration editor, such as `hermes -p agency-pixel-artist config edit` where available. Resolve the placeholder in the selected server's `args`, then set its `enabled` flag to `true` and retain the other fields. If the profile already has customized config, merge only the intended entry from the catalog's `mcp-servers.json` reference. Open a fresh profile session and check the available tools before editing art. Test with synthetic data first. If an editor or tool is unavailable, state which export or edit still needs it.

Server allowlists limit which tools Hermes exposes. The bridge processes still run with workstation-user permissions and may open or overwrite permitted file paths. Keep inputs and outputs in the authorized workspace. Do not forward editor ports or point the bridge at a different host.
