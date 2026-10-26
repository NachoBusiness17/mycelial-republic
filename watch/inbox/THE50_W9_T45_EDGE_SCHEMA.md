# THE 50 - W9 T45 - Mycelium edge-schema migration plan

- **Filed:** 2026-09-19 (T45, week 9)
- **Scope:** migration plan for `memory/mycelium/edges.jsonl` (current schema `mycelium.v1`) vs a proposed `mycelium.v2` edge schema.
- **Hard rule honored:** NO destructive rewrite. Nothing in this plan deletes, truncates, renames, or field-drops existing rows. Every write path either appends, or writes a NEW file and keeps the old bytes as a timestamped `.bak`.
- **Status:** plan only. No code or data file was modified for this task. All findings below cite code lines read this session and audit commands run this session.

---

## 1. Current schema: `mycelium.v1` (as coded)

Owner module: `mag/mycelium.py` (`SCHEMA = "mycelium.v1"` at `mag/mycelium.py:41`). Edge constructor `_new_edge()` at `mag/mycelium.py:125-131` defines the canonical row:

| field | type | set by | notes |
|---|---|---|---|
| `schema` | str | all rows | constant `"mycelium.v1"`, no version negotiation on read |
| `id` | str | `_uid("e")` | unique in live data (0 dups, audit below); **never used for lookup** |
| `src`, `dst` | str | link/reinforce | self-loops (`src==dst`) are legal and written on purpose (see 3.4) |
| `type` | str | link/reinforce | one of 11 `EDGE_TYPES` (`mag/mycelium.py:58-61`), silent fallback `"related"`; **mutated in place** by reinforce (`mag/mycelium.py:175-176`) |
| `note` | str | link | max 500 chars |
| `weight` | float | default 0.5 | clamped to `PROTECTED_FLOOR` 0.4 or `PRUNE_FLOOR` 0.15 (`mag/mycelium.py:53-56, 179-182`) |
| `success_count`, `failure_count`, `contradictions`, `refs_in` | int | reinforce/contradict | counters |
| `last_used` | float epoch | reinforce/contradict | mixed time format vs `created` |
| `created` | ISO-8601 UTC str | link | |
| `protected` | bool | link | |
| `salience` | float | reinforce/contradict only | **optional cache**, absent on link()-created edges; stale by design |
| `decayed`, `decayed_at` | optional | `decay()` (`mag/mycelium.py:273-274`) | no un-decay path |

## 2. Current-state audit (run this session)

Command (`.venv\Scripts\python.exe -c` inline audit over both live files):

- `edges.jsonl`: **142 rows**, all stamped `mycelium.v1`.
- Field presence: the 14 core fields on all 142 rows; `salience` on **13/142**; `decayed` on **0**; `protected` true on **3**.
- Type distribution: `produced` 125, `consumption` 13, `handoff` 1, `depends` 1, `supports` 1, `evidence_for` 1.
- Integrity: 0 duplicate ids, 0 duplicate `(src,dst,type)` tuples, 0 dangling `src`/`dst` (all resolve into `nodes.jsonl`), 0 malformed timestamps (`last_used` all epoch floats, `created` all ISO strings).
- **31 self-edges (21.8%)** with `src == dst`.
- Adjacent finding (nodes side, affects edge resolution): `nodes.jsonl` has **260 rows, 233 unique ids, 27 ids duplicated** with conflicting rows. `_load_nodes()` keeps the last row per id (`mag/mycelium.py:98-99`), so a node's `type`/`title` can silently flip while edges still resolve.
- Baseline tests: `.venv\Scripts\python.exe -m pytest tests/test_republic_os.py -q` -> **8 passed in 0.92s** (this file monkeypatches `mc.EDGES`/`mc.NODES` to tmp, `tests/test_republic_os.py:11-13`).

## 3. Findings that motivate v2 (each cited)

