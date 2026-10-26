# CASCADE-PORT RECEIPT (gala_20260925 build-it-all, division B, lane cascade-port)

Date: 2026-10-03. Lane file: `watch/inbox/gala_20260925/build-it-all/lanes/cascade-port.json`.
Raw check output: `watch/inbox/gala_20260925/build-it-all/lanes/cascade-port.check.txt`.

## WHAT THE DANCE OWED

Port the cascade per the localfirst-steal atlas lane's spec
(`watch/inbox/localfirst/atlas.md` section 4, the cascade ledger spec): add
`depends_on` keys to `memory/percolator/invariants.json` rows, write the cascade
function that re-evaluates dependents when a parent invariant changes, emit
cascade PROPOSALS (never mutations; proposals go to the review pass). Owner of
`mag/percolator.py` additions + the cascade test. The gap being closed: the
percolator's promote gate compiled invariants but never re-evaluated dependents
when a parent moved (atlas.md section 3 confirmed it at data level: 639 rows,
zero dependency fields).

Ticket note: the named CP-1 ticket was not found as a standalone file (searched
`queue/`, `memory/frontier/HELP_WANTED.md`, the gala_20260925 wave dirs w1/w2/w3/
rung, and the localfirst-steal lane outputs; zero CP-1 hits). The ask's own
finish line was used as the ticket contract. Everything below is measured
against that finish line.

## FINISH LINE, MET

1. **invariants.json rows carry depends_on keys** - DONE, byte-verified. Every
   one of the 639 rows now carries `depends_on` (0 missing, verified
   post-apply); 13 rows carry 13 real mined edges, 626 carry `[]`. Pre-edit
   bytes backed up to `memory/percolator/invariants.json.bak-cascade-20261003`;
   post-apply verification proved text/counts/timestamps identical to the
   backup and total count 1187 unchanged (check file, CHECK 4).
2. **The cascade function emits proposals (never mutations)** - DONE. `cascade()`
   in `mag/percolator.py` BFS-walks reverse `depends_on` edges (dependents
   first, visited-set cycle guard, max_depth 10 / max_nodes 5000,
   shallowest-first: the Atlas RippleEngine shape) and emits one proposal per
   dependent to the review pass (`memory/percolator/cascade_queue.jsonl`, status
   pending, promoted False) plus a chained receipt
   (`memory/percolator/cascades.jsonl`, schema `invariant_cascade.v1`,
   `cascade_id = sha256(prev|origin|proposals)[:16]`, prev_cascade_id chained).
   Route per origin change: escalate (origin absent, or kind
   removed/superseded/expired) or refresh (premise holds). The function NEVER
   writes `INVARIANT_REGISTRY` in any mode - test
   `test_cascade_never_mutates_registry` byte-compares the registry
   before/after across refresh + removed + default-change cascades. A
   compute-only dry run against the live 639-row graph fired 6 depth-1 refresh
   proposals for the six "path outside jail" container rows of parent
   `4cfd5d7d94dff7a4` and minted nothing (write=False; no queue/ledger files
   exist on disk after the run - check file, CHECK 5). No live write=True
   cascade was fired this session: no real parent change event occurred, and
   firing one without a real change would mint a false receipt.
3. **A test proves the cascade fires on a dependency change** - DONE, exit 0.
   `tests/test_percolator_cascade.py`, 12 tests passed
   (`pytest tests/test_percolator_cascade.py -q` -> "12 passed in 1.24s"); the
   proof test is `test_cascade_fires_on_dependency_change` (parent count change
   -> depth-1 refresh proposal for the dependent, pending queue row, chained
   ledger row). Regression: `tests/test_percolator_z15.py` +
   `tests/test_percolator_candidates.py` -> 24 passed.

## WHAT LANDED (mag/percolator.py additions; the ask's owned surface)

- `declare_depends_on(canonical, parents)`: DECLARED mode (atlas spec 4.1) -
  fold-time declaration, merges invariant-kind edges, all-or-nothing validation
  (unknown parent / self-edge / empty key reject the whole call before any
  append; registry bytes untouched on reject, test-proven).
