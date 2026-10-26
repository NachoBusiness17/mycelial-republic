# B2-55 build-lane model flip, 2026-09-26

## Verdict

LANDED. stealth/union-alpha is provider-dead (its 404 body names the successor). Primary flipped to unbiased/pareto in scripts/build_lane_game.py; briefs DD-blob-double and DD-split-path refired and both reached the gate honestly: DD-blob-double PASS in 2 gens, DD-split-path PASS in 1 gen, both promoted. promoted 19 -> 21, generations 84 -> 87. No silent 404 loop.

## Evidence with file:line quotes

- 12 transport-dead rows today: watch/inbox/union_fullsend_20260917/build_lane/proposals.jsonl:100-111, e.g. :100 `"error": "HTTP 404", "detail": "...Thank you for participating in the Stealth Union Alpha testing period. This model was Unbiased's Pareto. Use it now: https://openrouter.ai/unbiased/pareto"` on brief DD-blob-double; same body on DD-split-path through :111. All 2026-09-26, all key_index 0.
- public model list (openrouter.ai/api/v1/models, fetched 2026-09-26): `"id":"unbiased/pareto"` present, `"id":"z-ai/glm-5.3-flash"` present, no `"id":"stealth/union-alpha"` (only stealth/space-bunny-alpha).
- live probe through the script's own `_call` with the lane's real keys: unbiased/pareto ok=true (READY, 27s), z-ai/glm-5.3-flash ok=true (1.4s).
- flip: scripts/build_lane_game.py:64 `"models": ["unbiased/pareto", "z-ai/glm-5.3-flash"]`; :340 `primary = "unbiased/pareto"`; :350 the after-11:00 schedule branch also flipped (the old literal would have resurrected the dead model on alternating runs); docstring spec updated with the flip receipt.
- refire: proposals.jsonl:113 DD-blob-double gen 2 `"verdict": "PASS", "gate": "PASS  [ruins_go_pack_cand_DD-blob-double.json] the-blob-that-doubles The Blob That Doubles · 4 moves"`; :114 DD-split-path gen 1 `"verdict": "PASS", "gate": "PASS ... splitting_blob_aftermath The Splitting Blob: Aftermath · 8 moves"`. Receipts on disk: receipts/promoted_DD-blob-double_g2.json, receipts/promoted_DD-split-path_g1.json. Pack: dashboard/static/games/ruins_go_pack.json:989, :1019. state.json `"model": "unbiased/pareto"`, `"generations": 87`.
- independent gate re-run by this lane (not the driver's claim): `node test_ruins_go.js --pack-all` printed `PASS [ruins_go_pack.json] the-blob-that-doubles ... 4 moves` and `PASS [ruins_go_pack.json] splitting_blob_aftermath ... 8 moves`.
- honesty note: proposals.jsonl:112 (gen 1) the model answered `"error": "This encounter cannot be implemented under the supplied engine laws."` naming L3/L5 conflicts; gen 2 designed a gate-legal interpretation.

## Work done

Read the whole driver (475 lines pre-edit). Located the real lane dir (watch/inbox/union_fullsend_20260917/build_lane, not a root build_lane/). Counted the 12 x 404 rows and matched state gens 72 -> 84. Verified the successor three ways (404 body, public API, live READY probes). Flipped _LANES, primary, schedule branch, and the docstring spec; fix comments carry the receipt; py_compile clean. Ran `--batch 2`; both DD briefs promoted; verified promoted receipts, pack membership, state counters, and re-ran the node gate myself. Wrote this receipt, the ledger row, and 3 self-feed briefs: first drafted B2-150/151/152, but a pre-write census check caught concurrent lanes had claimed those numbers mid-flight (queue climbed to B2-186), so they landed as B2-187/188/189 (DD-briefs-vs-engine-laws, transport tripwire, retirement-body parser).

## Falsifier

- Any new stealth/union-alpha HTTP 404 row in proposals.jsonl dated after 2026-09-26 falsifies the flip.
- `node test_ruins_go.js --pack-all` no longer printing PASS for the-blob-that-doubles or splitting_blob_aftermath falsifies the promotions.
- state.json `"model"` differing from unbiased/pareto after the next run falsifies the sticky-model law.
- The promoted DD levels satisfying the briefs' literal duplication mechanic (not an interpretation) would falsify the B2-150 self-feed framing.

## Bibliography closed

scripts/build_lane_game.py (whole file) · watch/inbox/union_fullsend_20260917/build_lane/{proposals.jsonl,state.json,briefs.json,receipts/} · dashboard/static/games/ruins_go_pack.json · node test_ruins_go.js --pack-all · https://openrouter.ai/api/v1/models (2026-09-26) · watch/inbox/burn_wave_20260926/QUEUE.md · memory/burns/LEDGER.jsonl
