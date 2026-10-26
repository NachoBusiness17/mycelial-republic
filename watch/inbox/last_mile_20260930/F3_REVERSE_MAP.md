# F3_REVERSE_MAP - the wide-exploration engine, built and proven at 20-wide

2026-09-30/10-01 · seat: zcode (F3) · ownership: `tools/reverse_map.py`,
`configs/reverse_map_questions.json`, `watch/inbox/last_mile_20260930/F3_REVERSE_MAP.md`,
run artifacts under `logs/reverse_map/q39_quota_ledger_20261001T001945Z/`. No commit by me.

## Mission (operator)

"fifty wide to reverse-map novel solutions from higher dimensions": 50 parallel cheap
answers on the SAME hard question produce a solution-space sample a single expensive
answer cannot; the novel solutions live in the tails of the strategy distribution, not
the mean. Build: question loader (estate's real hard problems) -> dispatcher (same
prompt to N models in parallel) -> analyzer (cluster by SOLUTION STRATEGY, not
similarity; identify minority strategies) -> output (strategy map + novel candidates +
consensus head) -> one real question at 20-wide as the proof.

## What landed

1. **Question loader.** The bank lives as data in
   `configs/reverse_map_questions.json` (6 questions, each with source citation):
   the parity deep-cut (Q02 hydrology family, V5_PARITY), the route's open design
   question (r1_route_coldstart, AD4_GPS_SPEC AMENDMENT 5 cold-start probe
   allocation), and four NONE-instrument frontier items from the 52-question
   inventory (Q39 quota ledger, Q03 frame MAC, Q26 load bench, Q14 flock parity)
   (watch/inbox/mountain_climb/FIFTY_QUESTIONS.md ranking-honesty list). `--ask-file`
   loads any custom ask; `questions` lists the bank.
2. **Dispatcher.** `tools/reverse_map.py` fires the byte-identical ask to a fleet in
   one ThreadPool burst: flash bulk (qwen/qwen3.7-flash) + second flash family
   (deepseek/deepseek-v4.1-flash) + judgment tier (z-ai/glm-5.3-prime, temp pinned
   <= 0.7) + contrast families (openai/gpt-6-luna, google/gemma-4-31b-it,
   mistralai/ministral-3b-2512). Temperature ladder 0.5-1.15 per shard spreads the
   sample; the ask bytes never change. Call shapes ride the W8 receipts (qwen3.7
   400s on the reasoning param -> plain body; ds flash needs thinking-off; glm-prime
   capped reasoning) with a tiny liveness+shape probe per distinct model before any
   fire (V9 law 5: dead models dropped BEFORE dispatch, never rotated mid-run).
   Reuses tools/duel_harness.py for keys, base URL, and cost metering (usage.cost
   preferred). Worst-case projection vs budget cap refuses the run before any spend;
   resume is idempotent off answers.jsonl.
3. **Analyzer.** One funded-tier call (glm-5.3-prime, $0.027) clusters the N answers
   BY STRATEGY: "same mechanism (core structure + update rule)", not prose similarity.
   Strict-JSON contract; parse failure falls back to a marked lexical-vote clustering
   (mode=lexical-fallback, never silent). Digest per answer = section headers + head
   900 + tail 250 chars (25,415 digest chars for 20 answers).
4. **Output.** `logs/reverse_map/<run_id>/`: answers.jsonl (per-shard model, temp,
   cost, secs, content), run.json (ask + provenance + corr_id, AH14 shape),
   analyzer_raw.txt (judge output verbatim), strategy_map.json + strategy_map.md
   (the map: strategies with mechanism, ids, model composition; head = consensus;
   tail = clusters of size <= ceil(0.15 N) = novel candidates; consensus sketch).

## The live proof: q39_quota_ledger at 20-wide (the receipt)

Question: FIFTY_QUESTIONS Q39 (P9, instrument NONE) + RIB_DRIVING_LADDER: dollars
are metered per call but the binding currency is a 5-hour rolling-window quota with
no ledger; 50-wide bursts 429-storm. Design the window meter (structure, update
path, predict API, mid-burst recovery, wall-clock-free falsifier).

Fleet (20 shards, one parallel burst): 12 qwen3.7-flash, 3 deepseek-v4.1-flash,
2 glm-5.3-prime, 1 gpt-6-luna, 1 gemma-4-31b-it, 1 ministral-3b-2512.
Result: 20/20 ok, 13.3-100s wall per shard (parallel; whole burst ~100s), shards
$0.0574 + analyzer $0.0273 = **$0.0847 total** (cap $3.00; worst-case projection
$0.21 pre-computed and shown by --dry). Answers 829-10,130 chars.

### Strategy map (mode=judge, no orphans, every sid covered exactly once)

