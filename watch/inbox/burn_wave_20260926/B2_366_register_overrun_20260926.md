# B2-366 Annotate the qagg register overrun (2026-09-26)

## Verdict

LANDED. All 45 ok:false rows of watch/inbox/qdrop_export/media_register_qagg.jsonl now carry a machine-readable classification so no future completeness sweep recounts them as open gaps: the 44 tail rows (q_num 4967..5010) carry gap_class "register_overrun" + canonical_max 4966 + a note naming the B2-92 evidence (qalerts nav declares 4966 Q Posts; ?n=4966 renders post No. 17830326 = local drop_no 6242), i.e. they are ok:false BY CONSTRUCTION with no canonical drop to fetch; the mid-range row q_num 874 carries gap_class "generator_gap" + the B2-14/B2-92 chain (canonical drop exists at local drop_no 1088; only the auto-generated QAgg.news card 404s; nothing owed). Annotation is additive metadata only: every row keeps its original ok/err/url/bytes/sha256 fields, no row trimmed (trimming a generated register would rewrite history; the annotation makes the builder's overrun self-describing instead). Register integrity after the write: 5,010 data rows + 1 _scope_header line (the scope header is another lane's additive metadata, preserved byte-faithful through this lane's rewrite), 45/45 ok:false rows classified.

## Evidence

- watch/inbox/qdrop_export/media_register_qagg.jsonl q_num 4967 row post-annotation: {"q_num": 4967, "url": ".../qaggdropimage4967.png", "ok": false, "err": "HTTP Error 404: Not Found", "gap_class": "register_overrun", "canonical_max": 4966, "note": "no canonical qagg/qalerts drop exists at this q_num (B2-92...)"} (read back this lane)
- Post-write census: 5,011 lines = 5,010 data rows + 1 _scope_header (preserved); Counter of gap_class over ok:false rows = {register_overrun: 44, generator_gap: 1}
- watch/inbox/burn_wave_20260926/B2_92_qagg_sweep_20260926.md lines 5, 11, 13 (the classification this annotation encodes: 874 generator-gap mundane, tail 44 register-overrun, canonical top 4966 = drop_no 6242, all 45 URLs re-probed 404 live 2026-09-26T17:13Z) and B2_92_qalerts_nav.json (nav_posts_claim "4966")
- watch/inbox/burn_wave_20260926/B2_92_qagg_probe_results.json: not_ok_q_nums list = [874, 4967..5010] (the exact 45 rows annotated)
- The falsifier's disease, standing: any naive completeness recount (ok:false count) would re-classify these 45 forever; the gap_class field makes the classification queryable in one pass (filter gap_class)

## Work done

Chose in-row annotation over trimming (the brief offered both): trimming would falsify the register builder's historical output and break the append-only spirit, while annotation keeps the 404 bytes truthful and adds the verdict. Wrote the annotation pass (read all lines, classified by q_num against the B2-92 evidence, re-serialized preserving the concurrent _scope_header line another lane had added). Verified post-write state: row count, gap_class census, sample row bytes. Receipt + LEDGER row filed.

## Falsifier

`.venv/Scripts/python.exe -c` reading the register and counting rows with ok false and gap_class missing must print 0; if a future register regeneration overwrites the annotations (the builder iterating 1..5010 fresh), the recount disease returns - the durable fix is the builder gaining the gap_class logic itself, and the falsifier for that upgrade is the same count. A completeness sweep that still reports "45 open gaps" after this annotation is ignoring gap_class and should be corrected to exclude register_overrun by construction.

## Bibliography closed

watch/inbox/qdrop_export/media_register_qagg.jsonl (read in full, annotated in place, 45 rows); watch/inbox/burn_wave_20260926/B2_92_qagg_sweep_20260926.md + B2_92_qalerts_nav.json + B2_92_qagg_probe_results.json (read, unchanged, the evidence encoded); QUEUE.md (row note); memory/burns/LEDGER.jsonl (appended); watch/inbox/burn_wave_20260926/B2_366_register_overrun_20260926.md (this receipt).
