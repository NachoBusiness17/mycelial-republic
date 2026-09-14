# WARGAMES v0 SMOKE VERDICT — 2026-09-01 (halted by operator correction)
status: HALTED at ply 4. Harness PROVEN. Match frozen as evidence, playable on demand — no standing burn.

## What ply 1-4 proved (the entire v0 hypothesis)
1. **Registration + strict contracts**: lanes return JSON judgment only, zero board writes, 7s runtime each.
2. **Oracle validation**: illegal move (e2e4 with pawn already on e4) CAUGHT, rejected, strike recorded.
3. **Strike protocol**: retry lane corrected under forfeit threat; cross-checked ledger over stale state — judgment seat behavior confirmed.
4. **Tamper-evident ledger**: 4 rows, prev_sha→row_sha chain intact (GENESIS→ba369793→f78378cd→e65e3ee5→dc2bcd11); any rewrite detectable.
5. **State recovery**: ledger is truth; state.json corruption (stale fen/legal list) caught and repaired FROM the ledger.
6. **Format enforcement**: duplicate-rationale-key violation flagged in receipt without dropping a legal move.

## The burn (receipts, counted)
- 6 worker spawns: 4 moves + 1 illegal-retry + 1 voided in-flight (result = VOID on arrival) ≈ 44k lane tokens in + ~500 out (DeepSeek PAYG cash, not free).
- 4 xAI sandbox oracle calls (python-chess legal-list gen, ~10s each) + per-ply main-turn overhead.
- Total ≈ 55k tokens to prove a hypothesis that was proven at ply 4. Plies 5-20 would have been ~5× more for zero new information.

## Correction applied (operator-corrections law 3 + 1)
- STOP-WHEN-VERIFIED: success criteria met at ply 4; the "smoke stop line: ply 20" was invented AFTER the proof and was scope creep. Wasted motion after verification is a failure.
- CONSULT FIRST: per-ply loop cadence was never operator-approved. No multi-spawn loop runs past its verification point without a consult gate.
- SMOKE-STOP LAW (added to spec): any harness/arena test states its verification criteria BEFORE first spawn; loop halts the moment criteria are met; continuation requires explicit operator GO.

## What survives
- All 4 operator action-queue items remain done: patches (await host apply), passport v2, probe battery (10:30Z, capped 400cr — authorized spend, off-peak), wargames spec+scaffold (frozen).
- v0 verdict for v1 planning: the switchboard-arena harness works. Cost of a future match = lane tokens only, and only when a match is actually wanted.
