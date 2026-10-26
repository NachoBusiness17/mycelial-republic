# L2 - Hanafuda Game Pack (DRAFT) - `L2_games/hanafuda.DRAFT.md`

> **Status:** DRAFT. **Class:** L2 game statics - card information-set matching engine (koi-koi flagship ruleset). **Research status:** lineage attested except the late-18th-century origin anchor (unverified); dating and legalization caveats carried as honest; yaku values, point targets, and typical deal sizes are house-rule parameterized (honest caveat in SLOT 5).

---

## SLOT 1 - TOPOLOGY
`TOPOLOGY` = 6-zone card graph, no spatial grid: hidden hand H1, hidden hand H2, shared face-up field F, public capture piles P1/P2, hidden draw stack D. 48 cards total. "Neighbor" = month-equality match between a played card and field cards (not spatial adjacency). Motion edges: H* -> F (play); F -> P* on match (capture) or F -> F (stay); D -> F (draw flip, same match rule).

## SLOT 2 - DOMAIN
`DOMAIN` = 48 distinct cards, 12 months x 4 cards each; each card is (month 1-12, category in {bright (hikari), tane (animal/object), ribbon (tanzaku), plain (kasu)}). Brights total 5 (canon names them in deck order: pine crane, cherry curtain, moon, willow rain-man, paulownia phoenix); sake cup is the month 9 tane with a yaku-enabler dual role; the rain-man bright is often excluded from bright yaku. Hidden values (opponent hand, draw order) use `_`.

## SLOT 3 - CLAUSES
1. Month-partition: exactly 4 cards per month across all zones (engine clause-1 analog: all-different card identity within the finite 48-deck).
2. Match-capture: a played card captures exactly one same-month field card (player picks among multiple matches; some variants take all) or stays on the field.
3. Turn-pair: one turn = one hand play + one draw flip, each resolved by clause 2.
4. Yaku set-membership: scoring shapes over captured piles. Representative table: 3 brights = 5 pts, 4 = 8, 5 = 10; 5 tane = 1 pt; 5 ribbons = 1 pt; 10 kasu = 1 pt; +1 per extra (values vary by house rule - honest).
5. Koi-koi branch: on forming a yaku exactly one of {stop, continue}; continue risks forfeiture if the opponent scores first.

## SLOT 4 - INSTANCE
Canonical 2-player koi-koi deal, 48 tokens (token = month digit `1-9,A,B,C` + copy index `1-4`; zones H1 | F | H2 | D, arities 8/8/8/24 per the canon's typical values):
```
11 32 51 71 81 92 B3 C1 | 12 21 41 61 82 A1 A2 C2 | 22 33 42 52 62 91 B1 A3 | 13 14 23 24 31 34 43 44 53 54 63 64 72 73 74 83 84 93 94 A4 B2 B4 C3 C4
```
Actor-perspective transform (P1 seat; opponent hand and draw order become `_`, the house `_`-for-hidden analog of the sudoku dots transform):
```
11 32 51 71 81 92 B3 C1 | 12 21 41 61 82 A1 A2 C2 | _ _ _ _ _ _ _ _ | _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
```
The initial field holds at most 2 of any month, so the canon redeal trigger (3 of one month on the initial field) does not fire.

## SLOT 5 - VERIFIER
Parse -> verify month partition (48 distinct tokens, exactly 4 per month, copy indices {1,2,3,4} per month), deal arities 8/8/8/24, initial-field redeal check. Replay legality: every played or drawn card resolves to 0 or 1+ same-month field cards; capture removes the chosen match or the card stays. Yaku detection over captured piles per the representative table, house-rule flags on. No `solve-count == 1` requirement: imperfect information admits no unique solution, so the verifier asserts replay-consistency and yaku-availability at each stop decision instead. Technique ladder: month-depletion census -> forced single-match captures -> yaku-shape reachability from remaining months -> koi-koi option pricing (forfeit risk vs upside) -> hand inference from opponent captures. Honesty note: yaku values, point targets, and deal sizes vary by house rule.

### LINEAGE MODULE
- c.1543 - Portuguese contact introduces Western playing cards to Japan - attested (standard historiography; exact year approximate).
- 16th-17th c. - Japanese adaptation begins; early tensho karuta and related decks appear - honest (attested class, precise dating debated).
- 1633 onward - Tokugawa shogunate issues repeated gambling/card bans; hanafuda precursors are caught - attested (edicts documented; enforcement and scope varied).
- Late 18th c. - the 48-card, 12-month deck takes recognizable form; Kyoto/Osaka designer attribution - unverified (traditional origin story, not firmly documented).
- 1889 - Nintendo Koppai founded in Kyoto by Fusajiro Yamauchi as a hanafuda maker - attested.
- Meiji era (late 19th c.) - play spreads widely, including as a gambling game - honest (the legalization framing is debated; enforcement was inconsistent rather than a clean repeal).
- 20th c. - spread via Japanese diaspora; regional variants diverge (Hawaiian, Korean hwatu) - attested.
- Modern - koi-koi is the flagship international ruleset; Nintendo still sells hanafuda decks - attested.

### FLEET CROSSMAP
This game IS the card information-set matching organ. Family anchor per the rubric digest (mahjong row, `engines_tile_card_constraint.md` CELL G/engine/tile/matching_law): the tri-state ledger SUPPORTED/DISPUTED/UNPROVEN is the hand verdict per claim; discarded DISPUTED tiles go face-up to the shared pond; you grade the set a tile can join, never the tile alone. Hanafuda's extension beyond the digest row: the matching runs under imperfect information. The hidden hand and hidden draw order are claims whose evidence state you cannot fully see; the month-depletion census is the ledger's running tally of which claim-months are exhausted; and the koi-koi stop-or-continue call is the bank-or-extend decision - bank the yaku now (ship the verified artifact) or call koi-koi and extend, forfeiting if the opponent lands a scoring shape first (a sibling lane lands contradictory evidence first). Combo yaku such as boar-deer-butterfly (inoshikacho) are multi-claim unions: no single card scores, the shape does.

### CACHE-BOUNDARY NOTE
Swaps the clause family (all-different -> month-partition + match-capture + turn-pair + yaku-set + koi-koi branch) and the instance grammar (81-char grid -> 48-token zone deal). The dynamic layer is NOT unchanged: hands and field are static-visible, but draw order is runtime-only and cache-dark by design - a redeal reseeds it and no static prefix precomputes it.

### BUILD PROMPT
`{topology:6-zone-card-graph, domain:48-cards-12x4, clauses:month-partition+match-capture+turn-pair+yaku-set+koi-koi-branch, instance:<48-token-deal>, verifier:partition+arity+replay+yaku-detect}`

---

research_status: honest
