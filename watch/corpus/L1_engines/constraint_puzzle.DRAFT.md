# L1 — Constraint-Puzzle Engine (DRAFT) — `L1_engines/constraint_puzzle.DRAFT.md`

> **Status:** DRAFT. **Class:** L1 family engine — one shared meta-grammar that specializes a
> whole constraint-puzzle family (the Nikoli galaxy + Sudoku/Mahjong-flagship lineage) via
> per-game clause/verifier swaps. **Provenance:** primer §4 L1 slot, Fact 7 taxonomy
> (constraint-puzzle is the 2nd engine in the corpus build order), primer §5 historical
> compression ("one puzzle grammar generates the Nikoli galaxy — Kakuro, Hitori, Nonogram,
> Slitherlink, Nurikabe, Masyu, Hashiwokakero — each a clause-swap"). **Research status:**
> family structure is editorial (this grammar is the corpus's own abstraction, not an attested
> historical artifact); the Lo Shu → Euler (1782) → Garns (1979) → Nikoli (1984) → Gould/Times
> (2004) lineage is **attested** and carried as a shared historical module. Per-game clauses
> keep their own flags; never silently upgrade.
> **Consumption order:** L0 contract → this engine (family grammar) → one game pack
> (`L2_games/*`) → L3 variant pack → L4 instance state.

---

[PROMPT-BODY-START — byte-stable from here]

## CONSTRAINT-PUZZLE ENGINE — META-GRAMMAR

A **constraint puzzle** is a fully-encodable static challenge: a **topology** of cells plus a
**domain** of cell-states, constrained by **clauses**, presented as one **instance** (the clue
grid), whose **verifier** decides legality, uniqueness, and difficulty. Unlike the race engine,
there is no RNG and no live adversarial turn; the "transition" is _fill a cell_, and terminal
detection = _all cells assigned and all clauses satisfied_. You apply the grammar exactly plus the
pack's clause set and verifier signature, never anything else.

A puzzle is defined by exactly **five parts**:
`TOPOLOGY · DOMAIN · CLAUSES · INSTANCE · VERIFIER`. Every constraint game in the corpus is these
five slots filled by its pack. No sixth part exists.

### PART 1 — TOPOLOGY (the cell graph)

`TOPOLOGY(n, shape, NEIGHBOR)`. Two reusable shapes:

- **grid** — a `rows × cols` cell lattice; `NEIGHBOR` is 4-orthogonal (±row, ±col) by default
  unless the pack sets it to 8 (with diagonals) or an arbitrary edge list (slitherlink/Hashi
  often use custom edge/vertex graphs).
- **custom graph** — an explicit vertex + edge list (e.g., a Kakuro "runs" decomposition, Hitori
  adjacency via cell-neighbors, Hashi's island vertices + bridge edges).

`NEIGHBOR(a,b)` must be a pure function of cell ids. Encode cells in **r-major flat order**
(`id = row*cols + col` for a grid) — the canonical `board` string is that run of cell states.

### PART 2 — DOMAIN (cell-states)

`DOMAIN(S)` = the finite set of values a single cell may hold. Pack-defined (e.g., numerals `1..9`
for Sudoku/Nonogram, numerals `1..9` for Kakuro cells, binary `{filled,empty}` for Hitori,
`{blank,line|state}` per slitherlink). EVERY cell's state ∈ `S`; the verifier rejects any cell
outside `S`. Empty/unsolved cells carry a pack sentinel (`_`, `.`, `?` — pack-defined) so a
partial `board` is still a valid string of the same grammar.

### PART 3 — CONSTRAINT CLAUSES (the engine's reusable idiom)

A clause is a bound predicate over the topology and domain. The clause **vocabulary** below is
cached here and reused verbatim by every pack; a pack picks a subset and instantiates parameters —
no pack writes new clause prose, it only names existing clauses and their numbers. Defining a new
clause adds to THIS section once (a corpus patch), not per-game.

1. **all-different(region)** — every cell in `region` holds a distinct value. (Sudoku rows/
   columns/boxes; Kakuro runs.)
2. **pairwise-consecutive(region)** — the values in `region` form a consecutive block with no
   repeats and no gaps. (nonogram-adjacent runs.)
3. **sum-equals(region, target)** — Σ cell values in `region` == `target`. (Kakuro clue.
   Implies all-different when the pack also declares region `no-repeat`.)
4. **edges-diff(vertex-pair, delta)** — two orthogonally-adjacent cells differ by exactly
   `delta`. (Masyu; some Hashi edges.)
5. **isolate(cluster-id, seed-set)** — cells sharing a linked/connected region obey a per-cluster
   constraint (filled-region size, connectivity, no-touching). (Hitori: no adjacent same-value;
   Nurikabe: connected blanks / island sizes; Masyu turn rules.)
6. **line-model(edge-set, rules)** — the solution marks a subset of edges per an edge-degree or
   turn rule. (Slitherlink loop; Hashi bridge degrees.)
7. **count-marks(target-count)** — a quantified region or the whole board holds exactly
   `target-count` marked cells/edges. (Nonogram row/column sums.)

Clauses compose in **AND** (all must hold) unless the pack declares an explicit OR over a stated
case-set. A solution must satisfy every clause; clause order does not matter for satisfiability
but is fixed by the pack so the verifier output is byte-stable.

### PART 4 — INSTANCE (the clue grid)

`INSTANCE` = the fixed puzzle data a solver starts from: the `board` string with some cells
pre-filled (givens) and the pack's clue data (sum targets, region memberships, run lists) carried
in the `order` field of the canonical L0 state string. The LLM **emits** instances (given the
clue parameter set and seed) and **reprints** them; it never judges them. Instance grammar:

```
<game-id>:<state-hash>:<turn=0>:<solver>:<board-encoded>:<order-clues>:<seed-phrase>:-
```

`board-encoded` = the flat run of cell states with pre-fills and `_` empties. `order-clues` = the
clue table (region → target / run → sum) in a fixed pack-defined serialization. The verifier's
`parse` accepts exactly this string; a cell or clue not encoded is `UNKNOWN-RULE`.

### PART 5 — VERIFIER (the decisive, deterministic layer)

The LLM **never solves**. Every theory of a completed grid, uniqueness claim, or difficulty
rating is delegated to the deterministic verifier in this section. Vocabulary (called, never
invented):

```
parse(instance: String) -> { ok, regions, clues, cells }      // structural validity of the string
assert(clauses: Clause[], state: String) -> { sat : bool, rule-violated : String? }
solve-count(instance: String) -> { count: Int, min: Int?, max: Int? }   // # solutions
technique-ladder(instance: String) -> [ TechniqueGrades ]      // ordered, pack-defined
```

- **parse** — reject malformed grids, unknown cells, missing clues (each hard `false`).
- **assert** — check every pack clause against a proposed completed board; on `false` report the
  exact clause number violated. This is the legality gate for a submitted solution.
- **solve-count** — the uniqueness oracle: `count == 1` → valid puzzle; `0` → clue
  contradiction | over-constrained; `≥2` → invalid (multiple solutions) unless the pack allows
  non-unique. `unique-solution` is the standard acceptance test.
- **technique-ladder** — a pack-defined ordered list of human techniques (e.g., single-candidate,
  hidden single, naked/hidden pair, pointing, box-line, X-wing, swordfish, chains) used to rate
  difficulty as the **minimum technique tier required to solve without guessing**. The LLM quotes
  the tier; the verifier assigns it. This is the difficulty oracle (primer §8: benchmark vs.
  published ratings). Tier cutoffs are per-pack calibration data.

**Difficulty output:** `difficulty = min-tier-contacted` over all cells, computed by the verifier,
reported as an integer tier name (never a narrative "hard/easy"). Packs map tiers to labels
(15-floor Kakuro, Sudoku 1..5) in L3; the engine only emits the tier.

### CACHE-BOUNDARY DECISION RULE

Where new content sits is decided by *what kind of change it is*, not by enthusiasm:

- **Pure-rule variant** (a new game that reuses this engine's TOPOLOGY+DOMAIN+clauses and only
  swaps which clauses apply + instance format): extends the **static prefix** — it adds/alters
  parts of a pack body below the engine and above the instance. The engine text and existing pack
  statics stay byte-identical; the new pack is appended atomically at L2/L3. Cache-friendly: all
  prior layers still hit.
- **Structural variant** (new TOPOLOGY shape, new DOMAIN, or a genuinely new clause that demands
  a clause-vocabulary addition): extends the **dynamic layer** and first lands as a **patch to
  THIS engine's clause vocabulary (Part 3)** or a new reusable topo/domain in Part 1/2 — reusing
  the updated engine is then byte-stable for every future game on that shape. Nothing structural
  lives in an instance tail.

Rule of thumb: *rules that many games share go up (static, once); rules specific to one game's
surface go down (pack, small); anything per-play goes to the instance and is never cached.*

### HIT-RATE TARGETS (per layer, per primer §4/§7)

| Layer | Content | Hit-rate target | Notes |
| :--- | :--- | :--- | :--- |
| L0 contract (+ this engine Part 1–3 & 5 vocab) | universal + family rules | ≥95% | byte-stable first |
| L2 game statics (per game pack: clause subset, DOMAIN, instance grammar) | one game's fixed spec | ≥90% | shared across every instance of that game |
| L3 variant pack (clue-format tweaks, technique-tier labels) | game + difficulty calibration | ≥70% | small deltas |
| L4 instance (board-encoded + order-clues + seed) | one puzzle | 0% | always fresh by design |

### FAMILY PACK-LANDING (sketched — each becomes its own `L2_games/*`)

1. **Kakuro** — `TOPOLOGY: custom runs`, `DOMAIN: 1..9`, clauses {3 sum-equals on runs with
   no-repeat → all-different}, `INSTANCE: clue grid`, `VERIFIER: solve-count==1` + a sum-based
   `technique-ladder`. **(attested; American crossword-arithmetic puzzle, c.1950s, revived by
   Nikoli.)**
2. **Hitori** — `TOPOLOGY: grid 8-neighbor`, `DOMAIN: {filled,empty}`, clause {5 isolate:
   no adjacent equal filled, connected empties}, `VERIFIER: solve-count==1`. (Nikoli.)
3. **Nonogram** — `TOPOLOGY: grid`, `DOMAIN: {filled,empty}`, clause {7 count-marks per
   row/column}, `VERIFIER: solve-count==1`; a line-solving ladder.
4. **Slitherlink** — `TOPOLOGY: custom edge graph`, `DOMAIN: edge states`, clause {6 line-model},
   `VERIFIER: single-loop uniqueness`.
5. **Nurikabe** — `TOPOLOGY: grid`, `DOMAIN: {island,wall}`, clause {5 isolate with island
   sizes}, `VERIFIER: solve-count==1`.
6. **Masyu — line (turns) clauses.**
7. **Hashiwokakero — degree-constraint bridge edges.**
8. **Sudoku (flagship)** — `TOPOLOGY: 9×9 grid + 3×3 boxes`, `DOMAIN: 1..9`, clauses {1
   all-different on rows/cols/boxes}, `INSTANCE: 81-char string`, `VERIFIER: solve-count==1`,
   technique ladder {single→hidden→X-wing→…}. **(attested lineage: Lo Shu → Euler 1782 → Garns
   1979 → Nikoli 1984 → Gould/Times 2004; McGuire et al. 2012: 17 givens minimum for
   uniqueness — the canonical difficulty floor.)**

### OUTPUT / INSTANCE NOTES

- Apply the L0 OUTPUT CONTRACT: reprint the canonical instance with the `^` line, cite the
  governing grammar part + clause numbers, and — when a solution is claimed — state `assert` +
  `solve-count` results from the verifier, never claim uniqueness from inspection.
- A filled grid is only "solved" when `solve-count == 1` AND `assert` returns `sat:true`.
- Any collision between the grammar's structural parts (topology/domain/clause vocab/verifier)
  and a pack delta resolves the **pack may pick clauses, never redefine grammar structure**.

[PROMPT-BODY-END]

---

## Asset notes (NOT cached prompt body)

- **Target size:** ~1–1.5k tokens of prompt body. Mission = make the whole Nikoli galaxy +
  Sudoku a set of small clause/verifier pack-deltas over this one grammar.
- **The five-part grammar** (topology · domain · clauses · instance · verifier) is the engine's
  load-bearing claim, matching primer §5's abstraction. The verifier vocabulary (parse / assert /
  solve-count / technique-ladder) is the engine's answer to primer Fact 5 (LLM never the solver)
  — uniqueness and difficulty are verifier outputs, never LLM assertions.
- **Research status:** the grammar itself is an editorial abstraction (`speculative` as a
  historical descriptor — it is the corpus's own, not attested period art); each game's rules
  carry their own attested/Nikoli flags. Sudoku lineage is attested; the 17-givens floor is
  attested scholarship (McGuire et al., 2012).
- **Hit-rate targets** (L0/L1 ≥95%, L2 ≥90%, L3 ≥70%, L4 0%) are TARGETS, mirrored from primer
  §4/§7; not yet measured for this engine — the Corollary: static-first is a law, not a
  preference (`L2/L3` must be appended atomically, never interleaved).
- Cross-refs: parent `L0_universal_contract.DRAFT.md` (six-function contract + RNG); siblings
  `L1_engines/race_dice.DRAFT.md`; first proof-pack `L2_games/kakuro.DRAFT.md`; downstream
  `L3_packs/*`, `L4_instances/*`.
