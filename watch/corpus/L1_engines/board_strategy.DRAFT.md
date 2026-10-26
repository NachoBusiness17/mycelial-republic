# L1 — Board/Strategy (War/Capture) Engine (DRAFT) — `L1_engines/board_strategy.DRAFT.md`

> **Status:** DRAFT. **Class:** L1 family engine — one mechanical spec shared by every
> **war/capture** board game: chess → shogi → xiangqi → tafl → checkers → go. It is a **sibling,
> not a child**, of race/dice and sowing/capture: same L0 six-function contract, but the core
> operator is **positional capture by divergent piece-movement** on a grid (not movement-to-a
> finish, not sowing). The engine hosts **slots**; packs supply the predicates that characterize
> their game. **Provenance:** primer §7 build-order (war family), Fact 5 (LLM never solves), Fact
> 7 taxonomy, Fact 8 (contested rules travel openly). **Research status:** chaturanga→chess family
> mechanics `attested`; tafl king-escape **`reconstructed` with two readings** (Linnaeus 1732
> ambiguity); go ko/complexity `attested`. Flagged per pack, never silently upgraded.
> **Consumption order:** L0 contract → this engine (family mechanics + slots) → one game pack
> (slot-supplied predicates) → L2 statics → L3 cultural pack.

---

[PROMPT-BODY-START — byte-stable from here]

## BOARD/STRATEGY (WAR/CAPTURE) ENGINE — FAMILY MECHANICS

A **war/capture game** is a grid of cells holding pieces of two (or more) sides; players alternate
moving their own pieces, each piece type having a **move set** (displacement patterns per the
pack); a move may **capture** an opposing piece on or through a destination depending on the pack's
capture rule; the game ends when a **pack-supplied terminal predicate** fires. You apply these
mechanics exactly as written, plus the pack-supplied predicates, never anything else.

### SLOT PRINCIPLE (the engine hosts; packs define)

Every non-structural claim in this engine is a **slot** filled by the pack, not by the engine:
the capture resolution, the win/lose/draw terminal predicates, the move-generator's capture
sub-rules, and the scoring weights. The engine supplies the fixed machinery (grid, side-to-move,
turn swap, capture-takes-place, superseeding rule application); the pack supplies every
game-specific predicate. Where the engine states a canonical default, the pack may override it by
filling the slot; where the engine marks a clause **structural**, the pack may not override it.

### STATE (piece-list or grid; side-to-move)

- **Two representations, pack-chosen (one per pack):**
  1. **Grid (canonical):** a `W×H` grid of cells; each cell `(r,c)` holds `none` or a piece token
     `(side, type)`. FEN/PGN-style compact strings (L0 F1) are the canonical encoding for chess-ish
     packs; SGF/kifu-style for go/shogi. The **board string is the sole authority** on placement.
  2. **Piece-list:** an explicit enumeration per side — `P_side = [(type, cell), ...]` — used where
     placement is sparse or off-board capture/stocks exist (shogi, tafl edge cases).
- **side-to-move:** exactly one `active-role` per turn; turn alternates unless the pack's terminal
  or capture rules grant a pass, drop, or bonus move. **Canonical string** (L0 F1):
  `<id>:<hash>:<turn-index>:<active-role>:<board-or-pieces>:<order>:<seed-phrase `-`>:<reserved>`.
  The board/piece field is the sole authority; a `seed-phrase` of `-` unless the pack defines a draw.

### INITIAL (per-pack setup)

- **INIT:** fixed by pack **starting layout** — grid listing (chess/xiangqi/checkers) or empty grid
  with a **hand placing protocol** (go), or fixed ring/first-move rule (tafl). Fully determined by
  pack `INIT` + game id; reproduces identically each run.
- Empty grid for go: the first `N` moves place; `seed-phrase` seeds only the place-order if drawn,
  else `-`. The initial layout is legal by construction (no captures precede the first move).

### LEGALITY (move-generator signature: piece-type → move set)

`LEGAL?(state, T) -> Bool { legal, reason }` (L0 F3) — equivalently `legal(state, actor) -> [action]`
enumerating all pseudo-legal moves. A candidate `T = (side, from, to, promo?)` is legal iff:

1. **Ownership:** `from` holds a piece of the `active-role` whose piece-type's **move set** contains
   a displacement taking it from `from` to `to` — `MOVE?[type](from, to, state) -> Bool`, the pack
   **move generator** signature (see PIECE-HIERARCHY).