| # | strategy | size | tag | models in it |
|---|----------|------|-----|--------------|
| S1 | exact timestamp ring | 10 | HEAD (consensus) | qwen-flash x5, ds-flash x2, glm-prime x2, gemma-4 |
| S2 | time-bucket counter ring | 6 | mid | qwen-flash x5, ds-flash x1 |
| S3 | delta event ledger (+1 dispatch / -1 refund) | 4 | mid | qwen-flash x3, ministral-3b x1 |

Consensus sketch (head): per-account bounded ring/deque of exact dispatch timestamps
covering 5h, evict on slide, mirror every dispatch/429/refund to an append-only JSONL;
predict(N) compares active count + inflight reservations vs capacity returning
hold/fail/uncertain; mid-burst 429 -> halt, refund unconfirmed slots, cooldown;
logical-clock simulator replays two burst schedules to falsify without wall-clock.

Clustering spot-checked byte-honest against banked answers: s14 (ring of timestamps,
ds), s19 (deque of floats, gemma) = S1; s06 (300 x 60s buckets, qwen) = S2; s02
(deque of (expiry, delta) with refunds, qwen), s20 (sorted (ts, qty) pairs,
ministral) = S3. The judge's own caveat: S1/S3 boundary is fuzzy for s10/s20
(update rules differ in kind but share deque shape).

### Novel count - honest, both readings

- Pre-registered rule (tail = size <= ceil(0.15 x 20) = 3): **0 novel candidates**
  at 20-wide. The rule fired exactly as coded; no goalpost move after seeing results.
- Descriptive minority read: S3 (delta event ledger, 4/20 = 20%, the only strategy
  carrying refund/reversal semantics) IS the minority strategy signal, and it is
  over-weighted by the sampling tails (3 of its 4 members are temp >= 0.85 qwen
  shards plus the sole ministral-3b-2512 answer, the deep-tail model). The engine's
  design width for real tails is 50 (fleet: 36 flash + 9 ds-flash + 2 prime + 3
  contrast, worst case ~$0.35): at 20 samples with 12 shards from one flash family,
  the family prior dominates the distribution and tails of size 1-2 have not
  resolved. That is the instrument reading, not a failure.

## Bug found and fixed during the proof (fix comment carries it)

First analyzer fire died twice: `dh.fire` calls `caller(..., max_tokens=N)` as a
KEYWORD; the judge lambda had the parameter named `mt` -> TypeError, both attempts.
Fixed by naming the param `max_tokens` (comment in tools/reverse_map.py names the
cause + the live evidence). The 20 banked shards were NOT re-paid: the fix was
exercised through `analyze --run-dir`, which re-analyzes banked answers at zero
contender cost. That subcommand is itself the resume path (answers.jsonl idempotent).

## Conditions (one-bug law)

- Instruments: shards fired via tools/reverse_map.py (exit 0, 20/20 ok rows in
  answers.jsonl); analyzer via glm-5.3-prime, mode=judge, parsed clean, 0 orphans.
- Moments: dispatch burst 2026-10-01T00:19:45Z-00:21:30Z; analysis 2026-10-01T00:22:39Z
  (same machine, same key set; NOUS_SDD_API_KEY only live key in hermes/.env).
- Assumptions: digests truncate each answer to headers+900+250 chars (judge saw
  25,415 of ~103K total answer chars); prices are W8/V9-metered fallbacks, real
  metering preferred usage.cost on every row; minority threshold 0.15 fixed before
  the run; fleet composition fixed before the run.

## Gates and census

- Ratchet `check --changed`: tools/reverse_map.py at 400 lines (the cap), ZERO
  new debt (file-too-long was the fight; everything else clean: no bare except,
  no env-key literal reads, no cwd-relative paths). The one remaining NEW hit in
  the changed scope is tools/flock_parity.py (1,034 lines) - sibling lane's
  in-flight file, not F3's.
- Tests: no test file added (ownership names two files; the tool is exercised by
  the live run + smoke asserts in the session log). Census delta: 0 collected
  (no test file landed; grep proves no test imports reverse_map).
- Full `pytest -q` instrument reading (B2-216 law: name instrument, moment,
  completeness): started 2026-09-30 ~20:23 local, KILLED by the session harness
  at ~25% progress (log shows only passing dots through the 25% mark, zero
  failures observed in the observed portion). No full-suite number is claimed
  from a partial run. F3's exposure is nil either way: nothing in the tree
  imports tools/reverse_map.py except the tool itself.

## How to check / reuse

```
.venv/Scripts/python.exe tools/reverse_map.py questions
.venv/Scripts/python.exe tools/reverse_map.py run --question q39_quota_ledger --dry
.venv/Scripts/python.exe tools/reverse_map.py run --question r1_route_coldstart --width 50
.venv/Scripts/python.exe tools/reverse_map.py analyze --run-dir logs/reverse_map/<id>
cat logs/reverse_map/q39_quota_ledger_20261001T001945Z/strategy_map.md
```

Feeds: S3's refund-semantics minority is the candidate the next 50-wide pass should
watch; r1_route_coldstart is the loaded next question for the router lane (D2 GPS).
