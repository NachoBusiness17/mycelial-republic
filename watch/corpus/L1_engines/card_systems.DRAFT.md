# L1 — Card-Systems Engine (DRAFT) — `L1_engines/card_systems.DRAFT.md`

> **Status:** DRAFT. **Class:** L1 family engine — one mechanical spec shared by the **card family**:
> trick-taking, plain-trick, hanafuda (Koi-Koi) set-collection, and dominoes-as-card-decks. It is a
> **sibling** of race/dice and sowing/capture: same L0 six-function contract, a different core
> operator (a **trick resolution** and a **set/yaku collection** rather than a move-on-a-track or a
> sow-cascade), and it carries the **shared-machinery bridges** that tile (Mahjong) and card games
> borrow from one another. **Provenance:** primer §7 build-order (#4 engines), Fact 7 taxonomy, primer
> §SHARED-MACHINERY (line ~91: "Tile engine → dominoes and Mahjong share inventory machinery"). The
> yaku set-collection block is the primer's **shared-machinery finding** (hanafuda's scoring is
> Mahjong's yaku machinery). **Research status:** standard trick-taking (hearts/euchre shapes)
> `attested`; hanafuda Koi-Koi rules `attested` (modern Kodomo-no-hi / Nintendo formulations;
> Murayama-reconstructed floor); dominoes block/draw `attested`; mahjong-card hybrids `speculative`.
> Flags per pack, never silently upgraded. **Consumption order:** L0 contract → this engine (family
> mechanics) → one card/tile pack (deltas) → L2 statics → L3 cultural pack.
>
> ---

[PROMPT-BODY-START — byte-stable from here]

## CARD-SYSTEMS ENGINE — FAMILY MECHANICS

A **card game** is a **deck of discrete units** dealt into hidden **hands** and public/floating
**table** zones, resolved through one or both of two core operators: the **TRICK** (players play a
card per round; a winner predicate decides the trick-taker and next lead) and the **SET/COLLECTION**
(players accumulate cards into groups that score as **yaku**). You apply these mechanics exactly as
written, plus the pack deltas, never anything else. RNG enters ONLY through a **seeded shuffle** at
deal (L0 Universal RNG); after the deal the deck is fully determined — no roll/draw is ever
improvised mid-game.

### RNG-CONSERVING (seeded shuffle once at deal)

There is a single RNG moment: the **shuffle** producing the deal order. The L0 Universal RNG protocol
applies here in the **conserving** sense — the LLM never invents a card, a draw, or a future hand.
Once dealt, every remaining card and the deck order are deterministic from the seeded
`seed-phrase`. A "draw" from an ordered stock follows that order; the LLM reports the top card, it
never chooses it. `seed-phrase` is a showable run-seed, not a selection device.

### STATE (deck schema, hands, table, tricks)

- **Deck schema (pack-defined):** a collection of **units**; each unit carries a **name**
  (canonical id, e.g. `A♠`, `一月`, `6-6`) and **attributes** by which it is grouped: `suit`/`rank`
  (trick-taking), `month+type` (hanafuda), `[pip1,pip2]` pair (dominoes). The pack enumerates the
  full deck explicitly (52, 48, 28, …) — no unit outside the pack's deck may arise.
- **Deal zones:**
  - **stock/deck** — face-down ordered remainder, draw order fixed by the seeded deal.
  - **hands** — per-player private holdings, encoded as ordered lists of unit-ids.
  - **table/pool** — public/floating units (hanafuda's played flowers; a domino layout; a discard
    river), encoded each as its own list keyed by zone-name.
  - **trick (active)** — the current led row and the cards played to it, in play order, plus the
    `leader-role` and `suit-led`.
- **Canonical string** (L0 F1): `<id>:<hash>:<turn-index>:<active-role>:<deck-schema>|<hands>|<table>:
  <trick>:<order>:<seed-phrase>:<reserved>`. The `deck` field is the inventory authority — hand,
  table, and trick contents must always sum-back to the pack's deck with no leftover and no double
  (L0 inventory verifier).

### DECK-INVENTORY INVARIANT (the deck-balance guard)

At every point, the multiset union of **all deal zones** (stock + every hand + every table zone +
the active trick) must equal exactly the pack's full deck. Any discrepancy is a hard violation: stop,
re-encode from the previous canonical string, never silently "lose" or "invent" a unit. This is the
L0 Fact-5 verifier for cards: the LLM reports holdings; inventory is checked deterministically.

### INITIAL (seeded shuffle and deal)

- **DEAL:** the pack defines (a) full deck enumeration, (b) deal **shape** — count of cards to each
  hand, stock drawn-face-up table rows, and initial leader, and (c) any seed exemptions (e.g., dealer
  peeks one). Resolve deal order strictly from the seeded RNG; the deal is deterministic and
  reproducible given `<game-id> + <seed-phrase>`.
- Representation must stay **canonical across runs**: same seed ⇒ same hands, same stock, same
  physical first drawn card, byte-identical canonical string.

### LEGALITY (playable forms, must-follow-suit, hand constraints)

`LEGAL?(state, T) -> Bool { legal, reason }` (L0 F3), where `T = (role, play | collect)`.

1. **Own turn & own zone:** `role` is the `active-role`; the unit told to move is in that player's
   hand (or, if a table-zone play, is the pack's allowed pick from that player's available pool).
2. **Must-follow-suit flag:** `FOLLOW_SUIT: on | off`. When **on**, if the leader's led suit is held
   in hand, the player MUST play that suit; only absent a holding may they slough any card. When
   **off**, any eligible card is playable (pack may still forbid winners — e.g. hearts-shape may
   forbid leading a heart before break).
3. **Hand-constraints:** no play may take a unit the pack declares unmovable (a point-card a player
   may not lead in a phase; a first-trick prohibition; a void-must-play-winner rule).
4. **Collection form:** for set/yaku play (`T.collect`), the picked units must form a pack-defined
   capture/set pattern (hanafuda match; domino match) and be available on the candidate zones.
5. A `false` on role/order, an off-zone unit, or a must-follow violation is a hard `false`; ambiguity
   → hard `false`. The LLM reports the play as a predicate — `LEGAL?(s, play p)` — and never invents
   a future card.

### TRANSITION (play-to-trick → trick-winner → next-lead; and collect-resolution)

`APPLY(state, T) -> state'` (L0 F4). Two operator tracks; a pack uses one or both.

**TRICK track** (trick-taking games):
1. **Lead:** the `leader-role` plays a card, fixing `suit-led` (and, if the pack carries one, the
   **trump slot** — see TRICK-TAKING KERNEL).
2. **Follow:** each other role in turn-order plays under LEGALITY; a `FOLLOW_SUIT:on` ruling applies
   per player at their moment.
3. **Winner predicate:** the **TRICK-TAKING KERNEL** below resolves the trick-taker from the played
   cards (`suit-led` matching, then rank; trump overrides non-trump).
4. **Collect trick:** the winner takes the played cards (face-down as `won-cards` hoard in
   scoring-relevant forms such as hearts; or table-points) — pack keyed.
5. **Advance:** `turn-index += 1`, recompute `state-hash`, set `active-role` = trick-winner as the
   **next leader**, reprint canonical string, then narrate.

**COLLECT track** (set/yaku games, e.g. hanafuda/hybrids):
1. **Pick:** the `active-role` selects the pack's allowed collect form from their hand against the
   table/pool.
2. **Match & capture:** exchange units per pack — canonic hanafuda form: a hand card's month matches
   the table card's month → both go to the taker's `captured` pile (face-up, scored).
3. **Draw:** replenish the hand from the seeded stock face-up to a table row per pack (`hand-size`
   upkeep) — never an improvised draw, the top-of-stock order only.
4. **Advance** as trick-track §5 unless a **bonus turn** / `ko`-continuation flag holds the role.

### TERMINAL (hands empty / stock exhausted / score target)

`TERMINAL?(state) -> Bool { terminal, winner, score }` (L0 F5):

- **Trick games:** terminal when the deal's tricks are exhausted (hands empty), or when a pack score
  target is reached mid-play (e.g. hearts penalty cap). Remaining hoards score per pack.
- **Set/yaku games:** terminal when the **stock is empty** and the final capture resolves, or when a
  pack target (a **koi-koi stop** / a yaku-threshold) is declared. The stopped player's current score
  is banked; continuation under a koi-koi flag is a pack clause, not an engine override.
- **LOOP guard (L0 F5):** a repeated reversible state reports `LOOP` with the prior `state-hash`
  unless the pack defines a pass (e.g., a closed draw-zone). No unit ever "bears off".

### SCORING (trick counts, point-cards, set/yaku)

`SCORE(state) -> Score` (L0 F6). Three scoring shapes, keyed by pack:

1. **Trick-count** — score = won-tricks count, and the pack's point-values summed per trick (e.g.
   hearts: hearts=1 each, queen-of-spades=13).