1. **Read-modify-write without a lock.** `reinforce()`, `contradict()`, `decay()` all do full-file `_rewrite_edges()` (`mag/mycelium.py:201-205`) after an unlocked read. Concurrent writers exist today (`governor_autorun` cadence `mag/governor_autorun.py:1635`, `comms_trail` cadence, memlang verbs), so counter increments can clobber each other. The in-code comment "jsonl is append-only" at `mag/mycelium.py:183` is contradicted by the very next line, which rewrites the file.
2. **`type` is destroyed on consumption.** `reinforce(consumed=True)` overwrites `target["type"] = "consumption"` (`mag/mycelium.py:175-176`). The original relationship (handoff/supports/...) is lost forever; `refs_in` already records the consumption, making the mutation redundant and lossy.
3. **`salience` is a stale optional cache.** Stored on only 13/142 rows, never recomputed on write paths that do not call `salience()`. Every reader that cares (`status()` at `mag/mycelium.py:306`, `republic_os.py:175`) recomputes via `salience()` anyway, so the stored value has no authoritative role.
4. **Self-loops are intentional but undocumented.** Three writers create them by design: `mc.reinforce(nid, nid, etype="supports")` (`mag/comms_trail.py:160`), `reinforce(src, src)` / `contradict(src, src)` round-trip marks (`mag/republic_os.py:285, 288`), and the memlang `reinforce` verb `reinforce(r["spec"], r["spec"])` (`mag/memlang.py:268`). A migration that "fixes" self-edges would corrupt three live writers; v2 must keep them legal and document the semantics (self-loop = round-trip confirmation on one node).
5. **Mixed time formats.** `last_used` epoch float vs `created` ISO string. Both parse cleanly today (audit above); converting formats would touch every row for low value.
6. **No provenance.** No field says which seat/lane/verb created or last touched an edge. 142 edges, anonymous. Fleet-level graphs need `by` for trust weighting later.
7. **Raw readers bypass the module.** `mag/shape_map.py:162` and `scripts/build_knowledge_graph.py:10` read `edges.jsonl` directly (using `src/dst/type/weight`); `consumption_signal()` uses private loaders `mc._load_edges()` / `mc._load_nodes()` (`mag/comms_trail.py:202-203`). Any v2 change must keep those five fields byte-compatible.
8. **The contract table pins v1.** `MEMORY_CONTRACTS["reinforce"] = {"surface": "memory/mycelium", "schema": "mycelium.v1"}` (`mag/memlang.py:79`). A v2 rollout that flips this string alone would break the declared contract; it must move in the same commit as reader normalization.

## 4. Target schema: `mycelium.v2` (additive diff)

Design rule: **v2 rows are v1 rows plus new fields; v1 rows remain valid forever.** No field is renamed, retyped, or removed. Readers normalize both.

| change | v1 | v2 | mechanism |
|---|---|---|---|
| keep | all 14 core fields | unchanged | byte-compatible for raw readers (finding 7) |
| add | - | `by` : str (creating surface, e.g. `"lane:builder"`, `"verb:memlang.reinforce"`, `"comms_trail.capture"`; `""` for legacy) | written on new edges; `migrate_edge()` view defaults `""` |
| add | - | `origin` : str (free note of the creating call site) | optional, additive |
| stamp | `"schema": "mycelium.v1"` | new rows `"schema": "mycelium.v2"` | readers accept both values; per-row version preserved on disk |
| freeze | `type` mutated on `consumed=True` | `type` immutable | reinforce drops the mutation; `refs_in` (+1) already carries the consumption signal (`mag/mycelium.py:176` becomes `refs_in`-only) |
| demote | stored `salience` treated as meaningful | advisory cache only | `salience()` compute-on-read stays the single source of truth (both current consumers already recompute); no backfill needed |
| document | self-loops ambiguous | self-loop = round-trip confirmation, legal | doc + `salience()` unchanged; no data change |
| keep | mixed time formats | unchanged on disk | documented; optional new `last_used_iso` may be added later, additive only |

