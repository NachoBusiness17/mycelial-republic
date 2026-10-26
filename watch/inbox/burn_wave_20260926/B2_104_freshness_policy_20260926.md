# B2-104 Corpus map freshness policy (C6), 2026-09-26

## Verdict

LANDED and live. The salon's demanded refresh policy (C6: "incremental rescan
or scheduled rebuild ships") is three arms, one module per arm: incremental
rescan + dated rebuild (mag/catalog_rescan.py), tags re-run
(mag/catalog_tags.py), read-side disclosure (mag/catalog_freshness.py); fired
on a schedule by MagCorpusRescanDaily (Windows Task Scheduler, 03:30 local,
registered and verified State Ready, local janitor per the tier law, no LLM
lane, no daemon). First live run: 2m01s, appends 93 rows over the 489,455-row
base, tags re-run 489,548 rows, manifest stamped. The C6 falsifier executed
both directions on real bytes: corpus_search "qdrop" was 0 hits over 757,667
rows on the Sep-18 map (this lane's 18:44Z probe) and hits on the fresh map
after the rescan, on both engines. The brief's premise ("the Sep-18 snapshot")
was overtaken MID-LANE: the map was atomically replaced at 19:01:27Z by an
unnamed concurrent flow (489,038 rows, B2-332 still Open), which is itself the
strongest evidence for the policy: the estate mutates with no standing law,
the tags sidecar went stale within the hour, and nothing scheduled the next
refresh. Honest limits: Sep-18 kind-count parity of the tag-rule
transcription is Unproven (the base it was tuned against no longer exists on
disk and no archive was kept by the replacing flow), so the rules are pinned
fixture-first instead; 158 duplicate-path rows remain in the map until the
dated rebuild arm compacts them (self-fed B2-511).

## Evidence

- The disease, both directions: 18:44Z probe on the Sep-18 map:
  corpus_search("qdrop") -> hits 0, rows_scanned 757,667 (scan engine);
  B2-22 measured the same 0 on fts5. Post-rescan: corpus_search("qdrop")
  -> hits >= 1 (scan, engine=scan index_state=stale with B2-102's honest
  index_note; then engine=fts5 after the concurrent hand rebuild of the
  index), hits naming watch/inbox/qdrop_export/called_shot_ledger.jsonl and
  watch/inbox/burn_wave_20260926/B2_14_qdrop874_20260926.md.
- Live incremental run (2m01s): base_rows 489,455; added 17; refreshed 76;
  unchanged 489,194; vanished 27; reparse_records 7; walk_dups 0;
  machinery_dirs_excluded 1,013; tags_rows 489,548.
- Manifest (catalog/catalog_manifest.json): snapshot_ts 2026-09-26T19:16:46Z,
  mode incremental, map_bytes 133,894,969, map_sha256 1371a1db3005...,
  tags_ts 2026-09-26T19:16:46Z, staleness_budget_hours 48, scheduler named.
- Read-side stamp live: corpus_search returns map_asof 2026-09-26T19:16:46Z,
  map_age_hours 0.04, map_stale false; corpus_get carries no stamp (serves
  live bytes, never quotes the map).
- Task: Get-ScheduledTask MagCorpusRescanDaily -> State Ready.
- Mid-lane mutation: catalog.jsonl mtime 19:01:27Z, 214,470,472 ->
  133,772,210 bytes, 757,667 -> 489,038 rows, 0 malformed lines in the new
  map, junctions.jsonl born same second (pytest-tmp junction rows); the
  replacing flow is unnamed on disk (B2-332 Open, self-fed by B2-76).
- Tests: tests/test_catalog_rescan.py + test_catalog_tags.py +
  test_catalog_freshness.py + test_corpus_fts.py = 26 passed (joint runs can
  hit a transient tmp_path Permission error when sibling lanes run pytest in
  the same second; isolated reruns green, twice).
- Ratchet: tools/violation_ratchet.py check --changed -> PASS, NEW=0 (after
  the file-too-long split: all lane modules under 400 lines). Em-dash 0 on
  every file this lane wrote.

## Work done

- mag/catalog_rescan.py: incremental rescan (append-upsert by
  (bytes, mtime) signature, last-row-wins readers, deletions counted as
  vanished, never tombstoned), dated rebuild (temp walk, archive
  catalog_<prev-snapshot-date>.jsonl, two atomic os.replace), manifest
  writer; walk lineage inherited from mag.catalog_scan (ROOT projects parent,
  EXCLUDE set, zone map, junction policy P1/P2, device-space \\.\nul guards)
  so rescan rows are schema- and zone-identical to the filed map.
- mag/catalog_tags.py: the salon Appendix B tag pass as a module (first-match
  kind rules on the LSA-relative view, age classes at run time,
  temp+replace sidecar, dated TAG_REPORT.md; the Sep-18 report preserved as
  catalog/TAG_REPORT_20260918.md).
- mag/catalog_freshness.py: disclosure arm (manifest_freshness pure verdict,
  map_freshness IO wrapper, corpus_status CLI); missing manifest can never
  read fresh; budget read from the manifest, default 48h.
- tools/corpus.py: rebased on B2-102's landed FTS5 bytes per the shared-file
  claim law (their gate answers "index vs map", mine answers "map vs disk");
  corpus_search (both engines) and corpus_stats attach map_asof /
  map_age_hours / map_stale via the freshness arm; get/tail deliberately
  unstamped.
- Schedule: scripts/register_corpus_rescan_task.ps1 + 
  scripts/corpus_rescan_daily.ps1 (venv python -m mag.catalog_rescan
  incremental, logged to logs/corpus_rescan_daily.log); task registered,
  State Ready. The nightly FTS-rebuild leg is deliberately NOT wired yet:
  self-fed B2-510 pins the ordering first.
- Probes (kept as artifacts): B2_104_rule_parity_probe.py / _probe2.py /
  _probe3.py, the three-variant empirical rule solve over the real map.
- Tests: 15 pins originally, split to 15 across the three new modules (2
  rescan upsert, 10 tag rules, 3 freshness) and kept green through the
  split; B2-102's 11 corpus fts pins stayed green across my rebase.
- QUEUE.md: two claims filed then retired to CLAIMED with this receipt;
  B2-104 row's pre-checked [x] earned by this landing; self-fed B2-510,
  B2-511, B2-512 unchecked.

## Falsifier

- Rerun `.venv/Scripts/python.exe -m mag.catalog_rescan incremental`: a run
  over ~489k rows must stay under 10 minutes (measured 2m01s) and end with a
  manifest whose snapshot_ts is fresh; killed if it double-appends unchanged
  rows (unchanged must stay the dominant count) or if tags_rows != map rows.
- Rerun the disclosure: delete catalog/catalog_manifest.json, then
  corpus_search must report map_asof == the map file's mtime and map_stale
  computed against the same 48h budget; a missing manifest reading
  map_stale false with a day-old map kills the verdict.
- Kind-parity honesty: any claim that the salon Sep-18 kind counts are
  reproduced on today's map is false by construction (different estate);
  the pinned contract is the rule table (tests/test_catalog_tags.py), not
  the counts. A rule reorder that flips card/receipt first-match fails the
  pins.
- Attribution gap: if a receipt lands naming the 19:01:27Z replace, B2-512's
  premise dies and the brief should be closed with that pointer.

## Bibliography closed

watch/inbox/CORPUS_MAP_SALON_20260918.md (C6 at 76-83, Appendix B tag rules
at 349-356, execution receipt at 359-421); watch/inbox/burn_wave_20260926/
B2_22_fts5_spike_20260926.md (qdrop 0 on both shapes; 757,667-row census);
watch/inbox/burn_wave_20260926/B2_102_fts5_wiring_20260926.md (index gate +
rebuild entry point; rebase source); tools/corpus.py (pre- and post-rebase
bytes); mag/catalog_scan.py (v3 junction policy, ROOT, zone map, EXCLUDE);
catalog/catalog.jsonl (line 1 both estates), catalog/tags.jsonl (Sep-18
mtime vs 19:16:46Z re-run), catalog/TAG_REPORT.md + TAG_REPORT_20260918.md,
catalog/catalog_manifest.json (new), catalog/junctions.jsonl (new, born
19:01:27Z); watch/inbox/burn_wave_20260926/QUEUE.md (B2-332 Open, claim law
lines 51-56); scripts/register_improve_task.ps1 (scheduler house pattern);
memory/burns/LEDGER.jsonl (row shape); watch/inbox/INDEX.json (tail anchor).
