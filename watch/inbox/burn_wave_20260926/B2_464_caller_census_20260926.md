# B2-464 corpus_search caller census after the FTS5 wiring, 2026-09-26

## Verdict

CLEAN ON THE PRODUCT SURFACE, ONE CONFIRMED MISREAD IN THE BURN PROBES. Every
product consumer of corpus_search (tools TOOL_MAP registries, backend/server.py
/run_task, mag/mcp_server.py + mcp_http.py MCP transports, mag/agent_cli.py,
dashboard backend and static, scripts/) passes the result through whole or reads
only ok/ok-adjacent fields; none reads rows_scanned, hit_count, or engine with
math or labels that break under the fts5 shape. The falsifier is CONFIRMED on
exactly one caller: watch/inbox/burn_wave_20260926/B2_22_fts5_spike.py, whose
baseline arm (line 155 calls the production corpus_search with no scan force)
hardcodes "engine": "scan" at line 159 and classifies the full-scan class at
line 196 by rows_scanned >= rows_indexed, a predicate that is only true under
the pre-wiring lines-read semantics; re-run today it silently measures
fts5-vs-fts5 and every class median lands None. Two prose fossils filed as
self-fed briefs, no code misreads beyond the spike. Live context this lane: the
production index is currently STALE (catalog/catalog.jsonl rewritten
2026-09-26T19:16:30Z, 133,894,969 bytes / 489,548 rows by a concurrent rescan
while catalog_fts.sqlite still answers from the 18:55:08Z build over
214,470,472 bytes), so production searches honestly answer engine=scan,
index_state=stale today; the fts5 shape was verified on a hermetic mini-index
and by the 11 test pins (11 passed). The B2-104 map-plane stamp
(map_asof/map_age_hours/map_stale) landed on tools/corpus.py mid-census; this
census rebased on the post-landing bytes and verified the added fields are
additive and read by no caller.

## Evidence

All numbers read from bytes or run live this session, 2026-09-26 19:05 to
19:25Z. Caller-by-caller census; every consumer of corpus_search,
rows_scanned, hit_count, or engine found by repo-wide grep (code trees mag/,
tools/, dashboard/ backend+static, scripts/, tests/, burn probes, main.py,
backend/), prose-only hits in receipts/QUEUE/docs classified and excluded.

1. tools/corpus.py (the shape, current bytes with B2-104 rebased): fts5 result
   = ok/tool/engine=fts5/index_state=fresh/hits/hit_count/rows_scanned=
   walked/parity_note + map_asof + map_age_hours + map_stale + law, and NO
   index_note; scan result = engine=scan/index_state/index_note/hits/
   hit_count/rows_scanned=lines-read + the same three map_* fields, and NO
   parity_note; error shape = ok:False + error (kind unmatched, catalog
   unreadable) with no engine field at all.
2. fts5 rows_scanned semantics proven live on a hermetic mini-index (2 rows,
   both match "garden notes", zone=runs filter): hit_count 1, rows_scanned 2,
   i.e. walked counts matched rows BEFORE the zone/ext/tag/since filters; it is
   neither lines-read nor hits. Scan path verified live on production
   (stale-gate day): query "verkle" limit 3 -> engine=scan, index_state=stale,
   index_note naming tools/corpus_fts_rebuild.py, hit_count 3, rows_scanned
   136 (early-break lines-read); termless -> engine=scan, index_state=bypassed,
   rows_scanned 2.
3. tools/__init__.py TOOL_MAP (both registries, lines 36 and 204) + dispatch:
   pure pass-through lambdas/function refs, zero result-field reads. CLEAN.
4. backend/server.py /run_task (the dispatch mag/mcp_server.py:14 calls the
   "dashboard /run_task"): reads only result["ok"] for the failure-KB counter
   and embeds the whole result in the envelope. Additive map_* fields ride
   through harmlessly. CLEAN.
5. mag/mcp_server.py: corpus_search appears only in role allowlists (nurse,
   scout, historian, full _READ_TOOLS set) and call_tool() dumps the whole
   result as one JSON text; _tool_meta classifies it
   read_or_deterministic_compute with no shape claims. CLEAN. Docstring line 14
   wording nit ("/run_task" lives in backend/server.py; dashboard/rest.py
   imports no TOOL_MAP at all) -> self-fed B2-500.
6. mag/mcp_http.py: transport-only adapter, delegates to mcp_server.handle ->
   call_tool, same pass-through. CLEAN.
