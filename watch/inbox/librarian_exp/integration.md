# LIBRARIAN EXPEDITION: INTEGRATION REPORT (division B, integration lens)

Date: 2026-10-01. Lane: integration. Raw evidence: `watch/inbox/gala_20260925/librarian-expedition/lanes/integration.check.txt` (sections [0]..[11], every command + exit banked).

## Verdict

The expedition was NOT done when I picked it up: 9 of the 10 gathered primaries had zero catalog rows (unfindable by any engine), and the B2-465 freshness gate read STALE exit 2, so even the one registered holding (DESCENT_DAY1_STEAL_20261001.md) was findable only via scan fallback. I paid the integration debt with the two sanctioned writers; all 10 holdings are now proven searchable by real FTS5 queries on a fresh deep-verified index.

## Holdings delta (before / after)

| measure | before (section [0]) | after (sections [5], [9]) |
|---|---|---|
| catalog rows (repo HEAD) | 691,788 | 691,788 (unchanged; delta is uncommitted work) |
| catalog rows (working tree) | 691,789 | 821,676 |
| gathered primaries registered | 1 of 10 | 10 of 10 |
| gathered primaries + their retrieval receipts | 1 row total | 19 rows (9 primaries x2 + 1 steal; receipts live in docs/report_v1/sources/receipts/, zone doctrine) |
| FTS index rows | stale gate exit 2 | 821,676 indexed, deep sha256 "match" |
| map manifest snapshot_ts | 2026-09-30T07:32:33Z | 2026-10-01T23:39:05Z (tags_ts) |

The working-tree map had moved exactly +1 row past HEAD before I ran anything (the DESCENT steal, mtime 2026-10-01T21:36:43Z). The gather landed its primaries 2026-09-30T16:44Z..22:56Z, after the last map snapshot (2026-09-30T07:32Z), so they sat unregistered for roughly 25 hours: the delta of +125,884 added / +3,597 refreshed rows in my rescan pass is the whole estate catching up, of which the expedition's 10 holdings are the 19 rows above.

## FTS searchability of the new primaries (real queries, same driver both phases)

Driver: `lanes/integration_search.py` (loads tools/corpus.py hermetically, calls the estate's real corpus_search). Before ([3]): 9 of 10 queries hit_count 0 on BOTH engines; descent_day1 hit_count 1 but engine=scan, index_state=stale. After ([8]): all 10 queries hit, engine=fts5, index_state=fresh:

| query | after hits | finds |
|---|---|---|
| 2310.10158 | 2 | persona_priorart_2310.10158.pdf + its receipt |
| 2405.07248 | 2 | persona_priorart_2405.07248.pdf + receipt |
| 2506.11798 | 2 | persona_priorart_2506.11798.pdf + receipt |
| 2506.12657 | 2 | persona_priorart_2506.12657.pdf + receipt |
| 2508.06149 | 2 | persona_priorart_2508.06149.pdf + receipt |
| 2508.06950 | 2 | persona_priorart_2508.06950.pdf + receipt |
| 2511.17813 | 2 | persona_priorart_2511.17813.pdf + receipt |
| wilkes | 2 | computing_1951 wilkes/wheeler/gill txt + receipt |
| godfrey edvac | 2 | computing_2010 godfrey intro to EDVAC txt + receipt |
| descent_day1 | 1 | corpus/steal/DESCENT_DAY1_STEAL_20261001.md |

Engine note (read from tools/corpus.py:133-138, _fts_expr): multi-word queries are ANDed independent quoted prefix terms, never adjacency phrases, by design kept verbatim from the B2-22 spike; the "wilkes wheeler" hit is correct AND semantics, not a phrase match.

## Register / INDEX state

- INDEX (catalog/catalog.jsonl): CLEAN. All 10 holdings registered (grep proof [5]), map manifest written by the sanctioned arm, map sha256 cc7e01e4b289... then 073a27176513... after the second live pass, both matching the FTS meta deep check.
- Register (CORPUS_CATALOG.md): NOT CLEAN, pre-existing. Its own header reads "CANON MANIFEST: DRIFT - checked 205, missing 0, drifted 4 - resolve before trusting the shelves". My named probe ([1], canon_drift.py, mirrors mag/librarian_catalog.py verify_canon) names the 4: `_retired/x_canon_nachoquixotic_v1.jsonl`, `x_canon_2026_fx/fx_2094770591702098071.json`, `x_canon_2026_fx/fx_2096341325960417585.json`, `x_canon_enumeration_index.jsonl`. These are x_canon fixture/ledger files that moved after sealing. I did NOT re-seal the canon manifest (operator territory); the drift predates the expedition and is unchanged by it.

## Integration gaps (what the next seat must know)

1. Gather is not integrate. Bytes landing in corpus/ change nothing a reader can search until `mag.catalog_rescan incremental` runs. The gather lanes left receipts (good) but no lane ran the map/FTS integration; the debt sat ~25h.
2. Both daily freshness surfaces were DARK today: logs/fts_index.log and logs/corpus_rescan_daily.log contain zero 2026-10-01 stamps ([10]); last entries 2026-09-30 09:00. Both schtasks exist and read Ready with next-run 10/2, but Logon Mode: Interactive only, so a skip is silent. This is exactly the B2-465 incident class (no START stamp today = surface dark). My pass healed the decay by hand this once; the operator response per B2-465 (inspect why today's runs did not fire) is still owed.
3. Title extraction on the new rows is weak (the wilkes txt row's title field is just "WHEELER"); findability rides on path tokens, which FTS does index. Observation only, no action taken.
4. CORPUS_CATALOG.md is written by mag/librarian_catalog.py run_once, a different writer than the map rescan; its shelf counts lag the map I just advanced. No action taken.

## One-command repeat-verdict

Ran for real, exit 0, deep "match" ([11]):

```
cd C:/Users/foste/Documents/projects/local_sovereign_agent && .venv/Scripts/python.exe -m mag.catalog_rescan incremental && .venv/Scripts/python.exe tools/corpus_fts_rebuild.py && .venv/Scripts/python.exe tools/corpus_fts_rebuild.py --check --deep
```

Integration: rerunnable from that one line any time. Gather: no saved one-line entry point exists that I could find in this session (no librarian-expedition .dwf.ts under .zcode/workflows/, no row in memory/workflows/REGISTRY.jsonl; workflow-run introspection was unavailable to this session); the gather rode this gala run's inline asks. If the expedition should be repeatable, saving its workflow is the gap to close.

Ratchet: no code under mag/ or tools/ was touched by this lane (drivers live in the lanes dir), so the violation_ratchet conditional does not trigger.
