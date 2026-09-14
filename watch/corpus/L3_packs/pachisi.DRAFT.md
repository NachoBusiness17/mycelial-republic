# Cultural Pack: Pachisi / Chaupar (Mughal India) — `L3_packs/pachisi.DRAFT.md`

> **Status:** DRAFT. **Engine:** race_dice. **Consumption order:** L0 contract → L1 race/dice
> engine → this pack (deltas) → L2 statics → L3 cultural module.
> **Research status (game):** `attested` — cross-and-lap movement, cowrie/casting movement,
> capture-on-landing, four-arm cross board are documented in period accounts and modern
> cross-cultural practice. Contested origin-schools are named below, not resolved here.

---

## ENGINE: race_dice

This pack is a **delta** over the L1 race/dice engine and the L0 Universal Contract. It does not
restate engine mechanics; it supplies everything the engine leaves per-game. Where this pack and
the engine conflict on a non-structural clause, **this pack wins**; engine clauses that are
structural (track shape, capture order, bear-off machinery) may not be overridden by this pack.

## RULE DELTA (only what differs from the engine)

- **Track shape:** four-arm **cross**, which the engine encodes as a **lap ring**. Each player has
  a home arm (a "run") of squares leading to a shared central hub. Movement is clockwise up the
  player's own arm, through the hub, around the outer ring, back down toward the center. Pieces lap
  until turn-in (see WIN). Encode as linear indices `0..N-1` on a ring with the hub at an agreed
  index (pack constant `HUB`), laps tracked per piece.
- **ENTRY (home stock):** each player owns normally 4 pieces in a home stock (the cross's central
  court / outside the board). A piece may leave stock onto the player's start square only on a
  qualifying roll (cowrie count). Qualifying rolls are pack constants: on a ring-encoding where
  the qualifying cowrie value is `Q`, an ENTRY attempt spends that roll to place one stock piece at
  the start square. (Standard schools use cowrie-count-of-1 as the common entry roll; see dice.)
- **CAPTURE: on.** A piece landing on a non-safe square occupied by a single opponent piece removes
  that opponent piece and returns it to that opponent's home stock (per engine). 
- **Safe squares:** `safe`/ritual squares where capture is forbidden. Pack-supplied `SQEFFECT` marks
  the **hub (central square)** and each player's **home start square** as `safe` — no capture there.
  All other squares are capturable.
- **Blocking:** off by default (concurrent squares outside safe/capture rules), unless a variant
  in REGIONAL VARIANTS defines a two-piece block.
- **Dice / movement source:** **cowrie shells** per L0 historical mode **cowries**. *N* cowrie
  shells, open/closed count. **School A (count-only):** move = number of shells showing
  toothed-up. **School B (double-all-open):** move = double when all N show the same open face.
  The L0 cowrie mode supplies the special all-same double-count **per pack** — this pack declares
  which school's arithmetic the build uses, never both at once.
- **Six-function delta:** THE standard Pachisi counts are such that per-turn cowrie counts on the
  six-function transition arrive seeded-external (never improvised). A turn may chain moves while
  a qualifying landed square grants a reroll (see SQEFFECT), resolved by FIFO on the seeded table.
- **WIN / bear-off:** a piece must complete the fixed number of laps (pack constant `LAPS`) and
  reach the hub/finish. Once a piece is on its final run, `roll-exact` bear-off: an exact qualifying
  cowrie count exits it to the finish. **WIN when all 4 of one player's pieces have turned in.**

### SQEFFECT (per landing, engine fixed order)

| square | effect | target | param |
|---|---|---|---|
| `HUB` (central court) | `safe` | self | — |
| each home start square | `safe` | self | — |
| (variant-only squares) | per REGIONAL VARIANTS | — | — |

Default: every non-safe square is `none` (no effect) unless a named variant adds effectors.

## HISTORICAL MODULE

