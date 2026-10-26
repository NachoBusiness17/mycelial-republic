# gps_dedupe - lane 2 receipt, MICKEY17 V2 GO item 2

Lane: gps-dedupe (REFIRE; the first dispatch died in a provider burst before landing anything).
Moment: 2026-10-04T09:31-09:37Z. Executing `corpus/steal/MASTER_MICKEY17_V2.md` section 9 GO item 2
(a04-arena-gwap-gps#1/#2/#4/#6, a01-arena-cadence#5; a15 rank 2, former GO item 1).
Evidence rows: `memory/runs/mickey17_v2/runs/run-0/lanes/a04-arena-gwap-gps.json` (rows 1-5),
`memory/runs/mickey17_v2/runs/run-0/lanes/a01-arena-cadence.json` (row #5).

## Prior-attempt verification (before building)

`git status --porcelain tools/gps_mcp/ mag/gwap_to_gps.py` returned EMPTY: the dead prior attempt
left zero partial gps files. But the dedupe work was NOT virgin ground: commit `c3ff9d1bd`
("GPS DEDUPE (ladder escalation)", 2026-10-03 23:16:59 -0400, verified via
`git show --stat --format=%ci c3ff9d1bd`) had already landed the SELECT-based INSERT-that-skips in
`record_verdict` plus the first migration (81 duplicate rows removed, 4 arena capability rows
rebuilt; its pre-migration byte-copy sits at `tools/gps_mcp/gps_ledger.db3.bak-20261004`,
sha256 `560458b9dee651a9ff11bb179fc8b2d41d04fc825dc67135329b17705f538109`, gitignored via
`.gitignore:10 *.bak-*`). This lane built the missing legs on top; nothing c3ff9d1bd did was redone.

## Sub-item 1 - UNIQUE triple + INSERT-that-skips (a04#1, a04#2, a04#4)

`tools/gps_mcp/ledger.py`:

- `SCHEMA_SQL` gains the partial unique index
  `ux_verdict_log_evidence_triple ON verdict_log (model_id, task_shape, evidence_hash)
  WHERE evidence_hash <> ''`. Partial is load-bearing: the live db carries 6 hash-less
  `('z-ai/glm-5.3-prime','night-judgment')` rows and hash-less verdicts are distinct
  observations by definition (proved by `test_hashless_verdicts_stay_legal`).
- `init_schema` gains the index on every open, so legacy dbs self-migrate; a legacy db still
  holding duplicate triples FAILS CLOSED at open with sqlite3.IntegrityError (the migration
  contract, pinned by `test_legacy_db_with_duplicates_fails_closed_at_open`).
- `record_verdict` INSERT-that-skips: the c3ff9d1bd SELECT fast path stands, now backed by the
  index as the race layer - a lost race (hourly cron vs manual backfill feeding the same triple
  concurrently) returns the winner's unchanged standing flagged
  `evidence_status="duplicate-skipped"` instead of crashing or stacking a row. Discriminator
  reads the violated columns ("verdict_log" + "evidence_hash" in the message) because sqlite
  reports index violations by column list, not index name - observed live:
  "UNIQUE constraint failed: verdict_log.model_id, verdict_log.task_shape,
  verdict_log.evidence_hash". Any other integrity failure still raises (proved by
  `test_non_triple_integrity_failure_still_raises`).

## Sub-item 2 - .bak pattern migration of the live db3

Command run 2026-10-04T09:2xZ (inline python, shutil.copyfile byte copy, then in-place index
creation; full output banked in this session):

- PRE db3 sha256 `3c5de726392c335d28b68a4eed08c7f10bffee35d262f433babdf93f464046c2` (94208 bytes)
- BAK file `tools/gps_mcp/gps_ledger.db3.bak-20261004-gpsdedupe`
- BAK sha256 `3c5de726392c335d28b68a4eed08c7f10bffee35d262f433babdf93f464046c2`
  (byte-copy equality asserted in the run)
- POST index_list(verdict_log) = ['ux_verdict_log_evidence_triple']; verdict_log rows 494 before
  and after (zero rows moved); POST db3 sha256 at migration moment
  `bbca0a77f32d9a205c549f36e1f9fd53f085b0a00a93d294792c91e98b44b26d`
  (the file moves by design on every feed; the bak is the frozen pre-index bytes).

## Sub-item 3 - the failable backlog fed through the fixed path

Moving-tree census at 2026-10-04T09:31:34Z: chain `memory/runs/gwap/arena-capability.jsonl` 491
rows (last ts 09:07:46Z), failable (VERIFIED_AGREE+DISPUTE) 330, fed into gps 252, UNFED 78.

- First attempt `.venv\Scripts\python.exe tools\arena_gwap.py --backfill` (09:31:45Z) REFUSED:
  `GwapToGpsError: scene_id 'arena-tavern_20261004T083959Z-Brother Oswin' missing from
  scene_to_model`. Cause: the dir was deleted from playground after banking; chain seqs 460-465
  (6 scenes from `tavern_20261004T083959Z`) became unresolvable from disk, and the feed's
  whole-file law refused rather than guess keys. Zero rows written (pass-1 rejection).
  Census: exactly 6 of 391 chain scenes unresolvable; all 6 from that one dir.
  Why the dir is gone: `watch/inbox/go_wave_20261004/tavern_refresh.md` line 20 - the p0/p2
  collision (both launches stamped 083959Z, interleaved transcripts) was quarantined to
  `watch/inbox/playground/scenarios_lane9/void_stamp_collision_tavern_20261004T083959Z/`.
  This also explains why gps was stale since 03:16:56Z: the cron's post-08:41 feeds hit the
  same refusal.
- Identity byte-recovered (no guesses): the quarantine dir's transcript rows carry `actor` AND
  `model` per call, cross-checked against its surviving `scenario.json` personas - the two
  sources AGREE exactly (asserted in the run): Brother Oswin haiku-4.5, Greta Thornwood
  sonnet-5.5, Ilse Marrow haiku-4.5, Maud Ashgrove sonnet-5.5, Pell Quickfinger fable-5.1,
  Sir Edric Vane opus-5.5.
- Recovery feed (09:36:08Z) through the bridge's own documented caller argument
  `feed_session(..., scene_to_model=...)`: live-dir scenes via `tools.arena_gwap.actor_payloads`
  (the same resolution arena_gwap uses) + the 6 quarantine scenes; coverage asserted
  (chain scenes 391, map 391, uncovered []). Output:
  `GPS FEED RECEIPT: rows_seen=524 fed=99 skipped=173 distinct=351 duplicate_skipped=252
  task_shape=arena-agreement-v1 chain_tip=42f23ac85ad67d5b5b628bd56e31e80ac7963fdcae75b9099e7b3bf83ff5dcea`
  (rows_seen 524 not 491: the hourly cron banked more rows between census and feed; the
  whole-file feed takes the chain as it stands, moment-stamped).
- Post-feed census (09:36:27Z): verdict_log total 593, arena rows 351 (252 legacy + 99 new),
  evidence_resolved census [(0, 252), (1, 99)] - every new row byte-resolved, legacy rows
  honestly still 0. Capability: opus 0.6114/97, sonnet 0.2931/116, fable 0.2292/52,
  haiku 0.0/86 (sum 351).

## Sub-item 4 - evidence_bytes in feed_session (a04#6)

`mag/gwap_to_gps.py`: pass 1 now builds the canonical row core
(`canonical({seq, ts_utc, payload, prev_sha256})` - the exact bytes `gwap_payload._row_hash`
hashes into row_sha256, so the reconstruction is proven by the chain verify that already ran)
and pass 2 passes `evidence_bytes=` to `record_verdict`. Result: every future arena row lands
`evidence_resolved=1` instead of self-attested; rows are far under the 64 KiB retention cap so
the bytes stay re-auditable. Live proof: 99/99 new rows evidence_resolved=1; unit proof:
`test_bridge_refeed_is_idempotent_and_byte_resolved` asserts audit agreed=2,
resolved_at_append=2 AND that each retained blob is byte-identical to the canonical core.

## Sub-item 5 - per-invocation feed receipt (a04#3)

`mag/gwap_to_gps.py` `feed_session` now prints one stdout line per invocation,
`GPS FEED RECEIPT: rows_seen=... fed=... skipped=... distinct=... duplicate_skipped=...
task_shape=... chain_tip=...`, and the returned report gains `distinct` (dedupe target
cardinality computed from the plan, independent of the gate, so a future gate regression shows
as fed > distinct) and `duplicate_skipped`. Landing-spot note: a04#3 named the
`tools/arena_gwap.py` main() print block; that file was NOT touched - it carries another lane's
uncommitted GO-item-6 work (the `--status` banked_at diff). Printing inside feed_session gives
every caller the receipt instead.

## Sub-item 6 - idempotence proof (command + output, banked)

Rerun of the identical recovery feed (09:36:27-29Z), zero-row assertion inline:

```
GPS FEED RECEIPT: rows_seen=524 fed=0 skipped=173 distinct=351 duplicate_skipped=351 ...
IDEMPOTENCE PROOF: verdict rows before=593 after=593 new_rows=0
feed says: fed=0 duplicate_skipped=351
IDEMPOTENCE OK: zero new verdict rows on rerun
```

Literal backfill rerun (09:36:43Z) `.venv\Scripts\python.exe tools\arena_gwap.py --backfill`:
all dirs "SKIP ...: already banked", `CHAIN: verify ok=True bad=None scenes_mapped=0`, gps
verdict rows 593 before and 593 after. (Note for the arena_gwap owner: when nothing new banks,
main() skips the feed step entirely - `if scene_to_model and ...` is empty - so backfill-only
reruns never reach the dedupe gate; the recovery-feed rerun above is the proof that counts.)

## Sub-item 7 - tests (tests/test_gps_dedupe.py, new, 13 tests)

duplicate triple skipped (opposite outcome included) / distinct lands / same triple different
pair not a duplicate / hash-less verdicts stay legal (partial index) / evidence_bytes participate
in the key (same bytes dup, different bytes distinct, key = recomputed sha256) / retained bytes
re-auditable via audit_evidence / raw duplicate INSERT hits the index / race backstop returns
duplicate-skipped (blinded SELECT proxy, deterministic) / non-triple integrity failure still
raises / legacy dup db fails closed at open / bridge refeed idempotent + byte-resolved blobs are
the exact hash preimages / receipt line fields on a fed session / receipt zeros on a skip-only
session.

## Test verdicts (instrument: .venv\Scripts\python.exe -m pytest, repo root)

- `pytest tools/gps_mcp -q` -> 41 passed (the mandated gps_mcp testpath)
- `pytest tests/test_gps_dedupe.py -q` -> 13 passed (new file)
- `pytest tests/test_gwap_to_gps.py tests/test_gps_evidence_resolution.py -q` -> 28 passed
  (bridge + evidence gate, both touched by the feed_session change)
- Combined run of all four paths: 82 passed, 0 failed, 8.64s.

## Files touched

- `tools/gps_mcp/ledger.py` (index in SCHEMA_SQL + init_schema, race backstop, docstrings)
- `tools/gps_mcp/gps_ledger.db3` (in-place index migration) + `tools/gps_mcp/gps_ledger.db3.bak-20261004-gpsdedupe` (new byte-copy bak)
- `mag/gwap_to_gps.py` (evidence_bytes + distinct/duplicate_skipped + receipt print - see deviation note)
- `tests/test_gps_dedupe.py` (new, 13 tests)
- `watch/inbox/go_wave_20261004/gps_dedupe.md` (this receipt)

## Ownership deviation (flag for the coordinator)

My declared ownership was tools/gps_mcp/* + tests/test_gps_dedupe.py + receipt. Sub-items 4 and 5
name `feed_session`, which lives in `mag/gwap_to_gps.py` - outside that boundary. I asked the
coordinator (AskUserQuestion: grant the file vs file blocked); no answer returned. I proceeded on
the explicit sub-item order with the minimal feed-side edits only, because the file was clean in
git (no other lane's in-flight work, unlike tools/arena_gwap.py which I did NOT touch) and the
alternative strands GO item 2 half-done. `git diff mag/gwap_to_gps.py` is small and reviewable at
commit time; if the coordinator rules otherwise, reverting that one file leaves sub-items
1/2/3/6/7 intact (the recovery feed used the pre-existing feed_session signature minus
evidence_bytes, which only affects evidence_resolved flags, not the dedupe).

## Blockers

None for the sub-items. Upstream defects named for their owners (not mine to fix):

1. `tools/arena_gwap.py` main() builds the feed map by walking live dirs only: a banked dir that
   is later deleted or quarantined orphans its chain scenes and the whole-file feed refuses
   (observed live 09:31:45Z; the cron's feeds have been refusing since the 08:41Z collision
   bank). Fix shape: chain-native identity (persist scene->model at bank time in the chain row or
   a sidecar), not a wider filesystem walk. Same defect family as a04 row 6 (DUNGEON_ACTOR_MODEL
   sole identity source).
2. `tools/arena_gwap.py` main() skips the feed step when the invocation banked nothing new
   (`scenes_mapped=0` path), so a backfill-only rerun never exercises the feed.
3. The 6 collision scenes (seqs 460-465) were fed from quarantined data the tavern_refresh lane
   voided for ITS curve study; the chain banked them and the feed mirrors the chain - flagged so
   the router reader knows those 6 measurements ride a void-stamped carrier.
