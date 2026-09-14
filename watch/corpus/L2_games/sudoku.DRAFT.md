# L2 — Sudoku Game Pack (DRAFT) — `L2_games/sudoku.DRAFT.md`

> **Status:** DRAFT. **Class:** L2 game statics — flagship instance of the constraint‑puzzle engine. **Research status:** Sudoku lineage (Lo Shu c.650 BCE → Euler 1782 Latin squares → Garns 1979 Number Place → Nikoli 1984 Naming → Gould/Times 2004 Boom) is **attested**; minimal‑givens result (McGuire et al. 2012 arXiv:1201.0749) is **honest**.

---

## SLOT 1 — TOPOLOGY
`TOPOLOGY` = grid 9×9 with 3×3 box subdivision (standard Sudoku). Neighbor = 4‑orthogonal.

## SLOT 2 — DOMAIN
`DOMAIN` = {1,2,3,4,5,6,7,8,9}. Empty cells use `_`.

## SLOT 3 — CLAUSES
All‑different on each **row**, **column**, and **3×3 box** (engine clause 1 instantiated three times).

## SLOT 4 — INSTANCE
Canonical 81‑char string (dots replaced by `_`):
```
000000907000420180000705026100904000050000040000507009920108000034059000507000000
```
Transformed:
```
______9_7___42_18____7_5_261__9_4____5_____4____5_7__992_1_8____34_59___5_7______
```

## SLOT 5 — VERIFIER
Parse → verify all‑different rows/cols/boxes. `solve-count(instance) == 1` required. Technique ladder: singles → hidden‑singles → pairs → X‑wing → chains. Minimum‑givens honesty note: ≥17 givens per McGuire et al. 2012.

### LINEAGE MODULE
Lo Shu (c.650 BCE) → Euler 1782 Latin squares → Garns 1979 Number Place → Nikoli 1984 Naming → Gould/Times 2004 Boom.

### CACHE‑BOUNDARY NOTE
Pure‑rule variant (static prefix) – Sudoku swaps clause 1 and instance grammar only; dynamic layer unchanged.

### BUILD PROMPT
`{topology:9x9-box, domain:1-9, clauses:all-different rows/cols/boxes, instance:<canonical>, verifier:unique+ladder}`

---

research_status: attested
