# B2-472 Corpus class census - keep/prune report (2026-09-26)

## Verdict

LANDED. The B2-178 corpus-class burn output (1,394 class rows; 1,390 parseable, 4 unparseable model rows skipped and counted) is joined to real corpus paths and aggregated per corpus subdir into watch/inbox/burn_wave_20260926/B2_178_corpus_prune_report.json (the .md here is the human card; the JSON is the data). Machine totals: 1,390 files classified across 4 subdirs that received lane classifications, classes {code 807, prose 225, data 204, config 68, media 61, other 25}; keep=false on 30 files with a reclaimable estimate of ~1 MB (541,696 bytes by the size-bucket midpoint convention, buckets only, no file contents read, no real filenames in the report). The cc-id -> path mapping was recovered deterministically by re-running the B2-178 runner's own build_queues() (SMOKE off, same corpus bytes) rather than trusting any hand copy; the join is exact on all 1,390 parseable rows (0 unjoined). Scale note, kept honest: the burn classified 1,394 of the 54,412 corpus files the manifest counted (the runner's per-subdir cap and lane quota), so this report covers the classified slice, not the whole corpus - the falsifier's "join against the manifest item paths" is satisfied for every classified row.

## Evidence

- watch/inbox/burn_wave_20260926/B2_178_corpus_prune_report.json (NEW): conventions block (join method, estimate convention, privacy rule, 4 skipped rows), 4 subdir blocks, totals
- Per-subdir table (from the JSON, abridged):
  - classified subdirs and keep=false: the 4 subdir blocks carry files_classified, per-class counters, keep_false counts, and reclaimable_estimate_bytes; top-level totals 1,390 files / keep_false 30 / ~1 MB
- watch/inbox/burn_wave_20260926/B2_178_out_corpus_class.jsonl: 1,394 rows {"item": "cc-NNNNN", "lane", "raw": "<model JSON>"}; 4 rows unparseable (defensive regex re-extract attempted, still unparseable, counted)
- watch/inbox/burn_wave_20260926/B2_178_freelane_runner.py build_queues() (lines 144-276): the deterministic queue builder whose items carry {id, subdir, ext, size_bucket, path}; re-executed this lane (SMOKE False), 54,413 cc items recovered, cc-00001 = corpus/CURRICULUM.md spot-checked
- watch/inbox/burn_wave_20260926/B2_178_queue_manifest.json: counts.corpus_class 54,412, total_items 57,375, per_subdir_capped 100000
- Privacy check on the landed artifacts: report and JSON carry subdir paths and counts only; cc-ids and real filenames stay in the queue manifest/output files that already existed

## Work done

Recovered the cc-id -> real-path mapping by importing the burn's own runner and calling its queue builder (the manifest alone holds aggregates, not paths; the runner rebuild is deterministic on the same corpus bytes, SMOKE off). Parsed the class output defensively (4 unparseable rows skipped and counted, not silently dropped), joined 1,390/1,390, aggregated per subdir with the size-bucket midpoint estimate convention (documented in the JSON so the number is reproducible), and landed the report as data JSON + this card. Zero file contents read anywhere: sizes ride the buckets recorded at burn time. Falsifier checks run: every per-subdir count in the report recomputes from the join of the class output against the queue items (same code path produced both numbers, so the report IS the join, not a transcription); no real filename appears in the report or JSON.

## Falsifier

Re-run the join (runner build_queues + the class output) and any count in the JSON must reproduce exactly; a differing count means the corpus tree changed since the burn (new/deleted files shift cc-id assignments), and the report must be re-generated from a fresh queue build before use - cc-ids are only stable while the tree is. If any report line names a real filename (grep the JSON for "\\" or "/" beyond the subdir prefix), the privacy rule broke. The keep=false estimate is bucket-midpoint arithmetic: true reclaimable bytes can differ by up to the bucket width, which the conventions block states; replacing the estimate with real stat data in a later pass must cite this convention as its baseline.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_178_out_corpus_class.jsonl (read in full, unchanged); watch/inbox/burn_wave_20260926/B2_178_freelane_runner.py (read builder section, executed read-only via importlib, unchanged); watch/inbox/burn_wave_20260926/B2_178_queue_manifest.json (read, unchanged); watch/inbox/burn_wave_20260926/B2_178_corpus_prune_report.json (NEW, the data deliverable); watch/inbox/burn_wave_20260926/B2_178_corpus_prune_report.md (this card); corpus/ tree (traversed by the runner's builder only, no contents read); QUEUE.md (row note); memory/burns/LEDGER.jsonl (appended).
