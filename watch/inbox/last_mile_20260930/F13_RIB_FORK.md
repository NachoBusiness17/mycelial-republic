# F13 RIB FORK — pre-warmed ribs as forks via different world lines (2026-09-30)

**Owner:** last-mile F13 · **Tool:** `tools/rib_fork.py` (399 lines, ratchet-clean, READ-ONLY over
`memory/mycelium/` + `memory/rib/`) · **Operator insight proven:** "pre-warmed ribs can act as
forks via different world lines."

## 1. The higher-dimensional space (graph census, `census`)

Measured 2026-09-30, byte-backed in `F13_census.json`:

- 5,455 node lines -> **3,804 unique nodes** (dedup last-write-wins, same semantics as
  `mag/mycelium.py::_load_nodes`). Types: 5,318 artifact lines, 128 seat, 8 concept, 1 claim.
- **744 edges** (31 self-loops): related 407, same_thread 195, produced 125, consumption 13,
  handoff 1, depends 1, supports 1, evidence_for 1.
- **Density 9.747e-05** (705 unique undirected pairs over 3,804 nodes): a sparse mycelium, not a mesh.
- **3,211 components**; giant component **485 nodes**; **3,106 isolated nodes** (mostly unwired artifacts).
- Path-length distribution inside the giant component (exact all-pairs BFS): **mean 3.719 hops,
  median 3, diameter 28** (diameter pair: `DNA topic: kompromat_ring` to a conversational answer
  node). Histogram peaks at 3 hops (222 of 484 pairs) with a long dangling tail.

## 2. The matrix part (`indirect`, numpy A^2/A^3 over the salience-weighted undirected adjacency)

Byte-backed in `F13_indirect_census.json` (724 active nodes):

- Direct pairs: **705**. Two-hop-ONLY pairs (no direct edge): **13,444**. Three-hop-only: **10,711**.
  The indirect space is ~19x the direct space: almost everything the graph "knows" is latent.
- **Strongest indirect connection (A^2 = 6.25): `DNA topic: elite_cabal` <-> `DNA topic: kompromat_ring`**,
  bridged by the summary artifact "Tl:Dr The world is run by human trafficking cultists...".
  Same hub triangle repeats: elite_cabal/political_commentary/kompromat_ring/propaganda all
  mutually two-hop through summary nodes.
- Strongest A^3 (6.875): `DNA topic: kompromat_ring` <-> the "@xai's policies are a duplicitous
  charade" node (ai_censorship adjacency).
- Per-node top-N two-hop lists included in the JSON for every active node.

## 3. The fork (`fork --question "what should we build next?" --lines 3`)

Mechanism: rib projection (capped token counts, rib-corpus IDF) -> question pre-warmed with the
rib's 15 most distinctive tokens at half weight -> graph projection restricted to the giant
component (a world line is a PATH; leaves cannot fork) -> K lines, each with its own seed from the
one rib projection, its own edge-type affinity (lineage / semantic / thread), salience-weighted
walk, cross-line divergence penalty 0.35 -> convergence = exact node overlap OR line pairs linked
at <=2 hops in the adjacency matrix (the A^2 test).

Demo (byte-backed in `F13_fork_demo.json`, deterministic across processes, verified by double run):

- Rib projection winner: **RIB_CASTLES_FOUNDATIONS_20260810 (7.011)** over
  RIB_ROUNDTRIP_STATELESS_TURTLES (4.469) and RIB_DEADDROP_FUTURE_SELF (3.827) — the foundations
  rib IS the "what to build" rib.
- **Line 1 (lineage):** John Titor world-line node -> six same_thread hops through the x-status
  thread chain. **Line 2 (semantic):** "My architecture just took yours" -> kompromat_ring ->
  elite_cabal -> "Most of our world..." -> blackmail-faction node. **Line 3 (thread):** Elias
  parable -> republic_governance -> Helpful Strangers parable -> @AlexanderSoros.
- **Convergence:** L1<->L2 at 1 hop (Titor <-> elite_cabal), L2<->L3 at 2 hops
  (kompromat_ring <-> republic_governance) — the DNA-topic hub lattice is the shared answer
  neighborhood reached from three different directions. **Divergence:** L1<->L3 min 3 hops — the
  Titor thread is the novel fringe. 17 single-line novel nodes.
- **Reading for "what should we build next?":** every world line rides the topic-hub lattice;
  the estate's BUILD-* backlog nodes are degree-1 leaves OUTSIDE the giant component (among the
  3,106 isolated nodes). The fork's answer: **wire the build/queue corpus into the mycelium
  connective core** so backlog items are reachable world lines, not orphans.

## 4. Laws honored

- READ-ONLY: no writes to `memory/mycelium/`, `memory/rib/`, or chain; mount-only like `mag/rib_boot.py`.
- Ratchet-clean: 399 lines (<400 cap), no bare-except/except-pass, ROOT-anchored paths.
  Pre-push ratchet FAIL rows visible 2026-09-30 belong to sibling files
  (flock_parity, mountain_selfplay, mountain_units, reverse_map), not F13.
- Determinism: warm-token and novel-list tiebreaks keyed by name, verified byte-equal across two
  processes (only `ts` differs).
- Rib system read: 46 rib files (2,276 lines) + `mag/rib_boot.py` mount path
  (`mag.rib_bus mount --domain doctrine`, 25 ribs).

## 5. Artifacts

- `tools/rib_fork.py` — census / indirect / fork, schema `rib_fork.v1`, exit 0/1/2.
- `F13_census.json`, `F13_indirect_census.json`, `F13_fork_demo.json` (this directory).
