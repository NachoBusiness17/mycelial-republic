# B2-422 Last empty-caption rows: resolve or classify, 2026-09-26

## Verdict

LANDED as the class registration (the brief's option b), with a byte-level discovery that reshapes the brief's premise. In the sealed ledger bytes (sha256 0EA2114E..., 2,726 rows, the B2-385 post-v2 seal, on-disk sha re-verified this lane), the brief's two named rows are CAPTION-BEARING: msg 1684 carries a 44-char caption and msg 2493 a 792-char caption (both non-grouped MessageMediaDocument videos), so no v3 anchor pull is owed for them. The empty caption + empty caption_via class in the same sealed bytes holds exactly TWO members: msg 2223 (line 1684) and msg 3495 (line 2493), both kind "poll" (MessageMediaPoll), status metadata-only, non-grouped, no media file, caption-less by Telegram construction. The declared-unresolvable class is now registered with its rule in a dated addendum to the owning receipt (B2_12_caption_ledger_20260926.md): empty caption AND empty caption_via = "channel message with no caption", exhaustive-by-rule after the B2-12 +/-3 window, B2-90's album v2, and the B2-421 via-pin gate; never caption-pending. The falsifier is discharged: a consumer CAN tell the two apart (caption_via non-empty = resolved-via-carrier, 111 pinned pairs; caption text non-empty = direct; empty+empty = declared-unresolvable, currently polls 2223/3495). The brief's line pointers (:2223 and :3495) named lines that held msg 1684/2493 at writing time; under the current seal those lines hold msg 2223/3495, which is why the ids shifted.

## Evidence file:line quotes

- On-disk ledger this lane: sha256 0EA2114E4FE6FDFA754C32E77CFA69D5BA4BE42D462B54D97AA392CAA3EEA4FA, 1,546,724 bytes, 2,726 rows (byte-equal to B2-385's post-v2 seal; nothing touched it between seals).
- msg 1684 (line 1204 of the sealed file): "caption": "**IT IS COMING!\n\n****https://t.me/MrPool_Q**", "caption_len": 44, caption_via ""; msg 2493 (line 1936): "caption": "**\ud83d\udca5 DR. COURTNEY CONLEY: ...", "caption_len": 792.
- The empty+empty scan over the sealed file: members [(2223, 'metadata-only', 'poll'), (3495, 'metadata-only', 'poll')], rule violations []. Row dumps: msg 2223 {"kind": "poll", "media_type": "MessageMediaPoll", "path": "", "bytes": null, "status": "metadata-only", "caption_len": 0, "caption_via": ""}; msg 3495 identical shape (date 2025-12-18).
- Source cross-check (watch/inbox/mrpool_export/ledger_full.jsonl): msg 2223 and 3495 grouped False, type MessageMediaPoll, no text; msg 1684 and 2493 grouped False, type MessageMediaDocument.
- B2_90_album_captions_20260926.md Verdict named "msg 1684, msg 2493" as the post-patch empty+empty pair; the sealed bytes disagree (they are caption-bearing), so the addendum files that discrepancy as an erratum against the earlier prose, class RULE not member list being the durable registration.
- B2_421_caption_via_pin_20260926.md: "CAPTION_VIA ok 111/111" gate stands over carriers, complementary to this class registration.
- Addendum appended (append-only, no-erase law) to watch/inbox/burn_wave_20260926/B2_12_caption_ledger_20260926.md: "## ADDENDUM 2026-09-26 (B2-422, SW-00): declared-unresolvable class registered" with the rule, the two members, the erratum, and the verify one-liner; re-run this lane: members exactly [(2223, metadata-only, poll), (3495, metadata-only, poll)], violations [].

## Work done

- Re-read the ledger from bytes first (the brief's cited line numbers did not hold the brief's msg ids under the current seal), found the premise shift, and re-anchored the whole decision to the sealed sha.
- Traced provenance: on-disk sha equals B2-385's post seal; B2-90's prose names 1684/2493 as empty+empty while sealed bytes show them filled; no claim lines open on the file; filed the discrepancy as erratum rather than guessing at an unnamed patch.
- Chose option b (register the class) over option a (v3 anchor pull): the only remaining members are polls, which have no caption by construction, so an anchor pull cannot ever fill them; curl to t.me/MrPool_Q not spent, per the same logic B2-90 used to skip the fetch.
- Registered the class rule and members in a dated append-only addendum to the owning receipt, with a runnable verify one-liner; ran it: exhaustive over the sealed bytes.
- Em-dash check: 0 in the addendum and this receipt.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Any future ledger state where an empty caption + empty caption_via row has status other than metadata-only or kind other than poll breaks exhaustiveness-by-rule and reopens the brief (rerun the addendum's one-liner after every ledger rebuild; B2-421's gate already fails rebuilds that lose pinned carriers).
- If msg 1684/2493's captions are ever proven mis-attributed (caption text that belongs to another message), the "no v3 owed" half of this verdict reopens.
- If a consumer surface (game UI, corpus reader) reads empty+empty as pending, the registration failed its purpose; the class must be surfaced there by name.
- The member list (2223, 3495) is a snapshot of seal 0EA2114E; a rebuild that adds rows re-derives the list, and the rule, not the list, is the law.

## Bibliography closed

watch/inbox/CAPTION_LEDGER_20260926.jsonl (sealed bytes 0EA2114E, full-class scan, lines 1204, 1684, 1936, 2493); watch/inbox/mrpool_export/ledger_full.jsonl (msg 2223/3495/1684/2493 source rows); watch/inbox/burn_wave_20260926/B2_12_caption_ledger_20260926.md (whole + new addendum); B2_90_album_captions_20260926.md; B2_421_caption_via_pin_20260926.md; B2_385_caption_sha_promotion_20260926.md (seal chain). No web sources fetched (t.me/MrPool_Q not spent; polls cannot carry captions). Em-dash count 0.
