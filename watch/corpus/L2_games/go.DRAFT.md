# L2 - Go Static Pack (DRAFT) - `L2_games/go.DRAFT.md`

> **Status:** DRAFT. **Game id:** `go` (row id in `memory/runs/l2_statics_pour_20261020/results.jsonl`, this pour). **Class:** L2 game statics - the TERRITORY slot of the war/capture family engine `L1_engines/board_strategy.DRAFT.md` (TERRITORY BLOCK + go pack slot). **Research status:** rules canon and the lineage chain below are **attested** (source classes named per anchor); the c. 1000 BCE origin window is **honest** (debated, caveat carried); the complexity anchors (Robson 1983, Tromp 2016) are quantitative claims carried from the L1 engine's honesty note with their sources named. Nothing in this pack is fabricated: every date, rule, and estate claim cites the raw ore row, an L1 engine file, or an estate engine file read in this session.

---

## SLOT 1 - TOPOLOGY
`TOPOLOGY` = 19x19 grid of **points** (intersections; stones occupy points, not cells). Neighbor = 4-orthogonal: a **liberty** is an orthogonally adjacent empty point. A **group** is an orthogonally connected set of same-color stones. This is the L1 board/strategy engine's go slot: `19x19` points, liberty capture, ko/super-ko supersede, pass-terminal territory score (`L1_engines/board_strategy.DRAFT.md` go pack slot, TERRITORY BLOCK).

## SLOT 2 - DOMAIN
`DOMAIN` = three-state per point: `_` empty, `B` black, `W` white (`_` carries the house empty-cell convention). Scalar state rides alongside the grid: side to move (`B`/`W`), captured-stone counts per color, ko point (single-point recapture ban), turn indicator. Initial state: empty board, black to move, zero captures, no ko point.

## SLOT 3 - CLAUSES
The sudoku house grammar instantiates one all-different clause three times; go's clause surface is the **liberty family** instead (the pack delta the engine hosts):
- **C1 liberty-capture:** after a placement, any opponent group with zero liberties is captured and removed; then any own group with zero liberties is removed, legal only if the placement captured.
- **C2 no-suicide:** a placement that leaves the mover's own group with zero liberties without capturing is illegal.
- **C3 simple ko (the superseding constraint):** a move may not recreate the immediately prior board position (single-point recapture ban). The L1 engine carries this as the canonical supersede applied last in the transition order (`L1_engines/board_strategy.DRAFT.md` TRANSITION step 5 + TERRITORY BLOCK).
- **C4 two-pass terminal:** two consecutive passes end play; dead stones are removed by agreement, then scored.
- **S5 scoring:** Japanese territory scoring = empty points surrounded by one color plus captured stones (prisoners); komi 6.5 compensates white. Variant: Chinese area scoring (stones plus surrounded empties, komi typically 7.5, suicide rule differs) - changes endgame valuation and seki handling.

