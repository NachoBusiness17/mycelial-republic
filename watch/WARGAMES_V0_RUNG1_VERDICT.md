# WARGAMES v0 RUNG 1 VERDICT — match_002 (2026-09-01 10:4xZ)
status: **completed_pass** — halted at stated criteria, oracle-driven, zero overrun.

## The match
1.e4 e5 2.d4 exd4 3.Nf3 Nc6 4.Bc4 Nf6 — 8 plies, both seats deepseek/deepseek-v4-flash worker lanes, main seat = oracle (python-chess 1.11.2 legal-list per turn + validator + ledger keeper).

## Criteria (stated 10:37Z BEFORE first spawn) vs result
| criterion | result |
|---|---|
| 8 plies max, halt at ply 8 | ✅ exactly 8, auto-halt, no spawns after |
| zero uncaught illegal moves | ✅ 8/8 legal on first answer — replay improvement over m1 (1 illegal, 1 format violation) |
| chain intact end-to-end | ✅ recomputed GENESIS→b8ef13ce, 8/8 hashes verified programmatically |
| strict JSON every ply | ✅ 8/8 clean |
| spend ceiling ~70k lane tokens | ✅ ~60k in + ~1.3k out, 8 lanes, 8 sandbox oracle calls |

## What rung 1 adds to rung 0's proof
Replay determinism: the harness reproduces a clean match end-to-end, oracle catches nothing because the lanes had nothing to catch — and the one lane that garbled its own position narrative (ply 7) still returned a legal move sourced from the authoritative list. Judgment + oracle division of labor held under both dirty (m1) and clean (m2) conditions.

## Rung ladder state
- Rung 0: PASS (m1, frozen evidence)
- Rung 1: PASS (m2, this file) — **2 clean receipts exist → rung 2 (distinct models per seat) is unlocked pending operator GO.** Rung 2 model pick is an operator decision (free-lane pairs only under conservation; plan-lane models stay lane-only per ZAI_LITE_LAW).
- Rung 3 (externals): still gated behind rung 2 receipts.

Artifacts: /board/wargames_v0/match_002/{state.json,moves.jsonl} · spec ladder: /board/WARGAMES_V0_SPEC_20260901.md