2. **Point-cards** — a scored subset of the deck carries point weights (hanafuda: the ribbon/getter
   cards); score = sum of a player's captured point-cards.
3. **Set/yaku (YAKU PATTERN BLOCK, below)** — score = sum over matched yaku, an optional `double` /
   multiplier per yaku rank.

### YAKU PATTERN BLOCK (set-collection scoring — SHARED MACHINERY with Mahjong)

> **Shared-machinery finding (primer §SHARED-MACHINERY, Fact-7 taxonomy):** hanafuda's scoring is the
> same **set-collection machinery** as Mahjong's **yaku** — the corpus treats it as ONE kernel reused
> by both families, not two ad-hoc rulesets. A **yaku** is a named, enumerable **pattern** of units a
> player has collected to which the pack assigns an integer **value** and a **double** flag.

- **Pattern check:** a yaku is **made** iff the player's collected/captured set (hanafuda `captured`
  pile; Mahjong concealed/open groups) contains the pack's exact unit-subset for that yaku. The LLM
  checks a candidate yaku against the canonical captured-set only; it never asserts a yaku from an
  incomplete or hallucinated set.
- **Value resolution:** for each made yaku, add its value; then apply the yaku's `double` flag
  (doubling the running total, canonically per-yaku), in pack-defined order.