## SLOT 4 - INSTANCE
Canonical instance = flat 361-char row-major string over the DOMAIN, read top-left to bottom-right, plus the state suffix `|turn=B|capB=0|capW=0|ko=none`. This pack ships the **empty-board start position** as its canonical instance (the ore's initial state); a live position or a game record is a dynamic-tail instance and this pack fabricates none.

19-line form (each row exactly 19 chars):
```
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
___________________
```
Flat form (361 chars): `_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________`

## SLOT 5 - VERIFIER
Parse the 361-char string + suffix, then deterministic checks (the LLM emits the chosen move; the verifier owns the verdict, per the L1 engine's honesty note):
1. **Shape/alphabet:** length 361, only `_`/`B`/`W`; suffix fields in range.
2. **Clause replay:** step each move through C1-C3 in the engine's transition order (capture resolution, then the ko supersede); in any settled legal position no group may have zero liberties.
3. **Single verdict (go's analogue of sudoku's `solve-count == 1`):** the replay returns exactly one terminal verdict, and only after the C4 two-pass terminal fires; the mover never asserts a winner before the predicate fires.
4. **Score recomputation:** territory = surrounded empty points + prisoners, komi 6.5 to white, under the declared school (S5).

Technique ladder (the reading ladder the verifier assumes): liberty count -> capture reading (one-liberty groups) -> life-and-death reading -> ko-threat counting -> endgame valuation of dame and seki under the declared scoring school.

Honesty notes carried with caveats: komi is empirically tuned, not proven (its fairness is debated; the exact value is a convention, not a theorem). Generalized go on an NxN board is EXPTIME-complete (Robson 1983); the 19x19 game has on the order of 10^170 legal positions (Tromp 2016) - both quantitative anchors carried from `L1_engines/board_strategy.DRAFT.md` SOLVED-GAME HONESTY NOTE.

### LINEAGE MODULE
- c. 1000 BCE, China: earliest plausible origin window - **honest** (carried on later textual tradition and archaeological inference; the "1000 BCE Korea/China" attribution is contested: Chinese origin is the mainstream scholarly position, Korean-origin claims are minority and not archaeologically settled).
- c. 500 BCE - 200 CE, China: go (yi/weiqi) appears in early Chinese texts and tomb material - **attested** (source class: transmitted classical texts and excavated boards/pottery).
- c. 700 - 900 CE, China/Japan: go spreads to Japan via Korea and China - **attested** (source class: Japanese court chronicles and Chinese dynastic records).
- 15th - 16th c., Japan: rule refinements codify ko, scoring, and handicap conventions - **attested** (source class: Edo-period go house records and rule treatises).
- 1600s - 1800s, Japan: the four go houses (Honinbo, Inoue, Yasui, Hayashi) formalize professional play and ranking - **attested** (source class: house archives and game records).
- 1952: H.J.R. Murray, *A History of Board-Games Other Than Chess*, the scholarly synthesis of go's history and rules - **attested** (source class: published monograph).
- 20th - 21st c.: international standardization; Chinese/Japanese/Korean rulebooks diverge on scoring and ko - **attested** (source class: national federation rulebooks).

No `unverified` anchor is carried: every lineage row above rides the raw ore's own citation trail, and no claim beyond it was added.

### FLEET CROSSMAP
One line per family (digest order), with the go row byte-verified this session against `research/gaming_corpus/engines_war_territory.md` and `research/gaming_corpus/engines_tile_card_constraint.md`:
- **war/capture** (chess, shogi, checkers) -> the falsifier economy: every capture is a falsified assumption becoming a law; forced capture = the socratic gate (`engines_war_territory.md` section 1, lines 15-31).
- **territory (GO - this pack's organ)** -> the lightmap's lit/dark attention territory: cached reads and banked corpus are settled (already-paid) territory; unprobed capability renders dark; a vendor wall-change dirties a radius, not the board (`engines_war_territory.md` section 3, lines 47-65).
- **asymmetric war** (tafl) -> the solo agent vs the 50-walker swarm: one king ferries one load-bearing artifact to the board edge while hunters encircle (`engines_war_territory.md` section 4, lines 67-83).
- **card/matching** (mahjong per the digest; hanafuda is the sibling pack named in this pour) -> the tri-state ledger: SUPPORTED/DISPUTED/UNPROVEN is the hand verdict per claim; discarded DISPUTED tiles go face-up to the shared pond, and you grade the set a tile can join, never the tile alone (`engines_tile_card_constraint.md` CELL G/engine/tile/matching_law, lines 30-41).

The organ claim, extended (not copied) from the engine's three go lines onto this pack's ore invariants:
1. **Stones are probes.** Ore invariant: influence outlives the exchange - stones are probes whose value is positional control, not material count, so sacrifice (tesuji) can be correct even when it loses stones. Engine: "a probe is a stone spent to read the board"; free-lane probes spend cheap stones, premium tokens touch judgment only.
2. **Liberties are the life metric = the dirty radius.** Ore invariant: a group's survival is determined by adjacent empty points, not stone count. Engine: re-probe only the dirty radius (Lipschitz bound). A cached read lives while its radius stays clean and dies when the vendor wall-change re-dirties it, exactly as a group dies when its last liberty goes.
3. **Ko = the amendment law.** Ore invariant: ko forbids recreating the prior board state, forcing play elsewhere. Extension (this pack's own, marked as such): the estate's amend-not-rewrite discipline (`AGENTS.md` workflow-gate section - reruns are amendments) is the same shape: you may not recreate the prior state; you must spend a threat elsewhere and move the board forward.
4. **Settle step of the closure loop.** The engine's four-family closure ends "settle (Go territory: the lit region grows on the lightmap)" - go is the organ where won knowledge becomes settled ground, which is why this pack's cache boundary (below) reads as territory.

### CACHE-BOUNDARY NOTE
Static prefix (cached, byte-stable every request): the rules canon (19x19, three-state DOMAIN, C1-C4, S5 scoring with komi 6.5), the technique ladder, the crossmap, and the lineage module. Dynamic tail (never cached): the 361-char position string plus `turn/capB/capW/ko` - the live board is the dirty radius and is re-derived on every replay. In the engine's own idiom: the static prefix is settled territory, the dynamic tail is the probes standing on it (`engines_war_territory.md` section 3).

### BUILD PROMPT
`{topology:19x19-points, domain:_|B|W, clauses:liberty-capture+no-suicide+simple-ko+two-pass, instance:<361-char row-major + turn/capB/capW/ko>, verifier:clause-replay+single-verdict+territory-score}`

Build go on the board/strategy engine's TERRITORY slot: never invent a move; resolve every placement through C1-C3 in the engine's transition order; emit a winner only after the two-pass terminal fires, scored by S5; declare the scoring school (Japanese territory, komi 6.5) up front.

---

research_status: attested
