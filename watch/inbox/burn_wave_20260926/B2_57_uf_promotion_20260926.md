# B2-57 UF-119/UF-122 promotion check 2026-09-26

## Verdict

UF-119 (corpus MCP attack list, 3417 chars, groq-qwen, raw.jsonl: 2026-09-26T11:35:12Z): PARTIAL, 3 of 8 attacks survive. PROMOTED: attack 5 (corpus_tail undercount, real but cause is the 256KB window, not CRLF) and attack 7 (truncation invisibility, limit honored but totals hidden). Attack 2 and 6 are true restatements of fold conditions the prompt already accepted, filed as patch leads, not new findings. REJECTED as false against bytes: attack 1 (zone filter works per-row), 3 (search IS tokenized AND, the answer inverts it and its patch would install false docs), 4 (structured "binary refused" exists), 8 (realpath confinement refuses traversal). UF-122 (50-question eval spec, 4363 chars, groq-qwen2): SCAFFOLD PROMOTED with 3 named defects: arithmetic yields 55 not 50 (10 zones x 5 + 5 ext), requested zones queue and lsa silently dropped, all 11 example anchor files do not exist. The check itself found a defect neither answer named: corpus_search pointers and corpus_get addresses are on different path namespaces, so search-then-get fails on first use.

## Evidence

- Zone filter real: tools/corpus.py:115 `if zone and row.get("zone") != zone: continue` applied per row before append; probe corpus_search("grounding", zone="code") = 6 hits, all zone "code"; no public/private zone exists in the census.
- Tokenized AND real: corpus.py:84 `terms = [t for t in (query or "").lower().split() if t]` + :113 `all(t in hay for t in terms)`; probe "chain grounding" and "grounding chain" both return the same 2 hits.
- Binary refusal real: corpus.py:142 `return {"ok": False, "error": "binary refused"` before decode; residue: sniff corpus.py:69 checks only first 8192 bytes for null.
- Traversal refused: corpus.py:31-39 `_confine` realpath; probe refused "../../etc/passwd" and "C:/Windows/win.ini".
- Tail undercount TRUE: corpus.py:166 `chunk = min(size, _MAX_BYTES)` then splitlines()[-lines:]; probe corpus_tail(raw.jsonl, lines=500) served 115 (fat 3-4KB rows); catalog.jsonl served 500, so CRLF/multi-line-JSON cause is wrong.
- Truncation invisible TRUE: corpus.py:126 `if len(hits) >= limit: break`; probe "md" limit=100 gives hit_count 100, rows_scanned 9846, no total_matches or truncated key.
- New defect: corpus_search returns "local_sovereign_agent/scripts/grounding_chain.py" (scanner ROOT mag/catalog_scan.py:11 is the projects dir) and corpus_get refuses it; repo-relative "scripts/grounding_chain.py" serves.
- Dead zone: catalog_scan.py:14 EXCLUDE contains "catalog" while both zone maps define it; zone="catalog" scans 757,667 rows, 0 hits; catalog total is 757,667, not the 947K in corpus.py:6 and the prompt.
- UF-122 anchors: probe os.path.isfile all false for intake/sla_policy.md, watch/detector_rules.py, games/rules.md, ext/dependencies.txt and the other 7; census: queue 678 rows, lsa 157,715 rows exist but untemplated.

## Work done

Read mag/mcp_server.py, tools/corpus.py, scripts/union_fullsend_day.py, mag/catalog_scan.py whole; extracted both raw.jsonl rows and confirmed chars (3417/4363) match the brief; ran watch/inbox/burn_wave_20260926/B2_57_probe.py plus 3 follow-up probes live through the real tools; adjudicated all 8 attacks and the spec zone by zone; promoted survivors via this receipt per the DAY_PACK law "A lead is promoted only by a byte check"; filed leads B2-156..158; LEDGER row appended.

## Falsifier

Invert claim-1 rejection with any query where zone set returns cross-zone hits. Invert the tail-window cause with a >256KB-row ledger serving 500 lines. Invert the namespace defect with corpus_get accepting a corpus_search path verbatim. Invert UF-122 defect (c) by globbing any of the 11 anchor paths to existence.

## Bibliography closed

watch/inbox/union_fullsend_20260917/{queue.jsonl:119,122, raw.jsonl UF-119/122 rows, DAY_PACK.md:344,405}; tools/corpus.py; mag/mcp_server.py; mag/catalog_scan.py; scripts/union_fullsend_day.py:380-383; watch/inbox/burn_wave_20260926/{B2_07_grounding_20260926.md, B2_16_uf_sweep_20260926.md, B2_57_probe.py}; live probes via .venv python. No web sources used.