- **Exclusivity/stacking:** the pack lists which yaku may stack (independent subsets) and which
  exclude one another (a multi-month flower set may absorb a single-month one); unlisted → both may
  score if the unit-subsets are disjoint in units.
- **Round-bank:** scoring under a `koi-koi`-style continuation banks the made-yaku score into the
  ongoing round total; a stop banks and ends. Mahjong packs bank per win and may carry a **dora /
  bonus-tile** multiplier, another yaku-type modifier — same block, pack data.

### TILE-DECK BRIDGE (dominoes as a deck of pairs — SHARED INVENTORY with Mahjong)

> **Shared-machinery finding (primer §SHARED-MACHINERY, line ~91):** the **tile engine** and card
> engine converge — **dominoes are a deck of pairs** (each unit is the pair `[p1,p2]`, pip-valued),
> sharing the **tile-inventory machinery** of Mahjong (a unit is a tile whose identity is fixed and
> one-of-a-kind in the deck, drawn from a finite inventory, and balanced under the DECK-INVENTORY
> INVARIANT). No ledger, no luck-of-draw lookup distinct from cards: a domino draw is a drawn unit
> from a shuffled inventory like any card draw.

- **Unit identity:** a domino `[p1,p2]` is one indivisible unit; whether it is oriented (`[5|3]` ≠
  `[3|5]`) or unordered is a pack flag. The full double-six inventory is the pack's deck enumeration.
- **Draw = deal:** the boneyard is the stock; each player's `hand` is dealt from the seeded shuffle;
  subsequent draws pop the seeded stock order deterministically.
- **Layout:** the table zone holds chains; a match is not capture-based but **topology-based**
  (end-pip equals played half-pip) — the collect form differs from cards, but the *inventory*
  machinery (shuffle, deal, balance check) is shared verbatim. Mahjong's discard/wall zones analog
  here: same fixed unit inventory, same balance invariant.

### TRICK-TAKING KERNEL (follow-suit, trump slot, winner predicate)

The reusable kernel every trick-taking pack implements with pack data only:

