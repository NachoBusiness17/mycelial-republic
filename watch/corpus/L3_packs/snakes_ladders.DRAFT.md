# CULTURAL PACK: Snakes & Ladders (Gyan Chaupar → British commercialization)
ENGINE: race_dice

> **Status:** DRAFT. **Consumption order:** L0 contract → L1 race_dice engine → this pack (deltas)
> → L2 statics → L3 cultural pack appendix. This file is the L3 append-delta for this game ONLY;
> it does not restate the engine. Always read this as a delta over `L1_engines/race_dice.DRAFT.md`.
>
> [PROMPT-BODY-START — byte-stable from here]

## RULE DELTA (only what differs from the engine)

- **Track:** `linear` N = 100 squares, `ranked [0..99]`, index 0 start, index 99 the final square.
  No lapping. No stock off-board; all pieces enter at index 0.
- **Movement source:** single `1d6` modern mode (per L0 Universal RNG; seeded-external only).
  **`ENTRY`:** a piece enters from index 0 and moves on its turn; no qualifying roll needed for
  entry (unlike Ludo's entry-on-6).
- **Strict linear movement:** destination = `min(current + roll, 99)`. Overshoot on the final roll
  clamps with `land-exact` to index 99 → WIN.
- **`CAPTURE: off`** — no piece interaction by construction. Squares are always concurrent.
  There is no `block` rule; no piece is ever removed or sent back by another piece.
- **`SQEFFECT[square-id]`** — the moral-topology map. This REPLACES any capture mechanic with a
  virtue/vice ladder-and-chute table:
  - **ladder** square (virtue) → `jump` UP a specified square-id (advance toward 99).
  - **snake/chute** square (vice) → `jump` DOWN to a specified square-id (retreat).
  - All other squares → `none`.
  - Source squares of a jump land at the target square, then any effect AT the target is applied
    (standard engine rule 1–6 ordering: `jump` resolves before a second landing check).
  - The canonical 1892 arrangement (V&A-marketed English board): ladders at
    1→38, 4→14, 9→31, 21→42, 28→84, 36→44, 51→67, 71→91, 80→100;
    chutes/snakes at 16→6, 47→26, 49→11, 56→53, 62→19, 64→60, 87→24, 93→73, 95→75, 98→78.
    These exact bindings are pack-suggested and swappable; the topology (virtue=virtue-upleap /
    vice=vice-downfall) is the load-bearing cultural content, not the specific pairings.
- **WIN:** FIRST piece to `land-exact` on index 99 bears off and wins (single-piece race — the
  "all pieces born off" default is overridden to *one* winning piece, per the single-token
  ancestor Gyan Chaupar tradition).

## HISTORICAL MODULE — colonial commercialization of an Indian moral-race

- **Origin culture:** the Indian jñāna-chauper / gyan-chaupar (game of knowledge), a South Asian
  dice-and-ladder moral board played since at least the Mughal era (16th–17th c. attested; Jain &
  Hindu pedagogical boards with the same 100-square virtue/vice ladder-chute topology).
  **research_status: attested** (18th–19th c. painted boards survive; period references).
- **The contested-history engine (named schools, no single origin claim):**
  - **School A — "Indian transmission" (mainstream attested):** the British colonial presence in
    India (esp. late-18th/19th c.) transmitted gyan-chaupar to Britain, where it was reskinned as
    the morally didactic "Snakes and Ladders." **research_status: attested** for the game existing
    in both cultures; **reconstructed** for the exact transmission pathway and timing.
  - **School B — "separate/parallel" (minority):** argues the chutes-and-ladders motif could arise
    independently as a generic ascent-descent moral trope; treats the Indian → British link as
    plausible but unproven for every printed instance. **research_status: speculative.**
  - **Verdict this build uses:** *historians disagree on the precise route and date; this build
    uses the attested fact of a post-Indian-moral-board British "Snakes and Ladders" that strips
    virtue/vice capture by design.* Flag remains `reconstructed` for the transmission pathway.
- **1892 commercialization event:** the game was commercially introduced to the English market in
  the Victorian period, most famously under a moral teaching title. Rebranded boards neutralized
  the explicit karmic/virtue framing into generic ladder/chute mechanics while keeping the moral
  ascent-ascent metaphor in marketing. **research_status: attested** (published Victorian boards),
  with the precise year/patent history `reconstructed`.
- **Cultural note:** the "capture stripped by design" line in the L1 engine sketch is the corpus
  taxonomist's framing; mechanically Snakes & Ladders is a non-interactive race, and that
  one-player-vs-board purity is exactly what survived the commercial reskin.

## MATERIALS MODULE

- **Original:** paper/painted 100-square board (often with mantra/verse squares), two small dice
  (or cowries in early/Indian play), counters per player. Gyan-chaupar boards could be large
  cloth or paper sheets with verse labels; British boards shrank to card/tabloid stock.
- **Modern-skin equivalents:** any printed or digital 10×10 grid (index 0..99), one standard
  `1d6`, one token per player. The board is the only required physical object; tokens may be any
  pawn/button. The dice count may be two-dice cumulatively, but the pack enforces a single
  seeded `1d6` per the L0 protocol for determinism.

## REGIONAL VARIANTS

1. **Gyan-chaupar (India, c.16th–19th c.)** — 72 or 100 squares, verse-labeled; dice/cowries;
  virtue/vice squares mapped to karma paths (moksha ascent). **attested** (surviving painted
  boards).
2. **Moksha Patam / Paramapada Sopanam (South India)** — same moral-race genre, regional board
  and verse traditions. **attested.**
3. **English "Snakes and Ladders" (Victorian, specifically the 1892 commercial form)** —
  100-square, moral-slogan squares replaced by plain numbered squares; chutes/ladders only.
  **attested** for the form, `reconstructed` for the exact royal/commercial lineage.
4. **"Chutes and Ladders" (America, 20th c.)** — Hasbro-family modern reskin; same mechanics,
  sanitized theme, corporate IP. **attested.**

## ETHICS/ATTRIBUTION

- **Origin culture:** India (South Asian gyan-chaupar tradition). Any rendition must credit the
  Indian moral-race ancestry; the "invented by Victorian board-maker" framing alone is a
  commercialized retelling and must not be sold as the whole story.
- **Sources (named):** painted/colonial-era Indian boards; Victorian published Snakes &amp;
  Ladders editions (public-domain or archive-held); board-game-history secondary literature.
  Keep statuses honest: the Indian pedigree is `attested`; the British 1892 transmission path is
  `reconstructed`.
- **Sensitivity:** the virtue/vice content encodes religious (Jain/Hindu) moral pedagogy from the
  source culture. Modern reskins should treat it as cultural history, not as an endorsement or a
  neutral universal schematic; note the religious origin rather than strip it to a curiosity.

## BUILD PROMPT

Build a playable, deterministic single-player-vs-board Snakes &amp; Ladders, mechanically a delta
over the shared race/dice engine (L0 six-function contract + L1 race_dice family mechanics), NOT a
from-scratch rules set. Encode a `linear` 100-square track as `ranked [0..99]` with a flat state
string per the L0 canonical grammar, one token starting at index 0. Movement comes ONLY from the
seeded external RNG — a single modern `1d6` resolved against the seeded table, never improvised;
overshoot on the final square clamps `land-exact` to index 99. There is NO capture and NO blocking:
squares are always concurrent, and the per-square effect table is strictly a virtue/vice topology —
ladder squares `jump` the token UP (use the pack-suggested bindings, e.g. 1→38, 4→14, 9→31,
21→42, 28→84, 36→44, 51→67, 71→91, 80→100) and chute/snake squares `jump` it DOWN (16→6, 47→26,
49→11, 56→53, 62→19, 64→60, 87→24, 93→73, 95→75, 98→78), each jump applied once per landing then
checked again at the target. The first token whose final roll lands exactly on square 99 wins; all
other reachable outcomes are `LOOP` until that terminal condition. Every reply begins with the
`^`-flagged canonical state, cites the governing clause (RNG mode / effect rule), and applies the
five L0 output rules verbatim. When presenting the game, credit the Indian gyan-chaupar origin
culture and flag the Victorian 1892 commercialization history as `reconstructed` for the
transmission pathway — do not silently claim a single British invention origin.

[PROMPT-BODY-END]

---

## Asset notes (NOT cached prompt body)

- **Target size:** pack body ~700 tokens (within the 100–800 family pack budget).
- **Status of this pack:** RULE DELTA mechanics `attested`; HISTORICAL transmission pathway
  `reconstructed` (two-school: Indian-transmission attested-for-existence / parallel-origin
  speculative); 1892 commercialization event `attested` for the Victorian form with the precise
  year/patent `reconstructed`.
- **Variant inheritance:** Gyan Chaupar → Snakes &amp; Ladders (India → Britain 1892), the
  moral-race / virtue-vice topology replacing capture-on-landing; dice seeded-external single
  `1d6`.
- Cross-refs: parent `L0_universal_contract.DRAFT.md`, `L1_engines/race_dice.DRAFT.md`; downstream
  `L2_games/*`; honor `00_PRIMER.md` §8 open questions.