- `mine_depends_on(apply=False|True)`: MINED mode, deterministic + $0 - (a)
  16-hex hash citations (row text cites another row's canonical key) and (b)
  substring derivations (row text byte-contains another row's text,
  >= MIN_EDGE_TEXT_LEN 12 chars: the container's compiled signal includes the
  child's sentence). Report mode writes nothing; apply mode merges (never
  removes) existing edges, adds the key to every row, backs up pre-edit bytes,
  saves via the sanctioned atomic writer. On the live registry: 0 hash
  citations + 13 substring derivations, matching an independent pre-implementation
  scan exactly (check file, CHECK 3).
- `cascade(origin, change=..., max_depth=10, max_nodes=5000, write=True)`: the
  cascade above. write=False is pure compute.
- CLI: `--cascade KEY [--change-kind K] [--old V] [--new V] [--dry]`,
  `--mine-depends-on [--apply]`; `status()` now names both cascade surfaces.
- Docstring + section comments carry the receipt pointers (atlas.md spec, CP-1
  port, laws).

## LAWS KEPT

- PROPOSALS, NEVER MUTATIONS (the ask's law, and an upgrade over the atlas
  spec): the atlas spec auto-applies its REFRESH bucket; this port does NOT.
  Every route is a pending review-pass proposal. Atlas's unwired AUTO_APPLY
  (atlas.md defect 2.1) is the named anti-pattern avoided.
- Same alpha-budget discipline as the --candidates ingest: this port's review
  files never edit `invariants.json` rows.
- Edges are byte-level deterministic (hash citations + substring derivations);
  no judgment-mined edges were fabricated for the live file.
- No em-dashes in lane-written text (grep U+2014 over the test file, the check
  file, and the git-diff-added lines of mag/percolator.py: 0 matches each).
  The ratchet tool's own print format contains em-dashes; that is not
  lane-written text.

## GATE STATUS (honest)

`tools/violation_ratchet.py check --changed` exits 1 (check file, CHECK 6).
Decomposition:
- The TWO NEW violations (except-pass `tools/cialdini_scanner.py:53`,
  file-too-long `tools/lru_null_arm.py:602`) are in files this lane never
  touched (sibling lanes' concurrent working-tree edits). `baseline-update` is
  global (registers all unregistered tree debt, `tools/violation_ratchet.py`
  cmd_baseline_update L284-316), so this lane did NOT run it: it would register
  sibling debt under this lane's name. The two NEW hits belong to their owning
  lanes / the operator.
- This lane's file `mag/percolator.py` carries ZERO NEW violations; its only
  ledger fact is the B2-273 GROWTH claim (file-too-long accepted at 580 lines,
  now 1022, +442 - the cascade port itself: declare/mine/cascade/CLI/docstring,
  additive, no existing behavior path rewritten). Re-audit is recorded here;
  re-accept-by-name (`baseline-update --by`) is left to the operator because the
  command cannot be scoped to one file.

## HONEST GAPS

- The atlas spec's fact-kind dependency edges (census, file-sha, law-status,
  queue-state, receipt-exists, atlas.md section 4.1) and their instrument
  registry are the UNBUILT half: traversal uses invariant-to-invariant edges
  only, per the ask ("which invariants depend on which"). The schema tolerates
  spec-form fact edges (kind != "invariant" is ignored by traversal) so the
  instrument half can land later without a schema break.
- No live write=True cascade fired this session (no real change event; see
  finish line 2). The queue and ledger files will be minted by the first real
  cascade.
- The escalation path's real-world consumer (which lane resolves a pending
  proposal) is the review pass's to define; proposals sit at status pending
  with promoted False until then, mirroring the candidates review pass.

## DECISION LEDGER

Closes the atlas lane's decision "the estate port of downstream re-evaluation
is specced as the cascade ledger" from SPEC to CODE: the promote gate now
re-evaluates dependents - `mag/percolator.py` carries the dependency graph
(declared + mined edges on all 639 rows) and the proposal-emitting cascade, so
the localfirst cascade-ledger port decision is no longer pending an executor.
One deliberate divergence from the spec, on the record: REFRESH does not
auto-apply; all routes go to the review pass as proposals.

## FILES THIS LANE WROTE / TOUCHED

- `mag/percolator.py` (additions only: docstring section, deque import, cascade
  constants + 3 functions, status() fields, CLI flags)
- `tests/test_percolator_cascade.py` (new, 12 tests)
- `memory/percolator/invariants.json` (depends_on backfill, additive, backed up)
- `memory/percolator/invariants.json.bak-cascade-20261003` (pre-edit bytes)
- `watch/inbox/buildall/cascade-port.md` (this receipt)
- `watch/inbox/gala_20260925/build-it-all/lanes/cascade-port.json` (lane out)
- `watch/inbox/gala_20260925/build-it-all/lanes/cascade-port.check.txt` (raw checks)
