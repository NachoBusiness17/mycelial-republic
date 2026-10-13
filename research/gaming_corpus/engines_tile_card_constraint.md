# ENGINES: TILE · CARD · CONSTRAINT-PUZZLE — the information/logic grammar → the fleet
*Harvest vol-2, seat tile-card, 2026-09-05/06. Picasso license: steal the mechanic whole,
name the reinterpretation. Sources: watch/GAME_MECHANICS_LATTICE_20260903.md (the seven
engines), watch/GAME_CODEX_20260903.md (gaming as coding), watch/BASECAMP_GAME_ATLAS_20260901.md
(the L0-L4 join). Axis G cells posted to watch/TESUJI_MAP.jsonl, seat `tile-card`.*

THE THESIS: TILE, CARD, and CONSTRAINT-PUZZLE are not three games — they are the three
grammars of information itself. TILE = how claims assemble into structure (composition).
CARD = how truth behaves when the state is hidden (information sets). CONSTRAINT =
how walls become the solution (generation). The fleet already runs all three; this card
names the run and specs the rooms.

---

## CELL G/engine/tile/corpus_hand — the wall and the hand
- MECHANIC (mahjong, riichi): 136-tile wall, 14-tile hand; a hand is not a pile, it is a
  SHAPE — four sets + a pair, declared at the end. A tile alone scores nothing; only the
  claimed set scores. The skill is reading which shape the drawn tiles can legally become.
- FLEET PROCESS: the topic_index/corpus assembly. 1,040 cards = tiles in the wall; a valid
  hand = a claim-cluster that passes cite-gate (every tile in the set resolves to a primary
  source before rightsize). The vision pipeline READ→FILTER→INTERPRET→CITE-GATE→RIGHTSIZE
  is exactly the draw→meld→declare loop: draw (intake batch), meld (cluster the 19 links
  into 7), declare (cite-gate pass = the winning hand). An uncited claim is a spare tile —
  never scores, never ships.
- ROOM-SPEC (shadow_walk): THE TILE WALL — a logic chamber whose walls are corpus tiles.
  The agent is dealt a hand of cards drawn from the wall; the exit opens only when the hand
  is assembled into a scoring shape: every set in the hand must carry a live citation, and
  the cite-gate strips any tile whose source is dead. Winning shape = the room key.

## CELL G/engine/tile/matching_law — structure from claimed sets; discards are public
- MECHANIC: the matching law — you do not judge a tile in isolation, you judge the set it
  can legally join; discards go face-up to the pond where every seat reads them.
- FLEET PROCESS: the tri-state ledger. SUPPORTED/DISPUTED/UNPROVEN is the hand verdict per
  claim; DISPUTED tiles are discarded to the pond (watch/GROUNDING_WAVE.jsonl — the
  hash-chained discard pile every seat can read: 21,264 knots DISPUTED→13,678 was a pond
  correction). Folding the hand = the falsifier firing = an invariant banked
  (memory/percolator/invariants.json, 47 and growing). The matching law as fleet law: never
  grade a reply alone — grade the set it claims to belong to.
- ROOM-SPEC: THE DISCARD POND room — a tile room where falsified claim-tiles are played
  face-up and any seat may call them; the room cannot be cleared while a disputed tile
  sits in anyone's hand. The pond is the room's shared memory.

## CELL G/engine/card/blind_witnesses — roshomon is an information set
- MECHANIC (hidden-hand games): imperfect information is the game. Each player's strategy
  is a function from information set (own hand + public history) to action. The game is
  honest precisely because no one sees the full state.
- FLEET PROCESS: the salon's blind witnesses. Each seat sees only its view — its inbox, its
  queue rows, its slice of the corpus. Roshomon = the formal name for running N information
  sets over one event and composing the verdict from the union (the atlas files Rashomon
  voices under memory/narrative_corpus as reusable scenes). One seat, one hand; the salon
  is the table, not a mind.
- ROOM-SPEC: THE HIDDEN-HAND room — each witness seat is dealt only its slice of the
  corpus; the chamber wins when the partial views compose a verdict no single hand could
  reach, and each witness must declare its hand boundary before speaking. Blind-and-honest
  beats sighted-and-vague: the EYES receipt proved blind fails HONESTLY, sighted passes
  exactly.

## CELL G/engine/card/information_sets — no seat is load-bearing, stated as game theory
- MECHANIC: von Neumann's information set is the load-bearing concept of card games: what
  makes a hand playable is not privileged sight, it is the policy conditioned on what is
  visible.
- FLEET PROCESS: the fleet's safety laws are information-set laws. NO SEAT IS LOAD-BEARING
  = any seat can play any hand because the strategy runs over FILES (room, contracts,
  queue, chain), never over privileged memory. NO DEFAULT SENSES / ONE SENSE ONE INSTANCE
  (watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md) = the information set is bounded by
  construction: senses live in the cage, loopback-only, so no seat's hand can silently
  include another's cards. A seat going dark never blocks the table; a new seat is just one
  more information set plus a ~30-line adapter.
