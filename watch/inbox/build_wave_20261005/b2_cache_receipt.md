# B2 CACHE-RESUME RECEIPT LAW - landed 2026-10-05 (build-it-all wave, lane B2)

Source steal card: `watch/inbox/frontier_olm_2026-10-04/steal/kv-cache-and-context-engineering.md:14-20` (arXiv 2609.15030: token-prefix validity != state validity; strict-prefix recovery, determinism pinning). Port move executed as specified by the card's estate map at `:24`.

## The receipt shape (mag/context_checkpoint.py)

Every checkpoint now freezes a `prefix_receipt.v1` dict over the frozen prefix the next turn would otherwise re-read:

- `prefix_sha256` - sha256 of the longest verified frozen prefix (full hexdigest; the authority for a complete match)
- `block_digests` + `block_bytes` (fixed 64) + `verified_blocks` + `prefix_bytes` - per-block digests walked block-by-block, radix strict-prefix lineage (`tools/prefix_cache_sim.py` semantics: stop at the first bad block)
- `config_generation` - the determinism pin (paper move 2); defaults to the model name, overridable per checkpoint

API: `freeze_receipt()`, `verify_strict_prefix()`, `gate_skip_recompute()`, `CheckpointEngine.reuse_prefix(session, candidate_prefix, config_generation)`. `ContextCheckpoint` carries `config_generation` + `prefix_receipt` through `to_dict()` and the disk reload path (roundtrip test proves the gate survives a cold engine).

## The gate (skip-recompute ONLY on complete receipt match)

- config-generation mismatch -> verified_bytes 0, reason `config-generation-mismatch` (identical bytes, different state producer: recompute)
- prefix divergence -> partial `verified_bytes` (block granularity), reason `prefix-divergence`, no skip
- no receipt (pre-law rows) -> reason `no-receipt`, no skip: unreceipted reuse costs the same as a miss
- candidate = prefix + fresh tail -> prefix verifies, tail is new work, never cached

## The KPI split (tools/cache_kpi.py)

`tok_hit%` stays the NOMINAL rate (all claimed cached tokens). New per-provider and TOTAL fields: `receipt_tok` (receipt-verified cached tokens, clamped to the row's own claimed cache), `tok_hit_receipted_rate` printed as `recv_hit%`, `unreceipted_tok` = claimed minus proven. Rows are stamped by producers via `cache_receipt.ok` + `verified_tokens` or the flat `receipt_ok` twins. First reading on `logs/provider_usage.jsonl` (instrument: `python tools/cache_kpi.py`, 2026-10-05): deepseek nominal hit 96.6% while receipt-verified reads 0.0% - no producer stamps receipts yet, so today the entire claimed cache is unproven. That gap is the number the law exists to expose.

## Gate contract numbers (instrument + moment, 2026-10-05)

- `pytest -q tests/test_cache_receipt_law.py tests/test_context_checkpoint_pack.py tests/test_context_freeze.py`: 12 passed (4 new receipt-law tests + 8 neighbors), 34.30s, repo venv.
- `python tools/violation_ratchet.py check --changed`: PASS, scope 18 changed files, hits 12 registered 12, NEW 0, exit 0. No new debt on my files.
- Line counts: mag/context_checkpoint.py grew 474 to 616 (its file-too-long claim is registered day-one debt; growth is a non-blocking ledger fact per B2-273; a split is a later named move, not this lane's). tools/cache_kpi.py at 267, under the bar. tests/test_cache_receipt_law.py at 132, zero collection errors.

## Owed (not faked)

- Producers (dispatch/flight-recorder call sites) do not yet stamp `cache_receipt` on usage rows; recv_tok reads 0 until the first wired lane lands. Blocked as a follow-up, not silently claimed.
- The card's falsifiable probe (poisoned 10% stale-generation blocks replayed through the null arm) remains open; this lane banked the law and its tests, the probe is next seat's cheap local run.
