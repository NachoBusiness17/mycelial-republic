# B2-58 receipt: prompt-law v2 amendments landed in README (2026-09-26)

## Verdict

landed (spec change only; no code touched)

## Evidence

Every amendment traces to on-disk receipts from today's full-text reads, plus
two live corroborations fetched this lane.

- Law 1 split (anchor vs lock), watch/inbox/burn_wave_20260926/B2_09_prompt_uplift_20260926.md:25: "Law 1 HOLD, split in two: judge-side ANCHOR (VQQA p0 scoring, now first-hand canon) versus candidate-side LOCK (ships nowhere; PRIS and VisualPrompter rewrite freely). FAIL(BIB_LAUNDER) survives as the lock".
- Anchor quote, B2_09:17: the VQQA rater "assesses each candidate against the original prompt p0"; judge-must-quote anti-pattern, same line: judge closes "Respond with only a number between 0 and 100"; B2_09:26: "the judge seat returns element + quote + verdict. 'Only a number' is the named anti-pattern."
- Seed-paired uplift, B2_09:27: PRIS regenerates with "the top-k noise seeds", "seed-paired so the delta measures the prompt, not noise".
- TARA auto-revert, B2_09:19: "adopts the repair iff s(x̂)>s(x0) and otherwise reverts"; "This accept-or-revert regression guard is not a best-of-N selector"; gate removal "costs 3.6 points in ablation"; B2_09:30: "flag-only is insufficient; adopt-iff-score-improves-else-revert is the shipped pattern."
- Kill condition, B2_09:35: "a shipped optimizer that natively locks a user-fact block, or hard-anchors candidates to p0, demotes FAIL(BIB_LAUNDER) from law-patch to interop note. TARA is the closest live threat."
- Check shape + no-judge-instruction ruling, watch/inbox/BURN_prompt-uplift-lane_20260925_d.md:28,30: "compare against the SEED hash, never the previous candidate"; "No whitespace or unicode normalization (launder vectors)"; "a judge asked to verify bytes will paraphrase-verify"; :17 "DRAFT ONLY: roblox/prompts/ untouched" (this lane is the first landing).
- Original FAIL(BIB_LAUNDER) rule, watch/inbox/BURN_prompt-uplift-lane_20260925.md:22: "the optimizer may touch structure and instructions only; FACTS and bibliography lines are carried byte-verbatim into every candidate; any delta there is FAIL(BIB_LAUNDER)."
- Live corroboration this lane (2026-09-26): arxiv.org/abs/2607.18724 abstract confirms title "Type-Aware Repair Allocation for Text-to-Image Prompt Optimization" and "a semantic repair gate, an accept-or-revert controller over exactly one prescribed repair that prevents semantic regressions" (the s(x̂)>s(x0) sentence is full-text only, on record in B2_09:19); arxiv.org/abs/2603.12310 confirms title "VQQA: An Agentic Approach for Video Evaluation and Quality Improvement".
- Landing bytes: roblox/prompts/README.md grew 74 insertions, 0 deletions (git diff --stat), new "## THE V2 AMENDMENTS (2026-09-26)" section between the laws and THE TEMPLATES, changelog row appended; 0 em-dashes in the file (grep -c).

## Work done

1. Wrote the four v2 amendments into roblox/prompts/README.md: (A) law 1 split, judge-side ANCHOR vs candidate-side LOCK with per-template invariant blocks and the pass-d check shape; (B) law 3 judge-must-quote, "only a number" named anti-pattern; (C) law 5 seed-paired uplift, unpaired uplift claims are CLAIMED; (D) law 4 BIB_LAUNDER auto-revert per the TARA gate, adopt-iff-paired-score-beats-seed-else-revert, lock still rejects regardless of score. Kill condition carried. Per-template contract lines and the checker script remain owed (README only, per brief).
2. Receipt (this file) + LEDGER row + 2 self-feed briefs, landed as B2-154 (checker script) and B2-155 (paired-eval harness); first choice B2-150/151 was claimed by concurrent lanes mid-flight (the script's pre-write assert caught 150, dynamic re-pick took the next free integers per the B2-53 lesson), numbers verified unclaimed immediately before append.

## Falsifier

Pre-registered: (F1) the kill condition above demotes the lock to interop note if any shipped optimizer natively locks a user-fact block or hard-anchors candidates to p0. (F2) amendment D is untestable until a paired scorer exists; if the B2-151 harness lands and the TARA gate does not beat flag-only adoption on seed-paired regression rate, the auto-revert clause is vacuous and reverts to flag-only. (F3) if BIB_LAUNDER fires on a candidate whose invariant blocks are byte-identical under the pass-d marker extraction, the extraction spec is wrong, not the candidate.

## Bibliography

Closed. Repo: roblox/prompts/README.md (pre- and post-edit, in full), DETAIL.prompt.md (in full), section headers of PORT_GAME / CLONE_WHEEL / ONE_SHOT_GAME / NPC_HEAD; watch/inbox/BURN_prompt-uplift-lane_20260925.md, _b, _c, _d (pass d in full); watch/inbox/burn_wave_20260926/B2_09_prompt_uplift_20260926.md (in full), B2_08_judge_lane_20260926.md (in full); QUEUE.md tail + ledger tail for numbering. Web (2026-09-26, this lane): arxiv.org/abs/2607.18724, arxiv.org/abs/2603.12310 (abstract-level corroboration; full-text quotes rest on B2_09's same-day reads). Not read this lane, filed as owed: none new beyond B2_09's own owed list (alphaxiv 2603.00483 timeout, carried there).