7. mag/agent_cli.py: TOOL_MAP used for listings and the unknown-tool error;
   _run_tool proxies to the backend HTTP seam; no result-field reads. CLEAN.
8. dashboard/rest.py: no corpus_search, no TOOL_MAP import; the two "corpus"
   hits are dig_leaf/corpus_leaf edge-kind names (line 906) and research-lens
   prose (line 2343). NOT A CALLER.
9. dashboard/static: room_state.json + room_state.prev.json +
   salon_lightmap.html carry hit_count_200, the room-state wall fire histogram
   (mag/room_state.py:252 writes it); room_state.json contains zero "corpus"
   strings. NAME COLLISION ONLY, NOT A CALLER. vislab/catalog.html, the decks,
   and steal_tools_data.js embed their own generated JSON; none reference
   corpus_search. NOT CALLERS.
10. tools/research.py: hit_count at line 105 is research_search's own result
    field on its own tool; research.py never imports or calls corpus_search
    (the corpus_get mention is prose in its law line). NAME COLLISION ONLY.
11. scripts/: verkle_territory_audit.py's executable_kzg_hit_count is its own
    domain field; build_vislab_catalog.py and corpus_packer.py walk files
    directly. NO corpus_search CALLERS IN scripts/.
12. mag/catalog_rescan.py: exactly one mention, docstring prose (line 9, the
    C6 qdrop story citing "rows_scanned 757667", true only under pre-wiring
    scan semantics); no code reads any corpus_search result field. It IS the
    catalog writer whose 19:16:30Z run staled the index without chaining an
    FTS rebuild -> self-fed B2-499.
13. tests/test_corpus_fts.py: 15 corpus_search calls; asserts engine,
    index_state, index_note, parity_note contents, law prefix, and hit_count
    == 4 on the termless early-break (scan path, still scan post-wiring); ZERO
    rows_scanned asserts. Live run this lane: 11 passed in 0.39s. ALIGNED.
14. watch/inbox/burn_wave_20260926/B2_57_probe.py: 6 corpus_search calls; all
    result reads are .get() display-only (hit_count, rows_scanned, sorted key
    dump); no arithmetic on rows_scanned; the additive map_* fields will flow
    into its "keys" dump without breaking anything. CLEAN. (B2_94 and B2_85
    probes import tools.wandr_selfeval / tools.shell, not corpus.)
15. watch/inbox/burn_wave_20260926/B2_22_fts5_spike.py: THE MISREAD. Line 65-66
    build_index() DELETES the production db and rebuilds the spike-era
    meta-less schema, so on a re-run _fts_state() returns fresh-by-mtime-only
    and the line 155 baseline corpus_search takes the index path; line 159
    hardcodes "engine": "scan" regardless; line 196 classifies
    full = [q for q in QUERIES if scan_by_q[q]["rows_scanned"] >=
    out["build"]["rows_indexed"]], which under fts5 rows_scanned=walked (never
    757,667) yields full=[] and therefore full_scan_median_ms /
    full_scan_best_ms / fts5_same_queries_median_ms /
    fts5_same_queries_best_ms all None. The spike's displayed class math
    DEPENDS on rows_scanned meaning lines-read. Falsifier CONFIRMED ->
    self-fed B2-498.
16. B2_22_fts5_results.json (stored spike output): scan-arm rows_scanned
    757667 for the full-scan class and 5,985-598,529 for early-break queries,
    honest for its pre-wiring timestamp; a data fossil, not a live consumer.
17. Freshness gate proven live against a real concurrent write: catalog mtime
    19:16:30Z vs db mtime 18:55:08Z -> _fts_state() = stale, production search
    answers scan with the reason and the rebuild command, never silently stale.

## Work done

- Read the pointer receipt (B2_102_fts5_wiring_20260926.md) and the current
  tools/corpus.py bytes; pinned both result shapes from code before sweeping.
- Repo-wide caller sweep (corpus_search, rows_scanned, hit_count, engine,
  TOOL_MAP consumers) over mag/, tools/, dashboard/ backend and static,
  scripts/, tests/, backend/, main.py, and watch/inbox/burn_wave_20260926/
  probes; 16 caller classes adjudicated above, each verdict from the file's
  own bytes.
