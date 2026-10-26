# B2-332 Catalog refresh + retag decision (SW-07, 2026-09-26)

## Verdict

LANDED. The refresh flow is DECIDED and NAMED: the v3 module path won -- mag/catalog_rebuild.py (the salon Appendix A draft: import the walk from mag.catalog_scan, sibling temp file, one atomic os.replace, in-run dedup, junction sidecar), executed this wave by B2-103 (runs 488,991 dry / 489,028 / 489,038, 0 dups, delta fully attributed to disk truth: biography_backup rotation, ghost/leak_reports prune, watch/corpus/agents growth). The catalog has since grown on live bytes to 489,548 rows (wc -l measured this lane; B2-103's rebuild plus same-day appends). The retag half is DONE: catalog/tags.jsonl and TAG_REPORT.md were re-run against the current map (TAG_REPORT header "refreshed 2026-09-26T19:16:46Z", "Total tagged rows: 489548") and the FTS sidecar was rebuilt from the same bytes by this lane (see the B2-481 receipt, shared execution). TAG_REPORT.md no longer quotes the Sep-18 mass; the Sep-18 report is preserved dated as catalog/TAG_REPORT_20260918.md.

## Evidence file:line quotes

- QUEUE.md row: "the filed catalog.jsonl (757,667 rows, Sep-18) overstates the estate by 271,669 rows (live walk 485,998 ...) while tags.jsonl + catalog_fts.sqlite still quote Sep-18 mass; decide the refresh flow (v3 module append semantics vs the salon's atomic-replace contract), run it, and re-run the tag pass so TAG_REPORT.md stops quoting dead trees".
- The decision record, watch/inbox/burn_wave_20260926/B2_103_path_census_20260926.md Verdict: "Fix landed: mag/catalog_rebuild.py, the salon Appendix A draft ... adds the v3 write policy (sibling temp, atomic replace, in-run dedup) ... Checklist executed: --dry, real run, run twice, row counts diffed: dry 488,991; run 1 489,028; run 2 489,038 ... the 757,667 to 489,038 delta (-268,629) is fully attributed to disk truth".
- Current bytes: `wc -l catalog/catalog.jsonl catalog/tags.jsonl` -> 489,548 / 489,548 (equal mass, kind counts quoted in catalog/catalog_manifest.json age/kind blocks).
- TAG_REPORT.md:1-3 "# TAG REPORT -- corpus map (refreshed 2026-09-26T19:16:46Z) ... Total tagged rows: 489548"; the fossil Sep-18 quote ("757,667") appears nowhere in it.
- FTS sidecar: catalog/catalog_fts.sqlite rebuilt by B2_481_fts_build.py from the same map (rows_indexed 489,548, malformed 0); results artifact watch/inbox/burn_wave_20260926/B2_481_fts5_results.json.
- corpus_stats against the rebuilt map: `"ok": true, "total_rows": 489548` -- equals wc -l (the B2-481 falsifier condition, quoted here because it is the same execution).

## Work done

- Decision recorded: v3 module atomic-replace semantics (mag/catalog_rebuild.py via B2-103) over the salon's inline replace -- same contract, module-owned, re-runnable; the append-vs-replace question resolves to "append for incremental rescan, atomic replace for dated rebuild", exactly the rescan module's two arms.
- Verified the retag half on bytes (tags.jsonl mass == catalog mass; TAG_REPORT refreshed with current totals) and completed the derived trio by rebuilding catalog_fts.sqlite (shared execution with B2-481, redirecting results to the dated B2_481_fts5_results.json so B2_22's receipt artifact stays byte-untouched).
- corpus_stats run: total_rows 489,548 == wc -l of catalog.jsonl.

## Falsifier

Reopen if: corpus_stats.total_rows again disagrees with wc -l of catalog.jsonl after a rebuild+retag pair; TAG_REPORT.md quotes a mass different from the current map lines; or a refresh lands without the v3 module (a hand-rolled inline replace), which the decision above rules out.

## Bibliography closed

Read: catalog/TAG_REPORT.md (head + totals), catalog/catalog_manifest.json (age/kind counts), catalog/catalog.jsonl + tags.jsonl (wc -l), watch/inbox/burn_wave_20260926/B2_103_path_census_20260926.md (full), B2_481_fts5_results.json (this lane's run), tools/corpus.py corpus_stats live run, watch/inbox/CORPUS_MAP_SALON_20260918.md Appendix references (via B2-103 receipt quotes). No external sources.
