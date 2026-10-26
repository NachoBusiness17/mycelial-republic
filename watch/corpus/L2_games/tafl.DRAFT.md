# L2 - Tafl Game Pack (DRAFT) - `L2_games/tafl.DRAFT.md`

> **Status:** DRAFT. **Class:** L2 game statics - asymmetric-war engine instance (war/territory family, solo-agent organ). **Research status:** lineage chain (latrunculi horizon c.400-900 CE -> saga mentions c.900-1100 -> scratched boards c.1000-1200 -> Linnaeus 1732 tablut -> 1811 publication -> Murray 1952 reconstruction -> Fetlar-era 11x11 revival) is **attested** with honest caveats carried inline; the 11x11 piece canon (24 attackers vs 12 defenders + king) was **attested this session** against the fetched Fetlar and Copenhagen rules pages; the pour ore's "12 attackers on 11x11" figure is carried as an **honest** divergence (see SLOT 4). No claim in this file rests on unanchored memory.

---

## SLOT 1 - TOPOLOGY
`TOPOLOGY` = grid 11x11 (canonical hnefatafl; odd side N, variants 7x7 to 19x19, 9x9 tablut the Linnaeus-derived sharp variant). Neighbor = 4-orthogonal; both movement lines and custodian-capture flanks read orthogonal only. Special cells: throne at center (5,5), four corner camps.

## SLOT 2 - DOMAIN
`DOMAIN` = {`_`, `A`, `D`, `K`} - `_` empty, `A` attacker, `D` defender, `K` king. Terrain markers in the board frame: `T` throne, `C` corner camp. Turn parity and move count are state, not cells (pour ore, RULES CANON).

