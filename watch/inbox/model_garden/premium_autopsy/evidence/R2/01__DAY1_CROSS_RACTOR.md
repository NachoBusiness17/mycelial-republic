# DAY1_CROSS_RACTOR - cross-file laws from the whole 2026-10-01 burn (the lane a per-file ractor cannot run)

Scope: every .md in watch/inbox/hermes_burn/ (A1+A1_ASSEMBLED, A2, A3, B1, B2, C1+C1_ASSEMBLED,
D1-D3, DUEL1_hidden_1-4/6, DUEL2_train_01-14, MOVEMENT2_CHEAP_ANSWERS, T1W1 all six, T1W2 S5-S8,
WAVE24_BOARD, WINDOW1_STATE, WINDOW2_RACTOR) plus watch/inbox/x_intel_deepgemm_20261001.md,
memory/plans/BURN_PLAN_140.md, and memory/runs/hermes_burn/usage.jsonl.

Conditions. Instrument: file reads plus one ledger aggregation
(./.venv/Scripts/python.exe over usage.jsonl). Moment: 2026-10-01T20:12:58Z ledger read (179
rows, $29.91 total, 83 refusal rows, 38 distinct ask ids; the file is live and append-only, so
every money number below is that moment's snapshot). Context: read-only lane, no files modified,
no git operations. Cross-file only: anything one file says on its own is out of scope.

---

## ECONOMICS (ask-shape economics, findings per dollar)

Track ledger at the snapshot moment (cost / calls / landed value):

| track | cost | paid calls | what landed |
|---|---|---|---|
| A1 steer antiforgery | $20.00 | 48 (45 turn-1 + 3 turn-2) | one design, complete in reasoning after call 1 |
| T1W1 stranger audits | $2.74 | 4 | 9 laws + 14 tickets + 16 to-verify, then free verify settled 11 |
| B2 drift attribution | $1.48 | 6 identical burns | one spec |
| C1 censorship | $1.47 | 6 (never converged) | reasoning + a generic ASSEMBLED |
| A2+A3+B1 single-shot specs | $1.62 | 3 | three complete landable specs |
| D1+D2+D3 roast cycle | $1.38 | 3 | ~25 line-pinned defects, 3 amendments, 2 confirmations |
| DUEL2 train | $0.33 | 14 | 14 blocked outputs, zero verdicts |
| T1W2 audits | $0.25 | 7 | generic threat models (evidence empty), S8 near-empty |
| DUEL1 hidden | $0.12 | 5 landed / 42 refused | blocked outputs + refusal data |
| deepgemm sherpa (DS) | $0.0024 | 4 | the entire x_intel dossier foundation |
| N1 parables | $0.00 | 38 refused | nothing (policy block) |

### E1. one ask ate two thirds of the day
- claim: A1_steer_antiforgery consumed $20.00 of $29.91 (66.9 percent) across 48 ok-marked
  ledger rows, and its deliverable was complete in the reasoning channel after the first burn
  (13:11Z, 14,960 ctok); 47 later burns changed nothing.
- evidence: memory/runs/hermes_burn/usage.jsonl (48 rows id=A1, all ok:true, 13:11Z to 20:10Z);
  A1_steer_antiforgery.md carries the full design by the end of its first pass.
- steal (one sitting): the burn driver skips any ask id whose output file already exists unless
  revision.md mtime is newer than the last ledger row for that id; the ledger gains a
  duplicate_burns counter per id printed in the daily carrier.
- falsifier: a full day where duplicate_burns is zero and no re-fire ever lands content the
  first burn lacked, or a duplicate burn that does land new content the counter fails to exempt.

### E2. the findings-per-dollar ranking is not close
- claim: ranked by landed law per dollar: (1) T1W1 stranger audits, $2.74 for 9 laws + 14
  tickets + 16 to-verify claims that a free lane then converted (8 VERIFIED, 2 REFUTED,
  1 UNDECIDABLE); (2) the D roast cycle, $1.38 for about 25 line-pinned defects plus 2 landable
  amendments plus the L1 close; (3) single-shot A2/A3/B1 specs at $1.62; then a cliff: C1 at
  $1.47 for an assembled artifact that lost its best content, and the duel track at $0.45 for
  zero verdicts.
- evidence: T1W1_RACTOR.md (9 LAWS, 14 TICKETS sections), T1W1_TOVERIFY_VERDICTS.md (tally
  line), D1/D2/D3 receipts, usage.jsonl per-id costs.
- steal: tomorrow's budget follows this ranking: widen T1 stranger audits and roast movements
  before any new ask class; the BURN_PLAN_140 T1 track already holds ~$45, point it at the
  proven shape only.
- falsifier: a T1W3 batch at the same shape yielding under 3 laws per $3 ask would break the
  ranking; then the shape, not the track, is the variable.

### E3. the winning ask shape, named
- claim: every track that produced verdicts today shared one shape: full evidence bytes pasted
  into the context (T1W1 got whole files, D1-D3 got whole chapters plus later the gate source,
  A2/A3/B1 got the receipts), a small output contract (one deliverable, falsifier, no em-dash),
  and a cheap pre-read riding as evidence. Every track that failed lacked exactly one thing:
  the bytes (duels and T1W2 sent contracts whose EVIDENCE block arrived empty).
- evidence: T1W1_stranger_* files cite quoted bytes throughout; all 19 DUEL outputs open with
  "the EVIDENCE block is empty"; T1W2_S5/S6/S7 open with "Evidence status: The EVIDENCE block
  is empty".
- steal: add a pre-fire assertion to the driver: render(entry) length must exceed body length
  by the material bytes (tools/ask_bank.py:141-143 concatenates body + <SOURCE> + material);
  exit 2 on an evidence-less fire.
- falsifier: one duel fire that lands a verdict-rich output while its contract still carries an
  empty evidence block would show the material was never needed.

### E4. cheap legs are the volume layer, premium is the judgment layer, and today they met once
- claim: $0.0024 of deepgemm sherpa produced the dossier skeleton the whole intel lane stood on;
  $0 of free Task lanes produced the T1W1 distillation, the 11 to-verify verdicts, and the
  movement dig tickets; premium's only irreplaceable wins were adversarial reads of bytes
  already in context (roasts, audits, specs).
- evidence: x_intel_deepgemm_20261001.md (sherpa rows 1-4 named as foundation), WINDOW2_RACTOR
  W2-L4 (the loop legs and their costs), T1W1_TOVERIFY_VERDICTS.md (free lane).
- steal: keep the WAVE24 loop but make the rule explicit: premium fires only when the ask
  carries in-context bytes to judge; sensing and command-running never climb.
- falsifier: a week where premium asks without in-context bytes out-yield premium asks with
  them per dollar.

### E5. re-burn is a multiplier, not an event
- claim: B2 burned 6 identical times at $0.2466 (same ctok 20000 each, 13:18Z to 18:13Z) and
  WAVE24's board still described the defect as "B2 paid 3x ... fixed by flag hygiene"; A1 kept
  burning after the board landed (6 more burns 16:00-16:10 local). The fix claim is itself a
  report the ledger contradicts.
- evidence: usage.jsonl B2 rows; WAVE24_BOARD.md SPEND DISCIPLINE section (file mtime 15:18
  local) vs A1 rows at 20:01-20:10Z (16:01-16:10 local).
- steal: the driver prints, per cycle, ids re-fired whose output file predates the cycle; any
  such line is an incident, not hygiene.
- falsifier: three driver cycles with zero re-fire lines while queues stay non-empty.

---

## SCORECARD (premium vs cheap on the same question)

### S1. cheap bytes, wrong verdict, twice on one question
- claim: on the workflow_gate exit semantics, the cheap arm reported the correct docstring span
  and then drew the wrong verdict twice ("grep counts ZERO sys.exit(1) sites ... Exit 1 never
  blocks a push; the trivalent contract holds as logic.md states it. The chapter's claim is
  byte-true", then later "returns 1 (soft, lines 216/298)"), while premium D2 showed the grep
  instrument was blind (the file has one sys.exit; codes travel via returns) and that neither
  logic.md mapping matches the code, and D3 showed the "(soft)" label carried no bytes.
- evidence: MOVEMENT2_CHEAP_ANSWERS.md items 1 and movement-3 item 1; D2 section (1) exit-site
  table and defect C1; D3 section (1) residue R2.
- steal: cheap arms may collect bytes but a premium (or free verify) lane must sign the
  verdict-on-bytes; ticket answers land as PROPOSED until countersigned.
- falsifier: a week of cheap-arm verdicts on bytes with a countersign mismatch rate under 5
  percent would allow letting cheap verdicts stand.

### S2. cheap assembly of premium reasoning is lossy exactly at the best parts
- claim: C1's premium reasoning contained the load-bearing catches (gemma:2b is Gemma-1 lineage
  so the P2 abliteration comparison is confounded; P1 measured zero safety refusals so the
  fleet battery cannot measure refusal change; the DS 40-70 percent depth and 5-15 percent
  quant-recovery figures are uncited folklore; pheromone accumulation is impossible on a
  stateless chat wire; Ouroboros conflates layer-wise re-encoding with turn-wise self-repair),
  and C1_censorship_ASSEMBLED.md kept none of them, shipping generic mechanism rows instead.
- evidence: C1_censorship_mechanisms_crossfamily.md lines on lineage mismatch, P1 zero-safety
  refusals, uncited figures, stateless wire; C1_censorship_ASSEMBLED.md section 2 ("reported
  across open-weight families. UNVERIFIED as universal").
- steal: assembly prompts must name the class of content to preserve ("carry every catch that
  names a specific number, file, or model lineage verbatim") and the assembler must quote-check
  each carried catch against the reasoning text the way T1W1_RACTOR byte-verified 57 quotes.
- falsifier: an assembled artifact that carries 90 percent of the named-catch class verbatim;
  then the loss is prompt noise, not structural.

### S3. free lanes beat premium on premium's own facts
- claim: the free distillation and verify lanes corrected the premium audits on mechanism and
  numbers: os.kill(pid, 0) on Windows routes through GenerateConsoleCtrlEvent, not
  TerminateProcess (V1 CONTRADICTED, with the estate's own WinError 87 comment as the real
  path); the audit's leaf counts (2,821 of 8,626 / 9,873 lines / 5,874 leaves) matched nothing
  on disk while the live tree read 8,777 rows (V4); the drift-patrol laundering claim fell to a
  zero-write-call sweep (V14 REFUTED).
- evidence: T1W1_RACTOR.md TO-VERIFY V1 and V4 with the exact commands and outputs;
  T1W1_TOVERIFY_VERDICTS.md rows V1, V4, V14.
- steal: every premium audit lands with its TO-VERIFY block pre-attached and a free verify pass
  is part of the ask, not an optional follow-up (the T1W1 pattern is the template).
- falsifier: a verify lane that refutes under 1 in 10 premium audit claims for a week would
  make the pass optional.

### S4. the premium leg that never fired
- claim: the DeepGEMM mating-door adjudication (DG1) was staged in WAVE24 and still open at
  window close, so the $0.0024 sherpa verdicts carried the entire track with no premium
  confirmation and no premium correction; the loop's judgment leg is the one that can silently
  not happen.
- evidence: WAVE24_BOARD.md lane 7 (staged), WINDOW2_RACTOR.md DOORS item 1 ("DG1 verdict ...
  driver firing" still open); no DG1 file exist
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 10500 + tail 3500 of 21921 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
ree chapters
  certify that the record exists and then treat that existence as the law being in force").
- steal: the daily carrier reports distinct landed artifacts per track, not calls; calls per
  artifact above 2 print in red.
- falsifier: a day where calls-per-artifact is under 2 across all tracks with the driver
  running full queues.

### N3. the evidence defect is batch-correlated, not random
- claim: T1W1 (15:09Z) fires carried full evidence; DUEL1 (16:50Z), T1W2 (19:17Z) and DUEL2
  fires carried empty EVIDENCE blocks against materials that exist on disk (all five spec files
  present, 45-227 lines each); whatever path fires the duel and T1W2 asks drops the rendered
  material.
- evidence: file mtimes and ledger ts per batch; the contenders' quoted contract metadata;
  docs/ref/ directory listing (this lane checked: all five named materials exist).
- steal: one grep in the firing path for send(body) versus send(render(entry, text)) (the
  render contract is tools/ask_bank.py:140-143); the E1 pre-fire assertion closes the class.
- falsifier: a duel fire with the <SOURCE> block present that still lands a blocked output.

### N4. assembly fired once, premium re-fired forever
- claim: A1_steer_antiforgery_ASSEMBLED.md (09:57 local) predates the premium file's final
  write (16:10 local); the cheap assembly ran on an early burn and later premium burns never
  re-assembled, so the send-back wiring is asymmetric in the most expensive direction.
- evidence: file mtimes; usage.jsonl A1 burn times.
- steal: assembly is a driver step keyed to premium-output mtime, not a manual one-shot.
- falsifier: an assembled artifact whose mtime tracks the last premium burn for a day.

### N5. revision turns cannot carry converged output on this ask class
- claim: C1 burned three turn-2 attempts (ctok 922, 935, 759) that aborted as the three
  fragmentary "REVISION (turn 2)" blocks visible in the landed file; the WINDOW1_STATE owed
  item (revision turns return empty, suspected assistant-echo in messages) is visible in the
  artifact itself, unfixed all day, on a second model (fable) beyond the sonnet case named.
- evidence: C1_censorship_mechanisms_crossfamily.md REVISION blocks; usage.jsonl C1 turn-2
  rows; WINDOW1_STATE.md owed item 1.
- steal: revision turns drop the assistant echo and carry only [original user prompt, revision
  message]; if the second attempt still returns under 1000 ctok, the ask re-opens as turn 1.
- falsifier: a revision turn over 5000 ctok landing a converged deliverable.

### N6. the judge pass never ran, so the contamination question is untouched
- claim: no judge rows exist in the ledger and WAVE24 lane 11 ("RACTOR DUEL1+DUEL2 -> judge
  rules from 19 verdicts") stayed staged; the T4 track's whole purpose (judge diversity, the
  D6 cure) produced no judging signal on day 1 because its contender leg was blocked.
- evidence: usage.jsonl (zero judge-family rows); WAVE24_BOARD.md lane 11.
- steal: after the N3 fix lands, re-fire the 19 duel asks with materials attached, then the
  judge pass, before any new T4 spend.
- falsifier: a judge pass over the re-fired duels producing the verdict table.

---

## Footer

Cross-ractor conditions: this file was written by the free ractor lane, 2026-10-01, from the
41-file set plus ledger named above; every money figure is the 20:12:58Z ledger snapshot; no
file outside this one was modified. Every law row carries claim, evidence, one-sitting steal,
falsifier. No em-dashes in this file.
