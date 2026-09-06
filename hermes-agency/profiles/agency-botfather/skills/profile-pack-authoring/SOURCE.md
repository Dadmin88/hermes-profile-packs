# Source provenance

- Canonical source: `https://github.com/techjanitor/botmaker`
- Source skill: `skills/autonomous-ai-agents/botmaker/SKILL.md` with `references/process.md` and `references/soul-craft.md`
- Reviewed revision: `93eb3b6d3976b115a372598fa5c02c4f6ab63ed2`
- Review date: 2026-09-06
- Upstream author: techjanitor
- License: MIT

## Local adaptations

Hermes Agency preserves the upstream methods of sharpening one job, writing an explicit not-list, requiring human approval before materialization, keeping repeatable procedure out of the SOUL, and validating before roster publication. The Agency version rewrites those methods for portable repository distributions: it scaffolds pack source artifacts rather than installed profiles, follows namespace/manifest/catalog/evaluation contracts, and hands completed work to independent review.

## Excluded upstream material

The reviewed upstream repository also contains host-specific live-profile creation commands, alias and symlink management, provider/model pinning, credential-adjacent peer setup, memory-provider setup, vault bookkeeping, scripts tied to `~/.hermes`, and a proposed protected-instruction safeguard exception. None of those mechanics, scripts, runtime files, or configuration overrides are vendored here. BotFather never writes to a live Hermes home, copies runtime state or secrets, pins a provider/model by default, or disables protected-instruction safeguards.

## MIT license notice

Copyright (c) 2026 techjanitor

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.