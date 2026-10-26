# D8 LANDED - decay-family supersession lineage (2026-10-05 morning)

Door: D8-decay-family-schema - "port superseded_by/valid_at from
mag/republic.py into lattice_edge.v1 + mycelium, then mycelium.v2",
with the pre-gate falsifier "read supersede() first (letter-DAG shape
may not express edge supersession)".

## The falsifier's answer (read first, as ordered)

The letter law DOES express edge supersession - with one named
adaptation: republic letters are FROZEN after delivery (only
superseded_by + trail mutable), but a mycelium edge is a LIVING
measurement (weight, counters, last_used mutate by design through
reinforce/contradict). The port freezes ONLY the lineage fields:
superseded_by (set once, never re-pointed, target must exist in the
same book, no self-supersession - republic :209-218 verbatim) and
valid_at (immutable once set). Weight stays mutable: the guard admits
it explicitly (test_rewrite_guard_blocks_repoint_and_valid_at_edit
ends with a legal weight rewrite).

## What landed

**mag/mycelium.py**:
- EDGE_SCHEMA = "mycelium.v2": new edges carry superseded_by=None +
  valid_at=<creation ts>. Nodes stay v1 (the door is edges-only).
- supersede(edge_id, by_edge_id, reason): the sanctioned operation -
  set-once, target-exists, no-self; reason rides the note with a
  "superseded:" prefix. Never deletes (the ZEITGEIST law: a superseded
  fact keeps its lineage so the network can replay how it changed its
  mind).
- _rewrite_edges carries the ENFORCED-IMMUTABLE GUARD (the republic
  charter "the guard is in code, not in prose" ported): for every disk
  edge, re-pointing refused, first-set requires the target in the same
  book, self-supersession refused, valid_at immutable once stamped.
  v1 rows read as live-forever (fields absent = None; the guard skips
  what was never set).
- Reads unchanged by design: salience/neighborhood/reinforce/contradict
  behave identically; traversal semantics against superseded edges is
  the NEXT door's call, not smuggled into the schema port.

**mag/lattice_backfill.py**: all four lattice_edge.v1 emit sites
(day_bond, instrument_chain, session_dig, residual_bond) carry
superseded_by=None + valid_at=<later endpoint's date, honestly None
when unanchored> (_edge_valid_at helper; the edge exists from the
moment both endpoints do).

**tests/test_mycelium_supersede_20261005.py** - 7 passed: v2 lineage
fields at birth, set-once + refuse-re-point, target-exists +
no-self, the rewrite guard (blocks re-point, blocks valid_at forge,
admits weight mutation, admits the one legal None->existing move),
v1 back-compat (never-stamped rows read live and reinforce keeps
their shape), lattice emit-site contract (all four sites stamped).
The v1 test's first draft failed CORRECTLY: it forged a v1 row by
popping fields off a stamped edge, which is exactly the forgery the
guard refuses - the test now mints a never-stamped row instead, and
the refusal stands as a proven behavior.

Production read smoke: 744 edges load clean (744 v1, 0 v2 - no
production writes made; v2 rows mint as new links land). Lattice
backfill CLI runs rc=0. Ratchet PASS.

## The incidental catch (worth more than the door)

Mid-landing, a `git stash` tripped on the D5 errno-22 lock class
(the daemon holding runner_state files through the cage bind mount)
and half-reset the tree. The recovery exposed a SILENT-DROP class:
the eleven-doors ledger is tracked as watch/inbox/ractor_engine/
(LOWERCASE) while the night-shift commits all added it via
RACTOR_ENGINE - on the case-insensitive FS the adds never reached the
index, so the four night strikes existed only in the working tree,
which the half-failed reset then wiped. Recovered byte-exact from the
stash and re-committed under the tracked case (9d3b4b572). LAW: git
add path case must match the index recording on case-insensitive
filesystems - check `git ls-files` case before adding a file you did
not create. The stash@{0} entry is kept as the forensic artifact.

Banked by GLM-5.3 window, 2026-10-05.