Explicitly rejected (would be destructive or high-risk/low-value): renaming `src`/`dst`, converting `last_used` to ISO in place, pruning the 31 self-edges, deduplicating `nodes.jsonl` in place, deleting `decayed` rows.

## 5. Migration plan (phased, each independently landable)

**P1 - In-memory normalization + additive writer (first landable slice)**
- Add `migrate_edge(e) -> dict` in `mag/mycelium.py`: returns a v2 view of any row (fills `by=""`, leaves everything else untouched). `_load_edges()` keeps returning raw rows; `status()` / public readers go through the view. Disk untouched.
- `_new_edge()` stamps `"schema": SCHEMA_V2 = "mycelium.v2"` plus `by`/`origin`; `link()`/`reinforce()` gain optional `by=""` kwargs (default keeps current behavior).
- Tests: new `tests/test_mycelium_edge_schema.py` following the tmp-path monkeypatch pattern of `tests/test_republic_os.py:11-13`: v1 row + v2 row both readable, `by` present on new edges, `type` no longer mutated on `consumed=True`.
- Check: `pytest tests/test_mycelium_edge_schema.py tests/test_republic_os.py -q` green.
- Rollback: revert the commit; zero data impact.

**P2 - Copy-first backfill (optional, only if stored v2 rows are ever wanted)**
- `python -m mag.mycelium backfill-v2` writes `memory/mycelium/edges.v2.jsonl` (full v2 projection) after first copying the live ledger to `memory/mycelial/edges.jsonl.bak-<utc>`. The original `edges.jsonl` is never opened for write by the backfill.
- `dual_write()` snapshot gains `"schema_versions": {"mycelium.v1": n, "mycelium.v2": m}` (additive key inside the already-regenerated snapshot cache, `mag/mycelium.py:235-240`; the snapshot is derived, the ledger is not).
- Check: row counts of `edges.v2.jsonl` == `edges.jsonl`; `python -m mag.mycelium status` unchanged (`nodes`/`edges` counts identical).
- Rollback: delete the `.v2.jsonl` copy; the `.bak` stays.

**P3 - Contract + concurrency hardening (gated follow-up, not required for v2)**
- Update `mag/memlang.py:79` contract row to `"schema": "mycelium.v1+v2"` in the same commit reader normalization lands (finding 8).
- Guard `_rewrite_edges()` with a lockfile (msvcrt on win32) OR switch reinforce/contradict/decay to append-only mutation records with periodic compaction into a NEW file + atomic rename, previous bytes kept as `.bak` (fixes finding 1 without a one-shot rewrite).
- Node-side dedupe (finding: 27 duplicate ids) belongs to a separate task; if attempted, same rule: write `nodes.v2.jsonl` + `.bak`, never in place.
- Check: two concurrent `reinforce` processes on a tmp store produce `success_count == 2` (currently racy).
- Rollback: revert; ledger untouched throughout.

## 6. Non-destructive guarantees (the ask's hard rule)

1. `edges.jsonl` is never deleted, truncated, or field-dropped by any phase.
2. Version upgrade happens in memory (P1 view) or in a new file (P2 copy); on-disk v1 rows stay v1 rows.
3. Any future compaction writes a new file and keeps the previous bytes as a timestamped `.bak` before rename.
4. The 3 `protected` edges and the 31 self-edges are carried through every phase unchanged.
5. Raw readers (`mag/shape_map.py:162`, `scripts/build_knowledge_graph.py:10`) keep working without modification because the five fields they use are byte-compatible.

## 7. Checks run during this ask

| check | command | result |
|---|---|---|
| edge audit | `.venv\Scripts\python.exe -c` inline counter audit over `memory/mycelium/edges.jsonl` + `nodes.jsonl` | numbers in section 2 |
| consumer map | `grep -rn "mycelium" --include="*.py"` over `mag/ tools/ scripts/ tests/ dashboard/`, then targeted `sed`/`grep -n` reads | section 3 citations |
| prior-work scan | `ls watch/inbox | grep -i "THE50_W9\|EDGE_SCHEMA"` + grep for `edge.schema\|mycelium.v2` in THE50 receipts | none found; this is the first edge-schema plan |
| test baseline | `.venv\Scripts\python.exe -m pytest tests/test_republic_os.py -q` | 8 passed in 0.92s |

