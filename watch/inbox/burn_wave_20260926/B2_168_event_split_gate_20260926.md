# B2-168 Enforce the event split (SW-06, 2026-09-26)

## Verdict

HOLDS. The B2-28 schema split (LINKS.jsonl link-rows-only past the
migration marker) now has a validate door: `mag.shared_surface.validate`
fails on any NEW event-kind row appended to watch/inbox/LINKS.jsonl after
the B2-28 marker row, grandfathering pre-gate debt by content sha256 in
configs/links_kind_baseline.json (the B2-42 pattern). The two scout rows
that landed after the marker before this gate existed (lines 333-334) were
mirrored into watch/inbox/EVENTS.jsonl with origin provenance per the
B2-28 pattern and registered as debt; nothing was erased. Scout and
endpoint-news event filings are repointed: the repoint doc lives in
mag/link_library.py (B2-28 block, "New event filings go to EVENTS.jsonl
... never LINKS.jsonl") and the gate now enforces it with an error naming
EVENTS.jsonl, schema event.v1, and the load_events() parse path.

## Evidence file:line quotes

- watch/inbox/LINKS.jsonl:332 (marker row): `{"seq": 1790425909127296, "ts": "2026-09-26T12:31:49+00:00", "schema": "migration-marker.v1", "writer": "b2-28-schema-split", "note": "SCHEMA SPLIT 2026-09-26: LINKS.jsonl is link rows only going forward; ..."}`
- watch/inbox/LINKS.jsonl:333 (post-marker kind row, grandfathered sha e038df51e176fb719703715f40166dabb86aef944b1bb5de5ef270f8bc5fb37d): `{"ts": "2026-09-22T15:00:00Z", "writer": "free-resource-scout", "id": "ALERT-ORACLE-CUT", "kind": "ALERT", ...}`
- watch/inbox/LINKS.jsonl:334 (post-marker kind row, grandfathered sha d039deb5114f2b9d95a094d9b650deca1e55c28cdb46db09f841a88bd620a530): `{"ts": "2026-09-22T15:01:00Z", "writer": "free-resource-scout", "id": "SCOUT-QUIET-LANES", "kind": "finding", ...}`
- watch/inbox/EVENTS.jsonl:52 (mirrored provenance row): `"origin": {"file": "watch/inbox/LINKS.jsonl", "line": 333, "sha256": "e038df51...", "mirrored_by": "SW-06 B2-168 2026-09-26: post-marker kind row registered as debt and mirrored into the event ledger per the B2-28 provenance pattern"}`
- mag/links_split_gate.py:47-48: `def links_split_check(links_ledger: Path, baseline_path: Path, errors: list[str], warnings: list[str]) -> None:` (the validate-door gate)
- mag/links_split_gate.py:84-89 (the error text): `f"NEW event-kind row in LINKS.jsonl (line {rec['line']}, id {rec['id']!r}, kind {rec['kind']!r}, writer {rec['writer']!r}): LINKS.jsonl is link rows only past the B2-28 marker; file events in watch/inbox/EVENTS.jsonl (schema event.v1) via mag.link_library.load_events"`
- mag/shared_surface.py:265-266 (wiring): `# B2-168 LINKS event split; spec: mag/links_split_gate.py docstring.` / `links_split_check(LINKS_LEDGER, LINKS_KIND_BASELINE, errors, warnings)`
- mag/link_library.py:23-25 (repoint doc, pre-existing B2-28): `New event filings go to EVENTS.jsonl via load_events() as the parse path, never LINKS.jsonl.`
- scripts/endpoint_news.py:27-28 (endpoint-news writes its own file, not LINKS): `OUT = ROOT / "watch" / "inbox" / "endpoint_news"` / `NEWS = OUT / "endpoint_news.jsonl"`

## Work done

- New module mag/links_split_gate.py (145 lines, under the ratchet 400
  bar): MARKER_SCHEMA/MARKER_WRITER, links_split_marker_line(),
  scan_links_kind_rows() (records {line, id, kind, writer, sha256} for
  post-marker kind rows), links_split_check() (extends validate's error
  and warning lists; missing baseline registry is an error, missing marker
  and missing LINKS.jsonl are warnings).
- mag/shared_surface.py: docstring spec pointer, re-export import block,
  2-line wiring inside inspect_surface(); file held at exactly 400 lines
  because the sibling-module pattern (the B2-342 events_key_schema
  pattern) keeps the ratchet's file-too-long law un-tripped: final ratchet
  check --changed PASS NEW=0 (hits 42, registered 42).
- configs/links_kind_baseline.json: new debt registry registering the two
  pre-gate post-marker rows by content sha256 (lines 333-334), why-notes
  naming each.
- watch/inbox/EVENTS.jsonl: appended 2 mirrored provenance rows (52-53)
  for those same rows; LINKS.jsonl bytes untouched (append-only law).
- Fixture-first pins in tests/test_shared_surface_events.py (7 new tests:
  post-marker kind row errors with line number and EVENTS.jsonl pointer;
  legacy rows before marker pass; register rows after marker pass;
  grandfathered post-marker row passes via baseline; missing marker
  warns; missing file warns; real LINKS.jsonl matches the registered
  baseline). Suite: 21 passed. Red run recorded before implementation:
  4 failed / 16 passed with scan absent (first pins), then 6 failed after
  fixture patching exposed the missing constants; green after landing.
- Late-claim disclosure: this lane's first edits to mag/shared_surface.py
  and tests/test_shared_surface_events.py landed at about 19:40Z BEFORE
  the SW-06 CLAIM lines were appended to QUEUE.md at 19:45:47Z (the lane
  initially mis-read them as not-yet-shared); claims are on the board now
  and no foreign write was clobbered (SW-11's active claim on
  mag/shared_surface.py was honored: their split had already landed, my
  additions rebased on their bytes and the file is held at 400 lines so
  their pruned file-too-long fingerprint does not re-trip).

## Falsifier

Brief falsifier: "a scout or endpoint-news event row filed into
watch/inbox/LINKS.jsonl today fails validate" - executed live in both
directions. Red: with the gate absent, the two real post-marker scout rows
(lines 333-334) were invisible to validate (0 errors). Green: with the
gate landed and the baseline registry removed, live
`.venv/Scripts/python.exe -m mag.shared_surface validate` reports exactly
2 errors `NEW event-kind row in LINKS.jsonl (line 333, id
'ALERT-ORACLE-CUT' ...)` and `(line 334, id 'SCOUT-QUIET-LANES' ...)`;
with the registry present (shipped state) live validate reports 0 links
errors and 21/21 pins pass, including the real-file pin that fails if any
unregistered post-marker kind row exists on disk. Falsifier test:
tests/test_shared_surface_events.py::test_links_new_kind_row_after_marker_is_an_error
and ::test_real_links_jsonl_matches_the_registered_baseline.

## Bibliography closed

- watch/inbox/LINKS.jsonl:332 (B2-28 migration marker, read 2026-09-26)
- watch/inbox/LINKS.jsonl:333-334 (post-marker scout rows, sha-registered)
- watch/inbox/EVENTS.jsonl:1-3, 52-53 (event.v1 origin provenance shape)
- mag/link_library.py:15-25, 137-158 (ledger doc, split doc, load_events)
- mag/shared_surface.py (B2-42 events hygiene + B2-342 key schema patterns)
- mag/events_key_schema.py (sibling-module precedent for the 400-line bar)
- configs/events_malformed_baseline.json (grandfather pattern copied)
- scripts/endpoint_news.py:13-15, 27-28 (endpoint-news writer target)
- watch/inbox/burn_wave_20260926/QUEUE.md B2-168 row (brief text)
- watch/inbox/burn_wave_20260926/B2_28_schema_split_20260926.md (owning receipt of the split this gate enforces)
