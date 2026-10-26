# THE HORIZON OBJECT - a math-only session boundary (2026-10-16)

Classification: CARD (design + first mint)
Producer: zcode-seat-20261016
First mint: `state/HORIZON_20261016.jsonl` (append-only, one line, n=1,
self_hash e49de722f705d814ac55b4de3ae5d17dae8da76d2647bf54a5926c63525f8e17)

## What it is

An entire session's state, compacted to mathematics: an append-only,
hash-chained, classifiable boundary object. Not a summary - a horizon. The
session is the bulk; the horizon is the only part another window ever needs
to touch.

## The physics the operator named, landed on real organs

1. **The boundary of black holes in relation to one another.** Bekenstein-
   Hawking: a horizon's entropy scales with its AREA, not its volume. So a
   handoff that grows with session length is a transcript pretending to be a
   horizon. The horizon object scales with the SURFACE: what crossed between
   this window and the mesh (receipts, deltas, predicates) - never with what
   happened inside. Two horizons relate through hashes (prev_hash, bulk
   anchors), never through shared interiors: boundaries touch, volumes don't.
2. **Holography is already estate law.** The rib_boot core law printed it
   verbatim: "chain=record, window=reasoning. Never store the window as
   truth." The verkle root (bulk anchor 5e5a8365... committed over the whole
   knot store) is the bulk-to-boundary map, running since the beginning. The
   horizon object just stops re-deriving it in prose.
3. **The Buddhist chariot (Nagasena).** The object carries `"self": null,
   "parts_only": true`. A seat has no essence - it is a designation over
   parts (receipts, ribs, invariants, hashes). Each window assembles a new
   chariot from the same parts stream; "the same seat" is a convention, and
   the ledger is what makes the convention true. Nothing in the schema says I.

## Self-steal - every field is an existing organ

| field | organ |
|---|---|
| bulk.verkle_root | memory/biography/verkle_tip.json (rib_boot chain anchor) |
| surface.* | the delta_index pattern (sha256+mtime pins, memory/mesh/delta_index.json) |
| wave.* | mag/hydrology.py (head = elev*256 + depth; integer Q8 waves over cross_sections) + the pheromone field (index_events.jsonl) + decay (percolator half-life) |
| trajectory.census | the 5,158/611/0 census vector |
| trajectory.free_lane | the hermes_247_free ledger rows ($0.00, tokens banked) |
| exit_clause.predicates | the patrol/patrol pattern (if-then over beacon state) |
| chariot | the no-self law; SUPERSEDED.md for anything that dies |

## Classifiability

The horizon is an object other organs consume without prose: drift-patrol can
pin its self_hash; the percolator can percolate its rendered signal line;
the append-only n/prev_hash/self_hash chain makes a sequence of horizons into
a chain of boundaries - window exit = mint event, mesh propagation = the
chain growing. The wave surface is the mesh reading its own head gradients.

## Falsifiers

- A horizon that cannot let the successor act without reopening the bulk is
  TOO THIN (undercommitted surface).
- A horizon that grows with session length is A TRANSCRIPT, not a horizon.
- Two windows rendering the same horizon must converge on the same entry
  actions (the render-contract test from the interpretive-layer card).
- If the exit-clause predicates cannot be evaluated from beacon bytes alone,
  the clauses are prose, not clauses.

## Next wire

Mint the horizon in the window-close ritual (generalizing
mag.state_snapshot.capture_summary from prose habit to math organ): compute
surface hashes, trajectory deltas, predicate states; append one line; the
beacon and the horizon together are the exit.