## SLOT 3 - CLAUSES
- **Movement:** orthogonal rook-lines, any distance, no jumping, no diagonal.
- **Capture (custodian):** a piece flanked on two opposite orthogonal sides by two enemy pieces (or enemy piece + throne/camp, ruleset-dependent) is removed. The war/territory engine's capture clause instantiated as sandwich.
- **King clause:** only `K` may occupy the throne and may not return after leaving (most rulesets). King capture diverges by ruleset: Copenhagen requires a four-side flank (or two sides + throne); Fetlar takes the king by ordinary custodial capture. Carried **honest** - the two named rulesets disagree.
- **Dual terminal:** attackers win by capturing the king; defenders win by moving the king to a corner camp (any edge square in edge-escape variants). Stalemate/repetition handling varies by ruleset.
- **Asymmetry clause (the engine's signature):** 2:1 material, different victory conditions, one board.

## SLOT 4 - INSTANCE
Canonical 11x11 initial position (24 attackers, 12 defenders + king on throne, Copenhagen/Fetlar-style cross):

```
C__AAAAA__C
_____A_____
___________
A____D____A
A___DDD___A
AA_DDKDD_AA
A___DDD___A
A____D____A
___________
_____A_____
C__AAAAA__C
```

Verified by execution this session (`python` over the 11-row block): counts A=24, D=12, K=1, C=4, `_`=80; king at (5,5) on the throne; corner camps at (0,0),(0,10),(10,0),(10,10); full 4-fold symmetry; all four king-neighbors are `D`. Output line: `ALL CHECKS PASS`.

Count divergence, carried **honest**: the pour ore (`memory/runs/l2_statics_pour_20261020/results.jsonl`, id `tafl`, field `out`, RULES CANON) states "11x11: 12 attackers, 12 defenders + king"; the rulesets the ore itself names as its attested modern examples field twice as many attackers as defenders - 24 vs 12 + king per the fetched Fetlar rules page (aagenielsen.dk/fetlar_rules_en.php: "There are twice as many attackers as defenders") and the fetched Copenhagen rules page (tafl.cyningstan.com/page/768/copenhagen-hnefatafl-rules). The instance above uses the fetched canon; the ore's 12-attacker figure is recorded here rather than silently corrected.

## SLOT 5 - VERIFIER
Parse the 11-row block -> verify count invariants (A=24, D=12, K=1), king on throne center, camps at the four corners, 4-fold symmetry (all four ran green this session). Then the built-verifier contract: orthogonal-rook move generation -> custodian capture resolution -> flank-threat detection -> king-escape corridor search. Technique ladder: corridor singles -> forced corridors -> flank pairs -> siege lines. Honesty notes carried from the ore INVARIANTS: board size changes the game's character more than piece count (9x9 sharp tactics, 11x11+ positional siege) and defender optimal play often sacrifices pieces to open a corridor - both community consensus in tafl literature, not formal proof.

### LINEAGE MODULE
- c.400-900 CE - Roman *ludus latrunculorum* and Germanic tafl boards appear in archaeological contexts; direct descent debated. [honest: some scholars link tafl to latrunculi, others treat it as an independent Norse development] (pour ore, LINEAGE row 1)
- c.900-1100 CE - Norse sagas (*Fridthjofs saga*, *Hervarar saga*) mention hnefatafl/tafl play; textual, not contemporary. [attested: saga corpus, as literary references] (pour ore, LINEAGE row 2)
- c.1000-1200 CE - tafl-type grids scratched into stone and wood at Norse sites (Baldursheimur, Iceland; Ockelbo, Sweden). [attested: archaeological finds] (pour ore, LINEAGE row 3)
- 1732 - Carl Linnaeus records a Lappish game he calls *tablut* on a 9x9 board during his Lapland journey, with a rules sketch. [attested: Linnaeus, *Iter Lapponicum*] (pour ore, LINEAGE row 4)
- 1811 - Linnaeus's tablut notes published posthumously by J. E. Smith; primary written source for reconstruction. [attested: publication record] (pour ore, LINEAGE row 5)
- 1952 - H. J. R. Murray and others reconstruct hnefatafl from sagas, boards, and Linnaeus; reconstructions diverge on custodian capture details and king strength. [honest: Murray vs later reconstructions disagree] (pour ore LINEAGE row 6; the 1952 date anchored to `research/gaming_corpus/engines_war_territory.md:113`)
- modern era - variant revival: 7x7, 9x9, 11x11, 19x19 offshoots codified by clubs and the Fetlar ruleset. [attested: modern rulesets] (pour ore, LINEAGE row 7)
- 2000s-present - digital implementations and open-source engines; 11x11 the de facto tournament size. [honest: community practice; the ore names no single canon source for the standardization claim] (pour ore, LINEAGE row 8)

Anchor note: every row above is carried from the pour ore (tafl row, field `out`) plus this session's on-disk reads (`research/gaming_corpus/engines_war_territory.md`) and this session's fetched rules pages; nothing rests on unanchored memory, so no row needed the `unverified` tag.

### FLEET CROSSMAP
Tafl IS the asymmetric-war engine -> the solo-agent organ. `research/gaming_corpus/engines_war_territory.md` section 4 (lines 67-83): the solo seat as the king - one agent carrying one load-bearing artifact (an invariant, a proof, a deadline row) across hostile space, vs the 50-walker swarm whose win condition is different (blockade, verification, saturation). The organ's routing law, quoted: "the king-escape is a ROUTING problem, not a numbers problem" (engines_war_territory.md:77-78); the room spec is the ESCAPE CHAMBER (lines 80-83), which tracks escape streaks as the solo-agent reliability metric. In the combat grammar's closure loop tafl is the defend leg: the solo agent ferries the new law across hostile space to the record (engines_war_territory.md:108-109). The pour ore's INVARIANTS extend the organ: the 2:1 asymmetry is structural, not cosmetic, and custodian capture makes every piece a potential wall, so formation play dominates over individual captures - the king's route matters more than any single blockader.

Family rows, one line each, for slot placement: war/capture (chess) = the falsifier economy, every capture a falsified assumption becoming a law (engines_war_territory.md section 1); territory (go) = the lightmap's lit/dark attention territory (section 3); card/matching (hanafuda) = information-set matching (research/gaming_corpus/engines_tile_card_constraint.md, CELL G/engine/tile/matching_law, line 30 - the cell's canon example is mahjong; hanafuda rides the same cell per the pour family list). Tafl is the only family row whose two sides hold different victory conditions - hence the asymmetric solo-agent organ.

### CACHE-BOUNDARY NOTE
Unlike the pure-rule sudoku prefix, tafl's static prefix is the initial position plus the movement/capture grammar (cache-safe; the prefix is what SLOT 5's executed checks read); the adversarial move tree is dynamic layer and stays runtime. No new cache rails invented: the organ reuses the section-4 room spec unchanged.

### BUILD PROMPT
`{topology:11x11-throne-camps, domain:_ADK, clauses:rook-move+custodian+dual-terminal, instance:<canonical-11x11>, verifier:counts+symmetry+king-at-throne+ladder}`

---

research_status: attested
