# BURN free-resource-landscape 20260927 h

## Verdict

steal

## Evidence

All probes 2026-09-27, keyless, 4 curl attempts total, 20s timeouts.

1. `GET https://api.featherless.ai/v1/models` (no params): HTTP 200, 7,070,076 bytes. Top-level keys `['data']`, no pagination envelope. `len(data)` = 22044 (board said 22032; +12 drift). First item keys: `['id', 'is_gated', 'created', 'model_class', 'owned_by', 'context_length', 'concurrency_cost', 'pricing']`; sample: `{"id": "recursal/EagleX_1-7T", "is_gated": false, "created": 1719250778, "model_class": "rwkv5-7b", "owned_by": "Feather", ...}`. Every model carries a unix `created`.
2. Pagination: `?limit=2&page=2` returns HTTP 200 with top-level keys `['data', 'pagination', 'total']` and `pagination: {"current_page": 2, "per_page": 100, "total_items": 50586, "total_pages": 506}`. `limit=2` was clamped to `per_page` 100 (100 rows returned); all 100 ids appear in the no-params dump.
3. Filter/sort guess `?sort=created`: HTTP 422 `{"error":{"message":"Validation error","type":"invalid_request_error","param":"sort",...}` whose body enumerates the accepted enum: `'downloads' | '-downloads' | 'favorites' | '-favorites' | 'parameter_size' | '-parameter_size' | 'context_length' | '-context_length' | 'created_at' | '-created_at' | 'hf_created_at' | '-hf_created_at' | 'name' | '-name' | 'id' | '-id' | 'popularity' | '-popularity'`. The error doubles as API documentation.
4. `?sort=-created_at` returns HTTP 200, verified newest-first client-side; first row `open-unlearning/unlearn_tofu_Llama-3.2-1B-Instruct_forget10_SimNPO_lr2e-05_b3.5_a1_d1_g0.25_ep10`, `created` 2026-09-27T15:43:00Z, the day of the probe. Dump holds 173 models created 2026-09 month-to-date.

Owed (unresolved, not asserted): 22044 models with no params vs 22035 with `sort=-created_at`, a 9-model delta minutes apart, cause unknown; paged mode reports `total_items` 50586 vs 22044 in the default dump (paged route may see a superset, e.g. gated or archived rows). WebSearch snippet for featherless.ai/docs/api-reference-models says the endpoint paginates "sorted by popularity" and does not document the created_at sorts the live API accepts; docs page not opened.

## Steal or Vacuous

Yes, a nightly roster-diff is buildable on this exact shape. One small call per night, `GET /v1/models?sort=-created_at&page=1` (100 newest rows), diff `id`+`created` against yesterday's snapshot; the full 7 MB keyless dump is the weekly backstop for deletions and for client-side sort by `created`. In fleet canon this upgrades Featherless from recon-only to a churn telemetry freelane: catalog reads need no key and ride no RPD denominator, so the diff feeds the EPNEWS roster-diff ledger lane the way the openrouter/groq/mistral counts already do, and new-model additions are the leading edge for spotting stealth sponsored windows (every new drop gets a death-date check on arrival). No key material touched.

## Falsifier

Build is pre-registered as falsified if, across two consecutive nightly runs, `?sort=-created_at&page=1` returns zero rows with `created` newer than the prior run while the full dump's max(`created`) advances, or if the keyless 200 turns auth-gated (401/403). Either outcome kills the diff premise and drops Featherless back to recon-only.

## Bibliography

Closed, read this session: 4 live probe responses from api.featherless.ai/v1/models (variants: no params; `?limit=2&page=2`; `?sort=created`; `?sort=-created_at`); watch/inbox/LINKS.jsonl (tail 30); watch/inbox/BURN_free-resource-landscape_20260927_b.md; WebSearch result text for "Featherless API models endpoint pagination sort created_at" (snippet-grade; featherless.ai docs pages not opened).
