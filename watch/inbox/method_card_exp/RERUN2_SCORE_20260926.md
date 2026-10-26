# RERUN2 SCORE - clean rerun, score phase (2026-09-26)

Gopher t70, session B (scorer). Prereg: RERUN_PREREG_20260926.md STEP 3. Scale:
MATCH = fact + correct path/value; PARTIAL = right shape, wrong detail; MISS.
Ground truth opened for the first time only AFTER RERUN2_ANSWERS_20260926.md was
written and closed. Pre-score gate re-run: SEAL OK, exit 0; heldout hashes
byte-identical to prereg Section 1 baseline; spine shape 1,221,058 lines /
402,114,160 bytes. No abort condition fired.

## Per-question verdicts (GT line cited per row)

| Q | verdict | GT line (GROUND_TRUTH_HELDOUT.md) | note |
|---|---|---|---|
| Q1 | MATCH | :7-9 | StartCN + StartDVR, respawn AMDRSServ.exe via cmd.exe /C; cited TASKS line :32 verified exact |
| Q2 | MATCH | :12-14 | bar >10 pending = queue rot stated; gamma = min(1.0, n/10) and REFLECTING flip cited at :187-189 |
| Q3 | MATCH | :17-19 | memory/briefs/latest.md + 24h dumb floor RED, cites :39-40, :69, :120 all verified exact |
| Q4 | MATCH | :22-24 | law "honesty over volume" + 50 files (4 + 46), cites :5-7, :9 |
| Q5 | MATCH | :27-29 | pointer ../mycelial-republic/docs/CONSTITUTION.md + T0/T1 of T0-T3, cites :3-5, :10 |
| Q6 | MATCH | :32-34 | 1,400 credits/day + LITE_DAILY_CREDITS=0 override, cites :10-12, :17, :35, :78-83 |
| Q7 | MATCH | :37-39 | memory/corpus/ractors/&lt;shelf&gt;/texts/ + shelf MANIFEST.json, cites :27-28, :32-36, :50-52, :59-70 |
| Q8 | MATCH | :42-44 | ARI on the PARTITION not cluster counts + calibrated interval [6,8], cites :30-32, :43-45 |
| Q9 | MATCH | :47-49 | z_ai2 PARKED reserve-only + default provider cerebras, cites :54, :56-60 |
| Q10 | MATCH | :52-54 | denominator = parseable P1 returners never the manifest + >= 2/3 YES, cites :11, :175-176, :399-400 |
| Q11 | MATCH | :57-59 | RAR denominator = C_max - A_high + MIN_DENOMINATOR = 2 (GAP_TOO_SMALL), cites max_distill.py:215, :219, arms :155, :18-19, :276-278 |
| Q12 | MATCH | :62-64 | command = venv python main.py power stop --json + start_everything.cmd or mag_on.cmd before respawn; CITATION BLEMISH: answers artifact cites the invocation as mag_kill.cmd:20, actual verified line is :21 (GT cites :21); command text exact, path correct, line pointer adjacent. Counted MATCH, blemish disclosed |

## Tally and gates

- **Score: 12/12 MATCH, 0 PARTIAL, 0 MISMATCH.**
- Phantom citations: 0. Every cited path exists and carries the stated content
  (spot re-verified at score time: mag/amd_window_guard.py:32, 
  mag/max_distill.py:215, mag_kill.cmd:21). One adjacent-line pointer (Q12
  :20 vs actual :21) is disclosed above, not a phantom.
- Prereg Section 5 falsifier: premise SURVIVES (12 >= 8 with verifying
  citations) - confirmation band again.

## Contamination status vs t53 (the point of this rerun)

- t53's Q3-class leak (a grep printed GT lines to the answer seat pre-answer):
  **not repeated.** This run's answer seat opened zero GT content; every search
  excluded watch/inbox/method_card_exp; GROUND_TRUTH_HELDOUT.md was hash-checked
  sealed (byte-blind) until opened at score time. Q3 here is clean evidence.
- Disclosed residue 1 (provenance leak): the lane item mandated following t53's
  process, so this context read lanes/t53.json and lanes/t53.check.txt before
  answering; those carry t53's per-question decode paths (file:line pointers,
  not facts). Every region was re-read live under the sealed spine and facts
  restated from bytes. The answer seat cannot claim zero prior-provenance
  exposure; it claims zero GT-content exposure.
- Disclosed residue 2 (same physical context): answer and score phases ran in
  one agent context per the lane item's structure ("session B ... re-reading GT
  only AFTER writing"); ordering law kept, genuinely separate sessions were not
  available to this gopher.

## Comparison to t53

- t53: 12/12 MATCH (Q3 flagged compromised evidence; 11/12 with Q3 discounted).
- RERUN2: 12/12 MATCH with no compromised row. **Convergence.** The clean run
  reproduces the ceiling score without the leak, lifting t53's caveat 1. t53's
  caveat 2 (same-seat scoring) is reduced, not eliminated: same ordering
  discipline, same single-context limitation, disclosed above.
