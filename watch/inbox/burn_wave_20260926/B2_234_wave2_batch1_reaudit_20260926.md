# B2-234 receipt: re-audit MICKEY17_WAVE2_QUALITY batch 1.2 cohort (2026-09-26, lane SW-03)

## Verdict

DONE. The other 5 batch-1 artifacts (1.1 payoff matrix, 1.3 BG symbol census, 1.4 spectro log, 1.5 NPC dialogue bank, 1.6 WBN episode one) carry NO naive-index approvals and NO unstated-ruler approvals: every load-bearing count either states its rule and reproduces against live bytes today (called_shot_ledger 16 rows all BROKEN; qdrops.jsonl 6,242 non-empty rows; dialogue bank 30 rows; spectro 69 rows tallying exactly 1 corrupt_container + 50 no_audio_stream + 18 silent_track; BG media_full 14 files), or is a verbatim quote/existence check where identity is content, never row position. The batch-1.2 disease (drop_no-as-q_num indexing; blessing motif counts under no stated rule) did not propagate. Status of remaining notes: 1.5's 463-to-464 fix note is ALREADY APPLIED in the artifact bytes (rows 016-020 now pin mud.html:464); 1.4's two notes (no denominator row; register_sha256 1/69) remain UNAPPLIED and are cleared as safe to apply (id-clean, rule-stated), still owed to their owner.

## Evidence file:line quotes

- watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md:45-47 (the diseased approval): "qdrops.jsonl drop 200 ts = 2017-11-21T01:12:32+00:00 (drop 1 = 2017-10-28, matching the start claim)" and "the other 9 spot-checked motifs reproduce (crumbs 27, ... HUMA 19, ... rothschild 12 exact ...)".
- watch/inbox/burn_wave_20260926/B2_67_qvision_fixes_20260926.md Evidence: "The audit's window claim indexed rows, not drops" and "Census recompute deltas vs filed hand counts: crumbs 27->26, HUMA 19->16, rothschild 12->13 ... owl 9->6" (the refutation this sweep generalizes from).
- Live recompute (this lane, 2026-09-26): watch/inbox/mrpool_export/called_shot_ledger.jsonl = 16 rows, verdict set {BROKEN} (json.loads per line) — matches 1.1's approval and the matrix's own pin at THE50_W1_T05_PAYOFF_MATRIX.md:71/193; qdrops.jsonl non-empty rows = 6242 (stated rule: non-empty lines) — matches 1.1; memory/runs/the50/w1_t04_npc_dialogue_bank.jsonl = 30 rows W1T04-001..030, rows 016-020 donor_source now reads "dashboard/static/games/mud.html:464 BOONS array (torch id, boonVision)" — 1.5's note applied; memory/runs/the50/w2_t08_spectro.jsonl = 69 rows, class tally {corrupt_container: 1, no_audio_stream: 50, silent_track: 18} (reproduces the audit's stated rule exactly), register_sha256 populated on 1 of 69 (note still open); watch/inbox/bearableguy_export/media_full = 14 files — matches 1.3.
- Identity handling quotes from the audit text (id-clean by construction): 1.4 "msg_id 1840 appears twice ... media_matched/msg_1840.mp4 sha256 6d0f9fbd... vs media_full/msg_1840.mp4 dd51209c... are different bytes" (content-matched, the OPPOSITE of naive-index); 1.6 "verkle_chain.jsonl contains the receipted tip line (index 9824, ts ..., session mag-agent-orc-tbd75828c19)" (index+ts+session triple, chain advance disclosed); 1.3 "counter_code materialized to a scratch module and imported, no exec" (the ruler IS stated: the artifact's own counter).

## Work done

- Read MICKEY17_WAVE2_QUALITY_20260925.md batch 1 in full and B2_67_qvision_fixes_20260926.md in full; extracted the two disease shapes (naive-index identity, unstated counting ruler).
- Swept all approval claims in the other five artifacts for both shapes, then recomputed every load-bearing count against live bytes with .venv/Scripts/python.exe (counts listed above) instead of trusting the audit text.
- Classified remaining fix notes: 1.5 applied (verified in artifact bytes), 1.4 unapplied and cleared as uncontaminated (its defects are the artifact's own gaps: absent denominator row, inconsistent register_sha256 usage; applying them requires no re-audit).

## Falsifier

Kill conditions: (a) any of the five recomputed counts failing to reproduce (none failed today; a future drift means the artifact changed, not that the audit was diseased), (b) a batch-1 approval found resting on row-position identity or an unnameable counting rule (swept, none found; the specific 1.2 rows are already refuted/fixed in B2-67), (c) the 1.4 notes being applied with a naive-index method (they are index-free; if the applier introduces one, the disease returns). Re-check trigger: any future re-audit of MICKEY17_WAVE2_QUALITY batch 1 must include the sweep commands above rather than the audit's own prose.

## Bibliography closed

- watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md (batch 1 sections 1.1-1.6 and summary, read in full)
- watch/inbox/burn_wave_20260926/B2_67_qvision_fixes_20260926.md (read in full)
- watch/inbox/mrpool_export/called_shot_ledger.jsonl (recomputed)
- watch/inbox/qdrop_export/qdrops.jsonl (row count recomputed)
- memory/runs/the50/w1_t04_npc_dialogue_bank.jsonl (recomputed, rows 016-020 read)
- memory/runs/the50/w2_t08_spectro.jsonl (recomputed, keys + tally + sha coverage)
- watch/inbox/bearableguy_export/media_full (file count)
- watch/inbox/THE50_W1_T05_PAYOFF_MATRIX.md (ledger path pins at lines 71, 193, 236)
