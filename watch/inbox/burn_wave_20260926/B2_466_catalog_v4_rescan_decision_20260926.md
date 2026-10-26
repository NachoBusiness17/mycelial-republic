# B2-466 Catalog v4 rescan GO/NO-GO, 2026-09-26

## Verdict

GO, and the GO is already EXECUTED: the decision this brief asked for was overtaken by concurrent lanes landing the v4 map and index refresh the same day. The Sep-18 v3 map (757,667 rows, 214,470,472 bytes, qdrop 0 on both engines) was atomically replaced 2026-09-26T19:01:27Z (unnamed flow, B2-332 documented), B2-104's incremental rescan stamped snapshot 2026-09-26T19:16:46Z (489,455 base rows + 17 added, 2m01s live), and the FTS index was rebuilt over the fresh map (catalog/catalog_fts.sqlite 134,303,744 bytes, mtime 19:38Z). Live measurement this lane: corpus_search "qdrop" now returns 20 hits in 6.6ms on engine=fts5 (was 0 hits on both shapes). C6 staleness for qdrop_export is closed on real bytes. NO-GO on the watcher-triggered incremental tail: the priced scheduler arm (MagCorpusRescanDaily 03:30 local, incremental 2m01s, 48h staleness budget in the manifest) already bounds map age at 24 to 48h without a resident daemon, and B2-104 landed the policy with "no daemon" named. Residual registered, not hidden: 158 duplicate-path rows remain in the map until the dated rebuild arm compacts them (B2-511 self-feed, owed), and a second index rebuild was torn-in-flight mid-lane (catalog_fts.sqlite.tmp 32,768 bytes at 19:40Z, a concurrent lane's tmp; untouched by this lane).

## Evidence file:line quotes

- catalog/catalog_manifest.json: policy line "B2-104 C6 freshness: incremental rescan + dated rebuild + tags re-run; readers disclose map_asof/map_stale"; scheduler "MagCorpusRescanDaily 03:30 local (Task Scheduler, repo venv python -m mag.catalog_rescan incremental)"; summary "base_rows": 489455, "added": 17, "machinery_dirs_excluded": 1013, "base_dups": 158; snapshot_ts "2026-09-26T19:16:46Z"; map_bytes 133894969; map_sha256 1371a1db3005c7d44493775f4e2a974d4ebef82496085b6b64557bd1a628df65; staleness_budget_hours 48.
- catalog/catalog.jsonl line 1: {"id": "a54ff182c7e8", "path": "AGENTS.md", ...}; wc -l 489,549 lines (489,548 tag rows per manifest tags_rows).
- Fresh-map qdrop hits, read this lane 19:41Z: "local_sovereign_agent/watch/inbox/qdrop_export/called_shot_ledger.jsonl" and "local_sovereign_agent/watch/inbox/burn_wave_20260926/B2_14_qdrop874_20260926.md" among 20 fts5 hits; grep -c 'qdrop_export' catalog/catalog.jsonl = 4976.
- Measured denominators this lane (2026-09-26 19:41 to 19:42Z, warm cache): qdrop engine=fts5 20 hits 6.6ms; garden fts5 3.0ms; adventure_2d6 fts5 2.3ms. Forced-scan arm (FTS_DB pointed at an absent path in-process, no writes): qdrop 2,968.4ms / 453,407 rows walked (early break); garden 2,770.1ms full 489,548-row walk; adventure_2d6 2,899.4ms full walk. Full-scan class on v4 is 2.8 to 3.0s (v3 class was 4.0 to 4.9s per B2-22; the map shrank 37 percent).
- Index refresh cost denominator: B2-102 receipt, 10.308s rebuild through tools/corpus_fts_rebuild.py on v3 (217,694,208 bytes); the v4 rebuild in place on disk is 134,303,744 bytes (mtime 2026-09-26 19:38Z local).
- Junction pruning kept: catalog/junctions.jsonl present (12,078 bytes, mtime 15:16 local) and manifest machinery_dirs_excluded 1,013.
- Pointer receipts verified on disk: watch/inbox/burn_wave_20260926/B2_22_fts5_spike_20260926.md ("qdrop | 4461.6 | 0.20 | 0 / 757,667 | 0" row; "Both engines return 0 for qdrop: the Sep-18 map predates watch/inbox/qdrop_export"); watch/inbox/burn_wave_20260926/B2_102_fts5_wiring_20260926.md ("qdrop 3350.0ms 0 hits vs 1.5ms 0 hits (C6 staleness on both shapes...)").
- B2-104 receipt (watch/inbox/burn_wave_20260926/B2_104_freshness_policy_20260926.md) Evidence: "the map was atomically replaced at 19:01:27Z by an unnamed concurrent flow (489,038 rows, B2-332 still Open)"; live incremental run "2m01s"; "158 duplicate-path rows remain in the map until the dated rebuild arm compacts them (self-fed B2-511)".

## Work done

- Read both pointer receipts whole plus the B2-104 freshness-policy receipt; read catalog/catalog_manifest.json; counted rows and qdrop_export presence in the fresh map.
- Measured live on the wired path: fts5 arm (qdrop 6.6ms / 20 hits; garden 3.0ms / 16; adventure_2d6 2.3ms / 4) and forced-scan arm (qdrop 2,968.4ms; garden 2,770.1ms; adventure_2d6 2,899.4ms), read-only probes only, no writes to catalog/.
- Priced the watcher-triggered incremental tail and rejected it: the incremental already runs scheduled (03:30 daily, 2m01s measured), the manifest carries staleness_budget_hours 48, and B2-104's landed policy explicitly chose "no daemon"; a resident watcher would add a second mutation writer racing the 19:38Z hand rebuild class of events for a staleness bound the scheduler already beats.
- Named the GO as executed-by-concurrent-lanes with timestamps, and registered the two residuals (158 dup rows to B2-511; concurrent torn tmp left alone per claim law).
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Any corpus_search "qdrop" over the current map returning 0 hits on either engine kills the "C6 closed" claim (rerun: tools/corpus.py corpus_search, both arms).
- If the dated rebuild arm never compacts the 158 base_dups, or the 03:30 scheduler arm stops firing while the estate mutates, the 48h staleness budget is fiction and this GO decays to NO-GO on freshness (check manifest snapshot_ts age vs staleness_budget_hours).
- If a future full-scan query on v4 measures above 4s or any fts5 answer above 30ms (B2-22's bands), the "index now cheap" denominator is dead and the decision must be re-briefed.
- The watcher NO-GO rests on the scheduler being registered and Ready; Task Scheduler loss of MagCorpusRescanDaily voids it.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_22_fts5_spike_20260926.md (whole); watch/inbox/burn_wave_20260926/B2_102_fts5_wiring_20260926.md (whole); watch/inbox/burn_wave_20260926/B2_104_freshness_policy_20260926.md (whole); catalog/catalog_manifest.json; catalog/catalog.jsonl (row count + qdrop grep + line 1); catalog/junctions.jsonl (mtime, size); catalog/catalog_fts.sqlite and .tmp (mtimes, sizes); tools/corpus.py (FTS_DB constant line 68, gate lines 138-150); live probes run this lane. No web sources. Em-dash count 0.
