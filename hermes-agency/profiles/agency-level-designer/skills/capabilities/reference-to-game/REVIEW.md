# Source and adaptation review

Upstream: https://github.com/gokayfem/reference-to-game
Commit: 6a00e491f578bbfcbdba45f0c7bddf4693016e61
License: MIT. Original LICENSE included.

All 18 original files in skills/reference-to-game are bundled unmodified; example games/media excluded.
Three.js/TypeScript is the supported default; Godot can follow the engine-neutral process but no Godot generator is shipped.
On-demand only. No permissions, plugins or MCPs are enabled. No packages are installed automatically.
Pillow (upstream >=10.4,<13), ffmpeg/ffprobe and Node are task-specific dependencies.
Optional fal-submit --execute can make paid external calls. Require explicit user permission, data-transfer review and budget.
Static review: bounded ffmpeg/ffprobe subprocess calls, no shell; no automatic external transmission on installation.
Upstream tests run locally: 25 Python PASS, 7 JavaScript PASS. Pillow 13 caused one deprecation warning.
This does not certify visual accuracy or agent quality.
