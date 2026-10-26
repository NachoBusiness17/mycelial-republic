# B2-213 FULL_SCAN_REPORT stale sha refresh (SW-07, 2026-09-26)

## Verdict

LANDED. The drift cause is named and the registration shape is fixed at the root: watch/inbox/FULL_SCAN_REPORT_20260923.md is a whole-file rewritten derived report (tools/full_scan.py:229 write_text each Estate FullScan run), so the scheduled 13:39:32Z scan moved the bytes past the 11:10/11:35 F08A registrations and a static seal would have broken again on every future run. B2-280's 16:13:34Z seq-band re-pin had already restored hash-clean on current bytes; this lane re-registered the item living-open (event seq 1790453977822675457) so future scan rewrites verify instead of flagging. shared_surface validate now reports the item exists true, sha 168D3E1B... (current bytes), living true, purpose B2-213.

## Evidence file:line quotes

- QUEUE.md row: "verify 09-26 flags watch/inbox/FULL_SCAN_REPORT_20260923.md (actual 168D3E1B423C68BB... vs expected F08A229D0DA7C1AD..., the only mismatch of 976 items after the B2-157 refold); re-register at current bytes or re-seal with living per B2-156, and name why it drifted (which writer appended past the F08A registration)".
- The drift writer, named: tools/full_scan.py:33 `REPORT = ROOT / "watch" / "inbox" / "FULL_SCAN_REPORT_20260923.md"` and :229 `(ROOT / ...).write_text("\n".join(md), encoding="utf-8")` -- a whole-file rewrite per run; the file's own bytes carry the run stamp "run 2026-09-26T13:39:32.209454+00:00 - records: 278 - ok: 240 - fail: 38". The scheduled surface exists: schtasks lists task `\Estate FullScan`.
- Event history (index_events.jsonl lines 2646, 2881, 3247): 11:10:08.442Z exp002a register F08A229D...; 11:35:18.724Z b2-02-writer-debt-20260926 register F08A229D... (same bytes); 16:13:34.208Z zcode-b2-280-seq-band register 168D3E1B... (current bytes, the B2-280 re-pin that already healed verify).
- Current state: actual file sha256 168D3E1B423C68BBC2E84058F31F3BF617CE81B078349CA55FAD296F5AE8E02E (233 bytes) equals the INDEX item sha; INDEX item now `"living": true` with the B2-213 purpose; mag.shared_surface validate row: "path FULL_SCAN_REPORT_20260923.md, exists true, sha256_match true".

## Work done

- Traced the drift to the scheduled full_scan writer via the file's own run stamp and the tool source; distinguished the 13:39 rewrite from the 11:35 re-registration.
- Re-registered the item living-open through scripts/index_fold_host.mjs (add --living-open from the inbox root), purpose naming the rewrite law and the B2-280 re-pin it supersedes for future runs.
- Verify after: fold add refolded to 1059 active items; validate shows sha256_match true, living true.

## Falsifier

Reopen if: the next Estate FullScan run produces a FULL_SCAN_REPORT mismatch in fold verify or shared_surface validate (would mean the living-open registration did not take, e.g. a later static re-pin won last-register-wins); or the item's `living` flag reverts to false in INDEX.json while the schtask still runs. Note for the next auditor: the schtask itself is sanctioned (B2-73/B2-96 lane family); the fix is the registration shape, not the scanner.

## Bibliography closed

Read: watch/inbox/FULL_SCAN_REPORT_20260923.md (full, 233 bytes), tools/full_scan.py (lines 33, 229 + ts stamping), watch/inbox/index_events.jsonl (3 FULL_SCAN events traced), watch/inbox/INDEX.json (item pre/post), mag.shared_surface validate output, schtasks query (Estate FullScan presence). No external sources.
