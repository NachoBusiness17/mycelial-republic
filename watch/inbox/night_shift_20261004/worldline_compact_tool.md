# WORLDLINE COMPACT TOOL - night shift 2026-10-04 (free-lane draft, $0)

Seat: zcode night-shift subagent, repo `local_sovereign_agent`, repo interpreter
`.venv\Scripts\python.exe` only. Deliverable: a dry-run-by-default inventory and
operator-gated compaction tool for `memory/worldline`, plus its test battery.
Nothing was committed; no seed file was touched; no paid API was called.

## The ask (operator brief, verbatim facts checked against disk)

Brief said: `memory/worldline/` holds 2,156 per-session SEED.json dirs, ~45MB;
~2,150 dwf-* workflow actor children; writer now gated. Byte truth at moment
2026-10-04T08:48:04Z (instrument: `tools/worldline_compact.py --check`, default
`--root memory/worldline`): the 2,156 dir ENTRIES reconcile as 2,153 seed dirs +
3 loose files (`REGISTRY.jsonl` 5,334 B, `readings.jsonl` 1,592,626 B,
`seat_seed_20260908_night.md` 5,735 B - counted in `other_files`, never touched).
The 2,153 seed dirs split 2,107 dwf- actor children (39,118,517 B of SEED.json
bytes) + 46 seat sessions (852,716 B); total SEED.json bytes 39,971,233 (~38 MB
metric; the ~45MB headline rides dir overhead + the loose files - different
denominator, named here per the census-denominator law). All 2,107 dwf seeds
were minted 2026-10-03T20:58:53Z..22:16:40Z - one ~78-minute flash window, 98
distinct dwfrun ids. Seat seeds span 2026-09-07..2026-10-03.

## Measured dedupe potential (the real tree, instrument `--check`)

Criterion: a dwf seed is compactable when the canonical JSON bytes of its
genome+invariants slabs hash equal to the NEWEST seed of its created_utc minute
(tie-break session_id; record/position slabs differ per actor and are never
compared; seat seeds are never compacted).

- 2,040 of 2,107 dwf seeds (96.8%) are compactable duplicates.
- Compactable bytes: 37,874,587 B of 39,118,517 B dwf bytes (96.8%).
- 67 dwf minute buckets (median 34 seeds/min, max 50); 0 multi-variant minutes,
  0 unkeyed seeds - so the strict newest-of-minute metric and the per-minute
  cluster grouping coincide exactly on today's tree (both instruments named).
- Compaction leaves 67 dwf seeds in place (66 lineage-group keepers + 1
  singleton minute) + all 46 seat seeds; the plan groups those keepers into 66
  lineage rows with 2,040 members. A probe plan built against the real tree to
  a temp path parsed back clean: 66 groups, 2,040 members, 37,874,587 B, plan
  markdown 1,060,898 B (probe then deleted; no inbox artifact minted).

Cross-check: an independent ad-hoc sha256 pass over the same tree (before the
tool existed) produced the same 2,040 / 37,874,587 - tool and hand instrument
agree to the byte.

## The tool (files on disk)

- `tools/worldline_compact.py` (238 lines) - CLI + the three modes + the
  operator gate. Law docstring: the spray disease
  (watch/inbox/PROCESS_IMPROVE_WAVE1_20261003.md finding 3 + the writer gate
  mag/knot_at_close.py `_worldline_seed_hook` / tests/test_worldline_seed_gate.py),
  the never-delete-without-GO law, dedupe criterion, exit contract.
- `tools/worldline_compact_io.py` (322 lines) - the read-only byte layer (scan,
  slab keying, dedupe metric, report/table render, plan build/render/parse).
  Split keeps both files under the ratchet's 400-line cap (B2-248/B2-365
  precedent); one-way import. `tools/violation_ratchet.py check --changed`
  shows ZERO new debt from these two files (the two NEW rows it prints are
  sibling lanes' mag/route_chat.py + tools/dungeon.py, pre-existing).
- `tests/test_worldline_compact.py` (9 tests, tmp-path fixtures: three
  identical-slab dwf seeds in one minute + a divergent dwf seed + one seat
  seed) - pytest -q result: 9 passed in 0.74s (2026-10-04, repo venv).

## Usage lines (repo interpreter only; never bare python - PATH python is Hermes)

    .venv\Scripts\python.exe tools\worldline_compact.py
    .venv\Scripts\python.exe tools\worldline_compact.py --check --root PATH
    .venv\Scripts\python.exe tools\worldline_compact.py --plan
    set WORLDLINE_COMPACT_GO=1 && .venv\Scripts\python.exe tools\worldline_compact.py --execute --plan watch\inbox\worldline_compaction_plan_<date>.md

- `--check` (default): read-only inventory. stdout = human table, then the JSON
  summary between the `WORLDLINE-COMPACT-JSON-BEGIN` / `-END` marker lines
  (canonical shape, B2-245 lesson: parse only from the markers).
- `--plan [PATH]`: writes ONE markdown plan (default
  `watch/inbox/worldline_compaction_plan_<date>.md`; never overwrites an
  existing artifact - exit 2, pick a fresh name). Plan = law block + lineage
  table (one keeper per identical-slab group) + every member listed with its
  full-file sha256 + a fenced ```json machine block. Touches no seed file.
- `--execute`: FAIL-CLOSED. Refuses (exit 2, prints the operator-ask) unless
  BOTH env `WORLDLINE_COMPACT_GO=1` AND `--plan <file>` name the reviewed
  bytes. Then two-phase verify-then-move: every keeper/member is re-keyed and
  re-hashed against the plan BEFORE the first move (a stale tree aborts with
  zero moves); members are MOVEd to
  `memory/worldline/_compact_archive/<stamp>/<session_id>/` - never unlinked -
  and every move appends a row to `_compact_archive/MANIFEST.jsonl` (ts,
  session_id, from, to, slab_key, seed_sha256, plan_path, plan_sha256).
  Live-proven on the real tree: without GO the run refused, exit 2, nothing
  moved.

Exit contract: 0 = reported / planned / moved; 2 = cannot verify (gate closed,
plan missing/unusable/root mismatch/stale tree/archive collision). There is no
exit 1: this is an inventory + gated-fold tool, not a tripwire.

## The operator gate (what GO means here)

Estate law: NEVER delete sibling data without operator GO. The tool encodes it:
default mode is read-only; `--plan` writes only into watch/inbox; `--execute`
needs the env GO plus the named plan, and even then the only effect is a MOVE
into `_compact_archive` with a manifest trail - no code path in this tool
unlinks a seed. The ask, when it refuses, prints itself: review the plan's
lineage rows and member sha256s, then set `WORLDLINE_COMPACT_GO=1` and rerun
with `--plan <that file>`.

Expected effect if the operator GOes tonight's numbers: 2,040 seed dirs
(37,874,587 B) leave `memory/worldline/` for `_compact_archive/20261004/`;
67 dwf keepers + 46 seat seeds + REGISTRY.jsonl + readings.jsonl stay.

## Untouched siblings / notes

- The writer gate (disease cure) already landed earlier on 2026-10-03; this
  tool is the read-side fold only. No changes to mag/, no commit, no index
  events appended (the inbox md autoseal hook owns registration).
- `--check` treats `_compact_archive` as cold storage (skipped by every mode),
  so a future re-run after GO counts only the living tree.
