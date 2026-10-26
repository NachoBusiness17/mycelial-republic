# B2-172 image-drop schema card 2026-09-26

## Verdict

Landed, per the B2-28 split-law shape. The undocumented third schema at LINKS.jsonl:256 (canonical "image-drop:fibonacci_determinants_plate_20260918.png", url = repo-relative file path, canonical_sha256 = sha256 of FILE BYTES) is now a documented class with its own register watch/inbox/IMAGE_DROPS.jsonl (schema "image-drop.v1", origin {file,line} = LINKS.jsonl:256, seed row byte-faithful) and a bytes verifier: `python -m mag.link_library verify-images` re-hashes every registered file and exits 1 on mismatch or missing file. Live run 2026-09-26: 1 row checked, OK, expected 2BD19E83... equals actual, exit 0. The original line 256 stays in LINKS.jsonl untouched per the append-only law; new image-drop filings go to the register, never LINKS.jsonl.

## Evidence file:line quotes

- watch/inbox/LINKS.jsonl:256 (bytes): `"canonical": "image-drop:fibonacci_determinants_plate_20260918.png", "url": "watch/inbox/fibonacci_determinants_plate_20260918.png", "canonical_sha256": "2BD19E83594EF847F252A1397C23510D1ABA1B358D4554D4C8F4451DD654DEDB"` with title/note describing the plate; no "schema" or "kind" key, so it is neither link-shape (canonical_sha256 of file bytes, not of canonical string) nor event-shape.
- File bytes hash 2026-09-26: sha256 of watch/inbox/fibonacci_determinants_plate_20260918.png = 2BD19E83594EF847F252A1397C23510D1ABA1B358D4554D4C8F4451DD654DEDB, matching the ledger row (brief said "proven 2026-09-26"; re-proven from bytes this lane).
- mag/link_library.py docstring pre-edit documented only link rows and the B2-28 event split; no surface named image-drop (verified by reading the whole module pre-edit).
- watch/inbox/burn_wave_20260926/B2_26_links_sha_backfill_20260926.md evidence block: the PENDING-URL backfill treatise treats canonical_sha256 as sha256(canonical) for link rows, which is exactly why the image-drop row (file-bytes hash) is a different schema, not a broken link row.

## Work done

1. Classified all 338 LINKS.jsonl lines by canonical scheme: 281 https, 2 http, 53 event-shape, 1 migration marker, 1 image-drop (line 256 only; the class has exactly one member).
2. Claim law honored first: mag/link_library.py and tests/test_link_library.py are working-tree-modified (B2-28/26/27/122/171 lanes), so three CLAIM lines (B2-172, 19:49:02Z) landed in QUEUE.md under Open before any claimed-byte edit; edits rebased on freshly-read bytes including the B2-122 known_canonicals rewrite and the B2-171 convention block.
3. Spec first: docstring paragraph "Image-drop register (B2-172, 2026-09-26)" landed in mag/link_library.py before the code; CLI index gained verify-images.
4. Code: IMAGE_DROPS path constant, load_image_drops() (refuses schema-less or origin-less rows), verify_image_drops() (re-hash from bytes, name MISSING/MISMATCH rows), CLI arm verify-images with exit 1 on any not-OK.
5. Register file: watch/inbox/IMAGE_DROPS.jsonl created with the mirrored seed row (schema image-drop.v1, origin LINKS.jsonl:256); verifier run live OK.
6. Tests: 4 pins appended to tests/test_link_library.py (missing register empty, schema-less refusal, OK-then-MISMATCH on a tampered byte, MISSING file named); suite 35 passed.
7. Gates: violation_ratchet check --changed has no NEW hits on my two files; em-dash scan of added lines: only the pre-existing B2-27 docstring paragraph carried byte-identical through the insertion (not my text, left untouched per no-erase); my authored lines have zero.
8. INDEX: register events appended to watch/inbox/index_events.jsonl for IMAGE_DROPS.jsonl and this receipt (class register/receipt, writer zcode-sw-08); INDEX.json materialization rides the next fold run, as with the B2-28 precedent.

## Falsifier

Dies if: (a) `verify-images` exits 0 while any register file's bytes differ from its row's canonical_sha256 (rerun after any touch of the png); (b) a second image-drop-shaped row (canonical starting "image-drop:") lands in LINKS.jsonl past line 338 instead of the register; (c) a schema-less or origin-less row in IMAGE_DROPS.jsonl parses without ValueError; (d) the mirrored register row diverges from LINKS.jsonl:256 on any mirrored field.

## Bibliography closed

Read whole: mag/link_library.py (pre-edit working tree incl. B2-28/26/27/122/171 landings), tests/test_link_library.py (tail), watch/inbox/burn_wave_20260926/B2_26_links_sha_backfill_20260926.md, watch/inbox/burn_wave_20260926/B2_28_schema_split_20260926.md, LINKS.jsonl all 338 lines classified. Bytes: png re-hashed live, register row verified OK. Commands: pytest tests/test_link_library.py 35 passed, verify-images CLI rc=0, py_compile via pytest import, ratchet check --changed, em-dash scan. Nothing synthesized.