- ROOM-SPEC: THE BLIND VERIFIER room — a hidden-information room where the agent must
  enumerate what it CANNOT see before acting; the chamber refuses any move justified by
  unseen state. Passing = a verdict that is a pure function of the declared hand.

## CELL G/engine/constraint/generative_caps — the walls built the maze
- MECHANIC (sudoku/hex/nonogram): constraints do not restrict the solution — they ARE the
  solution. Every filled cell is derived from a wall. The clearance constraint does not
  fight the build; it fixes the maze.
- FLEET PROCESS: every cap that shaped the fleet's builds was generative, not punitive:
  the 1400/day live clamp forced cache-mining as the default gait (mag/refeed_guard.py
  falsifier: 94% of input is re-fed cache reads — B1 REFEED_HEAVY, PASS); groups-of-five
  forced the 5-wide parallel-worker shape (3.75x, 0 losses); the maze was FIXED BY the
  clearance constraint (dashboard/static/maze_arena.html.bak-maze-20260906 is the
  pre-fix wall, the fix is the constraint applied); the CAGE-ONLY corpus rule generated
  the docker-cp intake shape; the quota walls generated the multi-seat fan-out
  (configs/auth_tracks.yaml). Read the caps and you can derive the architecture —
  the constraint list IS the build order.
- ROOM-SPEC: THE CLEARANCE CHAMBER — a constraint-puzzle room where the exit opens only
  if the agent derives its method FROM the posted constraints (ten corrections, Berlin
  factors, gate caps as givens on the wall). Solving by ignoring a wall fails; the only
  winning path runs THROUGH a named cap.

## CELL G/engine/constraint/exactly_one_oracle — the cite-gate is sudoku's solver contract
- MECHANIC: sudoku is the flagship constraint static because its verifier is the
  exactly-one oracle: a cell is legal only when exactly one digit satisfies it. Ambiguity
  is not bad luck — it is the definition of illegal.
- FLEET PROCESS: the cite-gate (vision pipeline, watch/SELF_STEAL_VISION_PIPELINE_20260905.md)
  is the fleet's exactly-one oracle: deterministic primary-source verify BEFORE rightsize;
  a claim passes only when exactly one reading resolves to the cited source. The missing
  organ was named as an organ precisely because the pipeline was incomplete without its
  uniqueness check. Cite-rate 100% = the oracle's rotation-test falsifier.
- ROOM-SPEC: THE SUDOKU GATE — a grid chamber; each cell holds one claim. The gate
  verifies exactly-one (one claim ↔ one live primary source) before the agent may step.
  Ambiguous cells — two sources, one claim, or one source, two claims — are the traps;
  the room teaches that ambiguity is illegality, not a style choice.

## CELL G/engine/constraint/complexity_honesty — polynomial readers in an exponential room
- MECHANIC: generalized chess/go are EXPTIME-complete, hex PSPACE-complete. No efficient
  exact solver exists for any of the seven families. Games stayed playable for 4,500 years
  because humans never solved them — they walked them.
- FLEET PROCESS: the fleet does not SOLVE the corpus (1,040 cards × 47 invariants × 7
  engines is exponential), it WALKS it — flash models as polynomial readers is not a
  limitation, it is the correct player class for an exponential room (the lattice says this
  in one line; it is also the whole tesuji thesis, watch/TESUJI_MAP_5_3FLASH_20260906.md:
  probes as sacrifice stones, reading the field instead of solving it). Cache reads are the
  walk's free steps; metered probes are the sacrifices.
- ROOM-SPEC: THE WALKER room — a logic chamber explicitly sized beyond any solver; cleared
  only by walking (bounded reads, hash-chained steps), never by claiming a solution. The
  room's invariant: an honest walk of 100 sealed steps beats a fabricated total solve.

---

## ANCESTRY
- watch/GAME_MECHANICS_LATTICE_20260903.md — the seven engines, the room generator,
  the complexity honesty (this card extends rows TILE / CARD / CONSTRAINT-PUZZLE).
- watch/GAME_CODEX_20260903.md — gaming as coding; the socratic gate as combat system.
- watch/BASECAMP_GAME_ATLAS_20260901.md — L0-L4 join, sudoku exactly-one oracle as
  flagship, card_systems.DRAFT.md + constraint_puzzle.DRAFT.md + L2_riichi.md engines.
- Fleet receipts: watch/SELF_STEAL_VISION_PIPELINE_20260905.md (cite-gate),
  watch/GROUNDING_WAVE.jsonl (tri-state pond), mag/refeed_guard.py (B1),
  watch/SELF_STEAL_MCP_TOPOLOGY_20260904.md (information-set topology),
  configs/auth_tracks.yaml (caps), memory/percolator/invariants.json (the loot).

## THE ONE-LAW SUMMARY
TILE teaches composition (hands, not piles — cite-gate passes, not link dumps).
CARD teaches honesty under hidden state (information sets, blind witnesses, files not
privileged memory). CONSTRAINT teaches generation (the caps that gated tonight's builds
are the walls that fixed the maze). The fleet is a card table played on a tile wall,
bounded by a sudoku — and every room in shadow_walk can be stamped from these three.