- Live probes via .venv/Scripts/python.exe only: production shape probe
  (stale-gate day, both term and termless), hermetic mini-index build + fts5
  shape probe (parity_note present, index_note absent), walked-before-filters
  demo (rows_scanned 2, hit_count 1 under a zone filter), pytest
  tests/test_corpus_fts.py = 11 passed, stat pair proving the live stale gate.
- Rebased mid-lane per the claim law: B2-104's map_freshness stamp landed on
  tools/corpus.py after this lane's first read; bytes re-read, census and
  probes re-run against the post-landing file; verdict unchanged (additive
  fields, zero readers). No files were edited by this lane; no CLAIM on
  tools/corpus.py needed or filed.
- Filed this receipt, the LEDGER row (json.dumps via .venv python), the INDEX
  register event, and self-fed B2-498 (spike re-run guard), B2-499 (rescan
  writer must chain the index rebuild), B2-500 (prose fossils) UNCHECKED with
  the band claim per the lane-id claim law.

## Falsifier

1. The census's central claim is that only B2_22_fts5_spike.py misreads the
   new shape: re-run the spike unchanged today and it prints
   full_scan_queries [] with full_scan_median_ms null while labeling its
   baseline arm engine=scan; if any OTHER caller turns out to branch on
   rows_scanned/hit_count/engine in a way this census missed, the sweep grep
   (corpus_search|rows_scanned|hit_count over the six trees, all hits
   adjudicated in Evidence) is the replay path.
2. The "no product consumer breaks" verdict rests on pass-through dispatch;
   if a consumer surfaces that renders hit_count as a fraction of rows_scanned
   (progress math), it would show fts5 completions as absurdly efficient
   rather than wrong counts, because hit_count <= rows_scanned holds on both
   engines; the failure mode would be cosmetic, not crashing, which is why the
   grep sweep rather than a runtime canary is the check.
3. The live stale-gate reading depends on the catalog staying newer than the
   db; once B2-465's rebuild or a manual tools/corpus_fts_rebuild.py run
   lands, production flips to the fts5 shape and the Evidence-2 production
   numbers (rows_scanned 136 scan-path) become historical; the fts5-arm
   numbers from the hermetic probe and the test pins remain the standing
   evidence.
4. The walked-before-filters proof is a 2-row construction; on the real index
   the same code path applies (identical loop), but a skeptic can re-derive it
   from tools/corpus.py's _search_fts: walked increments before the filter
   continues, hits append after.
5. This census scoped to corpus_search result consumers per the brief;
   corpus_get/corpus_tail/corpus_stats callers were only classified, not
   audited (corpus_stats gained the B2-104 stamp too; its total_rows 489,548
   live reading confirms the post-rescan map, nothing more).

## Bibliography closed

Read: watch/inbox/burn_wave_20260926/QUEUE.md (header law block + Open tail,
fresh reads 19:05 and 19:20Z); watch/inbox/burn_wave_20260926/
B2_102_fts5_wiring_20260926.md (whole); tools/corpus.py (whole, first read
~19:05Z, rebased re-read ~19:18Z after B2-104's landing); tools/__init__.py
(TOOL_MAP regions); backend/server.py (/run_task region); mag/mcp_server.py
(allowlists, _tool_meta, call_tool, docstring); mag/mcp_http.py (whole);
mag/agent_cli.py (_run_tool region); dashboard/rest.py (corpus-mention
regions); mag/room_state.py (header + hit_count_200 write);
dashboard/static/salon_lightmap.html (hit_count_200 regions);
dashboard/static/room_state.json (grep-verified zero corpus strings);
tools/research.py (hit_count region); mag/catalog_rescan.py (function map +
docstring); scripts/verkle_territory_audit.py (hit_count regions);
tests/test_corpus_fts.py (whole); tools/corpus_fts_rebuild.py (check region);
watch/inbox/burn_wave_20260926/B2_57_probe.py (whole);
watch/inbox/burn_wave_20260926/B2_22_fts5_spike.py (whole);
watch/inbox/burn_wave_20260926/B2_22_fts5_results.json (rows_scanned rows);
scripts/index_fold_host.mjs (usage header); memory/burns/LEDGER.jsonl tail;
watch/inbox/index_events.jsonl tail. Run: pytest tests/test_corpus_fts.py (11
passed), production shape probes x2 (pre- and post-rebase), hermetic fts5
probes x2, stat pair. No web sources. Every number in this receipt was read
from bytes or run live this session; nothing synthesized; em-dash count 0.
