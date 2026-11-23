# fal asset workflow

fal is an optional production backend, not a dependency of the game runtime. Use it when the user authorizes generation and an asset benefits from it. Existing authorization persists; do not ask again for each routine asset. Model IDs, input names, capabilities and pricing change: inspect the current endpoint schema before a new model family is used. The toolkit intentionally does not hard-code a “best” image, video, audio or 3D model.

1. Define the asset and its reference authority in `assets.json`.
2. Read the current model card/API schema; record the endpoint, input payload, output format and estimated cost. Prepare or upload only the authorized source material using the official client or connector. Local filesystem paths are not remote image URLs.
3. Use an edit/reference endpoint when continuity matters. A full sheet helps art direction, but single-object geometry usually needs an isolated, tightly framed asset first. Maintain identity constraints through every stage.
4. Set `case.json` generation `enabled: true` and a finite `budget_usd` consistent with the user's scope. Estimates reserve budget conservatively; this is not a billing cap enforced by fal. If no defensible estimate exists, obtain pricing rather than entering zero.
5. Use `fal-submit` without `--execute` to inspect a dry plan. `--execute` records intent before POST and saves the returned request ID and queue URLs. The same asset+endpoint+payload returns its existing local job. Poll with `fal-status`; do not rerun POST because a model is slow.
6. If a connection fails after submission, the job is **ambiguous**. Reconcile it in the fal dashboard using the saved payload and time/context. Recover the existing request ID/URLs in the job record when found. Never delete an ambiguous record just to resubmit. Local deduplication cannot promise exactly-once server execution.
7. Download completed outputs, record provenance, normalize them and review inside the game. Mark assets accepted, rejected or deferred. Store actual cost only when known; keep estimates clearly labelled.

The adapter sends `Authorization: Key ...` only to HTTPS `queue.fal.run`, rejects redirects and untrusted returned queue hosts, and never logs the key. JSON job files can contain private prompts or signed media URLs; keep `production/fal/` private and excluded from the published game. A stale local ledger lock can be removed only after confirming no submit process remains.

The adapter is schema-neutral. It does not upload files, select an endpoint, validate a model-specific payload, download outputs, retry failed jobs, or cancel running jobs automatically. Use the official fal client/connector for those actions as needed. Current API documentation: [queue submission](https://fal.ai/docs/api-reference/inference-api/queue/submit), [queue result](https://fal.ai/docs/api-reference/inference-api/queue/result), [fal docs](https://fal.ai/docs/).
