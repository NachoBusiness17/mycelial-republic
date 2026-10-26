# B2-218 receipt: FRAGILE-ALIGNED vocabulary sweep (2026-09-26)

## Verdict

LANDED as the reader-note-plus-docstring form (the brief's explicit alternative). The fifth verdict string FRAGILE-ALIGNED is now enumerated in the registered vocabulary doc (tools/drift.py docstring) as ALIGNED-provisional stamped downstream, with the render law (amber-green, never blank/unknown) written where consumers will read it. The sweep found exactly one verdict-keyed renderer in the stamp flow, tools/drift_dashboard.py _verdict_color, and it ALREADY handles FRAGILE-ALIGNED (amber-green #b9e77a) with a comment citing the aging guard, so no code change was needed there. Zero FRAGILE-ALIGNED rows exist in the stamps ledger yet (the guard is armed, not fired), so no live row renders wrong today; the vocabulary is pinned before the first W40 stamp lands.

## Evidence file:line quotes

- tools/drift_pairs_stamp.py:409: "\"\"\"ALIGNED downgrades to FRAGILE-ALIGNED while its referent is immature."; tools/drift_pairs_stamp.py:423: `guarded["verdict"] = "FRAGILE-ALIGNED"` (the emitter, inside _apply_aging_guard).
- tools/drift_pairs_stamp.py:86: "verdict.verdict must treat FRAGILE-ALIGNED as ALIGNED's provisional" (the consumer law as registered).
- tools/drift.py:12-18 (pre-edit): "This organ computes that number. Verdicts: VACUOUS ... ALIGNED ... DRIFTING ... INVERTED ... INSUFFICIENT" (the enumerated list that omitted the fifth string; post-edit it carries the FRAGILE-ALIGNED entry naming the emitter and the provisional law).
- tools/drift_dashboard.py:197-204: `_verdict_color` returns `{"ALIGNED": "#6ee7a0", "FRAGILE-ALIGNED": "#b9e77a", ...}.get(verdict, "#ddd")` with the comment "FRAGILE-ALIGNED: provisional ALIGNED per tools/drift_pairs_stamp.py _apply_aging_guard ... styled amber-green, never default-gray."
- memory/runs/adv_arc_50/teleo_drift_stamps.jsonl: grep count FRAGILE-ALIGNED = 0 (measured 2026-09-26; no W40 row exists yet).
- Non-consumers named: tools/probe20_run.py and tools/thrash_meter.py and mag/seed_percolator.py each carry their own unrelated verdict vocabularies (probe runner INSUFFICIENT/VACUOUS/DEGENERATE/ALIGNED; thrash FOCUSED/STEADY/SWITCHY/THRASHING; percolator A/B/TIE); no teleo stamp flows through them, so the sweep's verdict-keyed surface is drift.py (vocabulary doc), drift_pairs_stamp.py (emitter), drift_dashboard.py + the generated dashboard/static/drift_board.html (renderers, already correct).

## Work done

1. Swept tools/ + mag/ + dashboard/ for verdict-keyed rendering of the stamp vocabulary (grep FRAGILE-ALIGNED and VACUOUS/INSUFFICIENT across all three trees); classified every hit as emitter, vocabulary doc, renderer, or different-organ verdict namespace (list above).
2. Edited tools/drift.py docstring (git-clean file, no claim line required): added the FRAGILE-ALIGNED entry naming the downstream emitter (_apply_aging_guard), the ALIGNED-provisional treatment, and the render law with the B2-218 receipt anchor. py_compile clean; file at 101 lines, ratchet-clean for this file (the one NEW ratchet hit this hour, mag/shared_surface.py file-too-long, belongs to another lane's in-flight edit, not touched here).
3. Renderer verified correct on bytes; no second renderer exists, so no consumer can render a future W40 FRAGILE-ALIGNED row blank/unknown through the paths swept.

## Falsifier

The brief's falsifier: a consumer that renders a W40 FRAGILE-ALIGNED row as blank/unknown. Decidable when the first FRAGILE-ALIGNED stamp lands in memory/runs/adv_arc_50/teleo_drift_stamps.jsonl and tools/drift_dashboard.py regenerates dashboard/static/drift_board.html: the row must show amber-green #b9e77a and the ALIGNED-provisional treatment; if any surface shows the default-gray .get(verdict, "#ddd") fallback or a blank cell for that row, this receipt is void. Second falsifier: any new consumer of the stamp ledger added after 2026-09-26 that keys verdicts without the fifth string files against this vocabulary doc (drift.py lines 12-27 post-edit).

## Bibliography closed

All read this lane: tools/drift.py (in full, pre + post edit), tools/drift_pairs_stamp.py (docstring 60-90, _apply_aging_guard 400-480), tools/drift_dashboard.py (_verdict_color, build_table, history_cell, drifting_days, OUT_HTML), dashboard/static/drift_board.html (generated snapshot, legend line), tools/probe20_run.py + tools/thrash_meter.py + mag/seed_percolator.py (verdict namespaces checked and excluded), memory/runs/adv_arc_50/teleo_drift_stamps.jsonl (grep census), QUEUE.md B2-218 row, tools/violation_ratchet.py check --changed output.
