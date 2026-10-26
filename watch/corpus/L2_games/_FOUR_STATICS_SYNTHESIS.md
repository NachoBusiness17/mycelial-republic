# FOUR STATICS SYNTHESIS - chess, go, tafl, hanafuda - crossmap over the L0 contract

> **Status:** synthesis of the four fresh L2 game statics against the L0 contract crossmap. Written 2026-10-20.
> **Sources read for every claim below:** `watch/corpus/L2_games/chess.DRAFT.md`, `watch/corpus/L2_games/go.DRAFT.md`,
> `watch/corpus/L2_games/tafl.DRAFT.md`, `watch/corpus/L2_games/hanafuda.DRAFT.md`,
> `research/gaming_corpus/l0_contract_crossmap.md` (section 1, the six-function table). The four statics are one pour's
> family rows: the pour ore `memory/runs/l2_statics_pour_20261020/results.jsonl` is named by chess.DRAFT.md:5,
> go.DRAFT.md:3 and tafl.DRAFT.md:39, and hanafuda rides the same pour's family list (hanafuda.DRAFT.md:45).
> Engine files (`engines_war_territory.md`, `engines_tile_card_constraint.md`, `L1_engines/board_strategy.DRAFT.md`)
> are cited only as quoted inside the four packs; this synthesis asserts nothing about an engine file beyond what a
> pack carries (`watch/corpus/L1_engines/board_strategy.DRAFT.md` and the two `research/gaming_corpus/engines_*.md`
> files existence-checked on disk this session). **Consumer:** the L2_games build lane (each pack's BUILD PROMPT) reads this for slot placement and
> organ claims. **Verifier:** the section 3 falsifier rows, plus the no-em-dash / zero-CJK scan run on this file at
> write time.

## 1. Cross-game table

L0 function labels follow `research/gaming_corpus/l0_contract_crossmap.md:9-17` (F1 STATE ENCODING through F6
SCORING, with the fallback-contract signatures). "Hardest" means the function each pack itself stresses hardest:
where its verifier checks cluster and where its honest flags live.

| Game | L0 function instantiated hardest | Estate organ (what the game IS) | Owning engine family |
|---|---|---|---|
| chess | F3 LEGALITY, `legal(state, actor) -> [action]` authoritative: the KING-SAFETY FILTER is the global clause, one predicate gating the whole move set (chess.DRAFT.md:39-41, verifier checks 1-2 at :77-80). Runner-up F1: the super-state is required, not optional; a board-only tail is not a valid instance (chess.DRAFT.md:27-29, :158-160). | the war/capture falsifier-economy organ: every capture = a falsified assumption becomes a law, the capture rate is the learning rate, and the socratic gate lands as the king-safety filter because canonical chess has no forced capture (chess.DRAFT.md:127-140, honest flag :55-57) | WAR/CAPTURE, `research/gaming_corpus/engines_war_territory.md` section 1 (chess.DRAFT.md:4-5 engine dock) |
| go | F5 TERMINAL, `evaluate(state) -> VERDICT {PASS,FAIL,TIE}`: exactly one verdict, returned only after the C4 two-pass terminal fires; the mover never asserts a winner before the predicate (go.DRAFT.md:52, check 3). Runner-up F6: two scoring schools with komi (go.DRAFT.md:19, S5). | the territory lightmap organ: stones are probes, liberties are the dirty radius, cached reads and banked corpus are settled territory, and go is the organ where won knowledge becomes settled ground (go.DRAFT.md:77-81, FLEET CROSSMAP points 1-4) | TERRITORY slot, `watch/corpus/L1_engines/board_strategy.DRAFT.md` TERRITORY BLOCK (the go pack cites it as `L1_engines/board_strategy.DRAFT.md` at go.DRAFT.md:3, resolved to this path, existence checked this session); crossmapped at `research/gaming_corpus/engines_war_territory.md` section 3 (go.DRAFT.md:73 crossmap row 2) |
| tafl | F2 INITIAL STATE, `setup(seed, players, opts)`: the canonical 11x11 setup is itself the contested claim (the 24 vs 12 attacker divergence carried honest) and the executed verifier is instance-shaped: counts, king on throne, camps, 4-fold symmetry (tafl.DRAFT.md:37-39 divergence note, :42 verifier first line). Runner-up F5: dual terminal, one win condition per side (tafl.DRAFT.md:17). | the asymmetric solo-agent organ: one king ferries one load-bearing artifact to the board edge against a 2:1 hunter swarm holding a different win condition; king-escape is a ROUTING problem, not a numbers problem (tafl.DRAFT.md:57-59, quoting engines_war_territory.md:77-78) | ASYMMETRIC WAR within the war/territory family, `research/gaming_corpus/engines_war_territory.md` section 4, room spec ESCAPE CHAMBER (tafl.DRAFT.md:57, :59) |
| hanafuda | F6 SCORING, evaluate + pack SCORE rule: yaku set-membership over captured piles with house-rule parameterized values, and the koi-koi stop-or-continue call rides on it (hanafuda.DRAFT.md:17-18 clauses 4-5, :32 verifier). Runner-up F3: replay-consistency legality under hidden information (hanafuda.DRAFT.md:32). | the card information-set matching organ: tri-state hand verdicts (SUPPORTED/DISPUTED/UNPROVEN) over hidden evidence, the month-depletion census as the ledger tally, and koi-koi = bank-or-extend against a sibling lane landing first (hanafuda.DRAFT.md:45, anchored to `engines_tile_card_constraint.md` CELL G/engine/tile/matching_law via the mahjong row) | CARD/MATCHING, `research/gaming_corpus/engines_tile_card_constraint.md` CELL G/engine/tile/matching_law (hanafuda.DRAFT.md:45; go.DRAFT.md:75 family row 4) |

Coverage note: the four hardest surfaces cover F2, F3, F5 and F6 of the six L0 functions. No pack in this pour
claims F1 STATE ENCODING or F4 TRANSITION as its hardest edge; both clear as the shared floor in every pack's
SLOT 2 and SLOT 3, and chess is the closest runner-up on both (super-state encoding at chess.DRAFT.md:27-29,
transition bookkeeping at chess.DRAFT.md:43-48, the HISTORY clause).

## 2. What the four jointly teach that none teaches alone

Read together, the four statics teach that the six-function L0 contract is substrate-invariant while each function's hardest edge is substrate-specific, so the contract is only fully exercised by the set. Chess proves legality can gate an entire move set with one global predicate (the king-safety filter); go proves a verdict belongs to the terminal predicate and never to the mover's assertion (two passes, then one verdict); tafl proves the initial state itself is a claim that needs execution-verified canon (the 24 vs 12 attacker divergence is an instance fight, not a rules fight); hanafuda proves scoring survives hidden information only as set-membership over piles, with the unique-solution requirement explicitly dropped. That sequence is also the estate's claim lifecycle across four organs: probes read dark capability (go stones), contact falsifies assumptions (chess captures), one agent ferries the surviving law across hostile space (tafl king), and the result is banked or extended under uncertainty (hanafuda koi-koi). The cache-boundary notes add the joint meta-lesson: the static/dynamic line is organ-relative, not contract-relative. Chess must carry castling rights, en-passant target and clocks with every board tail (chess.DRAFT.md:158-160); go re-derives the dirty radius on every replay (go.DRAFT.md:84); tafl caches the initial position and leaves the adversarial tree at runtime (tafl.DRAFT.md:62); hanafuda keeps draw order cache-dark by design (hanafuda.DRAFT.md:48). One contract, four different cache lines, four different hardest functions: no single pack could show that, which is the thing this synthesis exists to say.

## 3. Falsifier rows

One killing observation per game. Each names the crossmap claim at risk and the observation that would end it.

| Game | Crossmap claim at risk | Killing observation |
|---|---|---|
| chess | "every capture = a falsified assumption becomes a law" and "the capture rate is the learning rate", resting on the king-safety filter substitution because canonical chess has no forced capture (engines_war_territory.md section 1 as quoted at chess.DRAFT.md:128-139, honest flag :55-57) | A war/capture-organ run where learning events and capture events dissociate: a full-value game decided with zero captures (checkmate with every piece still on the board) while the organ's learning ledger moves, or heavy capture exchange banking zero assumption-falsifications. Alternate kill: evidence that the socratic gate needs the forced-capture form and a passive global filter does not instantiate it. Either dissociation ends the falsifier-economy organ claim for chess. |
| go | "a vendor wall-change dirties a radius, not the board": liberties equal the dirty radius, a cached read lives while its radius stays clean and dies when the wall-change re-dirties it (engines_war_territory.md section 3 as quoted at go.DRAFT.md:73 and :79) | One documented re-probe whose dirty set spans the whole board rather than a radius, or a cached read dying while its dirty radius is provably clean: either breaks the liberty-to-dirty-radius identity the lightmap organ stands on. |
| tafl | "the king-escape is a ROUTING problem, not a numbers problem", with escape streaks tracked as the solo-agent reliability metric (engines_war_territory.md:77-78 and the ESCAPE CHAMBER spec as quoted at tafl.DRAFT.md:57) | Outcome data in which swarm material ratio predicts solo-agent survival better than route or streak metrics do: numbers beating routing kills the organ's routing law, and with it the asymmetric solo-agent crossmap. |
| hanafuda | "imperfect information admits no unique solution", so the verifier asserts replay-consistency and yaku-availability instead of a solve-count, and the koi-koi call is bank-or-extend against a sibling lane landing contradictory evidence first (hanafuda.DRAFT.md:32 and :45) | An estate surface where a claim's evidence state is fully decidable from one lane's visible record, hidden evidence recoverable and no sibling contradiction possible: the tri-state ledger collapses to binary and the information-set organ has nothing left to instantiate. |

---

research_status: derived (every claim above cites one of the five files named in the header; engine-file facts
appear only as pack-carried quotes; no engine file was read directly for this synthesis)
