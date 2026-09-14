## Verdict — what your lens yields on the artifact

The fly-brain Gomoku post validates the fleet's core thesis: fixed wiring (connectome/corpus) + trainable heads (seats) produces emergent coordination behaviors (attacking/defending) that nobody explicitly programmed. The 138K-neuron scale is within Rocinante's 4x M5 Ultra envelope. The shuffled-connectome control is the falsifier the fleet already uses: doctrine cold-reads, tri-state claims, and the "same heads on shuffled corpus" test is the verkle chain's blessed-seal replay. The spectator neural activity maps to the fleet's per-lane token/verdict traces.

## The steal — the mechanism the fleet adopts (concrete)

**STONE-PROTOCOL v1 for Gomoku (9x9 board):**

- **Win condition**: First to place five stones in a row (horizontal, vertical, or diagonal) wins. Game ends immediately on the winning move.
- **Ko-analog (repeat position)**: If a move would recreate the exact board state (stone positions + colors) that existed at any prior turn, the move is illegal. The seat must play elsewhere. This prevents infinite loops and forces progression.
- **First-move handicap**: Black (the auditing seat) plays first. White (the building seat) receives komi compensation — 0.5 points (half-stone) awarded at game end if White has not won by five-in-a-row. This compensates for Black's first-move advantage without requiring complex scoring.
- **Atari-analog**: A "four-in-a-row threat" (one move from winning) triggers the atari signal — not panic, but pressure to respond. The game logs mark these as "pressure moves" in the kifu.
- **Seat lifecycle**: Each bot places one stone per turn, then yields. No seat is load-bearing — if a seat dies mid-game, the game pauses until a replacement seat resumes from the last kifu row.
- **Kifu format**: Each move recorded as `{turn, seat, x, y, pressure: bool, timestamp}` — append-only, verkle-knotted.

## The build — one week-scale act, file/schema/number named

**File**: `dashboard/static/stone_gomoku.html` — the playable surface.

**Schema**: `stone_protocol_gomoku.v1` — the rule engine as a standalone JS module (`stone_gomoku_core.js`) with:
- `Board9x9` class (state: 81-cell array, 0=empty, 1=black, 2=white)
- `checkWin(board, lastMove)` → bool (five-in-a-row scan)
- `checkKo(boardHistory, proposedMove)` → bool (hash lookup against prior states)
- `isAtari(board, seat)` → bool (four-in-a-row threat detection)
- `kifu` array → JSON export for chain append

**Number**: Target 50 self-play games logged to `memory/runs/gomoku/games_20260919.jsonl` by Sep 19, with at least one game showing emergent "defending" behavior (blocking opponent's four-in-a-row before completing own five).

## Falsifier — what would prove the steal wrong

1. **Shuffled corpus test fails**: If seats trained on shuffled doctrine (randomized law order, scrambled parable) produce equivalent or better coordination, then the frozen wiring claim is Disputed — heads alone suffice.
2. **No emergence in 50 games**: If all games show only random or greedy play with no blocking/defending patterns, the "emergent coordination" claim is Unproven at this scale.
3. **First-move advantage reverses**: If White wins >55% of games despite Black moving first, the komi calculation is wrong — the handicap fails.
4. **Ko rule never triggers**: If zero games hit the ko-analog condition across 50 games, either the game length is too short or the rule is unnecessary — the ko-analog is dead code.

---
*Lens executed: F11_gomoku_rules | Fleet wave lane | 2026-09-12*
