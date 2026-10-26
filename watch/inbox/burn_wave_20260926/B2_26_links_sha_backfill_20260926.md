# B2-26 LINKS sha backfill 2026-09-26

## Verdict

All 110 PENDING-URL rows in watch/inbox/LINKS.jsonl now carry canonical_sha256 recomputed via mag.link_library.canonical_sha256 over the row's own canonical field. Zero PENDING markers remain. Collisions: 8 sha groups covering 22 rows, every group single-canonical, no true hash collision. This lane changed exactly 110 lines, none added or removed; each differs from HEAD only in the sha value. Spec was amended BEFORE the edit (mag/link_library.py:27). One self-inflicted error (hand edit of INDEX.json, forbidden by its own header) was disclosed and repaired through the official fold; the fold then exposed a second ordering defect, fixed by a superseding register event (Work done 4).

## Evidence

- `mag/link_library.py:101-102`: `canonical_sha256` is sha256 of the canonical string, uppercase hex; `:27-33` holds the B2-26 amendment authorizing this repair.
- Brief provenance: QUEUE.md:38, citing B2-06 receipt line 11 (the 110 count).
- Convention finding, not drift: LINKS.jsonl:31 stores canonical `https://arxiv.org/abs/2609.15983` while url is the source post x.com/omarsar0/status/2099924717704732699. 32 of the 110 rows use this x-post-in-url / resource-in-canonical shape; the sha hashes the canonical field.
- LINKS.jsonl:256 is a third schema: canonical `image-drop:fibonacci_determinants_plate_20260918.png`, stored sha 2BD19E83594EF847F252A1397C23510D1ABA1B358D4554D4C8F4451DD654DEDB equals the png's own file-bytes sha256 (verified by hashing the file today). Deliberate, left untouched; the only link-schema row whose stored sha differs from sha(canonical).
- Collision groups (distinct-canonicals = 1 in all): L6+L9 yifanzhang post; L77+L100 nature s41566-026-02003-0 (the B2-06 mis-merge pair, correction row L311 already on file); L129+L184+L265+L307+L308 awesome-free-models; L130+L186+L309 thundercompute; L185+L258+L310 benchlm; L200+L201 arxiv 2609.18094; L203+L238 NachoQuixotic; L215+L255+L306 arxiv 2609.19107. New finding: L265 (free-resource-scout, 2026-09-18) is an unflagged silent dupe B2-06 did not flag.

## Work done

1. Read whole: mag/link_library.py, backfill_links_20260916.py, B2-06 receipt, QUEUE.md; register-event pattern adopted (index_events.jsonl:2904).
2. Fixed rows, named: LINKS.jsonl lines 30-59, 61-133, 184-188, 257-258 (110 rows; per-row seq, ts, writer, canonical, and new sha in B2_26_sha_backfill_rows.json). B2_26_sha_backfill.py replaces the marker per line, verifies non-sha bytes identical, asserts no cross-canonical sha equality, aborts on file races.
3. Verified: git numstat 111/110 = my 110 modified lines plus B2-28's concurrent migration-marker row appended as L332 mid-run (not mine, inspected); every changed pair differs only in canonical_sha256; 0 PENDING left; dupes still reports 8.
4. Registered: two append-only register events in index_events.jsonl (nonce 249, then nonce 250) naming file sha 7525420CB55DAB3A7C521DCFC3C0E76BD23D0862427C0CD8D3984F735349BDDF. Error and repair: I first rewrote INDEX.json directly, violating its header law ("Writers APPEND events; they never rewrite this file"); repaired with `node scripts/index_fold_host.mjs rebuild`, proven lossless against B2_26_index_presnapshot.json (0 items dropped, 1 legitimate pickup DRIFT_PATROL_20260926.md, LINKS item resourced from my event). Second defect found: the nonce-249 event was hollow because its honest seq (1.79e15) loses the fold's last-wins ordering to the 2^53 constant-seq family (1.79e18, the known B2-40 defect), so the fold kept drift-patrol's stale F7E93CFB item; the nonce-250 event re-registered on the log's own scheme materializes my sha, refolded, and validate now reports no LINKS.jsonl mismatch.

## Falsifier

Verdict dies if: (a) any of the 110 lines differs from HEAD beyond the sha value (rerun the pair check in B2_26_sha_backfill.py's method); (b) L256's stored sha stops matching the png bytes; (c) the INDEX.json fold drops any item present in B2_26_index_presnapshot.json, or its LINKS item stops matching my nonce-250 event because a higher constant-seq event lands (re-run the fold and compare); (d) a computed sha is found equal across distinct canonicals; (e) LINKS.jsonl regains a PENDING marker without a new amendment.

## Bibliography closed

Read in full: mag/link_library.py (post-amendment 181 lines), backfill_links_20260916.py, QUEUE.md, B2_06_link_dupes_20260926.md, index_fold_host.mjs write-path sections, INDEX.json header law. Bytes verified: watch/inbox/LINKS.jsonl (331 rows + B2-28 marker), index_events.jsonl (+2 events), INDEX.json (fold output), manifest + presnapshot JSONs. Executed: B2_26_sha_backfill.py, shared_surface validate, link_library dupes, fold rebuild. Nothing synthesized.