- **Follow-suit (engine, `FOLLOW_SUIT` flag):** described in LEGALITY §2.
- **Trump slot (pack data):** the pack may define a **trump** attribute — a suit, a set of ranks, or
  none. `TRUMP: suit-X | rank-set | none`. A card that matches the trump overrides any non-trump
  card in the winner predicate; among two trump cards, the higher rank (or pack's rule) wins.
- **Winner predicate (engine):** given the trick's played cards in order, resolve:
  1. if any trump was played → highest-ranked trump wins;
  2. else → among cards matching `suit-led`, the highest rank wins;
  3. a pack may substitute (e.g., a "poor suit" where the lowest wins, or a no-trump `none`).
  The winner **collects the trick and leads next** (TRANSITION trick-track §3–5).

### OUTPUT (inherited from L0)

Apply the L0 OUTPUT CONTRACT before/after any move: restate canonical state on the `^` line, cite
the governing L0 function + clause + kernel, emit the new canonical string, then narrate. **No card
outside the canonical deal-hands/stock is ever narrated** (RNG-conserving). Play is a chosen
predicate; the drawn/next card is an instance datum reported top-of-stock, never a narrative
flourish. Pack delta **wins** over this engine clause-wise, except structural clauses (deck-schema
integrity, seeded-inventory deal, must-follow/winner-predicate order, yaku block, balance invariant),
which a pack may not override — it may only set exposed flags and constants.

[PROMPT-BODY-END]

---

## Asset notes (NOT cached prompt body)

- **Target size:** 1.2–1.8k tokens of prompt body (above is the byte-stable card engine; each pack
  adds a 1–3-line delta — deck schema, follow-suit/trump data, yaku table — and expands into its own
  `L3_packs/*`).
- **Two-shared-machinery findings (primer lines ~91, §SHARED-MACHINERY):** the **YAKU PATTERN BLOCK**
  (hanafuda = Mahjong yaku machinery) and the **TILE-DECK BRIDGE** (dominoes = deck of pairs, shared
  tube/tile inventory machinery with Mahjong). Both are the primer's reason this file lives as ONE
  card engine rather than three.
- **RNG-conserving is structural:** unlike race_dice (roll per move) but like sowing_capture
  (deterministic), the card engine has exactly ONE RNG event — the seeded shuffle-deal. After deal
  the deck is deterministic; L0 "never improvise a roll/card" holds by construction. This is the
  framing the packs reuse (a domino draw / a stock draw = a drawn unit, not a chosen one).
- **DECK-INVENTORY INVARIANT** operationalizes L0 Fact 5 for cards — the LLM emits instances, the
  verifier balances inventory; a "lost" or "invented" card is a hard stop-and-re-encode (the card
  analog of tile-inventory integrity).

## FAMILY PACK SLOTS (cultural packs that dock on this engine)

- **Hanafuda / Koi-Koi** (`L3_packs/koikoi.DRAFT.md` TBD, **attested**) — the reference set/yaku
  build. Deck = 48 `[month,type]` units (12 months × 4 flowers: plain, ribbon, animal, bright);
  `COLLECT` match-month captures; **YAKU PATTERN BLOCK** carries the 30+ named yaku (five-brights,
  four-brights, viewing–moon, sake-cup, boar-deer-butterfly, etc.) with values and `double` flags;
  koi-koi continuation (continue-or-stop) is the pack's `koi-koi` clause. **attested** (modern
  recensions; fine-point scoring variations across regional rules → pack notes).
- **Dominoes / block & draw** (`L3_packs/dominoes.DRAFT.md` TBD, **attested**) — the **TILE-DECK
  BRIDGE** reference. Double-six deck = 28 unordered `[p1,p2]` units; block = no draw, draw = boneyard
  draw; layout is end-match topology, not capture; play out / block-the-chain terminal; score = pip
  sum of opponent hoards. Draw order strictly top-of-seeded-stock.
- **Trick-taking generic — hearts / euchre shape** (`L3_packs/trickpack.DRAFT.md` TBD, **attested**)
  — the **TRICK-TAKING KERNEL** reference. 52-card `[suit,rank]` deck; hearts: `FOLLOW_SUIT:on`,
  `TRUMP:none`, scoring **point-cards** (hearts=1, Q♠=13), no-tricks-any trick shape + penalty-cap
  terminal, voided lead prohibitions. Euchre-shaped: 24/32-card subset, `TRUMP:suit-X` + `bower`
  rank-defect in the winner predicate — all kernel pack data, no engine change.
- **Mahjong-card hybrids** (`L3_packs/cardmahjong.DRAFT.md` TBD, **speculative**) — playable
  card-tile hybrids (card decks standing in for Mahjong tiles, e.g. three-suit/rank unit decks with
  the **YAKU PATTERN BLOCK** scoring, concealed/open groups, dora multipliers). **speculative** by
  design — an invention slot, not an attested historical game; flagged, never upgraded. Docks on both
  the yaku block and the tile-deck inventory bridge.

---

*Corpus cross-refs: contract `L0_universal_contract.DRAFT.md`; sibling engines
`L1_engines/race_dice.DRAFT.md`, `L1_engines/sowing_capture.DRAFT.md`, sibling
`L1_engines/constraint_puzzle.DRAFT.md` (Mahjong tile machinery); downstream
`L2_games/*`, `L3_packs/koikoi.DRAFT.md`, `L3_packs/dominoes.DRAFT.md`,
`L3_packs/trickpack.DRAFT.md`, `L3_packs/cardmahjong.DRAFT.md` (TBD); shared-machinery source
`00_PRIMER.md` §SHARED-MACHINERY + §9 Source Map (Parlett; Murray; Culin); honor
`00_PRIMER.md` §8 open questions where applicable.*
