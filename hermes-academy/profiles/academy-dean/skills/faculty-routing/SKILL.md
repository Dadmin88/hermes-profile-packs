---
name: faculty-routing
description: Route a learning request to the smallest useful set of Academy professors or instructors based on subject, level, and goal.
---
# Faculty Routing

Identify the primary subject and the learner's intended outcome. Prefer one specialist when one specialist can teach it well. Add another faculty member only when the request genuinely crosses domains.

Prefer the most specific installed Academy faculty member before a broad chair. For example, a clearly physics-specific request routes to `academy-physics-professor`, chemistry to `academy-chemistry-professor`, and biology to `academy-biology-professor`. Keep `academy-natural-sciences-professor` for interdisciplinary science, general scientific reasoning, or science learning that genuinely spans those specialties.

Use the same specific-over-broad rule for statistics, data science, philosophy, law and legal studies, theology and religious studies, education and pedagogy, cybersecurity, cloud and systems, project management, automotive, culinary arts, and music when the dedicated v0.2 faculty member is installed.

If no exact specialist exists, choose the closest broad faculty profile and state the limitation instead of inventing expertise.

## Profile Learner Routing

When a Hermes profile (e.g. `agency-backend-engineer`) requests education, route using the Academy manifest as authority:

1. **Input contract.** Accept only: learner profile name, learner role, one requested objective, and optionally relevant skill names/descriptions. Never accept full profile state, memory, secrets, or conversation history.

2. **Specialist preference first.** Check `academy.json` → `routing.specialist_preferences` for an exact topic match. If the specialist profile is installed, route there.

3. **Broad chair fallback.** If no specialist matches, check `routing.broad_chairs` for an interdisciplinary fallback. Mark the match as approximate.

4. **Category fallback.** If the specialist preference exists but the profile is not installed, fall back to the broad representative of that category (e.g. `academy-computer-science-professor` for technology topics). Mark the match as approximate.

5. **Role-description scan.** As a last resort, match the objective against faculty role descriptions. Choose the profile with the most keyword overlap. Mark the match as approximate.

6. **Never invent.** If no installed faculty member is a safe match, say so. Never fabricate a profile name.

7. **Label approximation.** Always tell the learner whether the match is exact or approximate. An approximate match means the faculty member covers the broad area but may not have the narrow specialty.

Use `routing.py` → `route_learner()` for deterministic routing decisions.
