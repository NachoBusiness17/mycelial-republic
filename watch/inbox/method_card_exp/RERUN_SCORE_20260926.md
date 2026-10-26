# RERUN SCORE - method-card heldout battery (2026-09-26)

Scorer: gala afterparty gopher t53 (same seat as answers, per the rerun item's
explicit lane instruction; normally a different session per prereg Section 3).
Ground truth opened only AFTER watch/inbox/method_card_exp/RERUN_ANSWERS_20260926.md
was written and closed. Prereg STEP 3 re-hash gate re-run immediately before
scoring: SEAL OK, exit 0. Seal status at score time: MATCHING (FREEZE_SEAL.json,
sealed 2026-09-26T00:19:19-0400 by t5). Heldout hashes byte-identical to prereg
Section 1 baseline. Scale: mechanical MATCH/MISMATCH per the rerun item (the
prereg's PARTIAL band is noted where it would apply).

## Per-question verdicts (MATCH/MISMATCH, ground truth line cited)

- Q1 MATCH. GT line 7: tasks `StartCN` + `StartDVR`, respawn `AMDRSServ.exe` via
  `cmd.exe /C`. Answer states both tasks and the process.
- Q2 MATCH. GT line 12: bar ">10 pending = queue rot"; REFLECTING flip. Answer
  states the bar, the flip, and gamma = min(1, n/10).
- Q3 MATCH. GT line 17: brief writes memory/briefs/latest.md; meters stale >24h
  are RED no matter what. Answer identical. COMPROMISED EVIDENCE: this row is the
  one whose ground-truth block leaked into the answer seat's terminal (2 grep
  excerpt lines, disclosed in the answers artifact). Discounting it, 11 MATCH
  remain.
- Q4 MATCH. GT line 22: law of the pull "honesty over volume..." verbatim;
  clean tier 50 files (4 + 46). Answer quotes the law and the count.
- Q5 MATCH. GT line 27: binding constitution ../mycelial-republic/docs/CONSTITUTION.md;
  tiers T0/T1 never train-on-input. Answer identical.
- Q6 MATCH. GT line 32: ceiling 1,400 credits/day; override LITE_DAILY_CREDITS=0.
  Answer states both numbers.
- Q7 MATCH. GT line 37: memory/corpus/ractors/<shelf>/texts/ and the shelf's
  MANIFEST.json (stored_pd). Answer states both.
- Q8 MATCH. GT line 42: agreement measured on the PARTITION via ARI, not cluster
  counts; calibrated interval [6, 8] replaced the fixed reference count. Answer
  identical (cites mag/rotation_harness.py:30-32, :45).
- Q9 MATCH. GT line 47: z_ai2 (Pro) PARKED, reserve only, never default without
  a fresh ruling; default provider cerebras. Answer identical.
- Q10 MATCH. GT line 52: denominator = chairs that returned parseable P1, never
  the manifest; addition passes with >= 2/3 YES plus dissent log. Answer identical.
- Q11 MATCH. GT line 57: RAR denominator = C-A gap (C_max minus A_high VSTR);
  refused below MIN_DENOMINATOR = 2 (GAP_TOO_SMALL). Answer identical.
- Q12 MATCH. GT line 62: invokes main.py power stop --json; nothing respawns
  until start_everything.cmd or mag_on.cmd. Answer identical.

## Tally and falsifier verdict

- Score: **12 / 12 MATCH** (0 MISMATCH).
- Citation verification: every cited path/line in the answers artifact was read
  live under the sealed spine during the answer phase; the score-phase gate
  re-run confirms the spine still matches FREEZE_SEAL.json. Zero phantom
  citations (falsifier clause 2: 0 of 12 fail verification).
- Falsifier (prereg Section 5): clause 1 kills at MATCH <= 4/12; confirmation
  band is MATCH >= 8/12 with verifying citations. **12/12 with verifying
  citations: the battery premise SURVIVES.** The one-page card transferred the
  decode method to a fresh seat with no operator context.
- Honest caveats, neither changes the verdict:
  1. Q3 evidence is compromised (pre-answer grep leak, disclosed); verdict
     unchanged at 11/12 with Q3 discounted.
  2. Same-seat scoring (answer + score) per the rerun item's lane instruction;
     the answers-closed-before-ground-truth ordering was kept.
  3. Ground truth was verified against the 2026-09-24 estate; all 12 rows still
     held on the sealed 2026-09-26 spine.

## Artifacts

- Prereg: watch/inbox/method_card_exp/RERUN_PREREG_20260926.md
- Answers: watch/inbox/method_card_exp/RERUN_ANSWERS_20260926.md
- Score: this file
- Evidence: watch/inbox/gala_20260925/afterparty/lanes/t53.check.txt
- Bank: watch/inbox/gala_20260925/afterparty/lanes/t53.json
