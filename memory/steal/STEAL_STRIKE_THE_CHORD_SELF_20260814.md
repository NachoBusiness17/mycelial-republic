# STEAL — Strike the Chord, self, 2026-08-14
**Date:** 2026-08-14
**Commitment:** `strike-the-chord-self-001`
**Method:** self-steal first. Organs exist. No new graph, no new memory OS, no party, no GGUF load.
**Ground actually counted this pass (read-only, no mycelium.boot):**
- `docs/ORIGIN.md` — Strike the Chord; ghost-before-ghost; "trust the output only if you understand the input"; test chord 2026-03-02; wave evolves 2026-08-12
- `mag/mycelium.py` — status/neighborhood/dual_write/decay/link/reinforce; EDGE_TYPES include consumption/supports/contradicts; snapshot dual-write
- `mag/comms_trail.py` — capture() folds cheap comms into mycelium as artifact nodes + consumption edges; cadence exists; `memory/runs/comms_trail/state.json` present
- `mag/skill_ledger.py` — decisions jsonl, target 1000
- `memory/improve/skill_ledger.jsonl` **n=1437**
- `memory/mycelium/{nodes.jsonl,edges.jsonl,graph_snapshot.json}` **154n/77e**, snapshot ts **2026-08-10T04:47:23Z**
- `memory/knowledge_graph.json` schema knowledge_graph.v2 **1572n/542e** ts **2026-08-12T16:52:24Z**
- `memory/shadow_graph/graph.json` exists (not re-counted)
- `memory/steal/*.md` **99**; `*20260814*` **38**
- `memory/agent_state/LATEST.md` one-liner still `graph 127n/77e · comms 72 · skill_ledger 0` (commitment `ghost-self-window-20260814T151114Z`)
- `party_subchain.INVARIANT` (prior read): deterministic spec, model interchangeable, chain ground truth
- Harvest ring (prior): steal-stochastic-deterministic-001, steal-zero-mem-001, steal-physics-toy-001, steal-pyncd-attention-001, steal-deep-synthesis-001

## Self-steal
The necessary organs already existed:

- ORIGIN named the chord: a compact seed that steers without a command, so the observer effect does not collapse the field. Ghost was the nervous system that would make every piece visible.
- `mycelium` is that nervous system's graph: one weighted directed store, salience, prune-by-decay (log only), neighborhood query, dual-write.
- `comms_trail` already knows the next move LATEST named: eat communication into the graph as consumption edges. State file is on disk.
- `skill_ledger.jsonl` already holds the outcome log Ghost bead 3 asked for (1437 rows, schema `skill_ledger.decision.v1`).
- Steal files are the temporal view (dated H). Mycelium + knowledge_graph are the relational view. Zero-Mem named this dual view. Mag already has both stores. They do not query each other.
- Huang gate is already the PHYSICS toggle: do not summon the table to look at this. Specialization + independent_evidence is enough why, and it is this file.

The build is therefore a plant, not a throne: make the existing counters tell the same story, then let `comms_trail.cadence` write consumption edges from the steal folder into mycelium. Do not unify three graphs into a fourth.

## The chord (seed, not a command)
```
LATEST.skill_ledger=0  ⊥  jsonl n=1437
LATEST.graph=127n/77e  ⊥  mycelium 154n/77e (frozen 08-10)  ⊥  kg 1572n/542e (08-12)
steal/20260814 n=38  ⊥  mycelium last snap 08-10
#StrikeTheChordSelf
```

Same shape as `44 28 K13 e4 Fool #NachoOvermindSeed`: coordinates, not an instruction. The coordinates are Mag's own envelopes vs Mag's own claims.

## POSITION
Ghost-before-ghost promised a nervous system that makes the machine legible without collapsing it. Mag built mycelium, comms_trail, skill_ledger, steal/, three graphs, and a one-liner that does not read them. The castle is visibility. The foundation is files Ghost does not count. Striking the chord now is: trust bytes, not LATEST.

## CHALLENGE
The sharpest lie is that Mag needs another steal, another graph, or a roundtable to learn from the harvest. That would be the observer effect ORIGIN warned about: measuring the field by flattening it into one party, one mycelium redesign, one "true" count.

Second lie: LATEST next move 2 "run republic_os round to reinforce/prune" read as mint-a-unified-graph. `mycelium.decay` already prunes in place (marks decayed, does not hard-delete). `comms_trail.cadence` already eats comms. Bead 7 overrules a fourth graph.