2. **No self-clash (structural):** `to` must not hold the mover's own piece.
3. **Path:** if the move set requires a **clear line** (sliding), all intermediate cells (pack
   `EXCLUDES_DEST` for ordinary moves) are empty; the capture variant allowing a hop (see checkers
   CALCUTTA, xiangqi cannon) is a **pack predicate**, not engine default.
4. **In-edge / behind-line:** if a **zone** exists (river/palace per xiangqi, edge/corner per tafl
   king), `to` must satisfy the pack's zone predicate unless the piece-type says otherwise.
5. **Not leaving own king exposed** IF the pack defines king/check; ELSE the "in enemy fire after
   move" filter is off (go, checkers, tafl have no check → no pin/check constraint).

A `false` on ownership, self-clash, blocked path, or missing type → hard `false`; ambiguity → hard
`false`. The LLM reports the move as a chosen predicate — **never** invents one.

### TRANSITION (apply move; then capture resolution — pack-supplied)

`APPLY(state, T) -> state'` (L0 F4), in fixed order:

1. **Validate** against `LEGAL?` (reject first; an illegal move is a hard `false`, reason
   `ILLEGAL_MOVE`).
2. **Move:** relocate the piece `from → to` (grid or piece-list update), per the type's displacement.
   Apply the pack's **promotion predicate** here if any (`promo?` slot: piece-type changes on
   entering a rank/zone — shogi promo, chess pawn promotion, per pack).
3. **Capture resolution — PACK-SUPPLIED** (the engine hosts, the pack fires):
   - **targeted** (chess, tafl, checkers: win by force? no—) — the opposite-side piece **at `to`**
     is removed when `to` is the displacement target (capture-by-occupation, default).
   - **by-occupation-with-zone** (go): a group is captured **not** per-move but when it loses its
     last **liberty** (empty adjacent cell) after a placement — **`SUPERSEDE` rule** supersedes the
     simple remove (go ko, see TERRITORY BLOCK).
   - **by-hop** (xiangqi cannon, checkers jump): the piece is captured by **jumping over** it to a
     landing cell (pack `CAPTURE_MODE: hop|occupation|liberty`). For checkers (forced capture /
     **CALCUTTA**), when a jump is available it is **compulsory**: the mover must take the longest
     legal jump-chain (`FORCED_CAPTURE: on`), and chains resolve before the turn ends.
   - **asymmetric removal** (tafl): the **capture is two-to-one** — CANONICAL: `2` attackers remove
     a single non-king defender by **sandwich** (edge-`EXCLUDES` variants per pack); see
     ASYMMETRIC-WIN BLOCK for the king's 2:1 rule and the `attested`/`reconstructed` split.
4. **Drops (pack slot, shogi):** a moved-away piece enters the mover's **captured-stock**; on a
   `drop` turn the mover may place a stock piece on any empty legal cell (never into a zone the
   piece cannot move in; never into an immediate unpromoting two-pawn block — pack `DROP` clause).
5. **Superseding constraints (structural order):** apply any pack-defined **constraint that
   overrides an otherwise-legal outcome** last — canonical go **ko** (a move that would recreate a
   previous board state is illegal, see TERRITORY BLOCK), checkers forced-capture, xiangqi's
   "flying general" mutual-check ban, shogi's no-drop-mate/suicide constraints.
6. **Advance:** `turn-index += 1`, recompute `state-hash`, swap `active-role` (or keep on bonus
   turn — `LAPE`-style slot, default `off`), reprint canonical string, then narrate.

### TERMINAL (PACK-SUPPLIED predicates — the engine hosts the slot)

`TERMINAL?(state) -> Bool { terminal, winner, score }` (L0 F5). **The engine does not define win —
it hosts the slot.** Each pack supplies one or more terminal predicates evaluated in a fixed,
pack-declared order:

- **checkmate** (chess, shogi, xiangqi): mover placed opponent in check from which no legal reply
  exists → winner = mover.
- **stalemate** (chess canonical): side to move has **no legal move and is not in check** → `draw`
  (`STALEMATE_TIE`, L0). A pack may supply a `no-legal-moves-for-mover` generalizer (go: no legal
  placement without self-capture).
