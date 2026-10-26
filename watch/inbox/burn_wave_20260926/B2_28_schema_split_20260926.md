# B2-28 ledger schema split 2026-09-26

## Verdict

Landed. watch/inbox/EVENTS.jsonl is the new canonical event ledger (schema event.v1): 51 rows mirrored from LINKS.jsonl, each carrying "schema": "event.v1" plus "origin": {"file", "line"} pointing at its source line. LINKS.jsonl is link rows only going forward; the 51 originals stay in place untouched per the append-only law, and a migration marker row (LINKS.jsonl:332, schema migration-marker.v1) records the split in-ledger. The brief said 31 event rows; the true count is 51: 31 scout/seat rows (lines 275-305, the B2-06 census) plus 20 endpoint-news rows (lines 312-331) filed by the B2-03 lane after B2-06 ran. Spec first: the mag/link_library.py docstring (the ledger's owning schema doc) was rewritten before the reader code. Append-only held: git diff = 1 insertion, 0 deletions; lines 1-331 byte-unchanged (sha256 f7e93cfb7b280583... still equals the INDEX.json sealed hash).

## Evidence

- `mag/link_library.py` (pre-edit) `known_canonicals` filtered `if e.get("canonical")` and `dupes` filtered `entry.get("duplicate_of")`: the 51 event rows were skipped by accident of missing keys, not by design; the docstring documented only the link shape.
- Counts from bytes: 331 lines all parse clean, 280 link rows, 51 event rows; kinds ALERT x8, alert x1, finding x37, correction x1, operator-post x1, receipt x1, verdict x2 (the brief's verdict x2 matches exactly; finding and ALERT grew with the endpoint-news rows).
- `scripts/endpoint_news.py:28` writes watch/inbox/endpoint_news/endpoint_news.jsonl; no in-repo code appends event rows to LINKS.jsonl, so both cohorts were hand-appended by lanes (scout rows 09-20..09-22, endpoint-news rows 2026-09-26T11:37:05Z).
- Consumers verified tolerable after migration: known_canonicals() = 266 distinct canonicals and dupes = "8 duplicate submissions on file", both matching B2-06; `tools/research.py:48-62` can return an event row with an empty pointer (pre-existing); `scripts/build_fleet_imprint.py:292-296` counts all rows as "canonical rows" (pre-existing miscount); `scripts/build_deck.py:133-139` shows empty url on event rows in last5 (pre-existing).

## Work done

1. Baseline: classified all 331 rows (280 link / 51 event / 0 other / 0 malformed), read the 51 event rows in full, fingerprinted LINKS.jsonl (f7e93cfb... = INDEX seal; observed pre-existing mixed line endings 191 CRLF / 141 LF, left alone).
2. Spec: link_library docstring rewritten to own the split; added EVENTS constant and load_events(), which refuses schema-less or origin-less rows so the cohabitation cannot rot back silently.
3. Migration via .venv/Scripts/python.exe: mirrored 51 rows to EVENTS.jsonl preserving key order and values; appended the marker row to LINKS.jsonl.
4. Fidelity: 51/51 copies verified key-order-equal and value-equal to their origin lines.
5. Tests: 2 added to tests/test_link_library.py (missing file returns empty, schema-less refusal); suite 26/26.
6. Gates: ratchet PASS NEW=0; shared_surface validate ok:false pre-existing (unindexed-file disease, B2-41 territory); EVENTS.jsonl and this receipt join the unindexed set, named owed here.
7. Self-fed: writer enforcement, research.py pointers, imprint/deck denominator (B2-108/109/110).

## Falsifier

Dies if: (a) `git diff -- watch/inbox/LINKS.jsonl` ever shows a deletion or lines 1-331 drift from f7e93cfb...; (b) any EVENTS.jsonl row diverges from its origin line (rerun the equality check); (c) known_canonicals() != 266 or dupes != 8; (d) a kind row lands in LINKS.jsonl after line 332, proving the convention failed.

## Bibliography closed

Read whole: mag/link_library.py, scripts/endpoint_news.py, tests/test_link_library.py, watch/inbox/burn_wave_20260926/QUEUE.md, watch/inbox/burn_wave_20260926/B2_06_link_dupes_20260926.md, watch/inbox/SHARED_SURFACE_CONTRACT.json. Bytes: all 331 LINKS.jsonl rows parsed and classified, 51 event rows read in full, EVENTS.jsonl 51/51 re-verified against origins. Commands: pytest 26/26, link_library dupes/check, ratchet NEW=0, shared_surface validate. Nothing synthesized.
