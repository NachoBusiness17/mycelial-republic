# ENGINES IN CHARGE — mapping stone one (2026-09-16)

Origin: Mark's journal 2026-09-16 (#3): "put Stockfish / AlphaGo models in charge — they're
tricked into games as work. Hence the mapping."
PROVENANCE NOTE: first authored in a tool block killed by the subagent cancellation; the
bytes never landed until this rewrite. The reference existed before the file did — exactly
the forged-row shape the epistemology engine now has a VOID verb for. Filed honestly late.

## The inversion

Quest-cipher so far made fleet work legible to human spectators wearing a game skin. This
inverts it: the work becomes playable by game engines. The engine's game IS the lane's work —
that is the trick, and it only holds if the mapping is lossless, because an engine player
understands nothing but moves.

## Mapping contract (lossless or it doesn't ship)

- **state → board.** The lane queue + trail state renders as one legal board position.
  Go for judgment lanes: territory = lanes settled, ko = the append-only ledger.
- **action → move.** Every engine move compiles to exactly one real action:
  play a stone = claim a task, pass = defer, capture = close it out.
- **legality → lane rules.** Illegal moves are the policy engine's refusals. The engine
  cannot ask for an effect the broker won't authorize — the board is smaller than the world.
- **result → score.** The score is real: tasks closed, bytes verified. Never cosmetic.

## Falsifiers (bind the seat's own laws)

1. An engine player (KataGo over GTP) produces a move list that compiles to real lane
   actions with no human gloss in between. Any move needing translation = lossy = fail.
2. Replay law: same board + seeded RNG → same move → same action (the bones convention).
3. Anti-goal — theater: any board position that cannot be traced to repo bytes is void.
   The engine never sees a state we can't also render in the trail.

## First stone

One lane, one session: builder lane, KataGo via GTP, the INBOX rendered as territory.
Log move→action pairs to the trail so the session reads as both a game record and a work log.

## Open

Which engine for which work: Go = judgment lanes (territory, patience); chess/Stockfish =
forcing-line work (dependency ordering, tactical queues where one line must be walked to the
end). Do not decide this from the armchair — decide it after stone one's move log exists.