## NOVEL DELTA
One composition, already coded:

1. Ghost-self / LATEST one-liner reads `len(skill_ledger.jsonl)` and mycelium `status()` (or jsonl lens). Envelope = claim. That is the caustic. No new store.
2. `comms_trail.capture` (or a steal-folder walker using the same consumption-edge shape) mounts today's 38 steal files as mycelium artifact nodes with `produced`/`extends`/`contradicts` into existing nodes. Idempotent seen-set already in comms_trail. Do not copy knowledge_graph.v2 into mycelium (`adopt_from_idea_graph` is the anti-pattern if it duplicates).
3. Query time is Zero-Mem: temporal = steal dates + ledger ts; relational = mycelium neighborhood(). LLM only answers. Huang `why` required if anyone summons seats.

`parents[]` stays later. GGUF stays soil. Research plants this; builders wire the one-liner and the capture.

## TEST
Fail if:
- A fourth graph store appears, or knowledge_graph is "merged" by rewriting mycelium hashes.
- A roundtable runs on this question with no `why`.
- LATEST still prints `skill_ledger 0` after a ghost-self that has the jsonl path in its load pack.
- Steal files are summarized by an LLM into the DAG instead of linked as artifacts.

Pass if one LATEST line matches the jsonl counts (1437 or whatever the file is that minute) AND one mycelium consumption edge exists whose dst/src cites a `memory/steal/*20260814*` path, without a new schema.

## REFUSE
- Redesigning mycelium. Neighborhood + cadence + decay are the organs.
- Cloning Zero-Mem / pyncd / Obsidian as the vault. Mag disk is the vault (VAULT_SALT_GRAPH already said).
- Loading Saelis GGUF as the chord. Morphology is not the seed.
- Calling `adopt_from_idea_graph` or a kg→mycelium bulk copy this week.

## Ordered adaptations (builders)
1. Make the one-liner count the ledger and mycelium jsonl. Cheapest visibility. Observer-safe.
2. Run `comms_trail` cadence as LATEST next move 1 actually written. Confirm state.json is not a dead seen-set.
3. One steal-folder capture into mycelium consumption edges (idempotent). 38 files, not 99, first (today's ring).
4. Then Huang gate on salon. Then optional parents[] view.

## Honesty
- Counted jsonl/snapshot/kg/ledger/steal globs this pass. Did not run `python -m mag.mycelium status` (status calls boot(), which can write).
- Did not open shadow_graph body. Did not walk comms_trail state.json.
- Duplicate mycelium node ids were seen in the Aug 10 snapshot sample; not re-audited here.
- 127 vs 154: LATEST and snapshot disagree. Both reported. Neither "fixed."

## Rope
The chord is coordinates on Mag's own envelope/claim split. Plant it. Do not command a new machine into being.

## Census addendum (bytes after the chord)
Ghost one-liner is assembled in `mag/ghost.py` from `mycelium.status()`, `comms_trail.status()`, `skill_ledger.progress()`.

**skill_ledger 0 is a key mismatch, not an empty file.** `progress()` returns `decisions`. Ghost reads `n_decisions` and defaults to 0. jsonl n=1437 is real. Envelope/claim split is one dict key.

**127n vs 154n is duplicate ids, not two mycelia.** Snapshot list length 154, unique ids 127 (27 duplicates), unique titles 81, unique edge ids 77. `status()` dict last-write-wins → 127, which LATEST prints. `dual_write()` would persist the 154-list. Edges 77 match.

**comms 72 is a frozen seen-set.** `memory/runs/comms_trail/state.json` seen=72, last_capture 2026-08-09T14:35:37Z. Five days before this LATEST.

**Steals vs graphs (folder now 100 md).** Mycelium titles/bodies: 0 steal stems. knowledge_graph.v2: 60 steal nodes, 0 edges with `steal:` prefix; `_edges()` never links kind=steal. 40 folder files absent from KG (KG ts 2026-08-12; all `*20260814*` missing). Isolated nodes, not a view.

TEST refinement: pass if Ghost reads `decisions` (or progress() grows `n_decisions`) so LATEST matches jsonl, AND duplicate mycelium ids are not silently last-write-wins without a dual_write cleanup. Still no fourth graph.