## 8. Not run / open

- No pytest full-suite run (the full-suite census is a fleet-level gate, not this task's check; module-level baseline only). [2026-09-26: the "1,341-test" figure in this line was a hand-copied total, never byte-backed; retired by recount: 1,837 collected / 301 files, see AGENTS.md and watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md.]
- P2/P3 are proposals; no backfill or lock code was written or executed for this task.
- `mag/ghost.py:381` and `mag/swarm_health.py:136` consume `mc.status()` read-only and are unaffected by the plan; verified by reading their call lines only, not by executing those modules.

---

## 9. Re-verification 2026-09-25 (T45 re-seat, same task)

Re-seat on W9 T45. Every load-bearing claim in sections 1-8 was re-checked against the current tree and live data on 2026-09-25; the plan above is unchanged and remains the plan of record. No v2 code exists anywhere (`grep -rn "SCHEMA_V2|migrate_edge|mycelium.v2" mag/ tools/ scripts/ tests/` returns nothing), and `SCHEMA = "mycelium.v1"` is still at `mag/mycelium.py:41`.

- **Data audit reproduced exactly.** Re-ran the inline `.venv/Scripts/python.exe -c` audit over `memory/mycelium/edges.jsonl` + `nodes.jsonl`: 142 rows, all `mycelium.v1`, 14 core fields on all rows, `salience` on 13/142, `decayed` on 0, `protected` true on 3, type distribution `produced` 125 / `consumption` 13 / `handoff` 1 / `depends` 1 / `supports` 1 / `evidence_for` 1, 31 self-edges (21.8%), 0 duplicate ids, 0 duplicate `(src,dst,type)`, 0 dangling src/dst, 0 malformed timestamps, nodes 260 rows / 233 unique / 27 dup ids. Note: `edges.jsonl` mtime is 2026-09-24 15:22, i.e. the ledger was rewritten (reinforce/decay rewrites) between the original filing (2026-09-19) and this re-check, yet every audited invariant holds.
- **Code citations reproduced.** Read this session: `mag/mycelium.py:41` (v1), `:58-61` (11 EDGE_TYPES), `:125-131` (`_new_edge`), `:175-176` (`type` overwritten on `consumed=True`), `:179-181` (weight clamp), `:183-184` (append-only comment contradicted by `_rewrite_edges`), `:201-205` (`_rewrite_edges` full-file write), `:235-240` (`dual_write` snapshot), `:273-274` (`decayed`/`decayed_at`), `:306` (`status()` recomputes salience); `mag/memlang.py:79` (contract pins `mycelium.v1`), `:268` (memlang self-loop reinforce); `mag/comms_trail.py:160` (self-loop) and `:202-203` (private loaders); `mag/republic_os.py:285,288` (round-trip self-loops); `mag/governor_autorun.py:1635` (concurrent cadence writer); `mag/shape_map.py:162` and `scripts/build_knowledge_graph.py:10` (raw readers of `src/dst/type/weight`); `mag/ghost.py:381`, `mag/swarm_health.py:136` (read-only `mc.status()`); `tests/test_republic_os.py:11-13` (tmp-store monkeypatch).
- **Test baseline re-run.** `.venv/Scripts/python.exe -m pytest tests/test_republic_os.py -q` -> **8 passed in 0.41s** (this session).
- **Conclusion:** the v1->v2 additive diff (section 4) and the P1/P2/P3 phasing (section 5) are still correct against today's tree. P1 remains the first landable slice; nothing has been implemented, and no data file was modified by this re-verification (reads and test runs on tmp stores only).
