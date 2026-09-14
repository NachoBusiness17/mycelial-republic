# L3 — Oware / Mancala Cultural Pack (DRAFT) — `L3_packs/oware.DRAFT.md`

> **Status:** DRAFT. **Engine:** race_dice — **with an explicit boundary exception** (see RULE
> DELTA / BOUNDARY TEST below). **Class:** L3 cultural pack — a delta over the race/dice engine
> *where that delta is honest*, and a labeled refusal where it is not. **Consumption order:**
> L0 contract → L1 race/dice engine → this pack (deltas + boundary exception) → L2 statics →
> this pack's cultural/historical notes. **Research status:** board layout and the modern Oware
> ruleset are `attested` (multi-list variant rules chronicled since the 20th-c. collections;
> playing culture documented across West Africa, esp. Akan-Ashanti Ghana). The **origin/deep
> genealogy** of the mancala family is `reconstructed`/contested and ships as named competing
> schools below; it is never presented as rule fact and never silently upgraded.
>
> ---

## CULTURAL PACK: Oware (Mancala family)

**Variant family:** SOWING engine — *not* race/dice.
**Path in family:** Oware (Akan "Awoɔre") is the leading modern standard of the vast **mancala**
family (mankala/wari/awari: lap-sowing games). It shares a ring-of-pits geometry and seeded-stone
count with the race engine's ring track, but the governing rule is **sowing**, not movement-to-a-
finish. This pack states that difference as the load-bearing boundary result (see RULE DELTA).

## BOUNDARY TEST (required by SPORE_SEED, stated explicitly)

