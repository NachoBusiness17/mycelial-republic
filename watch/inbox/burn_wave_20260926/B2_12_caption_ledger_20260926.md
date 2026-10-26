# B2-12 caption ledger (mrpool_export), 2026-09-26

## Verdict

LANDED. `watch/inbox/CAPTION_LEDGER_20260926.jsonl` holds one row per media id: 2,726 rows, zero model calls, zero media reads, metadata only. Status split: **have 2,375** (file byte-verified on disk), **metadata-only 351**, **missing 0**. Every row cites handle + anchor per the dual-numbering rule (`@MrPool_Q#N`, never bare msg_id). The metadata-only class is explained, not vague: 314 rows are typed MessageMediaWebPage in the source yet carry .jpg ext, byte size, and a full caption (photos the export never downloaded to disk); plus 35 pure link previews and 2 polls. Every disk file has a ledger row (no orphans), all 2,375 sizes match ledger file_size exactly, and all 32 register-supplied sha256 hashes recompute clean.

## Evidence

- `watch/inbox/mrpool_export/ledger_full.jsonl:1` (msg 4633): `"media_type": "MessageMediaDocument", "file_size": 6588836, "file_ext": ".mp4"`; disk `media_full/msg_4633.mp4` stats 6,588,836 bytes, exact match.
- `watch/inbox/mrpool_export/ledger_full.jsonl:3662` (msg 176): `"media_type": "MessageMediaWebPage"` with `"file_ext": ".jpg", "file_size": 33881` and caption text present, but no file anywhere under mrpool_export. This is the metadata-only photo class (314 rows).
- `watch/inbox/mrpool_export/media_register.jsonl:1` (msg 2002): `"file": "media_matched/msg_2002.jpg", "sha256": "6d769f12723f1144..."`; recomputed from disk bytes, match. Register rows for media_full copies carry bytes but no sha256 (line 33), so the ledger's sha256 column is populated only where existing metadata supplied it (32 rows).
- `memory/burns/LEDGER.jsonl:44`: mapping rule "cite handle + anchor, never bare msg_id"; harvest = `@MrPool_Q`, watched surface `@Official_MrPool` is an independent anchor sequence.
- Independent re-derivation of all 2,726 rows against source bytes: 0 field errors; output file is pure ASCII, 1,345,177 bytes.

## Work done

Read ledger_full.jsonl in full (3,663 rows, anchors 1..4633, dates 2023-08-28 to 2026-09-18), media_register.jsonl (2,407 rows), transcriptions.jsonl (340), cache_index.jsonl sample; listed all three media dirs. Built `watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py` (sha256 42e6dd6e020827ea...) and ran it with this repo's venv python. Row fields: cite, msg_id, date, datetime, kind, media_type, file_ext, bytes, path, path_alt, sha256, caption (240-char preview), caption_len, caption_via, status. Captions come only from the ledger text field; 102 empty album siblings resolved to the same-date grouped caption carrier via `caption_via` (search order -1,+1,+/-2,+/-3); 11 remain empty (9 unresolved grouped: 4618, 4600, 4599, 3610, 2981, 1785, 1784, 1783, 1393; 2 non-grouped). Sorted by date then msg_id. Receipt + build script land in burn_wave dir per contract.

## Falsifier

Any one of these kills the verdict: (a) a disk file under media_full/ or media_matched/ with no row in the output; (b) a have-row whose path fails os.stat or whose size differs from ledger file_size; (c) a caption not equal to `ledger_full.jsonl` text.strip()[:240] for its msg_id; (d) a row citing anything but `@MrPool_Q#<its own msg_id>`; (e) register sha256 mismatch on any of the 32 hashed copies.

## Bibliography closed

ledger_full.jsonl:1,895,2194,3662; media_register.jsonl:1,33; transcriptions.jsonl:1; LEDGER.jsonl:44; QUEUE.md (## Open); CAPTION_LEDGER_20260926.jsonl (sha256 b95afbe0d889e9b8b867ebbc989f1b6693e585b2ff93272f5749a852b5821bf1); B2_12_caption_ledger_build.py. No external sources. Queue self-feed: B2-88..B2-90.

## ADDENDUM 2026-09-26 (B2-422, SW-00): declared-unresolvable class registered

Rule (option b of QUEUE row B2-422): a row with `caption_len 0` AND empty
`caption_via` is the DECLARED-UNRESOLVABLE class, exhaustive-by-rule after
this builder's +/-3 window, B2-90's album v2 (distance 4 to 6), and the
B2-421 via-pin gate all landed: a consumer reading the ledger can treat
empty+empty as "channel message with no caption", never caption-pending.
Members in the sealed bytes (sha256 0EA2114E4FE6FDFA754C32E77CFA69D5BA4BE42D462B54D97AA392CAA3EEA4FA,
1,546,724 bytes, 2,726 rows): msg 2223 (line 1684) and msg 3495 (line 2493),
both kind "poll" (MessageMediaPoll), status metadata-only, non-grouped, no
media file, so caption-less by Telegram construction, not by omission.
Erratum against this receipt's earlier prose and B2-90's: the pair this
brief named (msg 1684, msg 2493) is CAPTION-BEARING in the sealed bytes
(44 and 792 chars respectively, non-grouped MessageMediaDocument videos),
so the "2 non-grouped metadata-only rows" identity of the empty+empty class
moved to 2223/3495 under the same seal; the class RULE above, not the
member list, is the durable registration. Verify one-liner: iterate
CAPTION_LEDGER_20260926.jsonl, assert every row with empty caption and
empty caption_via has status metadata-only and kind poll.