- **territory-score** (go): the game ends on **both** players passing; win = larger **territory +
  captured stones** under the pack's scoring school (see TERRITORY BLOCK). This is the canonical
  **non-capture-by-force** termination.
- **asymmetric-escape** (tafl): the defender wins by getting the **king** to the pack's **escape
  cell(s)**; the attacker wins by **capturing the king** (2:1, see ASYMMETRIC-WIN BLOCK). Both are
  pack predicates; the engine only hosts the two slots and their order (escape checked first, then
  king-capture, per pack).
- **forced-capture exhaustion** (checkers): the mover captures the opponent's last piece, or the
  opponent has no forced capture left → winner = mover.
- **repetition/draw (structural guard):** a repeated `state-hash` does **not** auto-terminate
  unless the pack supplies a draw predicate (go ko already bans single-step repetition; chess
  threefold/fifty-move are pack predicates). Default: report `LOOP` with prior hash.

Each pack declares the **evaluation order** of its predicates; first to fire wins the verdict.

### SCORING (material / territory / outcome — pack-weighted)

`SCORE(state) -> Score` (L0 F6):

- **material** (chess, shogi, xiangqi, checkers, tafl): assign each piece-type a **value** (pack
  weight table) and price the sides' remaining force + captures; outcome (`WIN`/`LOSS`/`DRAW`)
  overrides raw material. The **PIECE-HIERARCHY BLOCK** gives the canonical chaturanga→chess
  values.
- **territory** (go): **stones + empty-territory** — score = enclosed empty cells (territory) +
  captured stones + (pack option) the move-size **komi** compensation for the second player
  (pack constant), under a declared scoring school (see TERRITORY BLOCK; area vs. territory).
- **outcome**: a terminal verdict maps to a score; a `draw` yields the pack's split (chess `½–½`,
  go jigo per komi).

---

## PIECE-HIERARCHY BLOCK (chaturanga → chess family: promoted moves per piece)