**Mancala/Oware is a SOWING engine, not a race engine, and the seed's race/dice engine cannot
express it as a race.** The reasons are structural (against the race engine's fixed clauses):

1. **No fixed track of ordered squares toward a finish.** The race engine requires a linear/ring
   track with a WIN (bear-off or lap-completion). Oware's pits are a **closed ring of 12+ pits**,
   but there is no finish line and no piece that "completes" it; a seed makes many circuits over
   a game, and pits are re-filled by others' sowing.
2. **Move length is NOT seeded RNG.** The race engine's movement amount comes ONLY from the seeded
   RNG (L0 Universal RNG, LLM never improvises a roll). In Oware the move amount is **player-chosen**:
   the player selects a pit and sows its full stored count. There is no dice, no cast, no external
   randomness. **This is the decisive divergence** — the race engine's RNG mandate cannot be
   fulfilled because the game has no chance engine at all.
3. **Scoring is counting, not bear-off.** WIN = capturing strict majority of the 48 stones (25),
   acquired by the *sowing-capture* rule (last-seed-into-empty-pit-then-take-opposite), with a
   `LOOP`/no-move safety (see HISTORICAL MODULE) — not by pieces leaving a track.
4. **Sowing is a redistribution operator, not a step advance.** ONE move reloads many pits in a
   cascade; the race engine's per-landing SQEFFECT resolution assumes a single destination square
   per roll, which cannot model a multi-pit sowing cascade without distorting the game.

**Honest adaptation.** The following race-engine primitives transfer cleanly and are retained:
the **ring layout** (encode pits as indices `0..(N-1)`, wrap `/N`), the **per-square SQEFFECT
table** (encode the sowing-capture triggers as per-pit effects), the **six-function L0 contract**
(state encoding, legality, transition, terminal, scoring — all well-formed for Oware), the
**seeded-external discipline** (here satisfied negatively: the game is deterministic, so there is
simply *no* RNG draw to improvise; the LLM reports moves as chosen predicates, never fabricates a
roll), and `research_status` flagging. **What does not transfer:** movement-by-RNG, capture-on-
landing in race form, bear-off. Those are refused rather than stretched.

**Counting-capture may be its own engine.** The sowing-capture interaction (last-sown-seed into an
empty pit captures the opponent's opposite seeds) is itself a coherent mechanical kernel — a
candidate `L1` **sowing/capture engine** distinct from race_dice. This pack flags that as a corpus
open item (see ETHICS/cross-refs), rather than shoehorning it into the race engine family.

## RULE DELTA (only what differs from the race/dice engine — and what is refused)

*(Because Oware is not a race game, "delta" here is a mapped subset; un-mappable race clauses are
listed as **refused**, not silently adapted.)*

- **BOARD / TRACK:** ring of **12 pits** (the Akan "Abapa"/2×6 board), indices `0..5` = Player A,
  `6..11` = Player B, wrap `/12` (a pit's "opposite" = `(i+6) mod 12`). Two **stores** (own end-pits,
  not part of the ring). **Retained from engine:** ring layout encoding. **Refused:** any "finish"
  square.
- **MOVEMENT SOURCE:** **none — no RNG.** A turn is the acting player **choosing a pit** that holds
  ≥1 stone on their side and **sowing** it: remove `s` seeds, then drop one seed into each next
  pit in ascending index, wrapping `/12`, for `s` consecutive pits (the chosen pit itself is left
  empty after emptying). **Delta vs engine:** the race engine's "move amount from seeded RNG" is
  **inapplicable and refused**; the L0 rule "LLM never improvises a roll" is satisfied by there
  being no roll at all. The LLM must report the chosen pit as a stated `LEGAL?` predicate (per
  L0 Function 3), never invent a roll.
- **SOWING-CAPTURE (the seed of the sowing engine):** if the *last* sown seed lands in an empty pit
  on the sower's own side AND the opposite pit (`(i+6) mod 12`) holds `2` or `3` stones, the sower
  captures those opposite stones **plus** the just-sown seed, moving them to their store; the chain
  may continue backward through pits whose opposite also holds `2`/`3`. **Refused as race
  `CAPTURE: on`:** the race engine's capture removes *pieces*, not seed-counts, and resolves on
  landing; the sowing-capture resolves on the *last* landing end-of-sow and transfers counts. This
  is a distinct mechanism — encoded here as `SQEFFECT` triggers, not as race capture.
- **ENTRY:** not applicable (no home stock; all stones start on the board, 4 per pit). **Refused**
  any engine `ENTRY` rule.
- **WIN / BEAR-OFF:** **refused as bear-off.** WIN = first player whose **store ≥25** (strict
  majority of the 48 stones), or, if all pits empty at once, the player with the higher store.
  **Refused:** the engine's bear-off/win-on-track-completion (there is no linear exit).
- **BLOCK:** only the no-move case — if a player's entire side is empty, the game is `LOOP`
  (non-terminal) under L0 Function 5 and the opponent has no legal move until stones return;
  once **no legal move exists for either side** (all pits empty), the **remaining stones on the
  board go to the player on whose side they sit**, then scores are compared per WIN. **Refused:**
  race `blocked` squares (there is no piece collision).
- **RESOLUTION ORDER (mapped):** each full move = `LEGAL?` (choose pit) → **sow cascade** (a
  deterministic chain applied pit-by-pit, in index order, wrap `/12`) → **sowing-capture** check at
  final landing → score check → next role. This *replaces* the race engine's single-per-landing
  SQEFFECT order; the SQEFFECT table below still encodes the capture triggers. **Delta vs engine:**
  this is the one genuine engine-loop replacement and is stated as such, not hidden.

### SQEFFECT (per-pit trigger table, mapped into ring indices)

- Each pit `i` doubles as a possible *final landing* of a sow. `SQEFFECT[i]`:
  - if `board[i] == 1` (just-sown seed, pit was empty before finishing) and side(i) == sower
    and `board[(i+6)%12] ∈ {2,3}` → `{ effect: sowing-capture, target: i, param: opposite count }`,
    transferring those stones + the seed to store, then **chain** to pit `i-1` if it also holds
    exactly 2/3 opposite (`board[(i-1+6)%12] ∈ {2,3}` and `board[i-1]` just became non-empty this
    sow) — resolve chain left-to-backward until a non-triggering pit, exactly once.
  - else → `{ effect: none }` (plain landing; seed remains on the board as a new count).
- Stores are **outside the ring** — not SQEFFECT targets; they only receive captured counts.
- **Critical rule:** a player **may not choose a pit whose sow would give the opponent zero legal
  moves next** (the "feeding"/supply rule, Akan Oware standard); `LEGAL?` hard-`false` if the only
  legal board would leave the opponent with no playable pit. **avoids** terminal-by-supply-starvation.

## HISTORICAL MODULE

**Era / culture:** the mancala family (from Arabic *mancala* / *manqala*, "to move"); playing
cultures are attested across Africa, the Arab world, and South/West Asia (rows of pits carved in
temples, e.g. Egyptian temple-floor rows ~1500 BCE and earlier for the broader family; "Alep"
boards in Syria; the two-row *Awoɔre/Oware* standard dominant among the **Akan peoples of southern
Ghana**).

**Oware specifically:** the modern ruleset (12 pits, 48 stones, sowing-capture on 2/3-opposite,
store-majority win of 25) is the **standard competitive form**, codified in the foundational
modern collections/research and played in African championship contexts. The **name** variants —
Awoɔre (Akan), Wari (Mande/sahelian), Awélé (Francophone) — are regional skins over fundamentally
the same sowing kernel.

**Sources / uncertainty** — the deep genealogy is contested; **named competing schools**
(seed rule: contested history ships as named schools, never one invented consensus):

- **African-continuity school:** holds the mancala family, and two-row lap-sowing, as indigenous to
  and oldest-attested in Africa (earliest pit-row boards in African/Afro-Asian archaeological
  contexts). Some maintain a North/East-African homeland with diffusion outward.
- **Asiatic-diffusion school** (older, now minority; e.g., some 19th–20th-c. diffusionist
  writings): argues origins in Sri Lanka/Malaysia/"Old World" diffusion zones, treating African
  forms as later arrivals.
- **Independent-publication school:** notes that independent two-row pit boards appear *without*
  firm priority evidence in multiple regions, so "oldest family" and "single homeland" both remain
  unproven at the family level.

**`research_status`:** the **Oware ruleset** (as standardized) is `attested` — the specific moves,
capture trigger, feeding rule, and win count are documented and reproducible from modern recensions.
The **family origin and diffusion geography** are `reconstructed` (contested, multi-school). This
file never upgrades `reconstructed` to `attested` for the genealogy, and never silently merges the
schools.

**Seed rule note:** "oldest family in the world" (the APPENDIX framing) is a *disputed* claim —
probably *among* the oldest board-game families attested, but no single school has demonstrated a
unique oldest priority. The pack states the dispute rather than endorsing one school.

## MATERIALS MODULE

**Original pieces:** (1) a **board** of carved pits in a wooden/stone platter — the West African
standard **6+6** pits with two larger store-hollows at the ends; (2) **seeds/stones** — the
canonical favor is the **calabash/false-vine seed** (*Caesalpinia bonduc*), also cowries, beans,
pebbles; the classic count is **48 seeds, 4 per pit**. (3) No dice, no sticks, no RNG tools — the
game is deliberately deterministic (a mental-arithmetic forecasting game).

**Modern-skin equivalents:**
- board → any **12-cell ring** drawn on paper or a 2×6 grid wrapped `/12`, with two end stores;
- seeds → counters/beads/tokens, 4 per pit (48 total);
- the **store** → a marked container/zone per player at each end;
- no randomness → **no RNG mode needed**; keep the L0 seeded-external frame but note the roll
  table is empty for Oware (deterministic game), so "LLM never improvises a roll" is honored by
  construction.

## REGIONAL VARIANTS (named deltas)

- **Akan/Oware (Awoɔre, Ghana)** — the 12-pit/48-seed standard above; capture on 2/3-opposite,
  feeding rule enforced, win 25. The reference build.
- **Wari (Mande/sahelian)** — 12 pits commonly; some recensions allow the **free move** (a play that
  lifts the last-seed capture restriction differently) and differ on whether a player may choose a
  pit that leaves the opponent with no move (`LOOP` handling). Named variant, `attested`.
- **Awélé (Francophone, Côte d'Ivoire/adjacent)** — 12 pits; capture often on **2-only** opposite
  (not 2-or-3), tightening scoring; the "feeding" rule variant appears. Named variant, `attested`.
- **Bao (East Africa, Swahili coast)** — a larger 4-row board with a **complex, skill-driven**
  sowing-capture kernel and multiple home/mark concepts; a distinct high-strategy mancala. Included
  to mark the family's breadth; ships in its own future pack rather than being flattened into
  Oware. (`reconstructed`/`speculative` for finer rule details.)

## ETHICS / ATTRIBUTION

**Origin culture:** the mancala family is a pan-African and Afro-Asian family with a deep,
contested genealogy; **Oware specifically** is the Akan (southern Ghana / Ashanti) standard, and
this pack attributes it to that living West-African heritage first. It is *not* presented as a
dice/race game and its mechanical identity as a **skill-driven sowing game with no chance engine**
is respected and foregrounded — an ethical point as well as a mechanical one: flattening Oware
into a race-with-capture would misrepresent a celebrated analytical game.
**Sources honored:** the modern Oware recensions and competitive ruleset (`attested`); African
archaeological/ethnographic record for board presence; the named diffusionist schools are cited and
flagged `reconstructed`, never merged. The "oldest family" claim is shipped as a dispute, per the
corpus rule.
**Sensitivity:** West African game traditions, including the Akan championship culture of Oware,
are living practice. This pack treats them as attributed heritage, names the culture, and refuses
to dilute the deterministic skill core into the race engine's chance framing. No invented
archaeology; all contested priority claims carry `research_status`.
**Corpus note:** the sowing-capture kernel (last-sown-into-empty → take opposite; chain) is flagged
as a **candidate `L1` sowing/capture engine** distinct from race_dice — an open expansion item,
not silently folded into race_dice (see cross-refs).

## PLAYABLE BUILD PROMPT (BUILD PROMPT)

> Build the Akan (Ghana / West Africa) mancala game **Oware** (Awoɔre) as a deterministic sowing
> game, NOT a race or dice game — there is no RNG and no track-to-a-finish; state this in your
> first line. Use the L0 six-function contract and the race engine ONLY where honest: encode the
> board as a **ring of 12 pits** (`0..5` = Player A, `6..11` = Player B, wrap `/12`, opposite pit =
> `(i+6) mod 12`), **48 seeds, 4 per pit**, plus an end **store** per player. On your turn choose any
> pit on your side holding ≥1 seed and **sow**: lift its seeds, drop one into each successive pit
> wrapping `/12`, leaving the chosen pit empty; if the **last** seed lands in an empty pit on your
> side whose **opposite holds 2 or 3 seeds**, capture those seeds plus the sown seed into your store
> and chain backward while the same 2/3 rule continues; you may not play a move that deprives your
> opponent of all legal moves (`LEGAL?` hard-false, feeding rule). Report legality via L0 Function 3
> (cite the pit as a predicate — there is no roll to emit). WIN when your **store reaches 25**
> (majority of 48), or on board-empty by higher store. In your output flag that the **ruleset is
> `attested`** but the family's **origin is contested** — ship the African-continuity and
> Asiatic-diffusion schools as named and marked `reconstructed`, never choose one. For every reply:
> restate the canonical state on the `^` line (game id `oware`, turn-index, active-role, board as
> 12 pit-counts + 2 stores, order, seed-phrase `-` since deterministic, reserved), cite the governing
> L0 function, apply the chosen-sow cascade, resolve the sowing-capture chain, then the new canonical
> state, then narrate. No dice, no cast, no improvised roll — ever.

---

*Corpus cross-refs: parent `L1_engines/race_dice.DRAFT.md` (used only where honestly mappable;
boundary exception documented above); contract `L0_universal_contract.DRAFT.md`; family siblings
`senet.DRAFT.md`, `ur.DRAFT.md`, `patolli.DRAFT.md`, `pachisi.DRAFT.md`, `ludo.DRAFT.md`,
`snakes_ladders.DRAFT.md`; **open item:** proposed `L1_engines/sowing_capture.DRAFT.md` for Oware,
Bao, and the wider mancala family.*
