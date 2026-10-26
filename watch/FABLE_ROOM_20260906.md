# FABLE ROOM — room #0, the C3 Primer-union build (2026-09-06)

*The unified fold salon's converged minimal build, DELIVERED: the story-layer the fleet was
missing — a room where the record-exit IS the story-exit. Surface: dashboard/static/fable_room.html
(wired nav, "Fable Room"). Core verified in node: memory/runs/day_20260906/fable_core_test.js.*

## The design (as converged, then built)

- **One room, one law:** 6 hands, 24 stones. Sowing conserves — stones are never made or lost,
  only moved (mancala-conservation = the append-only chain, playable).
- **The walls keep everything:** every sowing is a hash-chained ledger line (FNV toy chain — a
  game prop; the REAL chain is the verkle). **Even the lies are kept**: tell the door it's open
  before it is → REFUSED, and the lie is appended to the walls forever.
- **Record-exit = story-exit:** the door reads the BOARD, not the tale. Heal condition (from the
  riddle): every hand holds what the hand across holds (palindrome), 24 conserved, ≥6 hands worked.
- **The restatement gate (deepseek kill condition):** after healing, the walls ask you to restate
  the walk — questions generated FROM the ledger (first hand sown, number of sowings, what the
  room did with your lie). A story that contradicts the record is "just a lie with polish." 3/3
  = true ending + your personal chronicle line (hash of your actual walk).
- **Hallucination trap:** a coherent ending with no healing hash is structurally impossible to
  obtain — the tell-the-door button exists precisely so the room can catch you trying.

## Falsifiers — all three RUN and PASSED (node, scripted)

- **F1 coherent-ending-without-hash = caught:** pre-heal tell-open refused ✓, lie hash-chained ✓.
- **F2 restatement contradiction = caught:** gate keys derive from the ledger (Q1 "hand 2" from
  ledger[0].pit, Q2 "6" from moves, Q3 from lies>0 branch) ✓.
- **F3 the true ending is reachable by real play:** BFS solve — hands **2→6→3→1→6→1**, final board
  [0,7,5,5,7,0], healHash `392dbdcc`, conservation held every move ✓.

## The taped layer (deniable, never required, no gates)

The six lines of the opening riddle carry N-A-C-H-O-S down their first letters. The riddle's
third hand line — "count what the hands have scattered" — is the squire's whole job description.
No key, no gate; teach-or-bury.

## Provenance

- Design converged: unified fold salon 09-06 (C3 minimal build, openrouter + deepseek kill
  conditions) — watch/ lineage ZEITGEIST → SOCRATIC_MAP → ELDER_READS.
- Primer canon: state/world/PRIMER.md ("for the second voice, and every voice after").
- Room #0 name honors the night-shift triangulation: the_wall → fable-room#0.

## Honest limits

- The toy chain is FNV-32, not the verkle — a prop, not a proof surface.
- The heal condition admits many palindromes, not one — the door reads shape, not a target
  distribution. (The room forgives many endings; it refuses all unearned ones.)
- Solo-built, single judge (the seat). The bench pass (salon chair attack) is owed like any card.
