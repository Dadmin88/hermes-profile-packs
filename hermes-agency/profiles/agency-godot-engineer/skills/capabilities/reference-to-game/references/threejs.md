# Three.js implementation profile

Use the user's chosen stack. For a new browser game, TypeScript + Vite + Three.js is a practical default. Verify current library APIs against official docs, pin compatible versions and commit the lockfile. Do not impose one example's older Three.js revision on a new project.

## Representation

- Use actual meshes for free-view heroes, collisions and changing silhouettes. Normalize generated geometry once: units, ground contact, forward/up axes, pivot, sockets, material response and animation bindings.
- Use painted sprites or layered cards for illustration-first characters when camera freedom allows it. Author facing directions, baselines and scale consistently. Depth-sort and occlude correctly; a transparent plane should not cast an opaque rectangle.
- Use modular geometry, instancing, atlases, merged static parts and shared materials for repetition. Maintain readable variation; rotating one cliff repeatedly is not a convincing environment kit.
- Use a real map/level graph and simple proxies for collision. Reuse the same coordinate conventions for movement, routes and camera.

## Color and materials

Three.js works in a linear lighting space and converts output for display. Mark color/albedo/emissive textures as sRGB; keep normals, roughness, metalness and masks in a non-color space. Configure tone mapping/exposure deliberately and encode output once. Test the palette under final lighting and post effects, not only in a texture viewer. Check the installed version's official color-management guidance.

Use the reference's material language. A physical transmission material may be costly and wash out small candy; test the alternative under actual lighting. A less physical material can better preserve the intended look. Match contact shadows, outline treatment and edge softness as carefully as hue.

## Runtime

Separate `game/` rules, `world/` views, `ui/`, `core/` and level data where useful. The DOM is suitable for sharp, accessible HUD text and interactive controls; values must come from live game state. Design UI for the target aspect ratios. Use event-driven audio buses, unlock audio from a user gesture and rate-limit one-shots. Keep a visible mute control.

Measure frame time, draw calls, triangles, memory and load size on a named device/browser/resolution. Treat budgets as project constraints, not universal 150-call rules. Cap DPR, provide quality settings, cull and reuse assets. Test that low quality still reads like the reference. Dispose replaced resources and remove event listeners on restart/unmount.

Use local files for shipped assets. API keys belong in a server-side generation process, never `VITE_` variables. Keep raw references, generation ledgers and recordings out of `public/` unless intentionally shipped. Verify a production build served over HTTP; `file://` is not a realistic module test.

Official sources: [Three.js manual](https://threejs.org/manual/), [Three.js docs](https://threejs.org/docs/), [Vite guide](https://vite.dev/guide/), [glTF specification](https://github.com/KhronosGroup/glTF/tree/main/specification/2.0).
