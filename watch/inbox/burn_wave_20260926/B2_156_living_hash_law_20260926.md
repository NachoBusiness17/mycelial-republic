# B2-156 living-file hash law (2026-09-26)

## Verdict

LANDED. Spec first, then code, then migration, then live proof. The law has two writer-declared shapes: SEALED LIVING (`add --living`) seals (sha256, size) over a file's first N bytes so append-only ledgers grow without failing verify while prefix mutation or truncation still fails hard; OPEN LIVING (`add --living-open`) declares an edit-shaped board with no byte seal, counted only. Migrated LINKS.jsonl and phone_relay_log.jsonl (sealed) and QUEUE.md (open). The exact old failure mode, a self-feed append staling QUEUE.md within minutes, now verifies clean.

## Evidence with file:line quotes

- Cry wolf, pre-fix: scripts/index_fold_host.mjs:271-305 hashed whole files and printed HASH MISMATCH for any growth. index_events.jsonl shows LINKS.jsonl took 4 hash-refresh registers in about 2 hours (lines 2904, 3058, 3059, 3088; 11:35Z to 13:21Z). QUEUE.md registered 13:15:42Z (line 3075) was refreshed 13:19:02Z (line 3083) and stale again at lane start: "verify: 973 hash-clean, 1 mismatched ... HASH MISMATCH: burn_wave_20260926/QUEUE.md".
- Owed, filed not synthesized: the LINKS.jsonl INDEX purpose names receipt B2_41_hash_freshness_20260926.md; no such file exists anywhere under watch/inbox (find returned nothing). Carried as queue row B2-198.
- Landed: scripts/index_fold_host.mjs:367-434 verify (prefix rule :414, open line :407, summary :426), :470-502 add with exclusive flags; mag/shared_surface.py:222-262 living branch (:233 open shape, :249 "living prefix mismatch" error), result counters living_files {ok, open, unverified}.
- The first design false-failed real bytes 30 minutes after landing: the self-feed inserts rows mid-file under the ## Open anchor, so the sealed 75601-byte prefix no longer matched the 76772-byte file ("LIVING PREFIX MISMATCH ... sealed prefix (75601 bytes) changed"). That is why QUEUE.md is insertion-grown and takes the open shape; the spec was amended before the reclassification code (build discipline).

## Work done

1. Read whole: index_fold_host.mjs, shared_surface.py, md_record_seal.py, both test files, B2-145 and B2-26 receipts, INDEX living rows.
2. Spec watch/inbox/LIVING_HASH_LAW_20260926.md registered (class LAW), amended with the open shape, re-sealed at amended bytes.
3. Code plus tests: 8 mjs and 6 python tests new, all pass. Final file state: 31 passed, 1 failed; the failure is B2-157's in-flight composed-invalidate fixture (nonce gap in their seeded events), not a B2-156 path.
4. Migration via the official add path only, writer zcode-b2-156-living-hash-law, seqs 1789823567015749403-408.
5. Live: fold verify "973 hash-clean, 2 living-ok, 1 living-open, 0 mismatched, 0 missing"; shared_surface validate ok:True, living_files {ok: 2, open: 1, unverified: 0}, zero mismatch errors.
6. Self-fed B2-197 (living-law rollout census), B2-198 (owed B2-41 receipt), B2-199 (drift patrol adopts living shapes, stops whole-file refreshes).
7. Ratchet --changed: the NEW hit tools/drift_dashboard.py:37 (except-pass) is an untracked file this lane never wrote; named here, debt not accepted by this lane.

## Falsifier

Dies if: (a) appending to LINKS.jsonl or phone_relay_log.jsonl ever yields a verify failure; (b) mutating or truncating a sealed living prefix does NOT hard-fail; (c) mid-file edits to QUEUE.md fail verify while it holds seal:open; (d) any living item sits in living-unverified in steady state; (e) the 14 B2-156 tests fail on a clean checkout.

## Bibliography closed

scripts/index_fold_host.mjs (whole, post-edit :52, :76-96, :367-434, :470-502); mag/shared_surface.py (whole); tools/md_record_seal.py (whole); tests/test_index_fold_host.py and tests/test_shared_surface_events.py (whole, including B2-157 sections); watch/inbox/LIVING_HASH_LAW_20260926.md (whole); B2_145_phantom_paths_20260926.md and B2_26_links_sha_backfill_20260926.md (whole); INDEX.json QUEUE/LINKS/EVENTS rows; index_events.jsonl lines 2904, 3053, 3058-3059, 3075-3088, new seqs 403-408.
