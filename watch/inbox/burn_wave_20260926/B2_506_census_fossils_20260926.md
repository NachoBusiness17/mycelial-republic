# B2-506 census prose fossils (SW-07, 2026-09-26)

## Verdict

LANDED. Both anchors fixed to current truth: mag/catalog_rescan.py's C6 story now states the engine split explicitly (the 757,667 figure named as true only under pre-wiring scan semantics; fresh-index qdrop reports rows_scanned 0 walked; the figure reappears only on the stale-scan arm with early-break), and mag/mcp_server.py's security-posture block now names backend/server.py as the /run_task dispatch site with the explicit note that dashboard/rest.py imports no TOOL_MAP. Both files parse clean after the edits.

## Evidence file:line quotes

- QUEUE.md row: "mag/catalog_rescan.py:9 cites the qdrop probe as rows_scanned 757667, true only under pre-wiring scan semantics (post-wiring a fresh-index qdrop search reports rows_scanned 0 walked, and 757667 reappears only on the stale-scan arm where the early-break usually stops far earlier), and mag/mcp_server.py:14 says dashboard /run_task dispatches the same TOOL_MAP while the dispatch lives in backend/server.py /run_task (dashboard/rest.py imports no TOOL_MAP at all)".
- Pre-fix fossil bytes: catalog_rescan.py:9 `the Sep-18 map ("qdrop" 0 hits on BOTH scan and FTS5, rows_scanned 757667,` and mcp_server.py:14 `(dashboard /run_task dispatches the same TOOL_MAP)`.
- Truth verified on bytes: backend/server.py:32 `from tools import TOOL_MAP, dispatch as tool_dispatch` with `@app.post("/run_task", ...)` at :216; `grep -c "dashboard /run_task dispatches the same TOOL_MAP" mag/mcp_server.py` after the fix: 0.
- Corroborating anchor, B2_464_caller_census_20260926.md:83: `C6 qdrop story citing "rows_scanned 757667", true only under pre-wiring` (the same correction named by the B2-464 evidence this brief self-fed from).

## Work done

- mag/catalog_rescan.py: C6 paragraph rewritten with the B2-506 correction block (pre-wiring vs post-wiring semantics, stale-scan arm behavior, and the lesson that stands either way: the export postdated the snapshot).
- mag/mcp_server.py: security-posture paragraph rewritten to name backend/server.py as the dispatch site and dashboard/rest.py as importing no TOOL_MAP, dated and labeled as the B2-506 correction of the prior sentence.
- ast.parse green on both files; fossil greps confirm the old claims are gone (the surviving "rows_scanned 757667" occurrence is inside the correction sentence that disambiguates it, which is the fix the brief asked for).

## Falsifier

The brief's falsifier: "grepping the two files today finds both fossils" (true pre-fix) "and after the fix the qdrop C6 story states the engine split explicitly" (true post-fix, quoted above). Reopen if: the mcp_server docstring again attributes /run_task to the dashboard, or a census quote of the qdrop probe reuses 757,667 without the pre-wiring qualifier.

## Bibliography closed

Read: mag/catalog_rescan.py (docstring + policy section), mag/mcp_server.py (docstring), backend/server.py (import + /run_task route lines), dashboard/rest.py (TOOL_MAP grep, no match), watch/inbox/burn_wave_20260926/B2_464_caller_census_20260926.md (evidence anchors 5 and 12 region), QUEUE.md B2-506 row. No external sources.
