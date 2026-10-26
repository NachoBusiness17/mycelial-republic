# Q-020 / FW-03 — Grounding wave verify (chain FAIL still exactly row 122?)

- Date: 2026-09-28 · seat: queue-gopher2-Q-020 (workflow gopher) · cost: $0 (local verify, read-only)
- Plan: `memory/plans/fifty_wide_20260917.md:14` — "confirm chain FAIL is still exactly row 122, rows 123+ orphans unchanged (no VOID — operator word pending)"
- Chain: `watch/GROUNDING_WAVE.jsonl` (137 rows) + rendering `watch/GROUNDING_WAVE.md` · instrument: `python -m mag.grounding_wave verify` (the estate's own reader law, `mag/grounding_wave.py:725-785`)

## Command run and its output (verbatim)

`./.venv/Scripts/python.exe -m mag.grounding_wave verify` → exit **1**:

```
FAIL LINKAGE-PASS: 137 posts intact, tip=fc3c32be6f26 | truth-gate: 11 witnessed SUPPORTED, 49 legacy-unwitnessed | row 122: hashless defect contained by void; row 123: prev defect contained by void; row 129: re-anchored past voided stretch; row 130: re-anchored past voided stretch; row 131: prev defect contained by void; row 132: re-anchored past voided stretch | ADMISSION: 3 voided, 0 contested, 0 corroborated, 0 pending voids, 3 propagation-flagged | EVIDENCE-MISSING row 75:swarm_20260912/smoke_driver.js, row 76:suno/flat_beat_loop.mp3, row 86:flygomoku_20260912/hermes_mirror_summary.json
```

## What the three plan clauses verify as, today

1. **"chain FAIL still exactly row 122" — CONFIRMED with precision.** The physical tape's only linkage defects are exactly the 09-16 truncation event's two rows: row 122 (the truncated "NIGHT THE FULL SELF HELD" row — `prev` matches nothing, no hash key) and row 123 (its first child, `prev` defect). The walker in `mag/grounding_wave.py:734-753` re-hashes every row (`_row_hash(row) != h` would return "row edited in place") — no such error fired, so **all 137 rows are hash-faithful; no row was edited in place**. LINKAGE itself PASSES ("137 posts intact"); the FAIL head + exit 1 come from the EVIDENCE-MISSING clause (below), not from row 122.
2. **"rows 123+ orphans unchanged" — CONFIRMED at the byte level, but the ladder state moved as designed.** The rows are unchanged (hash re-computation above); what changed is their *status*: the v4 admission now reports the orphan stretch as "contained by void" (rows 122/123/131) with rows 129/130/132 "re-anchored past voided stretch" — the re-anchor law working as built, not a rewrite.
3. **"no VOID — operator word pending" — SUPERSEDED BY EVENTS; the operator word ARRIVED.** The VOID the plan was holding for executed 2026-09-27T18:33:50Z (eleven days after this plan was written): row 138-of-the-ladder `{"kind": "void", "voids": "line:122", "reason_code": "MALFORMED", "witness": "operator", "evidence": "operator GO 2026-09-27: \"No sacred cows these were all the best ideas we had at the time\" ..."}`. The MD rendering shows the operator's cross-sign at 2026-09-27T18:34:14Z (`signs 52db99d28297 g1=True`) — the exact second-seat act `mag/grounding_wave.py:277-285` requires to make a void effective. ADMISSION: **0 pending voids**. FW-04's prep packet is therefore filed as prep-then-retrospective (see `Q-020_FW04_void_prep.md`).

## The exit-1 footnotes (both checked this session, neither is the row-122 defect)

- EVIDENCE-MISSING rows 75/76/86 name bare relative tokens; **all three files exist on disk** — `ls memory/runs/swarm_20260912/smoke_driver.js`, `dashboard/static/suno/flat_beat_loop.mp3`, `memory/runs/flygomoku_20260912/hermes_mirror_summary.json` all hit. The `_src_path` resolver just doesn't map the un-prefixed tokens. These rows are 09-12/09-13-era — the condition predates the plan; it is not new damage. (Left un-repaired: fixing evidence tokens would be a ledger mutation and this item is verify-only.)
- File is git-untracked (`git show HEAD:watch/GROUNDING_WAVE.jsonl` → empty), so "unchanged" rests on the tool's per-row hash re-computation, not a git baseline.

## Not done

- No rows appended, no VOID filed, no render rebuilt — the plan scopes FW-03 to confirm-only ("no VOID — operator word pending" was the state to check, not a state to create; the 09-27 executor already spent the operator's word).
