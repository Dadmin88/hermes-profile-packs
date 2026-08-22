# Source provenance

- Canonical source: `https://github.com/OutThisLife/brooklyn-skills`
- Source skill: `skills/pr-ready/SKILL.md`
- Reviewed revision: `f60ab3b43f422309c74dff5ed7dc53af042c2908`
- Review date: 2026-08-10
- Upstream author: Brooklyn Nicholson / OutThisLife
- License: MIT

## Local adaptations

Hermes Agency keeps the upstream skill's core merge-readiness loop: reconcile the real PR revision, base state, CI/checks, and review threads, then re-query the forge before claiming completion. The Agency version removes mandatory worktree and specific `gh`/`glab` command assumptions, generalizes repository/forge policy, avoids time-based bot polling rules, and preserves Agency's existing source-control ownership and portability standards.

## MIT license notice

Copyright (c) 2026 Brooklyn Nicholson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.