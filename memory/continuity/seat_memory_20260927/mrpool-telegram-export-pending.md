---
name: mrpool-telegram-export-pending
description: Mr Pool corpus COMPLETE 2026-09-18/19 — 3,663 msgs + 2,375/2,377 media (3.64GB) + 340/340 transcripts + vision triage 440 images (symbol core stable at 5x scale: eye x142 water x132; views-weighted eye 3.98M) + full-image stego CLEAN (1,882 scanned, flat-art outliers only) + called-shot ledgers v1+v2 (16 video shots + 107 caption shots, Med Bed campaign ALL BROKEN); sound reading v2 (medbed x44 dominant, card+medbed x22 monetization cluster)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

Mr Pool Telegram channel harvest (2026-09-18) — **COMPLETE.**

**CORRECTION (kept for the record):** media was NEVER protocol-blocked. The earlier
memory claimed a no-forward flag and 2,726 server refusals; all were
`TypeError: download_media() got an unexpected keyword argument 'sleep'` — my own
malformed call. Lesson: read the actual error text before naming a cause.

**Final tally (receipt HARVEST_COMPLETE.json, committed a1c1e210a):** 2,375/2,377
media recovered, 3.64 GB — 2,011 jpg, 390 mp4, 5 pdf, 1 mov. Only 2 download errors.
Every file's mtime set to its true post date; register rows carry msg_id, post date,
views, sha256, bytes, and the FULL reaction ledger per post. Ledger v2.1
(ledger_full.jsonl, 3,663 rows May-2023 → Sep-2026): full text, emojis, edit dates,
forwards, reactions; ZERO comment threads exist on the channel; 87 links.

**KEY FINDING — the channel's own counter lies:** UI advertises 613 photos / 163
videos; the full-history walk found 2,011 photos and 390 videos (3.4x / 2.4x).

**Auth:** QR login session kept at watch/inbox/mrpool_export/harvest.session
(Marque/@Nacho_Business_co); channel "Mr. Pool" id -1001974403582.

**Dead ends (do not re-walk):** Telegram cache size-matching recovered 32/2,689;
Telethon qr_login().recreate() returns None — loop fresh calls.

**SOUND LAYER (transcriptions.jsonl, 340/340, 0 errors; committed c7389a11f):**
339 en + 1 nn; 248 speechy / 92 wordless; 8.27h speech. Sound reading v2
(SOUND_READING_FULL.json, idle bench drain, commit 7e795dab1): **medbed x44 is the
DOMINANT spoken symbol** (ahead of final x30), card+medbed strongest co-occurrence
(x22) — the monetization campaign IS the speech layer's center of gravity. FoJAk3
crossref: water-liquidity confirmed in speech 2024-07 → 2026-09-11; plan_ab and
bridge ZERO in speech (X-register only). Channel mixes prophecy narration + street
clips + news readings.

**CALLED-SHOT LEDGERS v1+v2 (committed fc793c913):** v1 = 16 genuine forward-dated
video shots, ALL ONE CLAIM (Med Bed hospitals Jan 2026 + card sales, blitz
2025-09-24→10-20) — ALL BROKEN, matches documented Med Bed card fraud format.
v2 from captions (called_shot_ledger_captions.jsonl): 107 shots, 18 targets, 94
expired, 13 pending (Oct 2026 → Mar 2028). Pattern proved: file a dated finale,
expire silently, file the next. Operator counter-reading ("bad actors seeded as
cover, traps deliberately set") → [[gstd-forensics-20260918]].

**VISION TRIAGE 840/2011 images, 0 errors (41.7% coverage; batches 1-5 folded,
commits a32bac533, e5db660b1, 1780de222):** stable symbol core through every
batch — eye x278, water x267, numbers x234, pyramid x197, bridge x193. The
proportions hold as the sample grows 5x = statistical signature of a DESIGNED
vocabulary, not sampling noise. Views-weighted leaders: eye 3.98M, water 3.90M,
pyramid 2.81M, bridge 2.65M — the symbol exchange rate is proportional to
audience attention. Type: art 71 dominates. msg_1033 screenshot of original X
handle **@looP_rM311_7211** (mirror-spelled) = lineage evidence. Most-viewed:
black swan over Earth, crashing chart (markets-died motif). Batches 6-10 remain
to full coverage.

**FULL-IMAGE STEGO SCAN CLEAN (stego_scan_full.jsonl):** 1,882 scanned / 29 errors;
median 7.46; 38 outliers all flat-fill poster art (30 flat-dark, 8 flat-bright), NO
payload corpus-wide. The open front remains the 390 video audio tracks
(spectrogram pass owed, not just ASR — see LINKS-299 spectrum analyzer note).

**GAP CLOSED 9/27 (operator asked "what two pool files are we missing"):** NONE missing anymore, proven by set-difference, not receipt-trust: ledger_full.jsonl holds 2,689 true-media message ids (file_ext/file_size present; the 37 MessageMediaWebPage rows are link previews, not media), and media_register + media_recovered_register together hold 2,689/2,689. The original errs:2 (HARVEST_COMPLETE.json carries only the COUNT, ids never written anywhere on disk) are subsumed — whatever they were, their ids now have bytes. B2-88 (9/26) recovered 314/314 caption-only rows via the public t.me/s/MrPool_Q preview; honest limit: 287/314 are re-encoded thumbnails (the 262-row 33881-byte group = ONE image held at 4,727 bytes; B2-386 probed every public surface, no full-size reachable logged out). Operator's own TG app beats every public door: t.me/MrPool_Q/<id> (e.g. 176, 550, 1136, 1196, 2153); saved originals land under watch/inbox/mrpool_export/ with the B2-386 supersede rule = NEW dated register row, never in-place edit. CAUTION reading the registers: they are LIVING files carrying metadata rows too (B2-89 hash-backfill addendum rows with computed_at; a B2-482 dedup_decision.v1 record that looks like a null "missing" row but is not media; ~2,376 rows still sha256:null pending backfill — null sha is NOT a failure marker). Telethon session revoked server-side since (AuthKeyUnregistered, B2-467); the t.me/s preview door is the no-auth path and the estate is now 3,693 rows via the 9/26 delta (ids 4634..4663 contiguous).

Related: [[time-travel-called-shot-steal-20260918]], [[riddle-triad-cadence-20260918]],
[[corpus-harvest-skill-cliff-scalar-20260918]], [[gstd-forensics-20260918]],
[[interpreter-layer-20260919]], [[riddler-corpus-harvest-20260919]]
