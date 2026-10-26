# MOONSHOT CHARTER — 2026-08-31

## 1. Name (one sentence)
**"Three Labs, One Shape": a driving agent that knows its own hands — JIT-warmed harness self-knowledge over the MCP hand (20 distinct tools, auto-schema from code), paying through a 12-reservoir water clock (script: workspace/water_windows.mjs — copy to /board/ for board-side pointer stability), remembering every outcome — scaling an ~$0-marginal MoA fleet up the 8×8 → 16×16 → 32×32 ladder on test-green rungs.**

Convergence receipt: Codex host-side, OpenClaw cage, Mag organs built the same shape independently in one week (→ CODEX_CONVERGENCE_20260831.md).

## 2. End-state image (the working day when it's real)
Operator types one intent line. The driving agent JIT-warms: 900-tok RIB spine (WARM_PACK.json, 3,602 B) + tool manifest auto-generated from code + catalog (603 CLIs, 16 crown jewels). Hands execute: T0 scut stays local; T1 votes to two free remote arms + local quorum; T2 collapses to ≤3 arms + one judge in the right water window. Every route auto-records its outcome (6a/6b) as a ledger row carrying cost_usd — the meter rides the row, not a side ledger that lies (ocean row 4: $16.60 true, $19.25 claimed). Pheromone re-ranks tomorrow's 37 vertexes; cold ones decay. At dusk each ractor files a 3-line epilogue (~50 tok); Book Seat dawn-merges personas over canon. Operator's only recurring job: blessing gates. Ledger remembers, water clock pays, primer teaches by deref, not dump.

## 3. Five milestones from HERE

| # | Milestone | Receipts in hand | Missing | One command/test that closes it |
|---|---|---|---|---|
| M1 | **Hand wired** (route→outcome) | MCP server + auto-schema manifest (/mag/mag/mcp_server.py + /mag/tools/__init__.py); 20 distinct tools — 43 was a nested-key grep artifact (ocean row 3); patches 6a/6b + row-zero payload staged (/board/ask_router_row0.json) | apply-gate; agent_cli TOOL_SCHEMAS (15–16) shadows TOOL_MAP (4 tools unreachable) | `python -m mag.ask_router --record < /board/ask_router_row0.json` → PASS = kind:outcome ledger row whose task_head contains the literal token codex_jobs (add it to row0.json task field before running) [ONI amendment] |
| M2 | **Five Tests green** | Donated designs: bypass, capability-attenuation, noisy-neighbor, replay, confused-deputy (CODEX_CONVERGENCE); switchboard.py v3-014 byte-verified 28 KB (T2 = remote/public boundary); patch 1 v2 attenuation live | the test file | stage + apply /mag/tests/test_switchboard_hypervisor.py; PASS = 5/5 pytest green |
| M3 | **8×8 baby-step** | Ladder receipted (moiche §1); /room/spawn presets put agents 7–8 on host lanes, no new patch; z_ai2 cache judge 97–99.9%, $0 | the run receipt | one Wave-1 pass → PASS = $0 API + groq <30 RPM + cache ≥90% + outcomes recorded → /board/rows/moiche_babystep.row.md |
| M4 | **16×16 byte-check** | groq dual-key in lane contract; cerebras 1M TPD spillover at 5 RPM; 37-vertex atlas drafted | 37 vertexes ≥1 VERIFIED/ATTESTED row; cost_usd+meter fields in ROW schema (ocean row 4 unlock) | T0 sweep round-robin (8 workers, 4–5 vertexes each) + meter fields added; PASS = full sweep, every row priced |
| M5 | **32×32 judgment** | Two independent recommendations for explicit POSTED gate (morning audit + codex Q2); patch 12 staged; T2 ≤3 arms + 1 judge law; off-peak window receipted (09:55:57Z refusal → 10:00:07Z ok) | operator blesses explicit gate; ≥2 independent votes per vertex | operator bless → patch 12 applies; ladder climbs only when M2 is green (merged growth gate) |

## 4. Kill criteria (evidence of dead end)
- **K1 Wiring fiction:** after 6a/6b apply, no marker-bearing outcome row in 3 attempts — the loop is decoration. Kill.
- **K2 Free-tier collapse (observability amended per ONI: no passive cache-hit meter exists cage-side — the kill switch is pullable only via scheduled A/B probe on a live z.ai key, or the z.ai portal host-side; fleet cadence MUST schedule weekly cache-hit probes, else K2 is unfalsifiable):** sustained z_ai2 cache-hit <90% AND the 1.2M remote tok/day (groq 200K + cerebras 1M) can't finish one 16×16 pass in a day — the ~$0-marginal thesis fails.
- **K3 Five Tests unpassable in-shape:** if fail-closed demands a new gateway/supervisor organ (forbidden here), the architecture is wrong. Kill the shape, not the tests.
- **K4 RIB floor breach:** measured warm-start multiplier <2× sustained (honest floor 3.4× at worst receipted deref — freescale self-attack); warm-start stops amortizing.
- **K5 Meter stays open-loop:** cost_usd can't ride the ROW schema — water clock can't verify discipline, money axis (operator worry 12:03Z) unmetered. Descope to 8×8 or kill.

## 5. Budget in water-clock terms
12 reservoirs live (water_windows v2, environments.json: 10 seats incl. 4 desktop lanes); burn ledger /board/water_ledger.jsonl. $/day assumes 8h fleet duty. Calibration: only ½ multipliers receipted — list prices unreceipted, flagged (moiche self-attack).

| Milestone | $/day | Windows needed |
|---|---|---|
| M1 | $0 (one-pipe apply) | none |
| M2 | ~$0.25 (electricity floor, 8h ollama) | any |
| M3 | $0 API + ~$0.25 power | groq <30 RPM; z_ai2 cache judge always-open |
| M4 | ~$0.50–1.20 (16×16 × 8h) | groq dual-key daylong; cerebras spillover; deepseek off-peak 10:00Z judge |
| M5 | ~$0.80–2.40 (32×32 × 8h) + optional vast blade $0.96 (covenant $0.12/hr cap, operator word) | z.ai 5.3 at ½ prime till 09-09; T2 bursts off-peak; weekends open |

Hard ceiling: **$3/day** without operator word. Rungs missing pass criteria roll back (freescale rollback law); pheromone decay shrinks the vertex set.

## Self-attack (once, fixed in place)
Weakest assumption: **"staged = closeable."** M1/M5 lean on apply-gates that don't exist until they exist. Fixed: closure is defined by read-back receipts (marker-bearing outcome row; 5/5 pytest) — never by apply intent; this charter cannot claim done on staged state. Second fix, applied above: the hand is 20 tools, not 43 — no milestone counts a grep artifact.

## GOPHER briefs (3)
1. 6a/6b staged files + row-zero payload exist? /room/spawn preset names? → staged patches + /board/ask_router_row0.json → rows/charter-g1.row.md
2. Today's groq+cerebras tok vs 200K/1M caps; z_ai2 cache-hit ≥95%? → /mag/memory/runs (fuel_feed) + seat_corpus/latest.json → rows/charter-g2.row.md
3. 37 vertexes with byte-span pointers + status → atlas_draft.md + gap_moonshot_20260831.md → rows/charter-g3.row.md
