# B2-228 B2-17 margin-wording erratum, 2026-09-26

## Verdict

LANDED. The brief's reading is CONFIRMED against bytes, and the erratum is now on the receipt it corrects: a dated one-line ERRATUM appended to watch/inbox/burn_wave_20260926/B2_17_adventure2d6_20260926.md (append-only, no-erase) stating that its caveat line "the quoted margin is stale by 0.006" names the NEW margin, not the shrink; the delta is 0.007 (old margin 0.013 = 0.031 vs 0.044 -> new margin 0.006 = 0.032 vs 0.038). The referee verdict already carried this correction in its B2-70 addendum (REFEREE_VERDICT_20260926.md:65-67: "a shrink of 0.007; the B2-17 receipt's 'stale by 0.006' names the new margin, not the delta") and cites B2-17 lines 32-35 as the caveat source, but the B2-17 receipt itself had no marker, so a B2-17-only reader would keep quoting the wrong delta. Confirmed-correct-as-meant was rejected: the sentence as written is numerically wrong, and the referee verdict already rules out the charitable reading. Verdict/order claims in B2-17 are unaffected (both scans still shorten water-first), as both receipts already state.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_17_adventure2d6_20260926.md:32-35 (pre-edit, unchanged bytes): "Caveat: the 09-22 rescan changed the descent_vote meter (chain 0.031 -> 0.032, star 0.044 -> 0.038) but not any cosine. ... Order unaffected; the quoted margin is stale by 0.006."
- watch/inbox/REFEREE_VERDICT_20260926.md:51-54: "(`watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260921.json:86-87`: chain 0.031 vs star 0.044, margin 0.013). The 09-22 rescan superseded that meter: ... water_first_chain_len 0.032, hub_first_star_len 0.038, margin 0.006."
- watch/inbox/REFEREE_VERDICT_20260926.md:65-67: "Net effect of the refresh: the quoted chain-vs-star margin narrows from 0.013 to 0.006 (a shrink of 0.007; the B2-17 receipt's 'stale by 0.006' names the new margin, not the delta)."
- watch/inbox/REFEREE_VERDICT_20260926.md:77: "Caveat source: watch/inbox/burn_wave_20260926/B2_17_adventure2d6_20260926.md lines 32-35."
- B2_17 post-edit tail: "ERRATUM 2026-09-26 (B2-228, append-only per the no-erase law): this receipt's caveat line ... names the NEW margin (0.006 = chain 0.032 vs star 0.038), not the shrink; the stale-by delta is 0.007 (old margin 0.013 = 0.031 vs 0.044, per watch/inbox/REFEREE_VERDICT_20260926.md:51-54, 65-67 ...). Order and verdict claims in this receipt are unaffected."
- Arithmetic checked this lane: 0.031-0.044 = -0.013 (old margin 0.013); 0.032-0.038 = -0.006 (new margin 0.006); 0.013-0.006 = 0.007 (the shrink).

## Work done

- Read the B2-17 caveat lines, the referee verdict's meter section and B2-70 addendum, and re-derived all three numbers from the quoted chain/star lengths; the brief's reading (old 0.013, new 0.006, delta 0.007, sentence names the new margin) verified exactly.
- Appended the dated one-line ERRATUM to the B2-17 receipt (append-only; original bytes untouched), naming the new-margin/delta confusion, the referee addendum's priority on the correction, and the unaffected-order statement.
- Checked B2-17 for pre-existing addenda (none; this is the first) and em-dash count (0 in the append).
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- The erratum is wrong if any quoted byte changes: CATHEDRAL_CURVATURE_SCAN_20260921.json:86-87 must still read chain 0.031 vs star 0.044 and the 09-22 rescan 0.032 vs 0.038; a different rescan superseding both would need a NEW erratum, never an edit of this one.
- If a reader can show the referee's B2-70 addendum is itself later-corrected, this erratum inherits that correction and must be extended.
- The append-only law: if B2_17_adventure2d6_20260926.md's original lines 32-35 are ever rewritten rather than appended-to, the no-erase law is broken independent of this landing.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_17_adventure2d6_20260926.md (lines 32-35 pre-edit; post-edit tail); watch/inbox/REFEREE_VERDICT_20260926.md (:51-54, :65-67, :77, ADDENDUM at :48, B2-227 addendum at :80); watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260921.json:86-87 (as quoted by the referee verdict; scan file cited through it). No web sources. Em-dash count 0.
