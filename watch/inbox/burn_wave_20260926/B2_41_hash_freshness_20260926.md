# B2-41 hash-freshness sweep (2026-09-26)

## Verdict

LANDED, with the brief overtaken by concurrent lanes mid-wave. Of the 27 stale rows the brief named, 23 were hash-refreshed by drift-patrol-cron at 12:03:24Z before this lane fired, and the QUEUE.md absolute row was invalidated plus re-registered bare by B2-145 (events 3070, 3075). The 4 rows left stale were handed to B2-41 by name in B2-145's ledger row; this lane re-registered all 4 with fresh hashes and landed the seal-hook path fix so hook registrations stop minting absolute-path phantoms. Verify moved 5 mismatched to 1 mismatched; the last (QUEUE.md) is owned by the in-flight B2-156 living-hash migration, not re-registered here to avoid a last-wins collision with that active lane. B2-156's spec named this receipt as owed on disk; it now exists.

## Evidence

- index_events.jsonl:2784 `{"ts": "2026-09-26T11:23:53+00:00", "op": "register", "file": "C:/Users/foste/.../burn_wave_20260926/QUEUE.md", ... "writer": "md-record-seal", "nonce": 3}` — the seal hook minted an absolute-path register; the fold keeps C:/ paths (scripts/index_fold_host.mjs:82 OUTSIDE_RE matches only repo-relative segments), so it became a phantom INDEX item.
- index_events.jsonl:3053 `"file": "/board/inbox/C:/Users/.../QUEUE.md"` — drift-patrol-cron refreshed the phantom in place with a double prefix instead of invalidating it; index_events.jsonl:3070 is B2-145's invalidate, :3075 the bare re-register.
- mag/shared_surface.py:212 `errors.append(f"hash mismatch: {item.get('path')}")` — stale rows are live validate errors, not cosmetic.
- scripts/index_fold_host.mjs:179 `active = active.filter((it) => it.path !== ev.file);  // last register wins (hash refreshes)` — the mechanism my re-registers and the B2-26 seq trap both ride on.
- tools/md_record_seal.py:77 `return path.relative_to(ESTATE / "watch" / "inbox").as_posix()` and :141 `"file": rel` — the fix: registers carry the inbox-relative path and fire only under watch/inbox (:131, :146-148).

## Work done

1. Byte-verified the mismatch census twice (node verify plus independent python hashlib on all 4 files; hashes agreed exactly).
2. Re-registered REJECTION_TAXONOMY_20260917.md (B2-33 recount addendum 12:36:48Z), BURN_JUDGE_LANE_BUILD_20260925.md (judge-lane amendments 12:38:57Z), phone_relay_log.jsonl, LINKS.jsonl under writer b2-41-hash-freshness, seqs ...398-...401. All 4 won last-wins ordering: the cron's seq family quantizes to one double (1789823567015749449 and ...477 both parse to 1789823567015749376), so ts tiebreak hands the win to later registers.
3. Landed the seal-hook fix in tools/md_record_seal.py (docstring spec updated first; cause and evidence in the inbox_rel comment): inbox-relative register path, register skipped for non-inbox durable roots the fold drops as outside anyway. Seq half stays with open brief B2-148.
4. Tests: 4 new in tests/test_md_record_seal.py (relative path, outside skip, nonce advance, dedupe), all pass; 5 fold tests pass; ratchet NEW=0 PASS.
5. Verified: verify 973 hash-clean / 1 mismatched (QUEUE.md, B2-156-owned); validate errors down to that single row; this closes the B2-156-named owed receipt.

## Falsifier

1. If B2-156's migration lands `add --living` for QUEUE.md and LINKS.jsonl, my plain LINKS seal at seq ...401 is superseded by design (law point 5) and this receipt's "4 of 4 won" reading is historical only.
2. If any hook Write under watch/inbox after this landing appends a register whose file field starts with C:/, the fix is falsified.
3. If verify still counts the 4 files mismatched after the next drift patrol, the re-registers lost ordering to a quantized-seq row and the receipt overclaimed.

## Bibliography (closed)

- watch/inbox/QUEUE.md (full read, 2026-09-26 wave state)
- watch/inbox/LIVING_HASH_LAW_20260926.md (full read; owning spec for living rows)
- watch/inbox/DRIFT_PATROL_20260926.md (read)
- scripts/index_fold_host.mjs (full read, 409 lines)
- tools/md_record_seal.py (full read, pre- and post-edit)
- mag/shared_surface.py (full read, 259 lines)
- tests/test_index_fold_host.py (full read)
- watch/inbox/index_events.jsonl lines 726, 2391-2415, 2581-3075 (registration history of every named file)
- watch/inbox/REJECTION_TAXONOMY_20260917.md and BURN_JUDGE_LANE_BUILD_20260925.md tails (drift causes read in full)
