# oral-03: the dirac_loop ancestor - what the operator's MAP saw in 08-2026 vs what the estate runs now

- **Item:** oral-03 · **Read:** 2026-09-28 · **Seat:** mirror gopher, flash50 oral-history lane
- **Source:** `corpus/oral_history/nacho_archaeology/extracted/nacho-archaeology-part10-mag-disk/mag-disk/mag/dirac_loop.py` (290 lines as read; raw disk bytes sha256 `a8af46af46feec34b37e85e24163ef325b8aa8df22167c5ab24747fd5044a4c4`, 11,698 bytes)
- **Method:** full Read of the ancestor; git archaeology on the descendant (`git log --follow`, `-S` pickaxe, blob greps); CRLF-normalized in-memory byte comparison of the ancestor against every tracked version; live run of the descendant module's own CLI verbs; `pytest` of its suite; read of its ledger. Every claim cites the file or the exact command output that produced it.

## 0. Provenance of the disk copy (byte evidence)

Command run (venv python, CRLF-normalized compare of ancestor vs each tracked version):

```
052732ebf differs bytes_norm 9400
d575bc168 IDENTICAL bytes_norm 11496
4638646d4 differs bytes_norm 14207
ancestor_norm_bytes 11496
```

- The disk snapshot is **content-identical after CRLF normalization** to the 2026-09-14 checkpoint `d575bc168` ("checkpoint 2026-09-14: Zenodo 17811909 capstone mined + forge-window recovery receipt"). It carries the `--scope operational|knowledge|all` graph loader that `git log -S "operational|knowledge|all" -- mag/dirac_loop.py` dates to `d575bc168` alone.
- The MAP itself is older than the snapshot: the first tracked version `052732ebf` (2026-08-14, "backup 20260814: ... flock_field/flock_grid port ...") already contains the MAP verbatim. The ask's "08-2026" frame is byte-true for the frame; the disk bytes are a 09-14 freeze of it.
- The descendant is `mag/dirac_loop.py` at HEAD (349 lines, schema `dirac_loop.v1`): same MAP (lines 14-18), same math, plus the closure machinery the ancestor never had.

## 1. THE MAP (operator's frame), quoted verbatim

Ancestor `dirac_loop.py:14-18` (identical text survives at `mag/dirac_loop.py:14-18` today):

