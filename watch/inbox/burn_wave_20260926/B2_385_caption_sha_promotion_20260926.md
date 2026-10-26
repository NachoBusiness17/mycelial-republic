# B2-385 Promote recovered sha256 into CAPTION_LEDGER via dated v2 (SW-07, 2026-09-26)

## Verdict

LANDED. Shape chosen and named: in-place patch plus INDEX re-seal (the B2-89/B2-90 precedent), not a v2 side file. 314 of 2,726 rows patched from the side register; the class now reads 2,375 have / 314 have-recovered / 37 metadata-only. INDEX verify passes on the new seal for this file and all 314 promoted rows resolve to a non-null sha256 backed by a file on disk (0 failures, spot hash re-verified). Status semantics decided in writing: "have-recovered" = a file on disk whose bytes hash to the recorded sha256, but the bytes are the t.me/s web-preview thumb, not the original export media (register row field size_matches_export_metadata false throughout); "have" stays reserved for original export media; provenance text is carried both in the register (persistent artifact) and in a new recovered_provenance field on each promoted row.

## Evidence file:line quotes

- QUEUE.md row: "land the B2-90-style dated v2 ... filling path, bytes and sha256 for the 314 rows from the side register, and decide the status semantics (have-recovered vs metadata-only-with-provenance) in writing".
- Pre-v2 ledger byte state: watch/inbox/CAPTION_LEDGER_20260926.jsonl sha256 A2C96FA49E02D60B959AF887627DC95F004CBE56C173E29D507473DC80466743, 1,490,857 bytes, 2,726 rows, 351 with null sha256 -- byte-identical to the B2-90 post seal quoted in B2_90_album_captions_20260926.md ("post sha256 a2c96fa49e02d60b959af887627dc95f004cbe56c173e29d507473dc80466743"), i.e. nothing touched the file between 18:14Z and this patch.
- Register: watch/inbox/mrpool_export/media_recovered_register_20260926.jsonl, 314 rows, all 314 cites present in the ledger, 29 unique shas (the t.me preview thumb dedupes across adjacent messages, e.g. rows msg_176/msg_177 share 66268013e17b0727...).
- Fail-closed gate (B2_385_promote.py): every recovered file hashed from disk and compared to the register BEFORE any ledger byte written; run output `{"patched": 314, "register_rows": 314, "register_cites_absent_from_ledger": [], "absent_count": 0}`.
- Post-v2: ledger sha256 0EA2114E4FE6FDFA754C32E77CFA69D5BA4BE42D462B54D97AA392CAA3EEA4FA, 1,546,724 bytes; INDEX.json item CAPTION_LEDGER_20260926.jsonl now carries that sha with purpose "B2-385 recovered-sha promotion v2: ..."; re-seal event seq 1790452640893267971 (writer zcode-sw-07 lineage, appended from the inbox root per the B2-40 path lesson).
- Falsifier run: "promoted rows lacking disk-backed sha256: 0"; spot verify @MrPool_Q#176 file sha == recorded sha == True. Fold verify after re-seal lists no CAPTION_LEDGER mismatch (the QUEUE.md mismatch on the same printout is the pre-existing concurrent-append set prior receipts already name; many lanes append between seals).

## Work done

- Claim line appended for CAPTION_LEDGER_20260926.jsonl (20:01:20Z) before the edit, per the shared-file claim law; pre-v2 sha recorded in the same breath.
- B2_385_promote.py: cite-keyed in-place patch filling path (media_recovered_20260926/msg_N.jpg, relative to mrpool_export/ like the existing media_full/ convention), bytes (recovered thumb bytes; the export-metadata size stays in the register's ledger_file_size field, so no metadata is destroyed), sha256 (register, lowercase hex per ledger convention), status have-recovered, recovered_provenance.
- INDEX re-sealed through scripts/index_fold_host.mjs add from the inbox root; shared_surface validate run afterward names no new errors for this file (only the known unindexed-files warning set).
- Receipt filed; LEDGER row appended; QUEUE.md row flipped with pointer.

## Falsifier

The brief's falsifier is discharged by the runs quoted above (INDEX verify clean on the new seal; 314/314 disk-backed; pre-v2 byte state quoted). Reopen if: any of the 314 rows' files drift from their recorded sha (the register plus this receipt pin the expected bytes); the INDEX item sha stops equaling the on-disk file sha without a later register event naming a writer; or a consumer misreads have-recovered as have -- the semantics paragraph above is the arbiter, and the 29-unique-sha duplication is the tell (original media would not collapse to 29 hashes across 314 messages).

## Bibliography closed

Read: watch/inbox/CAPTION_LEDGER_20260926.jsonl (shape census, pre/post hashes), watch/inbox/mrpool_export/media_recovered_register_20260926.jsonl (head + full-scan census), watch/inbox/LIVING_HASH_LAW_20260926.md (implementation contract + migration), watch/inbox/burn_wave_20260926/B2_90_album_captions_20260926.md (re-seal precedent + outside-drop lesson), scripts/index_fold_host.mjs (usage block), INDEX.json CAPTION_LEDGER item pre/post, live fold add/verify and validate outputs. No external sources.