The war/capture engine's default **move generator** is the **chaturanga→chess** hierarchy — the
attested diachronic root of the chess family (Murray 1952). Every pack that docks on this engine may
keep, prune, or extend the per-piece **move sets** and **values**; the hierarchy below is the
**default** the engine supplies, keyed by promotion (Promoted Move shown only when the pack enables
that piece's promotion).

| Piece | Default displacement (move set) | Promoted move (rank/zone promo slot) |
| :--- | :--- | :--- |
| pawn | 1 forward, capture 1 diagonal | (chess) on reaching last rank → queen/rook/bishop/knight per pack |
| rook | orthogonal slides (clear line) | — |
| knight | fixed `L` jump (2+1, 1+2), ignores blocking | (shogi) golden-general move |
| bishop | diagonal slides | (shogi) full-slide lateral |
| queen | rook ∪ bishop slides | — |
| king | 1 any direction | (xia not; tafl king is the escape piece; see ASYMMETRIC) |
| cannon (xiangqi) | orth slides only as an **empty-line rider**; captures **only by hop** | — |
| golden general (shogi) | 1 forward/orth/side, no full diagonal back | two pawns→golden (shogi promotion set) |

**Pack rule:** a piece's **value** and **promoted displacement** are pack weights/slots; the engine
only fixes the displacement *signature* (type → displacement predicate) and that **promotion is
always a pack predicate**, never engine-invented. `research_status: attested` for the chess-family
hierarchy (Murray 1952; chaturanga/Shahranj boards and piece values are documented), with the
exact promotion rules `attested` or `reconstructed` per pack.

---

## ASYMMETRIC-WIN BLOCK (tafl / hnefatafl: 2:1 attackers; king escapes edge-or-corner)

Hnefatafl (and the tafl family) is the **asymmetric** war/capture case: **attackers outnumber the
defender**, `2:1` is the canonical force ratio; the defender wins not by material annihilation but
by **extracting the king**. The killing rule is asymmetric too — the king is captured **by `2:1`
sandwich**, not by simple occupation, matching the header ratio (a lone attacker does not take the
king). **The king's escape target is `reconstructed`, with two competing readings from the corpus's
only eyewitness record, Linnaeus's 1732 tablut notes (Fact 8):**

- **Reading A — corner (the "Linnaeus" reading):** the king escapes only by reaching one of the
  **corner cells** (canonical 11×11 tablut inner-edge corner cells marked in Linnaeus's diagram).
  `research_status: reconstructed (Linnaeus 1732 board marks corners; followed by the hnefatafl
  "corner-escape" school)`.
- **Reading B — edge (the "edge" school):** the king escapes by reaching **any edge cell** of the
  board. `research_status: reconstructed (inferred from Scandinavian-period tafl cousins and
  later editorial syntheses; the "edge-escape" reading)`.

A century of debate sits on this one translation ambiguity (primer §8 open agenda). **The engine
does not canonize either school** — it hosts the `KING_ESCAPE: corner | edge` slot; each tafl pack
fills it and surfaces the dispute ("historians disagree — this build uses `corner`"), honoring the
primer's rule that contested history travels openly, never silently resolved. `research_status` for
the 2:1 capture is likewise `reconstructed` from Linnaeus + period synthesis; the force ratio and
king-capture-by-2:1 are attested within the tafl family's shared framing.

---

## TERRITORY BLOCK (go: stones + empty-territory scoring; ko = the canonical superseeding constraint)

Go is the war/capture engine's **non-capture-by-force** extreme: capture happens by **liberty-loss,
not displacement-onto**, and the win is by **counted territory**, not material dominance. The
engine slots these:

- **Capture-by-liberty (pack `CAPTURE_MODE: liberty`):** an opposing **group** (orthogonally
  connected own-and-only-own stones) is removed when a move removes its **last liberty** (empty
  orthogonal neighbor). This is the engine's generic liberty rule, pack-triggered.
- **Scoring — stones + empty territory:** a finished game scores each side's **live stones** plus
  the **empty cells they enclose** (territory), adjusted by the pack's **komi** (second-player
  compensation) and prisoners. `research_status: attested` for the stones+territory core (the
  modern scoring is codified; the dispute is **area vs. territory scoring** — a pack slot declaring
  the school). Board `19×19` (~`10^170` legal positions) is the attested canonical size (Tromp 2016).
- **KO — the canonical superseeding constraint:** go's ko rule is the engine's **structural
  supersede** (TRANSITION §5): a move that would **recreate a board position identical to an
  immediately previous legitimate position** is illegal — it forbids the single-cell **snap-back**
  that would otherwise be endless capture-loops. `research_status: attested` (ko is universal across
  go recensions). It is the load-bearing example of the engine's rule that a **superseding
  constraint overrides an otherwise-legal outcome**; a pack may generalize it to **super-ko**
  (full-position ban, shogi-style "no-draw" variants).

---

## SOLVED-GAME HONESTY NOTE (EXPTIME-complete; checkers-draw 2007; awari-draw 2002)

**The LLM emits instances; the engine verifies.** This engine's family contains some of the most
studied games in complexity theory, and the corpus is explicit that the LLM is never the solver
(Fact 5):

- **Generalized chess** is **EXPTIME-complete** (Fraenkel & Lichtenstein, 1981) — finding the *win
  with a perfect strategy on an arbitrary N×N board* is exponential-time-hard. Standard `8×8` chess
  is finite and (in principle) solvable but astronomically beyond practical search.
- **Generalized go on an N×N board** is likewise **EXPTIME-complete** (Robson, 1983); even the
  specific `19×19` game has ~`10^170` legal positions (Tromp, 2016).
- **Solved-game anchors (bounded-size families):** **checkers (English draughts)** was **proved a
  draw** with optimal play — **Schaeffer et al., 2007** — after essentially clearing the full
  `~5×10^20` positions of the 8×8 game. **Awari/Oware (sow/capture, this corpus's sibling engine)**
  was **proved a draw — Romein, 2002**.

**Implication for this engine:** a war/capture instance is a *state the LLM can legally step through
and narrate*, never a problem the LLM is asked to solve. `LEGAL?`, capture resolution, ko
enforcement, and terminal/score predicates all go to **deterministic verifiers** defined by the pack;
the LLM emits the chosen predicate and applies the engine's fixed order. No claim of "optimal play"
or "chess engine strength" belongs to the LLM — assign that to the verifier or a dedicated solver.

---

## FAMILY PACK SLOTS (cultural packs that dock on this engine)

- **Chess** (`L3_packs/chess.DRAFT.md` TBD, **attested**) — `8×8` grid, FEN/PGN, `CAPTURE_MODE:
  occupation`, check/checkmate/stalemate terminal, king + hierarchy moves, threefold/fifty-move draw
  predicates. The reference build: near-thin delta filling only the hierarchy, zone (none), capture,
  and terminal slots.
- **Shogi** (`L3_packs/shogi.DRAFT.md` TBD, **attested**) — `9×9`, **drops** from a captured-stock
  (`DROP` slot), **promotion** entering the top three ranks, no checkmate-by-pawn-drop, "no-drop-
  mate" and suicide constraints as supersedes; captured pieces change sides.
- **Xiangqi** (`L3_packs/xiangqi.DRAFT.md` TBD, **attested**) — `9×10`, **river** (pieces cannot
  cross / can cross once, per type) and **palace** (king/advisor confined to 3×3), **cannon**
  hop-capture, **flying-general** mutual-sight ban as a supersede.
- **Tafl** (`L3_packs/tafl.DRAFT.md` TBD, **reconstructed**) — asymmetric 2:1, `CAPTURE_MODE`
  sandwich with king-by-2:1, `KING_ESCAPE: corner|edge` per the ASYMMETRIC-WIN block's two readings;
  terminal = **asymmetric-escape** (king reaches escape) vs. attacker king-capture. All historical
  subslots `reconstructed` per Linnaeus.
- **Checkers / English draughts** (`L3_packs/checkers.DRAFT.md` TBD, **attested**; result proved
  draw 2007) — `8×8` dark squares only, diagonal moves/jumps, **forced capture (CALCUTTA)** with
  **compulsory longest jump-chain**, men→king promotion on the far rank; terminal =
  forced-capture-exhaustion.
- **Go** (`L3_packs/go.DRAFT.md` TBD, **attested**) — `19×19` (variable per pack), **liberty**
  capture, **ko/super-ko** supersede, alternating **pass** → territory-score terminal, stones+empty-
  territory with **komi** and area-vs-territory school slot. EXPTIME-complete / ~10^170 positions
  per the SOLVED-GAME HONESTY NOTE.

### OUTPUT / INSTANCE NOTES

- Apply L0 OUTPUT CONTRACT before and after any move: restate canonical state on the `^` line, cite
  the governing L0 function + engine clause + the pack predicate that fired, emit the new canonical
  string, then narrate.
- Moves are **chosen predicates** (never invented); capture/ko/terminal/score all resolve through
  deterministic verifiers; **no final "who should win" claim is emitted by the LLM** unless a pack
  terminal predicate has fired — then it is reported as a verdict, not a judgement.
- Any collision between this engine and a pack delta resolves **delta wins** for the specific
  predicate, except **structural** clauses (grid, side-to-move swap, capture-then-supersede order,
  round-robin predicate order, ownership/self-clash), which a pack may not override — it may only
  fill the exposed slots and constants.

[PROMPT-BODY-END]

---

## Asset notes (NOT cached prompt body)

- **Target size:** ~1.5–2k tokens of prompt body. Six family pack-delta sketches are 2–3 lines each
  (on the 100–800-token pack budget); each expands into its own `L3_packs/*`.
- **Slot-first design** is the engine's distinguishing move vs. race/sowing: terminal, capture,
  zone, drop, score, and king-escape are all **pack-supplied predicates the engine hosts** — the
  engine never silently canonizes any war game's win rule beyond coining structural order.
- **Two tafl readings** come straight from the primer's own §8 open-agenda note ("Hnefatafl's last
  eyewitness record is Linnaeus's 1732 tablut notes, containing a translation ambiguity — king
  escapes to *edge* vs. *corner*"). Both carried `reconstructed`, and the engine deliberately does
  not choose between them.
- **Complexity facts** are the primer's §5 anchors: Fraenkel & Lichtenstein 1981 (chess EXPTIME), Robson
  1983 (go EXPTIME), Tromp 2016 (10^170), Schaeffer 2007 (checkers draw), Romein 2002 (awari draw).
- **Cross-refs:** parent `L0_contract.md` (six-fn schema) + `L0_universal_contract.DRAFT.md`;
  sibling engines `race_dice.DRAFT.md` and `sowing_capture.DRAFT.md` (sow/capture shares the go/awari
  draw note — keep the two in agreement); downstream `L2_games/*`, `L3_packs/*` per game; honor
  `00_PRIMER.md` §8 open questions (esp. disputed-history presentation, difficulty portability).
