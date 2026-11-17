# Agency game development capabilities

These selections extend 17 existing Agency profiles. Skills install with the distribution and load on demand. The existing Continuing Education preload and role-owned jobs stay in place.

| Profile | Existing specialist jobs | Previous supplemental skills and integrations | Added skills | Added tools |
|---|---:|---|---|---|
| `agency-art-director` | 5 | `creative-ideation` | `create-game-assets` | gltf-validator, Godot MCP (8 tools) |
| `agency-asset-artist` | 5 | `creative-ideation` | `create-game-assets` | blender-cli, gltf-validator, Godot MCP (11 tools) |
| `agency-audio-designer` | 5 | `creative-ideation` | `godot-audio` | ffmpeg, ffprobe, Godot MCP (17 tools) |
| `agency-dialogue-writer` | 5 | `creative-ideation`, `humanizer` | `dialogue-systems` | inklecate, ripgrep |
| `agency-environment-artist` | 5 | `creative-ideation` | `godot-3d-essentials`, `create-game-assets` | blender-cli, gltf-validator, Godot MCP (17 tools) |
| `agency-game-designer` | 7 | `creative-ideation` | `game-feel` | python, Godot MCP (17 tools) |
| `agency-godot-engineer` | 6 | `systematic-debugging`, `test-driven-development`, `context7` | `godot-gdscript-headless-testing`, `godot-2d-movement` | godot-cli, Godot MCP (67 tools) |
| `agency-level-designer` | 6 | `creative-ideation` | `godot-tilemap` | godot-cli, Godot MCP (30 tools) |
| `agency-lore-writer` | 6 | `creative-ideation` | `excalidraw` | ripgrep |
| `agency-narrative-designer` | 5 | `creative-ideation` | `dialogue-systems` | inklecate, ripgrep, Godot MCP (17 tools) |
| `agency-product-manager` | 6 | `document-to-action-items` | `excalidraw` | godot-cli, Godot MCP (9 tools) |
| `agency-qa-tester` | 5 | `dogfood` | `godot-gdscript-headless-testing` | godot-cli, Godot MCP (22 tools) |
| `agency-release-manager` | 5 | `gh-ref`, `deepwiki` | `godot-export` | godot-cli, sha256sum, Godot MCP (10 tools) |
| `agency-technical-artist` | 5 | `creative-ideation` | `godot-shaders` | blender-cli, gltf-validator, godot-cli, Godot MCP (25 tools) |
| `agency-tools-engineer` | 6 | `systematic-debugging`, `test-driven-development`, `pep-ref`, `context7` | `godot-gdscript-headless-testing`, `godot-export` | godot-cli, gltf-validator, Godot MCP (13 tools) |
| `agency-ui-ux-designer` | 5 | `accessibility`, `design-md`, `excalidraw` | `game-ui-ux`, `godot-ui-control` | godot-cli, Godot MCP (22 tools) |
| `agency-worldbuilder` | 6 | `creative-ideation` | `excalidraw` | ripgrep |

## Three.js browser games

These on-demand skills cover code-authored scenes and procedural art. Frontend Engineer owns browser implementation. Game Designer, Level Designer, QA and art specialists retain their production roles. For engine-free projects, keep gameplay state and collisions in project code and use Three.js for rendering.

| Profile | Added skills |
|---|---|
| `agency-art-director` | `threejs-materials-lighting` |
| `agency-asset-artist` | `threejs-geometry`, `threejs-materials-lighting` |
| `agency-environment-artist` | `threejs-scene-setup`, `threejs-geometry`, `threejs-materials-lighting` |
| `agency-frontend-engineer` | `threejs-scene-setup`, `threejs-gameplay-systems`, `threejs-performance`, `threejs-game-ui-designer` |
| `agency-game-designer` | `threejs-gameplay-systems` |
| `agency-level-designer` | `threejs-scene-setup`, `threejs-geometry`, `threejs-gameplay-systems` |
| `agency-qa-tester` | `threejs-scene-setup`, `threejs-gameplay-systems`, `threejs-performance` |
| `agency-technical-artist` | `threejs-scene-setup`, `threejs-geometry`, `threejs-materials-lighting`, `threejs-performance` |
| `agency-tools-engineer` | `threejs-scene-setup`, `threejs-performance` |
| `agency-ui-ux-designer` | `threejs-game-ui-designer` |

## Source review

The Hub search covered Godot, Blender, game and level design, playtesting, Ink and Twine, audio, Audacity, and localization. The selected community trees come from the pinned [Awesome Gamedev Agent Skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills/tree/19d93f97c9c1ea0f8b306e77aa81e0d3e352d3e9) catalog. Complete trees and reference files ship with Apache-2.0 notices. The existing reviewed Excalidraw skill is reused for world, canon and player-flow diagrams. Installed project tools and engine versions govern usage.

- The Donchitos playtest report depends on Claude hooks and other agents. The Game Designer and QA Tester already own playtest and defect workflows.
- The official Blender Lab MCP offers arbitrary Python execution inside Blender. Blender CLI and Khronos glTF Validator cover local asset inspection and export validation here.
- Ink is an optional local tool for projects that already use the format. The narrative roles share a dialogue workflow while retaining separate ownership of quest state and writing.

## Setup and use

Load `profile-capabilities` in the installed profile. Its catalog gives the exact selected skills, MCP tool names, native command prerequisites, and setup steps. The Godot MCP starts disabled. Build and apply the shipped patch explicitly, then enable the selected profile entry. Use a disposable Godot project for interactive playtests and verify cleanup.

Blender, Ink, FFmpeg, ripgrep, Python, and the other local commands use the profile’s existing terminal access when available. A capability entry neither downloads the program nor adds a new Hermes toolset.

The Godot integration removes raw code evaluation and unrestricted runtime method/property calls. It retains project inspection, scene authoring, live input, runtime state, capture, tests, and approved exports where the role calls for them. Files and engine state still require authorized project scope.

[Full capability matrix](CAPABILITY_MATRIX.md) · [Profile capability setup](CAPABILITIES.md)
