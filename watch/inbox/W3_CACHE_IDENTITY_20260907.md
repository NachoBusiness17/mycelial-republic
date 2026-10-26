# W3 cache-identity probe — falsifier receipt (2026-09-07, zcode)

Falsifier F-W2 (watch/WORLDLINE_SEED_20260907.md §4): "byte-identical seed →
≥95% hit; one-byte genome drift → measurable hit-rate collapse." Instrument:
`mag/cache_identity.py` (PROXY, $0-local — host ollama v0.32.7 at 127.0.0.1:11434,
specimen `qwen2.5:3b-instruct`, non-streaming /api/chat, temperature 0,
keep_alive 10m, no docker, no config edits). Rows:
`memory/runs/cache_identity/probe_20260907.jsonl` (3 rows: calibration,
contaminated attempt, clean final — full trace kept honestly).

## Design

Body = ~1600 tokens (6400 chars) of REAL repo text, honestly labeled PROXY
corpus (AGENTS.md head + W0 tape digests; label chunk leads so every body
carries it; body_sha16 100a184797bbf489 constant across all runs). Fixed
continuation for every arm: "Repeat the last sentence of the context verbatim."
— the model answers the sentinel sentence verbatim (task-valid). Four timed
arms per round, 3 rounds, medians:

- COLD — seeded genome marker in the header; previous cache diverges at the
  marker → ~full prefill.
- WARM-IDENTICAL — the exact same request sent again back-to-back.
- DRIFT-TAIL — one byte flipped at 95% of the body, length preserved
  (honesty arm: "where the bytes are").
- DRIFT-HEAD — one byte flipped at 10% of the body — the production genome
  position (system-prompt region). Round order cold→warm→tail→head keeps the
  KV slot dynamics clean.

Per request: wall_ms stopwatch AND ollama's internal prefill stopwatch
(`prompt_eval_duration`), plus eval/load/unaccounted ms. The verdict gates on
prefill timing; wall corroborates (shared-host wall carries multi-second
scheduler/pagecache noise — calibration once logged an 18.3s wall on a 16ms
prefill).

## Medians (clean final run, seed 1788788412/nonce, ollama v0.32.7)

| arm | prefill ms (median) | wall ms (median) |
|---|---|---|
| cold | 10,711 | 11,089 |
| warm-identical | 13.8 | 366 |
| drift-tail (95%) | 922 | — |
| drift-head (10%) | 9,496 | — |

Metrics: speedup_prefill 778.1x · hit_ratio_est 0.9987 · collapse_ratio 0.887 ·
drift_vs_warm 689.9x · tail_retention 0.914. Calibration run (13:35Z) agrees:
732.6x / 0.9986 / 0.923 / 0.909 — round-to-round spread <1%.

## F-W2 VERDICT: SUPPORTED (PASS) — PROXY

All four documented gates met: identical warm re-lights at 778.1x prefill
speedup (≥2x gate) with hit-est 0.9987 (≥0.95 gate — the ≥95% hit line),
one-byte genome-region drift collapses to ~cold (0.887 of cold prefill), and
drift-vs-warm is 689.9x (≥2x). THE STANDING WAVE IS REAL IN TIMING: the
warmed prefix re-lights; the genome drift kills it. Secondary line MEASURED:
tail_retention 0.914 — one byte at 95% depth keeps ~91% of the benefit, one
byte at 10% depth (genome position) keeps none. "Byte-identity matters most
where the bytes are fewest" — MEASURED (PROXY). ollama's reuse is
longest-common-prefix per token: the production read is that genome bytes
(sitting at the head of the worldline) are the expensive bytes to let drift.

## The hazard the probe caught (emergent finding, on the record)

Attempt 1 of the dogfooded final run (seed pinned 20260907 = calibration's
seed) came back INVERTED: drift_head hit in 14ms while drift_tail fully
missed — because ollama's lingering KV slots served the previous run's
byte-identical `drift_head` sequence back as a cache hit. Cross-run
byte-identity re-lights the cache: the standing-wave thesis itself showed up
as instrument contamination. Row 2 keeps the honest UNPROVEN verdict. Fix
landed in the instrument: per-run nonce seed by default, `--seed N` pins a
run byte-for-byte for replay. Lesson for the worldline seed: resurrected
context must cite WHICH worldline it claims — byte-identity is so real it
resurrects strangers' prefixes.

## Honest limits

- PROXY: local 3B prefill timing on a shared host, NOT the production
  GLM-5.3-flash Max 1M-token meter — the c1/c2 context-anatomy screenshots
  (cache hit 97.3/96.7%) remain the manual production datapoints.
- Ollama cache semantics are implementation details: this measures PREFILL
  TIMING, not token-exact hit counts. `prompt_eval_count` reports total
  prompt tokens even on full hits (1794 with 13.8ms prefill); the recompute
  duration is the signal. Hit ratio is an estimate, 1 - t_warm/t_cold.
- KV-reuse behavior across slots/runs is version-specific (observed above);
  any replication must re-run, not assume.
- Verdict tri-state per fleet law: SUPPORTED here is the instrument's
  question (byte-identity → timing), not production resurrection fidelity
  (F-W1, still open; row 320 still open).

## Offline gates + dogfood

`python -m mag.cache_identity check` → PASS (27 assertions: composition
determinism, exactly-one-byte drift integrity at both fracs, marker
determinism/uniqueness, medians, metric formulas, all three tri-state
branches). `tests/test_cache_identity.py` → 10/10 PASS, offline.
DOGFOOD SEALED: the clean final probe ran through `python -m mag.bash_local`
(session w3-cache-identity-20260907, two chained rows — the contaminated
attempt b9f86c32e732288e, then the clean run 5e07f5758cc34332 <- b9f86c32...).
Tape after: 53 rows / 19 sessions, verify PASS, tip 5e07f5758cc34332 — the
chain tip IS the row describing the measurement that proved byte-identity.

## State

W3 LANDED. F-W2 measured SUPPORTED (PROXY). Still open on the card: F-W1
resurrection (row 320), F-W3 provenance tamper, F-W4 rate, F-W5 done
(LARGE_EFFECT, selector survives). The worldline seed now has its seismograph:
cache receipts are positional encoding, measured.
