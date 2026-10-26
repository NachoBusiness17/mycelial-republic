# CULTURAL PACK: Royal Game of Ur (Mesopotamia, ~2600 BCE)

> **Status:** DRAFT. **Class:** L3 cultural pack — a delta over the race/dice engine; not a rules
> rewrite. **Consumption order:** L0 contract → `L1_engines/race_dice` (family mechanics) → this
> pack (deltas) → L2 statics. **Engine overrides below are `delta-wins` clauses; structural engine
> clauses (track shape, capture ordering, bear-off machinery) may NOT be overridden.**

---

## ENGINE

`race_dice` — with the deltas in this pack. Defaults from the engine apply where this pack is
silent.

## RULE DELTA

- **Track shape:** `ring` — a *fixed* 20-square path (not a race around a loop with laps). The
  path is not a uniform loop; per the attested/reconstructed reading it is a serpentine course
  with **two routes sharing the two "safe" rosette squares (4 and 14 per the common numbering) and
  the entry/corners**. This pack's DEFAULT build ships the **short/long route distinction as a
  named variant** (see REGIONAL VARIANTS); the base instance uses the single shared track with both
  players moving the same direction, battle-square collisions at rosettes. Encoded as linear
  indices `0..N-1` with N=20; index 19 (or the route's far terminal) is the final square before
  bear-off.
- **Movement source:** seeded-external **Ur binary tetrahedral** — 4 tetrahedral dice, each marks
  exactly ONE face/corner "1", others "0"; roll result = count of marked faces (0..4). Mode
  per L0 historical mode #2 (reconstructed, Finkel/BM 33333). LLM reports, never rolls.
- **Roll-exact vs clamp:** **`roll-exact` for entry and bear-off** — a piece enters from the
  start/talley on an exact roll; a piece bears off only on an exact roll matching the remaining
  distance. Non-entry ordinary movement may clamp to the path length only if the route defines a
  terminal landing; otherwise a roll that overshoots the final square before bear-off is ignored.
- **CAPTURE: on** — a piece may capture an opponent piece by landing exactly on it. **Capture is
  DISALLOWED on `safe` rosette squares** (see SQEFFECT). A piece that is captured returns to its
  owner's `start`/entry square and requires a fresh exact entry roll.
- **SQEFFECT:** five squares are **rosette / `safe` squares** (the engine's `safe` effect) with
  indexing per the common layout:

  | square-id (linear) | effect | target | param |
  |---|---|---|---|
  | 4 | `safe` (rosette) | self | — |
  | 8 | `safe` (rosette) | self | — |
  | 14 | `safe` (rosette) | self | — |
  | (shared crossing) | `safe` | self | — |
  | (shared crossing) | `safe` | self | — |

  The **exact rosette count** (commonly 5 — four rosettes plus a crossing square read as safe) is
  a disputed detail: the **five-rosette reading is the conservative default** accepted by both
  scholarly camps (see HISTORICAL MODULE). Ships with `research_status: reconstructed`. Squares
  not listed are *battle* squares where `CAPTURE: on` applies.
- **Win / bear-off:** the first player to move all **seven** of their pieces off the far end of
  the track wins. Bear-off is `roll-exact` on the final square. (The piece count of seven per
  player is the attested reading of the board's 15-slot × two shared rosettes geometry; contested
  only in detail — see HISTORICAL MODULE.)
- **ENTRY:** all seven pieces start in a **home stock / talley** off-track; a piece enters on the
  roll `1` (equivalently the reverse face) or on any roll that is declared an entry roll per the
  pack — **this build uses entry-on-1** as the attested conservative reading. Captured pieces
  return to the stock and re-enter on an exact `1`.

## HISTORICAL MODULE

- **Era / culture:** Mesopotamia, **c. 2600 BCE** (Early Dynastic III royal graves of Ur),
   used ~2000+ years across Sumer/Akkad and beyond (board game tradition).
- **Archaeology:** the physical boards — wood inlaid with shell, lapis lazuli, and red limestone —
   excavated at the Royal Cemetery of Ur (Woolley 1920s). The most complete rules source is the
   **BM 33333 tablet**, a **Seleucid-era cuneiform copy (~177–76 BCE) written ~2400 years after
   the boards**, which preserves a set of play rules (published/analyzed by **Irving Finkel,
   2007–08**).
- **Sources / attributions:** Finkel, *On the Rules for the Royal Game of Ur* (2007); Finkel &
   Walker (BM documentation). Game studies reconstructions: Walker, Becker, Bell (later popular
   restatement).
- **attested vs reconstructed — the load-bearing distinction:**
  - **attested:** the existence of the 20-square board, the two-player seven-piece setup, the
    binary four-tetrahedral dice (a matched set was found with the boards), and the rosette
    squares as special/safe — all archaeologically documented.
  - **reconstructed:** the *precise* movement rules, the reading that rosettes block capture, the
    entry rule, and the exact rosette count. These are **readings of BM 33333**, not engraved
    rules, and are contested.
- **Contested-history schools (named, not resolved):**
  1. **Finkel school** — BM 33333 fixes the race-style play with rosettes as bonus/blocking
     squares and the tetrahedral dice; treats the Seleucid tablet as preserving the ancient rules.
     This build follows this school. `research_status: reconstructed`.
  2. **"Woolley ritual" / pre-rules school** — holds the earliest boards (ED III) may have had
     **non-competitive ritual/divinatory functions** alongside or before play rules; the Seleucid
     copy documents a later, possibly evolved game form. `research_status: reconstructed`
     (argued, not directly attested for the ED III boards).
  3. **"Twenty Squares" lineage school** — ties Ur to the Egyptian *Game of Twenty Squares* and
     later Babylonian games, treating the BM 33333 text as one regional member of a shared
     game-family diffusion, with local rule divergence. `research_status: speculative`.
- **Honesty note (always included in output):** historians disagree on the exact rules; the exact
  movement/entry/rosette behavior is a **reconstructed reading of the Seleucid copy (Finkel)**,
  not an engraved law, and this build uses the Finkel five-rosette reading.

## MATERIALS MODULE

- **Original (attested):** a 20-square rectangular board; two players with **seven** counters
  each (shell-bird / lapis-bird tokens, later counter shapes vary); **four tetrahedral dice** —
  each a small pyramid with one marked corner/face; sometimes the board was a folding case with
  the playing surface on top.
- **Modern skin (recommended build):** any 20-square linear/ring track printout or print of the
  board; two sets of **7** distinct tokens each (e.g., 7 white + 7 black); **4 binary dice** —
  a 4-sided die (`d4`) with one face marked "1" and the other three "0" per die, OR 4 coins
  (`1`=heads, `0`=tails) as an equivalent binary surrogate. The binary draw is seeded-external
  per L0; the physical surrogate is only a convenience for a human table, never a source of
  LLM-improvised randomness.

## REGIONAL VARIANTS

- **DEFAULT (this pack):** Finkel five-rosette, entry-on-1, seven pieces, single direction, battle
  squares capture.
- **Short/Long route variant (named, `research_status: reconstructed`):** some modern game-school
  restatements give each player a choice or a fixed **short route vs long route** through the two
  shared rosette junctions, differentiating how many squares each side traverses. **Not attested by
  BM 33333**; shipped as a named variant only, never promoted to the default.
- **"Twenty Squares" (Egyptian) variant (`research_status: speculative`):** the same family played
  on the 20-square Egyptian board with local safe-square and throwing-stick differences. Noted for
  lineage, not shipped as default.

## ETHICS / ATTRIBUTION

- **Origin culture:** ancient Mesopotamia (Sumer, Ur, Early Dynastic III; continuing through
  Seleucid Babylonia). This is an Indigenous-to-practice cultural game, not a European export;
  credit and provenance belong to Mesopotamian civilization and its modern scholarly custodians
  (Finkel / BM, Woolley excavations).
- **Sensitivity:** the boards came from **royal tomb contexts**; do not present the game as
  frivolous or trivialize its royal/funerary and later divinatory associations. Distinguish
  attested archaeology (boards, dice, setup) from reconstructed rules (BM 33333 reading) at all
  times.
- **Attribution note for output:** when rules differ between archaeological boards and the
  Seleucid tablet, prefer stating "Finkel's reading of BM 33333" rather than "the rules of Ur",
  which would silently merge a 2400-year gap (c. 2600 BCE boards vs c. 177–76 BCE copy).

## BUILD PROMPT

Render the Royal Game of Ur as a two-player race game on a fixed 20-square ring track per this
delta: both players hold 7 pieces in an off-track starting stock; on your turn, cite and apply the
seeded-external Ur binary tetrahedral roll (4 dice, one marked face each, count of marked = 0..4,
drawn from the L0 seeded table for `game-id[ur]` / mode `ur-binary-tetrahedral` / current
`turn-index` — you never choose the roll). Enter a piece from the stock on an exact roll of 1;
move a piece that many squares forward toward the far terminal; a piece landing on an
opponent-occupied **non-rosette** square captures it (return to its owner's stock); rosette
squares 4, 8, 14 and the two shared crossing squares are `safe` (no capture). Bear off after the
final square only on an exact-matching roll. First to bear off all 7 pieces wins. Before any move,
restate the canonical `^` state string and cite the governing clause (Ur dice mode §Universal RNG
mode 2, capture clause §RULE DELTA, entry-on-1), then emit the new canonical string, then narrate
in prose if at all. Wherever a rule is reconstructed, include the one-line honesty note:
"historians disagree — this build uses Finkel's reading of BM 33333 (five-rosette, entry-on-1)."
Enforce `roll-exact` for entry and bear-off, `CAPTURE: on` at battle squares, `safe` at rosettes.
Score by win/loss only (no partial score unless a pack SCORE rule is added).

---

> **Asset notes (NOT cached prompt body):** skeleton per `SPORE_SEED_20260901.md`; deltas align to
> `race_dice` family sketch #2 (Royal Game of Ur) and L0 historical mode #2. Dice + rules are
> `reconstructed` (Finkel, BM 33333); board/setup/dice objects are `attested`. Cross-refs:
> `L0_universal_contract` (RNG mode 2), `L1_engines/race_dice` (family sketch #2),
> `L2_statics/*ur*`, and the sibling Senet/Patolli packs for the family's shared reconstructed
> school handling.