- **Era / culture:** Indian subcontinent; the cross-and-cowrie race family is attested in textual
  and material record from the Gupta-era — **origin contested, two named schools**:
  - **School G (Gupta-origin):** places the cross-board/cowrie family in early Gupta-period
    practice, seen as Pan-Indian ancestor of later Chaupar/Pachisi forms (`reconstructed`; based on
    iconographic/textual retrojection).
  - **School M (medieval-clearing / Mughal-etiquette):** holds that the *specific* four-arm-cross
    board with a central court, as the Mughal court knew it, is a medieval crystallisation, not a
    continuous Gupta survival (`reconstructed`; older material may differ in board count/rule).
  Both rest on imperfect surfaces; **this pack ships the Mughal-period form** (the named
  `Chaupar/Pachisi` at Akbar's court), flagged where reconstructive.
- **Fatehpur Sikri courtyard module:** the Mughal court played on a **full-scale courtyard board**
  at Fatehpur Sikri, with **living pieces (courtiers/slaves) as markers** and, in some accounts,
  cowrie/bean throws from a central point. This is a **play-surface / spectacle module**, not a
  rules change: encode the same four-arm cross at courtyard scale. Dice remain real cowries (seeded
  externally), never improvised by the LLM — even with many live pieces. `research_status:
  attested` for the *practice of courtyard board play* (period accounts); `reconstructed` for the
  *precise live-piece movement protocol* (no unambiguous rule text survives).
- **Sources:** period travel/account literature; Mughal palace-economy accounts (Akbarnama-era
  descriptions of court gaming); modern ethnography of village Pachisi/Chaupar. All flag-bearing.
- **Uncertainty:** exact cowrie count (6 shells common; other counts per region), entry-qualifying
  value, and lap count vary across schools — shipped as pack constants, flagged, not "historically
  fixed".

## MATERIALS MODULE

| original | modern-skin equivalent |
|---|---|
| Cowrie shells (open/toothed-up counting) | ~6 marked coins/tokens each showing an "open" face |
| White/ivory-paste pau-sized pieces, 4 per player | 4 disks/pegs per player (Modern Ludo pieces reskin cleanly) |
| Cloth/court yard with painted four-arm cross | drawn board / page grid, 4 arms + central court |
| (courtyard module) living pieces/courtiers | tall markers or tokens, one per encoded piece |

Historical-mode RNG: **cowries** (per L0), seeded-external, if using the "live pieces" module the
throw is still the reported drive, never authorial flourish.

## REGIONAL VARIANTS (named deltas)

1. **Chaupar (four-player cross)** — same cross/capture/safe shape; typically 4 players in two
   partnerships; dice often cowries or long dice; `research_status: attested` (modern practice) /
   `reconstructed` early records. May define a **two-piece block** on a partner's square.
2. **Pachisi-as-race-to-center** — the common village swing toward all-out footrace across the
   four arms; may relax exact bear-off to `land-exact`. `research_status: attested` (modern).
3. **In-board entry variant** — pieces all start on the outer ring at fixed spots rather than a
   home stock; ENTRY rule becomes a placement clause not a qualifying-roll. `reconstructed`;
   some colonial-era descriptions.
4. **Double-open-cowrie school (School B)** — all-same open face doubles the count. `attested`
   as a live regional arithmetic in modern reports.

Only one variant's conflicting deltas apply at a time; the pack declares the active variant in the
build prompt.

## ETHICS / ATTRIBUTION

- **Origin culture:** India (South Asian subcontinent); the Mughal-era Chaupar/Pachisi form is a
  courtly South Asian game later diffused (Ludo is a 19th-century UK commercial reskin of the same
  cross — see engine family delta).
- **Attribution:** the four-arm-cross/capture/entry mechanics and cowrie movement trace to South
  Asian practice; do not re-attribute to later commercial reskins. Cite origin school/Sources when
  shipping the courtyard or rule-scholarly claims.
- **Sensitivity:** the **Fatehpur Sikri living-piece module** involved coerced servants as markers
  within a court spectacle. A build MAY use proxy markers (tokens). It must not romance or invite
  role-play of coerced participation; if live-piece spectacle is simulated, present it as a
  historical-mode note, not as endorsement, and default to proxy tokens.
- **Known unknowns:** cowrie count, qualifying entry value, lap/hub rules differ across schools —
  ship constants as flags, never as universal history.

## BUILD PROMPT

> Build the playable race game Pachisi / Chaupar (Mughal India) on the race/dice engine and the
> L0 six-function contract. Track: a four-arm cross encoded as a lap ring with a central court
> (`HUB`, a `safe` non-capturable square) and each player's home start square also `safe`;
> entry is the qualifying cowrie roll `Q` placing one stock piece at the start. CAPTURE: on —
> landing on a non-safe single opponent piece returns it to that opponent's stock; no other
> blocking. Dice: **cowrie mode** per L0 (this build uses School A count = shells open, resolved
> seeded-externally, never improvised); a landed piece reaching a reroll-capable square chains its
> next draw from the seeded table. WIN: all 4 of one player's pieces complete `LAPS` laps and bear
> off `roll-exact` at the hub. Ship the Fatehpur Sikri courtyard module as a scale note with
> **proxy tokens** for pieces (no coerced-lived-piece role-play), and include the named contest:
> flag origin-sahip schools Gupta-origin vs medieval-clearing as `reconstructed`, state which the
> build follows, and honour every `reconstructed`/`speculative` rule with a one-line honesty note
> before applying it. Emit canonical `^` state first, cite the L0 clause/RNG mode, then narrate.

---

(Static-first: shareable prefix is the engine + L0; this pack is the appended variant content.)
