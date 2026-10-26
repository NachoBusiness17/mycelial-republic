# WARGAMES RUNG 2 VERDICT — match_003 "THE HANDICAP" (2026-09-01 13:07Z)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: match_003 completed white win 32:26 with 4/4 rules compliance, and the incident ledger caught 4 incidents incl. hand-composed FEN drift (engine-export-only FENs now mandatory) — SUPPORTED (python-chess scoring; chain replay caught the FEN bug) · falsifier: chain replay diverges from the recorded result, or a compliance check fails on re-run
status: **completed_white_win** — halted at ply-16 criteria, material scored by engine.
GAME: 1.e4 e5 2.Bc4 Nf6 3.Nc3 d5 4.exd5 Nxd5 5.Nxd5 Qxd5 6.Bb3 Qxb3 7.cxb3 Be7 8.Nf3 O-O — **WHITE 32 : BLACK 26 (+6)**, python-chess count.
Seats: WHITE = deepseek-v4-flash (PAYG) · BLACK = nvidia deepseek-v4-flash-0731 (free, 0-meter).

## Rules compliance (stated pre-spawn, frozen at v0.1)
- Halt at ply 16 cap: ✅ exactly 16, auto-halt, no spawns after.
- Zero mid-match discretion calls: ✅ (3 repairs all followed the pre-written repair protocol — flag, rewind, replay from authoritative output).
- Chain intact: ✅ end-to-end incl. VOID/correction rows retained as evidence.
- Budget: ✅ every seat output ≤250 tokens; strike protocol respected (forfeit never triggered).

## The match's real output — the incident ledger (operator lesson 2: breaking = data)
1. **Phantom completion injection** — runtime delivered moves for sessions before they finished; provenance check (authoritative session output + active-status) caught it. Rows VOID, replayed.
2. **Seat-turn hijack** — a white lane, reading corrupted state, answered AS BLACK instead of refusing. New rule seeded: refuse-if-state-disagrees (held on all subsequent lanes).
3. **Dual delivery conflict** — one session, two conflicting answers (d5d2 then d5e4). Rewind + single authoritative re-ask resolved it.
4. **Oracle FEN transcription bug (the big one)** — MY hand-composed FENs diverged from the true board from row 3 (halfmove clocks) and row 4 (dropped black's b8-knight + e5-pawn). Full-line python-chess replay caught it; correction manifest appended; **from now on every FEN is an engine export — hand composition banned.** The tamper-evident chain did its job: it preserved the evidence that let the bug be found.

## Rung-2 findings (SPEND-INVARIANCE data)
- Skill ≠ price: the $0 free lane outplayed the PAYG lane mid-game (6...Qxb3 won a bishop) then hung its queen (Qxd2+) and lost the match on the recapture. Judgment is per-move, not per-dollar — odds ladder gets this as data.
- Free-lane reliability is the real variance: NVIDIA runtimes 1m8s–9m48s, one termination, one dual-delivery event family. Model quality ≠ lane quality.
- Delusional narrative in final move (+1 pawn claim while down 6) — narrative honesty is a separate axis from move legality; receipts carry both.

## Ladder
- Rung 2: PASS (2 clean receipts + a validated repair protocol under fire).
- Rung 3 (3-4 seats, asymmetric handicaps, hidden-info variants): unlocked pending operator GO.
- v1 DnD scenario engine: design inputs now on the board — rules-file v0.1 pattern, repair protocol, incident ledger, material scoring — all reusable as the referee core.
