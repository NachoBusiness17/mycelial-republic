# PURPLE HARVEST B4 — FORECAST mode on decl_attention (built 2026-09-06; 5 of 6 falsifiers PASS, 1 FAIL reported honestly)

**Card:** watch/PURPLE_HARVEST_TRIAGE_02_20260906.md · **Paper:** SparDA —
Sparse Decoupled Attention for Efficient Long-Context LLM Inference,
arXiv:2606.04511 (abstract re-verified against arxiv.org bytes this turn: the
Forecast is "a fourth projection... alongside Query, Key, and Value" that
"predicts the KV blocks needed by the next layer, enabling lookahead
selection," decoupled from the attention query; 1.7× decode speedup is OVER
THE SPARSE-OFFLOAD BASELINE — the triage card's baseline qualifier stands).
**Extends:** watch/PURPLE_HARVEST_B3_DECL_ATTENTION_20260906.md (the organ).
**Built by:** background builder, same turn as launch (LAUNCH LAW amendment 5).

## What changed (file:line)

`mag/decl_attention.py` only — an addition, not a rewrite (445 → 740 lines).
Existing modes, quiz, `demo`, and `view` CLI untouched; B3 `demo` re-run after
the edit: EXIT=0, byte-identity shas reproduce (dfded2e9a77f / 7be832380c5d).

- FORECAST section header + honesty rules: decl_attention.py:425-447.
- Knobs, fixed BEFORE measurement: `FORECAST_TOPIC_BUDGET = 60` blocks,
  `FORECAST_DOC_LOOKAHEAD = 2` blocks, `BASELINE_SEED = 2609` (:442-444).
- `WalkStep` + the two scripted walks, frozen pre-measurement (:449-516).
- `build_topic_adjacency` (:520) — topic→topics from the cards' own topic
  lists: within-card cliques PLUS consecutive-card tag links; build-time
  metadata only, the deterministic stand-in for SparDA's learned head.
- `forecast_prefetch` (:543) — the Forecast analog: topic docs → top-budget
  blocks by shared-neighbor count with the current topic's co-occurrence set
  (ties by block index); text docs → the next `budget` blocks in document
  order. Deterministic end to end.
- `baseline_prefetch` (:561) — F4(a) control: same walk, same budget, blocks
  drawn uniformly (seeded). No adjacency knowledge.
- `run_walk` (:570) — the serving harness, SparDA's order: step k's predict
  runs at the END of step k; step 0 is a cold start and counts its miss.
  Hits served from the prefetch buffer, misses fall back to the existing
  on-demand seek()+read path and are COUNTED; a mask invariant asserts the
  reader-visible slice never leaves the declaration mask (never-silent guard).
- `forecast_demo` (:648) + `forecast` CLI command (:711, :722); exit code =
  verdict, same convention as `demo`.

Zero-Mem zero-token law honored: walk readers are the B3 regex readers
(`extract`/`extract_last`/count) — zero tokens end to end.

## Walk definition — chosen BEFORE measuring (stated, per triage law)

Walks, budgets, and seed were frozen from the artifacts' shapes before any
forecast number existed. Pre-flight checked only that every needle ANSWERS
from the GLOBAL slice (reader sanity, 24/24 OK) — not hit-rates. B3 `demo`
regression ran first. **The one falsifier that failed was NOT retuned; it
stands as a finding.**

- **TOPIC_WALK** (watch/topic_index.json, 12 queries, budget 60, seed 2609):
  mcp bucket → intake → auth-lite → vision → docker-fleet → economics →
  self-steal → verkle-chain → trajectory → concurrency (a session moving
  through the mcp bucket's co-occurring neighbors) → newest cards
  (`<local window="100">`) → overseer (deliberate low-adjacency jump so a
  miss is visible).
- **CURRICULUM_WALK** (corpus/CURRICULUM.md, 12 queries, budget 2, seed
  2609): Headline → sections 1-10 in reading order → ONE jump to ADDENDUM
  (the newest clone).

## Falsifier numbers (real, from `python -m mag.decl_attention forecast`)

**TOPIC_INDEX — 3/3 PASS.** (1,041 blocks; 1,964 block-visits over the walk.)
- F4(a) hit-rate ≥ 2× uniform baseline: **PASS — 14.2% (279/1,964) vs 4.6%
  (91/1,964) = 3.07×.** Adjacency ranking beats uniform draws at equal
  60-block budget.
- F4(b) attended cut vs GLOBAL ≥ 30%: **PASS — 620,356B vs 3,398,652B =
  81.7% cut.** Split: forecast-served 110,961B + on-demand fallback
  509,395B; skipped vs GLOBAL 2,778,296B. Plain FOCUS on the same walk:
  identical 620,356B (see COMPOSE).
- F4(c) every miss reported: **PASS — 12/12 steps missed (cold start
  included); all 12 listed with fallback bytes** (e.g. w_intake
  246blk/77,672B, w_auth_lite 290blk/87,969B, w_overseer 14blk/5,097B — the
  deliberate jump missed honestly). Mask invariant held on every step.
  Integrity: all 24 served answers (12 steps × 2 policies) == GLOBAL answers.

**CURRICULUM — 2/3 PASS, F4(a) FAIL (reported, not tuned).**
- F4(a): **FAIL — 31.2% (5/16) vs 18.8% (3/16) = 1.67×, under the 2.0× bar.**
  Two structural causes, visible in the numbers: (1) small population — with
  6 blocks total, a uniform draw of 2/6 is a 33% chance per draw, so the
  random baseline is strong; the same policy that triples the baseline on a
  1,041-block catalog only manages 1.67× on a 6-block doc — forecasting pays
  when the block space is big. (2) intra-block locality unmodeled — sections
  are ~1.3KB against a 1,200B block target, so consecutive sections usually
  share a block; the doc-order policy looks FORWARD past max(visible) and
  never predicts the current block itself, which the mask already serves.
  11 of 12 steps missed exactly 1 block — that block. This is the honest
  boundary of cheap adjacency at proxy scale: a learned Forecast head (or a
  co-location term in the policy) is the paper's answer to what our dumb
  policy misses.
- F4(b): **PASS — 23,343B vs 94,956B = 75.4% cut** (forecast-served 6,318B +
  fallback 17,025B; skipped 71,613B).
- F4(c): **PASS — 11 misses listed, each 1 block with its exact fallback
  cost; and the ONE jump in the walk (w_addendum_jump) HIT 2/2** — the
  doc-order forecast covered the ADDENDUM jump completely. Integrity: 24/24.

**OVERALL: FAIL (by the letter — one falsifier under bar on one walk), with
every number above landed as measured, exit code 1 by design.**

## COMPOSE — does forecasting compose with FOCUS? (measured, not argued)

Yes, mechanically, and the measurement says exactly what composition buys
and what it costs. On both walks every step was served through the FOCUS/
LOCAL mask while the forecast populated the buffer: served bytes were
byte-identical to plain FOCUS on every step (620,356B == 620,356B topic;
23,343B == 23,343B curriculum) — the forecast never widened or narrowed what
the reader sees; it changed WHO PAYS the read, not WHAT is read. What it
bought: 279 of 1,964 topic block-visits (14.2%) and 5 of 16 curriculum
block-visits came from the prefetch buffer with no fallback read — that
fraction is the latency-hiding win, SparDA's actual mechanism. What it
cost, honestly: prefetch is speculative bandwidth — total disk traffic rose
(767,578B vs 620,356B topic, +147,222B; 45,977B vs 23,343B curriculum,
+22,634B). The paper buys this back by overlapping prefetch with compute on
a GPU; our proxy counts the bytes and shows the trade naked.

## Verified vs not (tri-state)

- SUPPORTED (measured here): all numbers above, from one frozen-code run of
  `python -m mag.decl_attention forecast` on the two real artifacts; B3
  regression re-run clean; every miss itemized; mask invariant assert-held.
- SUPPORTED (paper's, not ours): Forecast projection mechanics, 1.7× decode
  speedup over the sparse-offload baseline, <0.5% added parameters. **No GPU
  in this cage — our numbers are a byte proxy; theirs are kernels.**
- DISPUTED-by-this-build (our own earlier hope): "adjacency forecasting
  generalizes to any doc scale" — FALSIFIED at 6-block scale (1.67× < 2×).
  The 2× bar holds on the big catalog, fails on the tiny doc.
- UNPROVEN: byte→token transfer to live lanes; whether a co-location term
  (predict current-block continuation) lifts the small-doc ratio past 2× —
  that is a NEXT-DOOR experiment, not tuned here.

## Lineage (steal the bones, name the reinterpretation)

SparDA's fourth projection (learned head, KV blocks, lookahead prefetch)
→ B3's declarative-attention organ (hashed block table, declaration masks,
seek()+read serving, attended-bytes counter) → B4: the Forecast as a
DETERMINISTIC serving-layer policy — adjacency instead of a learned head,
the walk's next query instead of the next layer. pyncd law holds: axes stay
distinct — FORECAST is not a fourth declaration mode; the GLOBAL/FOCUS/LOCAL
grammar is untouched and the forecast lives entirely in serving. Zero-Mem
law holds: regex readers only, zero tokens. Seat law "read the row, not the
zone" now has a prefetch: predict the next row's neighborhood.

*Files: mag/decl_attention.py (extended, +295 lines) and this receipt.
Nothing else touched — no dashboard/static, no chain writes, no processes,
no Docker. Both commands are idempotent and read-only. NEXT-DOOR (not built,
no scope creep): co-location term for the doc-order policy; serve the topic
walk's hit pattern to real seat queries; a learned-adjacency (count-based)
head as the paper-faithful upgrade.*

## SEAT VERIFICATION (independent re-run, 2026-09-06)

Seat re-ran `python -m mag.decl_attention forecast` and `demo` fresh: every
number reproduces line-for-line — topic_index 3.07× (14.2% vs 4.6%), 81.7%
attended cut, 12 misses itemized; curriculum 1.67× (31.2% vs 18.8%) FAIL
standing as reported, 75.4% cut, 11 misses; compose byte-identical served
bytes (620,356B / 23,343B) with prefetch overhead +147,222B / +22,634B counted
naked; B3 demo regression EXIT=0, shas reproduce. True exit code 1 CONFIRMED
(seat's first capture read the pipe's tail exit, not python's — re-measured
clean; the seat's own measurement bug, own it in one line). The receipt's best
row is the self-falsification: "adjacency forecasting generalizes to any doc
scale" DISPUTED-by-its-own-build at 6-block scale, stated not softened. Walks
and seed were frozen before measurement — verified by the deterministic
reproduction. VERDICT: PASS — the build is verified *including its failed
falsifier*; an honest FAIL with numbers is a finding, and this one names its
own next door (co-location term).
