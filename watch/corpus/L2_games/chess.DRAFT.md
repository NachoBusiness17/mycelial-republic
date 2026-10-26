# L2 - Chess (Western, FIDE, 8x8) Game Pack (DRAFT) - `L2_games/chess.DRAFT.md`

> **Status:** DRAFT. **Class:** L2 game statics - flagship instance of the war/capture engine.
> **Engine dock:** `research/gaming_corpus/engines_war_territory.md` section 1 (WAR/CAPTURE:
> chess, shogi, checkers = the falsifier economy). **RAW ORE:** `memory/runs/l2_statics_pour_20261020/results.jsonl`
> row `chess` (model deepseek-chat, ok_api + ok_material true, 1 attempt; all rule text below is
> carried from that row's `out` field). **House grammar:** per `L2_games/sudoku.DRAFT.md`
> (five slots + lineage module + cache-boundary note + build prompt + status trailer).
> **Research status:** lineage anchors are **attested** except where tagged **honest** (debated
> early dates, the mad-queen reform window, the Murray reprint erratum); the game-theoretic-value
> claim is **unverified** (open problem, tagged at SLOT 5); one notation-name claim is
> **unverified** at SLOT 4.

---

## SLOT 1 - TOPOLOGY
`TOPOLOGY` = grid 8x8, 64 squares, algebraic coordinates a1-h8 (ore: "8x8 array, 64 squares,
algebraic coordinates a1-h8"). Neighbor relation is piece-dependent: 4-orthogonal rays for the
rook, 4-diagonal rays for the bishop, all 8 for the queen (rays stop at the first occupied
square); single-step any direction for the king; L-jumps for the knight (jump over blockers,
land on empty or enemy); pawns step forward one, or two from their start rank when both squares
are empty, and capture one diagonal forward.

## SLOT 2 - DOMAIN
Per-cell `DOMAIN` = 13 states: empty (written `_`, house convention) plus 6 white piece types
{K,Q,R,B,N,P} and 6 black piece types. Position super-state (required, not optional - see
SLOT 3 history clauses): side to move {w,b}; castling rights subset of {K,Q,k,q}; en-passant
target square or none; halfmove clock (50-move rule) and fullmove number (ore state-encoding
block). A position = board + side to move + castling rights + en-passant target + clocks.

## SLOT 3 - CLAUSES
Four clause families over the ore rules canon (standard FIDE chess, 8x8, two players, white
moves first):

1. GEOMETRY: one move-geometry clause per piece type (the SLOT 1 relations; promotion: a pawn
   reaching the last rank becomes Q/R/B/N, player's choice).
2. KING-SAFETY FILTER (the global clause): a pseudo-legal move is legal only if it does not
   leave the mover's own king in check, including discovered check. This is chess's analogue
   of the engine's all-different sweep: one global predicate gates the whole move set, and per
   the ore invariant the king is the only piece whose safety constrains every other piece's
   legality.
3. HISTORY: castling (king and rook both unmoved, squares between empty, king not in check and
   not passing through or landing on an attacked square) and en passant (target square exists
   only after the immediately prior double pawn step) are the only history-dependent clauses;
   the state is therefore not Markov in the board alone (ore invariant). Transition bookkeeping:
   update castling rights on king/rook moves and rook captures, set the en-passant target on a
   double step, reset the halfmove clock on a pawn move or capture, increment the fullmove
   number after black.
4. TERMINAL: checkmate (side to move in check with no legal move = loss for that side);
   stalemate (not in check, no legal move = draw); draw clauses: halfmove clock reaching 100
   plies (the 50-move rule), threefold repetition, insufficient material; resignation and
   timeout end games under tournament rules. Scoring 1 / 0.5 / 0 is tournament convention;
   piece values (P=1, N=3, B=3, R=5, Q=9) are heuristics, not rules.

Honest flag (ore forced-capture note): standard chess has NO forced capture. The war/capture
family's forced-capture clause (the socratic gate, see FLEET CROSSMAP) is enforced in checkers
and in some shatranj-adjacent regional variants, not in canonical FIDE chess.

## SLOT 4 - INSTANCE
A chess instance is a position (board + super-state). Canonical start instance, constructed
from the ore initial-state spec (back rank R N B Q K B N R; pawns on ranks 2 and 7; white to
move; all castling rights live; no en-passant target; clocks zeroed):

```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

The bytes are anchored by construction to the ore initial-state spec (attested-by-derivation);
the name "FEN" for this string format is common interchange usage and carries no source anchor
in this pour - research_status: unverified for the name, not for the string.

## SLOT 5 - VERIFIER
Parse (board + super-state) -> legal-move generation (GEOMETRY, then the KING-SAFETY FILTER) ->
checks:

1. START-COUNT: the start instance yields exactly 20 legal moves (P=16, N=4, B=0, R=0, Q=0,
   K=0). Rules-derived and enumerated in this pour by a full piece-by-piece enumeration run
   against the ore start spec (run 2026-10-20, output: total 20).
2. KING-SAFETY INVARIANT: after every transition the side not to move's king is never
   capturable (the global filter held on every generated move).
3. TRANSITION DETERMINISM: apply-move updates castling rights, en-passant target, halfmove
   clock and fullmove number exactly per the SLOT 3 bookkeeping.
4. TERMINAL DETECTION: checkmate, stalemate and the three draw clauses fire on exactly the
   positions that satisfy them.

Technique ladder (the sudoku ladder's war-game analogue, ore-grounded): captures and
recaptures -> checks -> tempo and zugzwang (ore invariants: tempo is a first-class resource,
white's first-move advantage is real and measurable, and zugzwang shows tempo can be a
liability) -> combinations (discovered attacks, pins, sacrifices) -> endgame technique under
the draw clauses. Honesty note (ore invariants block): the first-move advantage magnitude is
debated by rating and format - research_status: honest; the game-theoretic value of chess
(forced win or draw for either side) is an open problem with no proof either way -
research_status: unverified.

### LINEAGE MODULE
Dated, status-tagged anchors (statuses carried from the RAW ORE lineage block):

- c.600 CE, India: chaturanga - honest (early dates debated; Murray 1913 argued this window,
  later scholarship pushes some texts later; the Bhavishya Purana passage is contested, the
  Harshacharita of Bana is the firmer anchor).
- c.600-700 CE, Persia: shatranj, the Sasanian adoption with the same piece set renamed
  (shah, rukh, fil, asb, farzin) - attested (Persian literary sources, e.g. the
  Karnamak-i Artakhshir).
- c.800-1000 CE: shatranj spreads west via conquest and trade; al-Adli and as-Suli write the
  earliest surviving strategy treatises - attested (Arabic manuscript tradition).
- c.1000-1200 CE, Europe: chess enters via Iberia and Sicily; the Alfonso X manuscript
  (Libro de los Juegos, 1283) is the key surviving European rules text - attested.
- c.1475-1500, Europe: the "mad queen" reform (queen and bishop gain long-range movement,
  producing modern chess; "queen's chess" in Spanish sources) - honest (the c.1475 date is
  conventional; exact origin and pace of reform are debated among Murray, Eales and others).
- 1497, Spain: Lucena, Repeticion de Amores y Arte de Ajedrez, first printed European chess
  book with the new rules - attested.
- 1561, Spain: Ruy Lopez, Libro de la invencion liberal y arte del juego del Axedrez, early
  opening theory - attested.
- 1749, France: Philidor, L'Analyse des Echecs, first systematic positional treatment - attested.
- 1851, London: first international tournament (Anderssen wins) - attested.
- 1886, USA: first official world championship match (Steinitz vs Zukertort) - attested.
- 1924, Paris: FIDE founded - attested.
- 1913: H.J.R. Murray, A History of Chess, the standard scholarly history - attested (primary
  citation); the 1952 Oxford date is a reprint/abridgement reference, not a new claim - honest
  (erratum carried from the ore).
- 1997, New York: Deep Blue defeats Kasparov, first machine win over a reigning champion in
  match play - attested.
- 2000s-present: engine era (Stockfish, Leela Chess Zero) and online play reshape the
  metagame - attested.

### FLEET CROSSMAP
Chess IS the estate's **war/capture falsifier-economy organ**
(`research/gaming_corpus/engines_war_territory.md` section 1): "every capture = a falsified
assumption becomes a law" (section 1 mechanic), and "the capture rate is the learning rate"
(section 1 fleet process). The engine file states the mapping is not analogy: "the falsifier
economy IS the combat system ... the same loop at two substrates" (combat-grammar preamble).

- Chess-specific instantiation of the socratic gate: canonical chess has no forced capture, so
  the gate lands as the KING-SAFETY FILTER (SLOT 3 clause 2) - every candidate move must first
  answer "does this leave my king safe?", one global predicate gating the whole move set. The
  forced-capture form of the gate is the family's checkers instantiation ("when a capture
  exists you MUST take - no passing", engine section 1), and per the ore some shatranj-adjacent
  regional variants enforce capture too.
- "Dragons = assumptions with HP" (load-bearing score as the HP bar) is the engine's COMBAT
  CHAMBER room-spec; per the ore crossmap note this is a reskin layer over chess, not a rules
  claim - flagged here, not encoded in the clauses.
- Sibling organs in this pour (family rows, one static each): go = the territory tesuji
  lightmap (engine section 3: cached reads and banked corpus are settled territory, unprobed
  capability is dark, a vendor wall-change dirties a radius); tafl = the asymmetric solo-agent
  organ (engine section 4: one king ferries one load-bearing artifact to the board edge while
  hunters encircle, capture by sandwich); hanafuda = the card information-set organ (card
  grammar in `research/gaming_corpus/engines_tile_card_constraint.md`,
  CELL G/engine/card/information_sets + CELL G/engine/tile/matching_law; the hanafuda-specific
  static is the sibling lane of this pour).

### CACHE-BOUNDARY NOTE
Static prefix (byte-stable every request): rules canon, the four clause families, lineage,
crossmap. Dynamic tail (never cached): the position instance (board + super-state) and the
chosen move. Delta over the constraint-puzzle engine (`L2_games/sudoku.DRAFT.md` grammar):
chess swaps the clause class for geometry + a global king-safety filter and swaps the instance
grammar from a fixed string to a position; it adds the transition layer (apply-move), which
sudoku's static board never needs. Because of the history clauses the dynamic tail must carry
castling rights, en-passant target and clocks with the board - a board-only tail is not a
valid instance (SLOT 3 clause 3).

### BUILD PROMPT
`{topology:8x8-a1h8-piece-rays, domain:13-state-cells+super-state, clauses:geometry+king-safety+history+terminal, instance:<canonical-position>, verifier:start-count-20+king-safety+transition-determinism+terminal-detection}` -
organ: war/capture falsifier economy (`research/gaming_corpus/engines_war_territory.md`
section 1); no forced capture in canonical rules - flag any variant that adds it.

---

research_status: attested
