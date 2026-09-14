# DUMB-AGENT GPS B — Mag-side NAV primitives for low-capacity (flash-tier) agents
Mined: ask_router, seat_corpus lanes, elder audit, verkle tail, SURFACES, basecamp, water_computer. Every pointer verified below. Total primitives: 7.

## (1) MAGSIDE NAV PRIMITIVE LIST
- **P1 OUTCOME-MEMORY ROUTING (GPS core)** — ask_router ranks lanes by `ok_rate`, `cost`, `freshness`: `100*ok_rate −10*tier +5*fresh` (`score_lane`). Ledger rows -> lane rank -> cascade; **$0, makes NO model calls** (docstring). DUMB-SERVES: pure arithmetic, no reasoning. `mag/ask_router.py:95-150,180-192,30-42`
- **P2 ORGAN MAPS AS TERRITORY** — basecamp `atlas.build("operational")` -> organs + `gap_codes`; structural gaps (source/caller/state missing) are the frontier. DUMB-SERVES: one pick `structural[0]`, deterministic. `mag/basecamp.py:21-46`
- **P3 ELDER AUDITS AS POSITION-FIXES** — audit.json = snapshot of DECLARED/INSTRUMENTED/WIRED/STATEFUL/VERIFIED/LIVE per organ = "where am I" latitude. DUMB-SERVES: flat counts. `memory/runs/elder/audit.json:4-14`
- **P4 VERKLE KNOTS = HASH-ANCHORED BREADCRUMBS** — chain.jsonl rows carry `filename`, `leaf_hash` (sha256), `ts`, `session_id`, `start/end_minute`. Tamper-evident trail; **the only across-time NAV**. DUMB-SERVES: read tail, hash = fixed anchor. `memory/biography/verkle_chain.jsonl` (6386 rows; tail 2026-09-01)
- **P5 SEAT CONTRACTS = LANE RULES** — latest.json `lanes.*` gives `thinking:off`, `pack_chars`, `never[]` (T0/T1/thinking-on), `models[]`. **Explicitly dumb-agent guidance** (deepseek_v4-flash, thinking OFF). DUMB-SERVES: direct. `memory/runs/seat_corpus/latest.json:28-102`
- **P6 BASECAMP ONE-STEP CLIMBS** — `status()` returns next_steps; "one bounded climb step, receipt, remap". Smallest loop unit. DUMB-SERVES. `mag/basecamp.py:37-62`
- **P7 WATER GATES/LEVELS** — heights(source/work/out), valves(source_work/work_out), phase(liquid/gas), masses. **Gravity cannot read steam = warning when instrument breaks**. DUMB-SERVES: integer heights read like a sight-glass. `mag/water_computer.py:64-80,95-127,189-191`

## (2) GAPS FOR A COMPLETE DUMB-AGENT GPS
- **G1 HEADING/COURSE MISSING** — P1-P7 give position (where), none give *intended direction among reachable organs*. ask_router cascade is order-only; no vector "next=closest gap in that direction". `ask_router.py:180-192`
- **G2 NO CURRENT-GOAL CONTEXT BINDING** — routing is prompt-keyed (memlance select per prompt) and basecamp is goal-keyed, but no persistent "agent X is on goal Y, at breadcrumb N, heading Z" runtime state. Position is re-derived each call, $cost per fix. `ask_router.py:108-125`
- **G3 NO FLASH-TIER REASONING GUARANTEE** — unless explicitly pointed, these organs assume a smart reader (atlas, receipts, verkle digests). seat_corpus `never[]` is per-lane guardrails, not a GPS prompt-pack; a dumb agent must be *given* the compact position line, not trusted to compute it. `latest.json:35,60-71,85`
- **G4 WATER META (P7) EXPLICITLY-NAV WARNS NOT GUIDES** — "Height was the wrong instrument. Gravity cannot read steam" is a *philosophy*, not a re-route instruction. Dumb agent stuck in gas phase gets no exit vector. `water_computer.py:222-227`

## (3) VERIFIED vs VIBE
- **VERIFIED (read code/exact rows):** P1 (score_lane math), P2 (basecamp gap_codes), P3 (audit counts), P4 (tail knot schema), P5 (lanes.never/thinking), P6 (receipt schema), P7 (heights/valves/phase funcs).
- **VIBE (inferred, unverified):** that outcome-memory routing *alone* suffices as dumb-agent GPS (needs a heading layer); that verkle chain = reliable breadcrumb ordering at 6386 dense rows (truncation/exact-knot-topology unverified); that seat-corpora `never`-rules translate into usable prompts (untested end-to-end).

*Extracted 2026-09-01 by subagent GBM (lane B) — 7 primitives, 4 gaps.*
