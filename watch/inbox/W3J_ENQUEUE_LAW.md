# W3J - enqueue law: zombie census + graveyard (2026-09-29)

Lane: Mickey17 W3J (wave ledger return 18 enforcement). Files owned and landed:
`tools/enqueue_law.py` (297 lines, new) + `tests/test_enqueue_law.py` (171
lines, new, 8 passed in 0.57s). No commits made (lane law).

## The law built (disposable-clone, as speced)

Every enqueue lands or dies+epitaph within one cadence (default 7d,
`--days`). A ZOMBIE entry = `enqueued: true` strictly older than the cadence
whose target module does not exist on disk. Fresh enqueues to a missing
module are GRACE (evidence only); enqueues whose module exists are healthy
regardless of age. Fail-closed exit 2 on missing/unparseable ledger, rows
missing ts/piece/module/enqueued, naive timestamps, absolute or traversing
module paths, unreadable graveyard, or a prune target equal to the ledger.
Exit 0 clean / 1 zombies / 2 cannot verify (census_drift_patrol convention).

Effects: (a) census printout, (b) append-only idempotent epitaphs to
`memory/game/GRAVEYARD.jsonl` (frozen shape `{piece, module, times_enqueued,
first_ts, epitaph: "module never existed"}`, dedupe by piece+module),
(c) `--prune` writes `memory/game/flow_ledger.pruned.jsonl` (a COPY minus
zombie entries; original never reopened for write). The operator merges.

## The real census (2026-09-29, live run, exit 1)

179 ledger rows, cadence 7d, 0 landed pairs. All three pieces in the ledger
are zombies:

| piece | missing module | stale/total enqueues | first | last |
|---|---|---|---|---|
| nomic_rules_patch | mag/game_rules.py | 126/133 | 2026-08-17T10:12:20Z | 2026-09-29T23:58:45Z |
| diplomacy_multi_party | mag/game_diplomacy.py | 2/2 | 2026-08-17T12:56:53Z | 2026-08-17T12:58:30Z |
| pandemic_common_pool | mag/game_threat.py | 2/2 | 2026-08-17T12:57:18Z | 2026-08-17T12:59:10Z |

Byte-truth note on the return-18 claim: "174 times" was row-count prose; the
bytes say 133 actual enqueue events (enqueued: true) for nomic_rules_patch
across 175 rows. The census names instrument and denominator.

CRITICAL LIVE FINDING: nomic_rules_patch's last enqueue is TODAY
(2026-09-29T23:58:45Z) and 7 fresh enqueues sit inside the cadence past the
epitaph. The promising loop is still running; the epitaph is filed but the
writer (game_flow / FLOW_IMAGE freeze) does not read the graveyard yet.

## Proofs

- Tests: `pytest tests/test_enqueue_law.py` -> 8 passed (census names zombie
  not healthy; grace window; epitaph shape + idempotency; prune touches copy
  only, original bytes pinned; exit-2 paths; same-path prune refusal).
- Live idempotency: second real run printed `0 filed, 3 already buried`.
- Original untouched: `memory/game/FLOW_LEDGER.jsonl` sha256
  `7af8fdb4e14ff24709e8ad79a2f414ecff2d831cc62ac164de7919fced23c548`
  identical before and after `--prune`.
- Pruned copy: 130 zombie entries removed (126+2+2), 49 of 179 rows kept;
  fresh cadence-window enqueues and enqueued:false markers survive.
- Ratchet: `violation_ratchet.py check --changed` names no debt in either
  owned file (297/171 lines, under the 400 bar). The one NEW hit
  (mag/physical_compute_acquire.py, 606 lines) is another lane's file,
  untouched by this lane.

## Operator next steps

1. Merge or reject `memory/game/flow_ledger.pruned.jsonl` (the copy is the
   proposal; the original is the truth until you merge).
2. Decide the writer-side fix: the enqueue loop still promises to
   mag/game_rules.py today. Either land the module or teach the flow writer
   to check the graveyard before re-promising (return 18's improvement).
3. Optional: schedule `tools/enqueue_law.py` on the 08:30 patrol cadence;
   exit 1 is the HOLD signal naming any new zombie class.
