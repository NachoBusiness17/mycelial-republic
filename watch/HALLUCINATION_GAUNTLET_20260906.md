# HALLUCINATION GAUNTLET — is the volume a hallucination? (2026-09-06, worker RB / rb-gauntlet)

Commission: SHADOW WALK quantizes 9,305 behavioral parts to a 288x64 voxel grid. The operator
sees corridors, biomes, gold invariants. The machine asks: do those perceived structures exist
in the source, or are they projection artifacts?

ORGAN: `mag/volume_fidelity.py` (stdlib-only, $0, no host processes)

    python -m mag.volume_fidelity dashboard/static/shadow_walk.html --from-shadow-walk

Port proof baked in: fnv1a32("aaad8ddf:1") = ba10a605 — exactly the game's recorded run #1 seed.
fnv1a32, mulberry32, the BFS leak field and carve() are line-faithful transcriptions of
shadow_walk.html (lines 63-156). A generic grid json also works (`--parts` for part-level features).

## THE RUN (K=20 nulls, 200 pairs, 3 reseeds — actual numbers)

| test | result | verdict |
|---|---|---|
| 1 NULL-MODEL CONTROL | carved=42; giant-component frac 0.286 vs null 0.169 (z=+2.43); frontier/carved 0.619 vs 0.224 (z=+3.44); entropy z=-0.18 | **STRUCTURE: z=1.90 above null — the layout is not noise** |
| 2 NEIGHBOR FIDELITY | rho=0.17, z=+2.38 vs label-shuffle, 45 law-carrying chunks | carried, but weakly — most neighborhood variance is NOT in the geometry |
| 3 INVARIANT STABILITY | pairwise Jaccard .113/.164/.061, mean **J=0.11** | **artifacts of run #1, not invariants** |
| 4 SEMANTIC PROBE | THE CHAIN @ c_07_03: rank 1/45 chunk by law density (mean_law 30.46) — earned. THE ROOM @ c_12_01: weights/tensor annex (0 points, 12 tensors) — position earned, meaning convention. BOOT_CHECK @ c_07_01: rank 20/45, ordinary chunk — design not data. | convention-marked — 2/3 positions source-justified, all names operator convention |

FAMILY FALSIFIER RUN (null-gate): the same gauntlet on a synthetic random terrain scores
**z=0.52 — decoration until proven otherwise**. The kill test kills.

## THE ANSWER (tri-state)

- SUPPORTED: the terrain is not noise. Structure z=1.90 clears the 1.5 gate; the law gradient
  is spatially carried (z=+2.38).
- SUPPORTED (against the game): the corridor LAYOUT is seed-dependent. J=0.11 across reseeds —
  the carved dungeons the player walks are artifacts of run #1's RNG over an invariant terrain.
- CONVENTION (marked, not discovered): every gold-invariant NAME; BOOT_CHECK placement;
  THE ROOM's meaning.

What deserves the word "invariant": the solid mass, the core position (rank-1 law chunk), the
law gradient. What does not: the corridors.

## WHAT EACH TEST CAN AND CANNOT PROVE (honest limits)

1. NULL-MODEL — CAN: prove the corridor network is non-random AS A GRAPH (connectivity and
   frontier above shuffled terrain with the identical height multiset). CANNOT: prove meaning,
   usefulness, or source-derivation. Passing means non-random, nothing more. Entropy is
   null-equal BY CONSTRUCTION — permutation preserves the height histogram, so entropy only
   echoes the multiset; it is carried as a control, not evidence.
2. NEIGHBOR FIDELITY — CAN: detect spatial autocorrelation of a source feature in the volume's
   geometry (volume-close pairs are source-close). CANNOT: certify every feature; rho=0.17 is
   real but weak. Granularity limit = the 16x16 chunk manifest; `--parts` lifts it when a
   part->feature table exists.
3. INVARIANT STABILITY — CAN: prove seed-dependence cleanly, because the BFS field is
   seed-independent — any difference between reseeds is pure RNG artifact, and J=0.11 is almost
   total artifact. CANNOT: say anything about the terrain layer, which reseeding never touches.
4. SEMANTIC PROBE — CAN: measure whether anchor POSITIONS sit where the source justifies them
   (law rank, biome composition). CANNOT: earn a NAME. "THE CHAIN" is a convention pasted onto a
   coordinate the data happens to justify; no measurement can bless language.

## FALSIFIERS FOR THE FAMILY

- NULL-GATE: run the gauntlet on any height-permuted or synthetic-random grid — STRUCTURE must
  return z<1.5. Verified live (z=0.52 on random terrain). If a null ever clears the gate, the
  kill test is broken (or you drew a ~3% tail — rerun with more K before claiming either way).
- SEED-PORT: fnv1a32(data_hash:1) must equal ba10a605 on the real html. Printed every run.
- RESEED: stability recomputes from seeds each run, never cache. Any cached J is disqualified.

Standing law this machine serves: discovered structure earns "invariant" only against a null
and a reseed. Everything else is decoration until proven otherwise.

## FOLD (RA×RB, 09-06 ~04:5xZ) — the answer to "is this a hallucination"

| Structure | Verdict | Evidence |
|---|---|---|
| The terrain itself | **REAL — not noise** | z=1.90 vs 20-null ensemble (gate 1.5); giant-component z=+2.43, frontier z=+3.44; kill test verified: random terrain scores z=0.52 = decoration |
| The law gradient in space | **WEAKLY REAL** | rho=0.17, z=+2.38 — signal above null, thin; a thread of truth, not a map |
| The corridors you walked | **ARTIFACT of run #1** | re-seed stability J=0.11 — different seed, different corridors; the paths are one traversal, not the territory |
| THE CHAIN's position | **EARNED (the eerie one)** | seeded by convention, then measured rank 1/45 law chunk — naming aligned with reality before we checked |
| BOOT_CHECK / ROOM names | **CONVENTION** | labels, not findings |
| Felt meaning while walking | **OPEN — confabulation until probed blind** | the Grok board (Sep 7) is the cross-substrate probe: does an independent model, playing blind, read the same regions the same way? |

RA's pre-registered bet (70% macro survives) PAID; the invariants-under-alignment line (~25-30%) matched: THE CHAIN earned, the rest convention. Research lane claim: projection fidelity for walkable operator surfaces is unstudied in the literature (18 sources, none cover it) — this card + mag/volume_fidelity.py is the open lane's first instrument.
