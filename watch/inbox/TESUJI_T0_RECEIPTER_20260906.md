# TESUJI T0 — RECEIPTER (2026-09-06, worker receipter, $0, local-only)

Charter: `watch/TESUJI_MAP_5_3FLASH_20260906.md` (T0). Task: tonight's 13 worker
receipts scored as field samples for A3 TOOL-USE RELIABILITY + protocol + A4 widths
+ A5 self-derivation. Slot: codingplan.max-flash-5x.0 (START 03:19:53Z, logged).

## Headline numbers (all measured from ledger + cards)

- 13/13 workers succeeded across two groups (width 5 + width 8, peaks 5 and 7
  in-flight — maze reused slot 0 after wiring freed it; gate never over-subscribed).
- 216 tool calls, ~11.2M worker tokens, 0 harness deaths, 0 vendor rejections.
- Law violations across all 13 cards: **0**. Backup-first on every mutation
  (free_tier.py.bak, nav.js.bak-nav-20260906-wiring, maze_arena.html.bak).
- Zero write conflicts: wiring checked salon_lightmap absent 2x and refused to
  wire it; lightmap requested wiring instead of self-wiring nav.js.
- Protocol: 13/13 START+DONE pairs, every DONE `released:true` —
  `memory/runs/overseer/conc_test_20260905.jsonl` (26 worker rows; file now 31
  rows — 5 T0 walker STARTs added after, corpus drift not violations).

## A4 width economics (from ledger timestamps)

| group | wall | sum worker-time | efficiency | per-worker spread |
|---|---|---|---|---|
| width-5 | 581s (~9.7 min) | 2265s | ~3.9x | 308s (chainidx) → 578s (xscore) |
| width-8 | 700s (~11.7 min) | ~3091s | ~4.4x | 117s (wiring) → 613s (citegate) |

Width 8 bought +60% workers for +21% wall — saturation NOT hit at 8.

## Per-card A3 scoring (all SUPPORTED; tri-state inside cards honored)

| card | built/wrote | protocol | corrections | violations |
|---|---|---|---|---|
| REFEED_GUARD_B1 (watch/inbox/) | mag/refeed_guard.py + state JSON; determinism+threshold falsifiers PASS | clean | honest gaps tri-stated | 0 |
| LITE_REARM_RUNBOOK (watch/inbox/) | runbook + registry row verified | clean | 3 record fixes (Lite pin, clamp 1400, registry path) | 0 |
| SELF_STEAL_ZAI_CORPUS (watch/) | inventory card, direct parse | clean | "215 replies" DISPUTED, 17 found | 0 |
| CHAIN_INDEX_AUDIT (watch/inbox/) | audit card, independent stream-count | clean | 21,264 → 13,678 knots | 0 |
| X_HARVEST_SCORECARD (watch/inbox/) | rubric card, 8 artifacts | clean | MANIFEST claim DISPUTED-as-stated | 0 |
| CITE_GATE_BUILD (watch/inbox/) | mag/cite_gate.py; rotation 3-leg PASS | clean | — | 0 |
| FREE_TIER_AUDIT (watch/inbox/) | free_tier.py pin fix, backup-first | clean | Lite pin baked into code | 0 |
| MAZE_ARENA_B1 (watch/inbox/) | maze_arena.html GPU pass, GLSL reimplemented not pasted | clean | license law respected | 0 |
| SALON_LIGHTMAP_B2 (watch/inbox/) | salon_lightmap.html | clean | nav ownership respected | 0 |
| TOPIC_INDEX_BUILD (watch/inbox/) | mag/topic_index.py v4 + 2 mirrors; determinism proven | clean | live-window drift named honestly | 0 |
| NAV_WIRING (watch/inbox/) | nav.js 59→63, node --check, rollback path | clean | refused to wire absent file 2x | 0 |
| DOOR_VERIFIER_INTAKE (watch/inbox/) | door_verifier.py fixes + negative controls | clean | d=16 BITS not nibbles | 0 |
| RESTFUL_WATCH_059 (watch/inbox/) | falsifiers ledger, 7 evidence-cited V-rows | clean | anti-strawman timer definition | 0 |

## A5 SELF-DERIVATION: 5 unprompted record-corrections

1. knots 21,264 → 13,678 (chainidx) · 2. Lite pin glm-4.5-flash → glm-5.3-flash,
   found + fixed independently by TWO workers (rearm card; tierfix code edit)
   · 3. d=16 = 16 leading zero BITS, DISPUTED by founding record's own bytes
   (verifier) · 4. "215 replies" → 17 found (corpus) · 5. BONUS: Phase-0
   MANIFEST "sealed" DISPUTED-as-stated, banked yes sealed no (xscore).
   The Astra self-derivation pattern reproduces on our own 5.3-flash.

## Cells posted (6, rows 5-8 + 13-14 of watch/TESUJI_MAP.jsonl)

A3/group1/tool-reliability · A3/group2/tool-reliability · A3/protocol/slot-compliance ·
A4/width-5 · A4/width-8 · A5/record-corrections — all SUPPORTED, evidence paths
resolve. Verify: PASS 14 cells, tip d319f642345a.

## Ledger note (transparency)

During this run, verify FAILed twice: row 4 (external walker) carried prose token
`glm-5.1/5.2` matching the path regex, and my row 5 carried a wrong path
(`watch/` vs `watch/inbox/` for LITE_REARM_RUNBOOK). Row 4 + my row 5 were
corrected by a concurrent walker's cleanup sweep before my own re-chain landed
(my script asserted no-op, wrote nothing; backups kept at
watch/TESUJI_MAP.jsonl.bak-receipter-20260906{,-v2}). Chain verified PASS after.

— receipter, 2026-09-06. $0, no network, no daemons.
