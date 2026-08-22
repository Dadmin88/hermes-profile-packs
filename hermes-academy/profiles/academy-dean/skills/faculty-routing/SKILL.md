---
name: faculty-routing
description: Route a learning request to the smallest useful set of Academy professors or instructors based on subject, level, and goal.
---
# Faculty Routing

Identify the primary subject and the learner's intended outcome. Prefer one specialist when one specialist can teach it well. Add another faculty member only when the request genuinely crosses domains.

Prefer the most specific installed Academy faculty member before a broad chair. For example, a clearly physics-specific request routes to `academy-physics-professor`, chemistry to `academy-chemistry-professor`, and biology to `academy-biology-professor`. Keep `academy-natural-sciences-professor` for interdisciplinary science, general scientific reasoning, or science learning that genuinely spans those specialties.

Use the same specific-over-broad rule for statistics, data science, philosophy, law and legal studies, theology and religious studies, education and pedagogy, cybersecurity, cloud and systems, project management, automotive, culinary arts, and music when the dedicated v0.2 faculty member is installed.

If no exact specialist exists, choose the closest broad faculty profile and state the limitation instead of inventing expertise.
