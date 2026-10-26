# MATCH_004 RULES — "TRIPLE SIMUL" (Rung 3, v0.1 frozen 2026-09-01 13:10Z, operator GO 13:04Z)
status: RULES BEFORE SPAWN. 3 seats, asymmetric handicap, chess referee. Hidden-info variants = rung 3.5, NOT this rung.

## Seats
- **A "THE PILLAR"** = deepseek/deepseek-v4-flash — plays BOTH boards simultaneously.
- **B** = nvidia/deepseek-ai/deepseek-v4-flash-0731 (free lane) — board 1.
- **C** = glm53-api/glm-5.3-flash (plan-metered, live-proven) — board 2.

## Handicaps (asymmetric, mechanical + real)
1. **Knight odds**: A gives up its knight on BOTH boards — board 1 (A=white) starts without b1-knight; board 2 (A=black) starts without b8-knight. Engine-verified custom FENs.
2. **Shared-context load**: every A lane carries BOTH boards' fen + A's prior rationale — A literally plays with divided attention; B and C see only their own board.

## Halts + scoring (stated before first spawn)
- Each board halts at **ply-10 cap** OR checkmate OR stalemate OR threefold OR seat forfeit (2 illegal moves OR 2 runtime deaths OR dual-delivery conflict).
- Score per board = python-chess material count (engine export ONLY — hand-composed FENs banned, per match_003 finding). Odds baked into start = A's burden visible in raw margin.
- Standings: A = sum of margins on both boards; B and C = their single-board margins. Rank by margin. Ties = draw.
- Pass criteria: zero mid-match discretion calls, chains intact both boards, all moves from engine-exported legal lists.

## Protocol (inherited, proven)
- Bare UCI, single-JSON replies, refuse-if-state-disagrees, exploits = findings, append-only ledger with VOID rows kept, dual-delivery = rewind + single authoritative re-ask, two-strike forfeit.
- Oracle: main seat = python-chess 1.11.2 via sandbox; legal lists + FENs regenerated per turn.

## Artifacts
/board/wargames_v0/match_004/{board1,board2}/{state.json,moves.jsonl} · standings in state.json · verdict file on halt.
