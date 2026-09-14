# FREESCALE — how far does ~$0 scale (2026-08-31)

Receipts: moiche.md ladder (groq 200K TPD, cerebras 1M TPD/5 RPM, ollama = electricity, z_ai2 cache 97–99% $0, deepseek cached $0.03/M list), WARM_PACK.json 3,602 B ≈ 900 tok / 12 spine concepts, MEMORY_RIB.jsonl deref spans 789–17,385 B.

## 1. Daily free-token budget (all $0 reservoirs)

| Reservoir | tok/day | Basis |
|---|---|---|
| groq free tier | 200,000 | receipted cap (moiche §1) |
| cerebras free tier | 1,000,000 | receipted cap, 5 RPM paced |
| ollama local | ~302M ceiling (3,500 tok/s × 86,400 s); **~100M realistic** at 8h fleet duty | electricity only, ~$0.03/hr floor |
| deepseek cache-mine | 166.7M per $5 at $0.03/M cached list → **~5.5M/day amortized monthly** | cache-hit implies ~10× cheaper than list |
| z_ai2 cache judge | **unbounded** while hit ≥97% ($0) | catalog receipt |
| **Total** | **~470M tok/day at $0 marginal** (1.2M remote + ~100M local duty + 5.5M cached + judge) | |

## 2. RIB multiplier math

- Naive 128k session ≈ 262k cumulative tokens (geometric self-attention, ~2×128k).
- RIB-fed session: 900-tok spine + deref-on-mention only (0.4 × 12 handles × ~6,000-tok spans ≈ 28,800) + 8k own output ≈ **37,700 tok**.
- **Multiplier ≈ 262,000/37,700 ≈ 7.0×** (task's naive 250k vs 3k frame is the pure-context bound: ~83×; 7× is the honest whole-session number including output).
- **1M free tokens buys:** ~3.8 naive 128k sessions vs **~26.5 RIB-fed sessions** — the same $0 buys a full working week of context-complete sessions instead of one afternoon.

## 3. Permanent probe fleet (T0/T1 law → N=8)

**Workers N=8** (T0/T1 rung: 6 OpenClaw seats + 2 /room/spawn ROW lanes). 37 atlas surface rows ÷ 8 ≈ **4–5 vertexes per worker**, assigned round-robin so shared vertexes get independent re-probes (dissent preserved per MoA law).

**Cycle:** deref warm pack (900 tok) → probe assigned vertex (read span, byte-check) → ROW row → pheromone drop. Pheromone = 1-line append to the vertex's row: hit-strength + next-probe hint; high-pheromone vertexes re-probed first, cold ones decay to UNMAPPED.

**Cadence (token-bound, not RPM-bound):** probe cost ≈ 3,600 tok (900 spine + 200 deref + 2,500 output). groq+cerebras 1.2M tok/day → **~333 remote rows/day**; RPM caps (30+5/min) allow ~50k req/day, so tokens bind first. Local ollama T0 probing at 3,000 tok/s × 8h ≈ 86.4M tok → **~24,000 rows/day** additional. Fleet ceiling: **~24k rows/day at $0**; conservative scheduled cadence: 1 remote probe wave/hour/worker + local T0 sweeps between.

**ROW schema (receipts-first, from atlas_draft):** `pointer | span | sha256 | status(VERIFIED/CORRECTED/ATTESTED/INCONCLUSIVE/UNMAPPED) | checked_at | checker | pheromone(strength,hint)` — no pointer, no row; pheromone rides every row.

**Growth rule 8→16→32 (receipt-gated, per moiche ladder):**
- 8 → **16** when the T0 byte-check pass completes (all 37 vertexes have ≥1 ATTESTED/VERIFIED row): add 10 host lanes, groq dual-key, cerebras spillover.
- 16 → **32** when T1 voting pass completes (≥2 independent votes per vertex, z_ai2 judge $0): add openrouter rotation ×6 + nvidia ×2; T2 arbitration stays ≤3 arms + off-peak deepseek judge.
- Rollback any rung that misses its pass criteria; pheromone decay auto-shrinks active vertex set.

## Self-attack (weakest assumption)

**The 302M/day ollama ceiling assumes 100% duty cycle 24/7 — no real fleet sustains that.** Headline total is a ceiling; the honest planning number is ~100M/day at 8h duty. Second weakness: the 7× multiplier depends on the 40% deref rate; a deref-heavy session (100%) drops it to ~3.4× — still >3×, but the "~$0 buys a week" claim should always carry the duty-cycle asterisk.

**GOPHER:** pull today's actual groq+cerebras token usage from fuel receipts to confirm headroom vs 200K/1M caps | pointer: /mag/memory/runs (fuel_feed, groq) | output: /board/octant_20260831/rows/freescale-g1.row.md
**GOPHER:** verify z_ai2 cache-hit ≥95% in latest seat_corpus (catalog claims 97–99%) | pointer: /mag/memory/runs/seat_corpus/latest.json | output: /board/octant_20260831/rows/freescale-g2.row.md
**GOPHER:** enumerate the 37 surface rows with byte-span pointers so the 8-worker vertex assignment can be minted | pointer: /board/octant_20260831/atlas_draft.md + /board/gap_moonshot_20260831.md | output: /board/octant_20260831/rows/freescale-g3.row.md
