# W3 CONSUME OP + ORPHAN CENSUS (2026-09-29, Mickey17 wave 3)

Lane: return 5 (inbox + registry). The finding was 96 percent write-only: the
event log had register/autoseal/amend/invalidate but ZERO read ops, 11,144
claimed orphans and 632 claimed dangling. This lane wires the missing read op
and runs the real drift-style join.

## Landed files

- `tools/inbox_consume.py` (new): the consume verb. Appends exactly one line
  to `watch/inbox/index_events.jsonl`: `{ts, op: "consume", file, consumer,
  note}`. Refuses ghosts, outside-surface paths and empty consumer names.
  Fold-verified design: non-register/invalidate ops are log-only markers, so
  INDEX.json is never touched; no seq/nonce (ts-keyed, the md_record_seal
  hook precedent). Path resolution reuses `mag.surface_rebuild._norm`, the
  fold's canonical normalizer.
- `tools/orphan_census.py` (new): read-only disk-walk join producing
  `watch/inbox/ORPHAN_CENSUS.json`. Classes: `never_registered`,
  `registered_missing`, `registered_never_consumed` (+ `consumed` telemetry).
- `tests/test_inbox_consume.py` (new): 9 tests over a fixture repo carrying
  the real log's path spellings (/board/inbox/ alias, B2-02 watch/inbox/
  prefix, drive absolutes, bare board/, repo files, double slashes,
  malformed grandfathered lines).
- `configs/events_key_schema.json`: `consumer` registered as a new event key
  with first-seen evidence (line 7037, 2026-09-30T00:24:19+00:00), per the
  B2-342 closed-vocabulary law; `op` carries note now names consume.

## Real test line

`./.venv/Scripts/python.exe -m pytest tests/test_inbox_consume.py -q`
-> `9 passed in 0.63s`

## The three real census numbers (2026-09-30T00:29:57+00:00 snapshot)

Instrument: `tools/orphan_census.py` over 7,038 parsed events / 3 malformed
(grandfathered), disk walk of 13,272 content files (controls skipped):

- **never_registered: 11,066**
- **registered_missing: 59**
- **registered_never_consumed: 2,207** (of 2,269 inbox-scope registered;
  3 consumed so far, all by this lane)

Worst offenders, never_registered: qdrop_export 4,979 + mrpool_export 2,842
(two export trees = 70 percent of all orphans), burn_wave_20260926 704,
.mimosa 522, gala_20260925 418.

## Delta vs the miner's return-5 numbers (attributed, B2-216 law)

Same order of magnitude on orphans (11,066 vs 11,144; disk grew during the
day). The 632 "dangling" decomposes under honest path joining into:
59 true dangling + 328 fold-blind `watch/inbox/`-prefixed registrations
(the B2-02 spelling the fold drops as OUTSIDE_RE but the log DID see) +
122 outside-surface registrations (drive absolutes, bare board/, repo files
like tools/ and memory/) + double-slash artifacts. The join counts each
bucket in `meta` instead of silently dropping them; `fold_blind_watch_prefix`
is the piece the fold itself is blind to and the surface-rebuild verb
should heal.

## Real consume events (the first read ops in the log's history)

consumer `zcode-mickey17-w3-20260929`, lines 7037-7039:
INDEX.json, SHARED_SURFACE_CONTRACT.json, MICKEY17_WAVE_LEDGER_20260929.md
(the three receipts this lane actually read before building).

## Fence compliance

No git commit. The event log was touched only by the three consume appends
above. INDEX.json untouched. Em-dash count in landed files: 0.
