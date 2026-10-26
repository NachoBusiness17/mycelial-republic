# B2-367 receipt: cross-reference the two qdrop media registers (2026-09-26, lane SW-03)

## Verdict

LANDED. Both registers now open with a _scope_header row naming what the register holds, what it does NOT hold, and the sibling register's scope: media_register_qagg.jsonl declares itself the RENDERED CARD register (qaggdrop_*.png keyed by q_num; a card 404 is a render gap, not a missing original) pointing at media_register.jsonl as the ORIGINAL-post-media register (1,891 urls, 1,890 dead per RECEIPT.json forensics, CDX recovery pending, keyed by drop_no + id); media_register.jsonl carries the mirror-image header. The falsifier is answered: a reader holding only media_register_qagg.jsonl can now tell a card gap from a missing original. Both files remain line-parseable JSONL (0 bad rows post-edit: 5,011 and 1,892 rows including headers).

## Evidence file:line quotes

- watch/inbox/qdrop_export/media_register_qagg.jsonl:1 (new header): "\"_scope_header\": true, \"register\": \"media_register_qagg.jsonl\", \"registers\": \"qagg.news RENDERED CARD images (qaggdrop_*.png in media_full/), one row per q_num ...\" \"sibling_register\": \"media_register.jsonl (ORIGINAL post media: 1,891 urls, 1,890 dead per RECEIPT.json media forensics, CDX recovery queue pending; keyed by drop_no + id)\"".
- watch/inbox/qdrop_export/media_register.jsonl:1 (new header, mirror image, with the per-domain forensics: media.8ch.net 1311 DNS-dead, Tor-only 488, 4plebs 403, 8kun.top 54, 8kun.net 11, archive.fo 1).
- watch/inbox/qdrop_export/RECEIPT.json media block (lines 22-35): "tasks": 1891, "ok_direct": 1, "dead": 1890, "recovery_queue": "web.archive.org CDX retry when IA returns online ..." (the numbers the header cites, read from the bytes).
- Pre-edit state: media_register_qagg.jsonl row 1 was "{\"q_num\": 1, \"file\": \"watch/inbox/qdrop_export/media_full/qaggdrop_0001.png\" ... \"ok\": true}" (no scope anywhere in either file; the B2-92 brief recited the conflation per the QUEUE row).
- Post-edit validation (this lane): both files parse line-by-line, 0 bad rows; qagg register 5,012 lines, original register 1,893 lines.

## Work done

- Prepended one JSON _scope_header row to each register (idempotent by first-line check), each carrying: what the register holds, what it does not hold, the sibling register's name and scope, and the reader rule that separates a render gap from a missing original.
- Line-citation shift disclosed: prepending shifts every legacy row citation by +1 (notably the QUEUE B2-404 brief's "media_register.jsonl lines 118-119" qanon.pub numbering cite becomes 119-120; B2-404 runs later in this lane and resolves rows by content, not line). No code consumer reads these registers (grep over mag/ tools/ scripts/ found no readers; the receipts cite them as evidence text).

## Falsifier

Kill conditions: (a) a reader holding only one register still unable to distinguish a card gap from a missing original (impossible while the headers name both scopes; deleting a header reopens it), (b) the headers drifting from RECEIPT.json's forensics numbers (1,891/1,890 and the per-domain counts are quoted from the bytes; a RECEIPT.json update must update the header), (c) a consumer breaking on the header row (any JSONL reader must skip unknown-shaped rows; none exists today, and the parse check above proves line-validity). The conflation class is falsified-evidence: B2-92's brief itself recited it; the headers stand as the correction surface.

## Bibliography closed

- watch/inbox/qdrop_export/media_register_qagg.jsonl (header prepended; full-file parse validated)
- watch/inbox/qdrop_export/media_register.jsonl (header prepended; full-file parse validated)
- watch/inbox/qdrop_export/RECEIPT.json (media forensics block, lines 22-35)
- watch/inbox/burn_wave_20260926/B2_92_qagg_sweep_20260926.md (the recited conflation, named by the brief)
- QUEUE.md B2-367 row (brief and falsifier)