> THE MAP (operator's frame):
> * A problem/session is a KNOT (closed loop of steps). Its topological invariant = the content root.
> * A DIRAC LOOP = an independent cycle in the knowledge graph. Walking it (holonomy) returns a value.
> * A loop whose invariant ALREADY exists in the lattice = CLOSED/SOLVED (Tesuji, verify-without-replay).
> * A loop whose invariant is NOVEL = OPEN = a GAP the swarm/flock should fill.

Supporting frame from the same docstring: the research steal anchors (cycle space / first Betti number beta1 = m - n + c, fundamental cycle basis, graph Laplacian kernel) at lines 3-12, and the schema contract "dirac_loop.v1 · deterministic · $0" at line 20-21.

## 2. Concept -> current estate organ (9 patterns)

**P1. KNOT (session as closed loop, invariant = content root) -> the verkle knot lattice.**
`mag/verkle_knot.py:1-26`: "Living Verkle-knot record of session dossiers", chain tip = "a succinct root (Merkle-Verkle hybrid)", leaves at `memory/biography/knots/`, chain `memory/biography/verkle_chain.jsonl`, tip `memory/biography/verkle_tip.json`. `mag/ghost_server.py:39` exposes it as the `state/commit` organ: "immutable content-addressed save", via verkle_knot. The ancestor's line-15 claim ("invariant = the content root") is exactly this organ's contract.

**P2. DIRAC LOOP (independent cycle, enumerated) -> mag/dirac_loop.py itself + the two graphs it walks.**
The descendant keeps the same algorithm: fundamental cycle basis over a spanning forest (`mag/dirac_loop.py:168-182`), beta1 = m - n + c (`:257-269`), Laplacian kernel (`:272-292`). Its graph sources: `mag/organ_map.py` `operational_graph()` (docstring "the declared operational lifecycle graph used by Dirac", `mag/organ_map.py:641`), which registers the dirac organ itself as a node (`mag/organ_map.py:171-179`, `"id": "dirac_loop", "label": "Dirac loop", "proof": "dirac"`), plus `mag/knowledge_graph.build()` (`mag/dirac_loop.py:82-87`).

**P3. CLOSED/SOLVED (Tesuji, verify-without-replay) -> the BANK verb + the banked-invariants ledger.**
`mag/dirac_loop.py:228` `BANKED_FILE = ROOT / "watch" / "inbox" / "DIRAC_BANKED_INVARIANTS.jsonl"`; `bank(edge, receipt, seat)` at `:231-254` ("The tesuji act - verify-without-replay from now on"); CLI `bank --edge --receipt --seat` at `:325-328` and `:339-341`. Live ledger read this session: **6 rows**, ts 2026-09-27T22:31:25Z (organ:verkle_knot->organ:manifest) through 2026-09-28T02:59:25Z (organ:context_checkpoint->organ:context_pack), every row carrying a receipt path. Scan result feeds three surfaces: `mag/dogfood_audit.py:137-144` (dogfood probe), the visor dirac line via `tools/dirac_loop_shim.py` import seam (landed `988101f51`), and the context pack (see P9 honesty note).

**P4. OPEN GAP (novel invariant = food for the swarm/flock) -> the quests organ + the self-building loop.**
`mag/ghost_server.py:38` registers `quests/open`: "the open loops / gaps to fill", `"via": "dirac_loop.scan"` - the ghost server serves open Dirac loops to actor seats as quests. The consumer side is the self-building loop, commit `a23928aca` (2026-09-27): "pop queued build -> hermes headless implements in-repo -> tests -> receipt -> commit -> dirac bank; SI-01 autonomously built (pack->swarm_surface offload) and BANKED". The gap-to-work pipeline the MAP sketched ("a GAP the swarm/flock should fill") is now literally rows 5-6 of the ledger, banked by seats, not the operator.

**P5. Holonomy (walking a loop returns a value) -> portal's belt trick.**
`mag/portal.py:97-108` `_dirac_deficit`: "Dirac's belt trick: does the input's knot close at 360 degrees (surface Tesuji, one worldline) or does it need the 720 degree double-cover (the cold fold / antipode) to be a TRUE Tesuji? Deterministic: the hash decides." Wired into every portal lift at `mag/portal.py:138-143` (`dirac=<deg>/<worldlines>wl`). `mag/grok_brief.py:43-44` briefs it to remote seats as "dirac belt trick / portal._dirac_deficit".

**P6. Determinism as law ($0, schema-stamped) -> the deterministic-organs tier.**
Ancestor line 20 "Schema: dirac_loop.v1 · deterministic · $0" is the same contract `mag/ghost_server.py:50-54` meters as TIERS "C": "free deterministic (the $0 floor) - always ours". The module needs no model, no network; its verdicts are hash-determined (P5, P2).

**P7. FOSSIL 1 (found 08-2026, cured only 09-27): the closure verb that never existed.**
The 2026-08-14 version advertises `CLI: python -m mag.dirac_loop scan | cycles | rank | spectrum | closed <label...>` (blob `052732ebf:mag/dirac_loop.py:21`) but its `main()` wires only four subparsers, `scan/cycles/rank/spectrum` (same blob, lines 235-238). No `closed` command ever existed; by 09-14 the mention was silently dropped from the docstring. The closure verb the operator asked for in August only became real as `bank` in `4638646d4` (2026-09-27).

**P8. FOSSIL 2 (the gene-pool-class one): closed_solved could never fire.**
`_known_invariants` hashed individual node labels (`_h("dirac_loop:" + lab[:200])`) while `loop_invariant` hashes the sorted-joined label-SET (`mag/dirac_loop.py:185-188` vs `:202-208`); two formulas that never meet, so the CLOSED/SOLVED branch of scan() (declared 08-14, ancestor `:214-228`) was dead code on every scope for six weeks. The fix is documented at `mag/dirac_loop.py:192-201` ("2026-09-27 structural fix (found closing loop 3): the two formulas never met... closure is now a receipt-backed act") and landed in `4638646d4` ("DIRAC BANK verb + first closed loop in estate history"). The operator's own queue entry independently diagnosed it: `queue/todo.md:277` ("scan() can never report 'closed' on default scope - _known_invariants filters knot/case_law/doctrine kinds, operational nodes are all kind='organ'") - still an unchecked checkbox there, though `4638646d4` + the f-30 triage receipt (commit `ac8123340`: "dirac 272-277 all closed") implement exactly its second proposed cure (teach dirac_loop to honor receipt-backed evidence).

**P9. Live discrepancy found this session: rank says 8 loops, scan enumerates 6.**
Same live run: `rank` returns `betti1: 8` while `scan` returns `n_loops: 6` (outputs below). Cause: `_spanning_forest` stores tree edges as frozensets (`mag/dirac_loop.py:131`), so parallel edges between the same vertex pair collapse, and the second parallel edge is skipped as a cycle generator (`:177-178`) even though it counts in m. Measured duplicate pairs in `operational_graph()`: organ:context_admission<->organ:context_pack (2), organ:context_admission<->organ:openclaw (2), organ:blackboard<->organ:switchboard (2) - 21 edges over 18 undirected pairs, hence beta1 counts 2 more generators than the enumeration walks. Unharmful today, but a subtle overcount if anyone reads beta1 as "open work".

## 3. Timeline (all byte-backed)

| When | Commit | What |
|---|---|---|
| 2026-08-14 | `052732ebf` | dirac_loop.py enters tracking WITH the full MAP already written; scan/cycles/rank/spectrum verbs; same-day consumers `mag/ghost_server.py` quests/open organ and `mag/dogfood_audit.py` dirac probe (both first appear in this commit per `-S` pickaxe); docstring advertises a `closed` verb main() never wires (P7) |
| 2026-09-14 | `d575bc168` | scope-aware graph loading (operational lifecycle vs knowledge graph) + organ_map registers the dirac node and lifecycle edges; this is the state the nacho disk froze (Section 0) |
| 2026-09-27 | `988101f51` | "dirac organ cured (self-steal deep-dive follow-through)": 7 tests pin the topology math on known graphs, `tools/dirac_loop_shim.py` import seam, visor read-only dirac line |
| 2026-09-27 | `4638646d4` | BANK verb + formula-mismatch fix (P8) + "first closed loop in estate history" (verkle_knot->manifest, ledger row 1) |
| 2026-09-27 | `6c43c15d2` | "burn lane dirac6: water proof anchored, loop 6 banked" (water_computer anchor_proof) |
| 2026-09-27 | `a23928aca` | SELF-BUILDING LOOP LIVE: the dirac bank is the closing step of an autonomous build pipeline; "dirac CLOSED 5 / open 1" at that moment |
| 2026-09-28 | (ledger rows) | rows 5-6 banked: context_pack->swarm_surface offload, context_checkpoint->context_pack restore - the first loops closed by seats, not the operator |

## 4. Answer: what did the operator see in 08-2026 that we only implemented now?

He saw the whole thing. On 2026-08-14 the MAP already declared the four concepts in final form (Section 1), and the scan verb already computed `closed_solved` / `open_gaps` fields (ancestor `:214-228`). What the estate could not do for six weeks was **close a single loop**:

1. The closure verb he advertised in the August CLI never existed (P7).
2. The one closure path the code had (invariant already in lattice) was dead by a hash-formula mismatch (P8) - the August code could enumerate loops forever and report "all open" forever.
3. The swarm-filling-the-gap half of the MAP existed as a data surface (quests/open, 08-14) but had no producer: nothing autonomously turned an open loop into banked work until the self-building loop (`a23928aca`, 09-27).

So the one-line answer: **in August 2026 the operator saw that solved problems should be recognized by topological invariant and never re-walked (verify-without-replay), and that open loops are the flock's food; the estate only grew the organ that makes recognition durable and receipt-backed on 2026-09-27 (`4638646d4`), and only grew seats that feed themselves from open loops on 2026-09-28 (ledger rows 5-6).** The MAP was not revised once in that period - the fix was to make the map's own verbs real, not to redraw the map.

## 5. Checks run this session (exact commands + outputs)

- `git log --follow --format="%h %ad %s" --date=short -- mag/dirac_loop.py` -> `052732ebf 2026-08-14` / `d575bc168 2026-09-14` / `4638646d4 2026-09-27`.
- CRLF-normalized byte compare (venv python, in-memory): ancestor IDENTICAL to `d575bc168`, differs from `052732ebf` and HEAD (Section 0).
- `.venv/Scripts/python.exe -m mag.dirac_loop scan` -> `"betti1": 8, "n_loops": 6, "closed_solved": 6, "open_gaps": 0` (33 vertices / 21 edges / 20 components, ts 2026-09-28T23:50:51Z).
- `.venv/Scripts/python.exe -m mag.dirac_loop rank` -> `n_vertices 33, n_edges 21, components 20, betti1 8`.
- `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` read -> 6 rows, 2026-09-27T22:31Z .. 2026-09-28T02:59Z, each with receipt path.
- `.venv/Scripts/python.exe -m pytest tests/test_dirac_loop.py -q` -> `8 passed in 9.14s`.
- Multi-edge census on `mag.organ_map.operational_graph()` -> 21 edges / 18 undirected pairs / 3 duplicate pairs (P9).

## 6. Honesty notes

- The context-pack dirac line (`mag/context_pack.py:19-24`, rendered at `:931` and `:1057`) is **working-tree only right now**: `git status --short` shows ` M mag/context_pack.py` and `git show HEAD:mag/context_pack.py | grep -c dirac` returns 0. It is real code I read, not a landed organ yet.
- `988101f51`'s message says "7 tests" but the suite collects and passes 8 today (8 passed in 9.14s) - the count moved since that commit; both numbers are reported, not reconciled further.
- The ancestor disk file is a 09-14-content freeze; its MAP text is nonetheless byte-identical to the 08-14 first tracking. If the disk was meant to be an August snapshot, the snapshot postdates August by a month in content.
- The betti1-vs-enumeration gap (P9) is my own finding, observed in this session's run, cause identified in code; no fix attempted (read-only item).
- Em/en dash scan of this file: run after write, **0 occurrences** of U+2014/U+2013 (command below).
