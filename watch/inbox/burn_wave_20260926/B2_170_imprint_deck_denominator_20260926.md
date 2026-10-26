# B2-170 imprint/deck links denominator 2026-09-26

## Verdict

Landed. Both consumers of watch/inbox/LINKS.jsonl now report link rows and event rows as separate denominators per the B2-28 schema split: scripts/build_fleet_imprint.py prints "284 link rows + 53 event rows + 1 migration marker = 338 lines total (B2-28 split)" (measured live) and previews link rows only, and scripts/build_deck.py ledgers card plus CLI summary carry links_rows=284 and links_events=53. The old single "canonical rows"/"rows" count that mixed 280-era links with cohabiting event rows is gone from both surfaces. Falsifier seed retired: the 332-style mixed count can no longer be read as a links denominator.

## Evidence file:line quotes

- scripts/build_fleet_imprint.py:292 (pre-edit): `rows = [l for l in lk.read_text(...).splitlines() if l.strip()]` then line 293 `lines.append(f"- {len(rows)} canonical rows:")` counted every line, event rows included.
- scripts/build_deck.py:131 (pre-edit): `lines = [l for l in read(links).splitlines() if l.strip()]`, line 139 `led["links"] = {"rows": len(lines), ...}` same mixed count; deck template line 640 rendered `${L.links.rows}</span> rows`.
- watch/inbox/LINKS.jsonl bytes 2026-09-26: 338 lines = 284 link rows + 53 event rows + 1 migration marker (line 332, schema migration-marker.v1); EVENTS.jsonl holds 51 mirrored rows.
- B2-28 falsifier (d) FIRED, named here: two scout event rows landed in LINKS.jsonl AFTER the line-332 marker: line 333 id ALERT-ORACLE-CUT (kind ALERT, writer free-resource-scout, ts 2026-09-22T15:00:00Z) and line 334 id SCOUT-QUIET-LANES (kind finding, ts 2026-09-22T15:01:00Z). The B2-28 law says new event filings go to EVENTS.jsonl; these two bypassed that door. Not erased (append-only law); filed as owed to the B2-28 owner.

## Work done

1. Read the brief's cited regions and the B2-28 receipt (B2_28_schema_split_20260926.md) to fix the classification rule before editing (spec-first).
2. scripts/build_fleet_imprint.py: added json_row_kind() classifier (event = has kind, marker = schema migration-marker.v1, else link) and split the LINKS LEDGER section into per-denominator counts with link-only preview.
3. scripts/build_deck.py: added _links_row_kind(), mine_ledgers() now emits rows (link only), events, markers, total_lines; last5 preview draws from link rows only (event rows previously showed empty url in the card); deck card and CLI summary print both denominators.
4. Verified end to end: py_compile clean; build_fleet_imprint.py run ok (digest 8054bc88134d4e3b, 404309 bytes, new line 1514 in FLEET_IMPRINT_20260917.md); build_deck.py run ok (links_rows=284 links_events=53); classification cross-checked against raw bytes (284/53/1).
5. Gates: violation_ratchet check --changed has zero NEW hits on my files (the one NEW, file-too-long mag/shared_surface.py:472, is another lane's concurrent edit, not mine); em-dash count in my added lines = 0.

## Falsifier

Dies if: (a) either script again reports a single undivided LINKS.jsonl count (the string "canonical rows:" or a rows field equal to total lines returns); (b) the split classification diverges from bytes, e.g. link_rows + event_rows + markers != total lines; (c) an event-kind row lands in LINKS.jsonl past the current line 338 and neither EVENTS.jsonl nor a receipt names it (extends the fired B2-28 falsifier (d), lines 333-334 already on record here).

## Bibliography closed

Read whole: scripts/build_fleet_imprint.py, scripts/build_deck.py, mag/link_library.py, watch/inbox/burn_wave_20260926/B2_28_schema_split_20260926.md. Bytes verified: all 338 LINKS.jsonl lines classified, EVENTS.jsonl 51 rows counted, FLEET_IMPRINT_20260917.md line 1514, deck CLI output. Commands: py_compile, both builders run live, ratchet check --changed, git diff em-dash scan. Nothing synthesized.
