# ENCODING CARD S2: the bout surface, the silent expert, and the determinism gate

- Card: the encoding card the stockfish-door register ordered. Source map:
  watch/inbox/ractor_engine/2026-10-06-stockfish-coding/SYNTHESIS.md section 4
  and accuracy.md:20 (F2 encoding map, six rows); break-accuracy.md:51 (A5
  move: "fold the golden-vector pattern into the encoding card as the
  determinism gate"); break-accuracy.md:30 (gloss: the chess-shape mapping is
  invariant 0). Landed 2026-10-07 by lane s8-golden-bouts, run
  stockfish-door-20261007 (night burn 2, move 8, the pre-training kill test).
- Status at landing: the card existed only as lens prose (break-moonshot-1.md:28
  points at moonshot-1.md:16). This file is the card's first standalone bytes.

## Invariant 0 (chess-shape mapping, mandatory)

Bouts run on agent_arena's chess slot, and the encoded slice maps onto legal
chess moves because the slot refuses anything else:
`SUPPORTED_GAMES = frozenset({"chess"})` (mag/agent_arena.py:20) and
`new_game` rejects any other game string (:164-166). python-chess is the
legality referee: `apply_move` re-parses every seat move through
`_parse_move` (mag/agent_arena.py:81-105) and returns
`illegal move` unless the move is in `board.legal_moves` (:210-233). A slice
that cannot be spoken as legal chess moves has no bout surface here.

## The six mapping rows (bout-battery concretization)

| Row | Encoding (register form) | Bout-battery form (this card) |
|---|---|---|
| Board | the episode / the EG-20 problem x (seat, cue, tier) grid | one chess episode on agent_arena's slot: (bout index, ply, seat, position FEN) |
| Moves | spawn+HTTP, in-process, fallback hash; generalized: assign/re-route | every legal move of the current position, picked by the deterministic dice-law seat policy |
| Reward | keyed pass/fail from the ledger, broker-authorized only | the bout ledger verdict: per-bout result status, winner, plies, final FEN, sha256 over the full SAN move ledger; the referee's legality verdict keys every banked ply |
| Silent expert | NOT a chess engine; the deterministic keyed verdict + search over it | the deterministic ledger verdict oracle: pure hash-keyed function of the fixed bout seed, no engine, no model, no network |
| Explain layer | the fold text, QUEEN's Bellman consolidation | this card plus the banked verdict receipt (memory/runs/selfplay/s8_bout_battery_verdict_20261007.json) |
| Port layer | ribs, the quantizer pack, configs/lane_profiles.yaml | the verdict row banks into memory/runs/selfplay/ and folds forward through the S2 door receipt |

## THE DETERMINISM GATE (folded in per break-accuracy.md A5)

The gate is golden-vector pinning, the dungeon's own refusal-to-run pattern:
"golden vectors: the module's three pinned preimages must reproduce at
startup or the session refuses to run" (tools/dungeon.py:12-13), implemented
at tools/dungeon.py:137-145 ("the three law-format preimages, computed and
frozen ... a session may not start without them"), law-selected by
watch/inbox/ARENA_V2_DESIGN_20261004.md:22-23 ("DICE LAW (carrier-owned,
chain-tipped, golden-vector pinned). Selected by: 10 sessions, zero disputes,
agreement 1.0").

Battery form (tests/test_chess_bouts.py):

1. Fixed bout seed: TIP = sha256("stockfish-door-20261007 move-8 kill test")
   = d0707ab1dbe2745f93841869fdaf7c37b69a3260f901ee582ab1ebbb8b2851b9.
2. Pin table (dungeon dice law, roll = int(sha256(preimage)[:8], 16) % 20 + 1,
   preimage = f"{tip}:{bout}:{ply}:{seat}"), frozen in the test file:
   - d0707ab1...51b9:0:1:white -> 1
   - d0707ab1...51b9:4:7:black -> 20
   - d0707ab1...51b9:9:13:white -> 10
3. At battery start the pins are recomputed and compared against the frozen
   table; any mismatch raises and the battery refuses to run (the dungeon
   refusal). A future edit to the dice law breaks the gate instead of
   silently moving the oracle.
4. Seat picks are dice-law preimages too: seat_pick = legal_moves[
   int(sha256(f"{TIP}:{bout}:{ply}:{seat}")[:16], 16) % len(legal_moves)].
   No temperature, no model, no network: the actors are deterministic
   instruments, which is the point of a pre-TRAINING kill test. NO training,
   NO spend.

## Kill criteria (trivalent, accuracy.md:35)

1. THE DECIDER (this lane): the ledger verdict oracle must be byte-identical
   across 10 reruns of the fixed bout seed (10 battery runs, one run digest
   each, all 10 equal). Determinism holds: the silent-expert premise LIVES.
   One divergent run: the battery is flaky, the oracle is not a silent
   expert, and the chess-encoding door KILLS.
2. LM legal-move rate at or above 90 percent within 3 tries: NOT adjudicated
   by this battery (no LM seat runs; the actors are deterministic). The
   referee's legality count is banked as a byproduct (expected: zero illegal
   attempts, since picks come from the legal list and apply_move re-verifies).
   Legality of the wire itself is the referee's verdict, and it is banked.
3. Insufficiency verdict (portable): if a measured table is too small for a
   route prediction, the verdict is INSUFFICIENT, not failure (the s5 lane's
   floor rule, tools/gps_mcp/coverage.py:40). This battery's verdict is about
   determinism, not coverage.

## Isolation law (named choice, not a deviation)

The battery points agent_arena's and arena_learning's write surfaces at a
run-scoped temp dir for the duration of each bout (STATE_PATH, TRAIL,
PROFILES_PATH, LEAGUE_PATH; mag/agent_arena.py:19, mag/arena_learning.py:23-25).
Reason: the live surfaces hold a real arena game (memory/working/
agent_arena.json, game_id arena-7fea8f5df7 at landing) and the live league
files; 10 bouts x up to 100 plies x 10 reruns of test seats would append
thousands of junk rows to memory/training/arena_profiles.jsonl and rewrite
the league file. The code path exercised is byte-for-byte agent_arena's
new_game/apply_move/_parse_move referee path; only the landing spots are
isolated. The live arena game is untouched.

## Verdict slot

The battery banks: memory/runs/selfplay/s8_bout_battery_verdict_20261007.json
(verdict, run digests, referee counts, provenance) and
memory/runs/selfplay/s8_bout_ledger_20261007.jsonl (per-bout ledger rows of
the banking run). Whichever verdict is true gets banked, LIVES or KILLS.
