# B2-423 carrier-position honesty

## Verdict

LANDED. The distribution claim is byte-true and is now documented where the next attribution rule will read it: a dated POSITION LAW block in the B2-12 builder header (B2_12_caption_ledger_build.py docstring, the caption_via field spec). Across the 6 albums the B2-90 v2 resolved, the caption carrier sits on the FIRST member in 5 (4595 in 4595..4600, 3606 in 3606..3610, 2977 in 2977..2981, 1779 in 1779..1785, 1389 in 1389..1393) and on the LAST member in 1 (4622 in 4618..4622): real sender variance, not a fold artifact. The falsifier fired exactly as pre-registered: a first-member-only rule re-empties msg 4618 while the other 8 v2 targets still resolve (watch/inbox/burn_wave_20260926/B2_423_position_falsifier.json).

## Evidence file:line quotes

- B2_12_caption_ledger_build.py, caption_via spec block, now carrying: "B2-423 POSITION LAW (2026-09-26, byte-verified): the album caption carrier sits on the FIRST member in 5 of the 6 B2-90 v2 albums (...) and on the LAST member in 1 (4622 in 4618..4622): real sender variance, not a fold artifact. NO attribution rule may assume first-member; search the whole album run for the unique non-empty-text member."
- Byte verification (this lane, from watch/inbox/mrpool_export/ledger_full.jsonl, the v2 album rule: maximal grouped=True run contiguous in msg_id with consecutive stamps <= 60s apart): album 4618..4622 carriers=[4622] position=last distance=4; album 4595..4600 carriers=[4595] first; 3606..3610 carriers=[3606] first; 2977..2981 carriers=[2977] first; 1779..1785 carriers=[1779] first (targets 1783/1784/1785 at distances -4/-5/-6); 1389..1393 carriers=[1389] first.
- B2_423_position_falsifier.json summary: {"albums": 6, "carrier_first_member": 5, "carrier_last_member": 1, "first_member_only_empties": [4618]}.

## Work done

1. Recomputed the 6 album runs from ledger_full.jsonl independently of the B2-90 script (same rule, fresh code) and located each carrier's position; confirmed the brief's 5-first/1-last distribution on bytes before writing any note.
2. Ran the falsifier both arms: v2 any-position rule resolves all 9; a first-member-only rule resolves 8 and leaves 4618 empty (its album's unique carrier 4622 is the last member, distance 4). Results persisted to B2_423_position_falsifier.json.
3. Appended the POSITION LAW block to the B2-12 builder header docstring (anchored edit inside the caption_via spec, the field any future rule must read). No code behavior changed; the builder script itself is untouched below the docstring.
4. Filed this receipt, the LEDGER row, and the QUEUE row annotation.

## Falsifier

Pre-registered and executed live: "a first-member-only rule leaves msg 4618 empty again while every other check stays green" - CONFIRMED (8 of 9 targets resolve under the restricted rule, 4618 alone goes empty). This is the decidability proof that position variance is load-bearing: any future rule that hardcodes first-member reintroduces the B2-90 unresolved set member 4618, and the persisted falsifier JSON names it. Reproduction: rerun the album-run computation in B2_423_position_falsifier.json's rule description against ledger_full.jsonl; any different carrier map inverts this receipt.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_90_album_captions_v2.py (the v2 rule, read in full)
- watch/inbox/burn_wave_20260926/B2_12_caption_ledger_build.py (builder header, POSITION LAW appended)
- watch/inbox/mrpool_export/ledger_full.jsonl (3,663 rows, album runs recomputed)
- watch/inbox/burn_wave_20260926/B2_423_position_falsifier.json (falsifier evidence, this lane)
- QUEUE.md row B2-90 (the v2 landing this documents)
- Nothing owed.
