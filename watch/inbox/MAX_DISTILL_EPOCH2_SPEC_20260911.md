# MAX_DISTILL EPOCH 2 SPEC (2026-09-11, night rotation lane — FILE WORK ONLY, no execution)

Status: SPEC, awaiting operator GO before any run. Build freeze respected: this card
spawns nothing; it pre-registers the measurement so the future run is one command.
Sources: memory/runs/max_distill/epoch1_report.json (+ trials.jsonl row audit),
mag/max_distill_arms.py, watch/NIGHT_FOLD_20260911.md, watch/PYRAMID_VISION_20260911.md.
Dating method (night-fold law 3): card dated by OPERATOR date Sep-11; any run stamps
carry BOX time and say so. Box clock skew is known.

---

## 1. What epoch 1 measured, and why it was INCONCLUSIVE

Epoch 1 (fired 04:00 box-time Aug 27) measured whether a distilled action_policy
(SkillCandidate template) lifts glm-4.7-flash toward the glm-5.3-flash ceiling on a
frozen 10-instance concurrency-invariant batch — 4 arms (A plain / B +hint /
C 5.3-flash ceiling / D +distilled policy), 40 trials, twin renames per amendment A1.

The report, quoted (epoch1_report.json):

    "arms": { "A_high": {"n":10, "native":"1/5", "twin_heldout":"1/5"},
              "B_high_info": {"n":10, "native":"2/5", "twin_heldout":"0/5"},
              "C_max": {"n":10, "native":"0/5", "twin_heldout":"0/5"},
              "D_high_distilled": {"n":10, "native":"1/5", "twin_heldout":"1/5"} },
    "gaps_vs_A": { A:0, B:0, C:-2, D:0 },
    "a3_trigger": { "rule": "(D-A) >= 1.5x (B-A)", "fires": false },
    "rar": { "rar": null, "verdict": "GAP_TOO_SMALL (C-A=-2 < 2)" }

Why INCONCLUSIVE — three stacked causes, in order of damage:

1. TRANSPORT, NOT TREATMENT. The row audit of trials.jsonl: only 10 of 40 rows have
   a clean call. 23 rows died on HTTP 429, 3 on the reasoning-budget empty-content
   bug (since fixed in code: 5.3 rides thinking=low + 1536 max_tokens), 2 remote
   closed, 2 DNS/socket. C_max was hit worst — 3/10 valid calls — so its 0/10 is a
   lane reading, not a capability reading. The first attempt
   (trials_epoch1_attempt1_transportfail.jsonl, 40 rows) failed outright.
2. FLOOR EFFECTS. A=B=D=2/10 means the baseline, the info arm, and the distilled arm
   are indistinguishable AT the floor. A gap of 0 vs 0 carries no information — you
   cannot compute RAR on it. n=10 per arm was too small (amendment A2's power
   pre-registration was sized for a medium effect, then the floor ate even that).
3. SCORING GATE STRICTNESS. A VIOLATED pass requires naming the conflict, not just
   the label — correct design, but it pushes weak arms to floor. No difficulty bands
   were recorded, so a floor was invisible in the report until someone read rows.

No law was promoted. Correct call. The harness itself (commitment hash per row,
epoch filter, A3 trigger logic) worked exactly as built.

## 2. What changed since Aug 27 that epoch 2 must account for

1. LANE MAP REWRITTEN. z_ai2 proved saturated 24/7 — all arms already repointed to
   z_ai3 in the harness (lane is TRANSPORT, not treatment). Promo Sep 3-20: 5.3-flash
   rides the in-ZCode FREE plan with a LIMITED daily per-seat quota (receipt 09-05:
   49% burned by midday). glm-4.7-flash is the only free cache-mining lane
   (fuel_feed pinned by model). Verify 4.7 pool health the night of the run.
2. WAVE PROTOCOL + ROTATION DOCTRINE EXIST NOW (09-09; night-fold law 1). Epoch 1
   fired 40 calls nearly back-to-back and got a 429 flood. Rotation at bounded width
   (two, never past refill) landed the same lanes for ~1/5 the cost. The 18-25s
   heartbeat between waves is sanctioned idle. Epoch 2 fires as waves, not a stream.
3. NO SILENT PASS (night-fold law 2). Epoch 1 swallowed transport errors into scored
   rows — a failed call scored as a fail. Epoch 2: every caught exception emits a
   receipt row; failed calls are retried (3x, backoff); an arm under 80% valid calls
   is TRANSPORT_BLOCKED and rescheduled — never scored as zero.
4. OPERATOR VOLUME PATTERN. His quota burns 8AM-6PM PT, midday worst. The 04:00 box
   quiet window (proposed law 12) is empty grid: run there, zero contention.
5. NEW DISTILLATION TARGETS. The readable laws (PYRAMID_VISION_20260911) — plain
   English, short lines, earned names used back, never metaphor-stacked — are now a
   policy that can be distilled and machine-scored. "Drift is default behavior,
   reward gravity UNPROVEN" is an open claim a D2 probe can test directly. The wave
   triage shape (TYPE / CONNECTS TO / NEXT STEP / FILE TO) is a second candidate.
6. CONSTRAINT PINNING STEAL (night-fold docket): ~47 tokens restores 0% violations —
   the D-arm policy should stay short and sit near the decision step, not bloat.
7. MACHINE GATES COUNT STRIKES (night-fold law 5): two same-category machine verdicts
   = the answer. Scoring disputes resolve by second gate, operator only on split.

## 3. Epoch 2 design (pre-registered — change nothing after first firing)

DOMAINS (two, so the result is not a one-quiz artifact):
- D1 CONCURRENCY: reuse the frozen epoch-1 batch verbatim (comparability) + 20 new
  instances, pre-registered once, difficulty-tagged. Mix per 30: 12 VIOLATED /
  18 SAFE; 18 native + 8 rename twins + 4 held-out; bands 40% easy / 40% medium /
  20% hard.
- D2 READABLE-REPLY: same 30-instance structure. Task: shape a fleet answer (given a
  messy finding + audience) under the readable laws. Machine-scored checks:
  outcome-first first sentence, short lines, no banned-register stack (riddler
  336-term falsifier list style), correct use of earned names, no moon-speak drift.
  D2 doubles as the drift-is-default probe when C runs it in plain mode.

ARMS (unchanged treatment matrix, z_ai3 transport; code already carries this):
- A_high      4.7-flash, plain          - baseline
- B_high_info 4.7-flash + hint          - controls for info, not policy
- C_max       5.3-flash, thinking=low, 1536 max_tokens (bug fixes already in code)
- D_high_distilled 4.7-flash + SHORT pinned policy (constraint-pinning shape:
  <=60 tokens, placed after the procedure, before the verdict step)
- E_max_info  5.3-flash + hint — the A3 pre-committed arm; fires ONLY if the trigger
  (D-A) >= 1.5x(B-A) holds on clean epoch-2 A/B/D. No early firing.

SAMPLE SIZE — sized against the epoch-1 floor error:
- 30 paired instances per arm per domain (same instances across arms = paired
  design; discordant-pair comparison, far more power than two independent n=10s).
- 60 rows per arm across both domains; 240 rows total; +30 if E fires.
- CALIBRATION PILOT (one time, pre-registered, not p-hacking): before the main run,
  6 instances per arm per domain. If A < 20% or ANY arm hits 0/6, rebalance the
  difficulty bands once, re-freeze, then run. Purpose: keep A off the floor so gaps
  are measurable — the exact epoch-1 failure.
- Per-band pass rates appear in the report so a floor is VISIBLE, not discovered.

PRE-REGISTERED SUCCESS THRESHOLDS:
- P1 PROMOTION (the point of the program): D-A >= 8 of 30 paired instances
  (>=26.7 pts) on BOTH domains; twin transfer >= 50% of native gain (A1's test:
  structure survives rename). One domain only = PARTIAL, no law.
- P2 RAR: C-A >= 4 verified events (epoch-2 MIN_DENOMINATOR raised 2 -> 4); RAR via
  the existing compute_rar.
- P3 A3 trigger: as coded, 1.5x, on clean data only.
- P4 VALIDITY: every arm >= 80% valid calls; below that the arm is TRANSPORT_BLOCKED,
  receipted, and rescheduled to the next quiet window. Validity gate runs BEFORE any
  score is read.
- P5 DRIFT PROBE (D2, secondary): C plain-mode readable-check pass rate — if < 50%,
  "moon-speak drift is default behavior" moves UNPROVEN -> SUPPORTED with receipts.

QUIET-WINDOW SCHEDULE (04:00 box-time, box clock; operator asleep, zero contention):
- Night 1: D1 arms A + C.      Night 2: D1 arms B + D.
- Night 3: D2 arms A + C.      Night 4: D2 arms B + D.
- Night 5: E if fired + full report. One arm-domain block per night.
- Firing shape: width-2 waves, one call in flight per lane, 18-25s heartbeat between
  waves, retry 3x with backoff, receipt per failure. ~30 calls/night = ~15 waves —
  minutes of firing, the rest is the wave holding.
- BUILD CHECKLIST for the executor (file work, small): new frozen EPOCH2_INSTANCES
  section (never touch epoch-1 constants), --domain flag, receipt-emitting retry in
  run_arm, report(epoch=2, domain=...). Schema bump max_distill_arms.v2, epoch field
  preserved. No credential edits, no new lanes.

## 4. Cost estimate

- ~270 calls total x ~1.1K tokens avg ~= ~300K tokens, ALL on $0 lanes: A/B/D ride
  the 4.7-flash free cache-mining lane; C/E ride the 5.3-flash promo quota at 04:00,
  outside the operator's midday burn (est. <5% of one seat's daily pool per night).
- Cash: $0. Premium tokens touch judgment only — this spec was the premium part;
  execution is fleet lanes, not the seat.
- Lawful per the standing rule: bulk work routes to free lanes.

## 5. The falsifier (pre-registered — this is what would KILL the hypothesis)

PRIMARY: Under valid transport (every arm >= 80% valid calls) on the calibrated
batch, if D-A < 8/30 in BOTH domains AND twin transfer < 50%, then trace
distillation (injected action_policy) gives NO measurable lift on glm-4.7-flash.
MAX_DISTILL retires to UNPROVEN; the harness stays as a reusable instrument; no
epoch 3 without a NEW mechanism hypothesis (e.g., constraint-pinning at the decision
step instead of a procedure policy).

SECONDARY: If C_max still scores < 20% with valid transport on the calibrated batch,
the "frontier ceiling" reading is DISPUTED — the task format starves the model, not
the capability. No RAR claim survives; C gets re-specced before epoch 3.

TERTIARY (not a failure — a finding): if the D arm shows no lift in D2 but C plain
also fails the readable checks, the drift-is-default claim gains SUPPORTED status
from an independent probe. A killed hypothesis that bought a confirmed law is not a
wasted epoch.

---
Filed to watch/inbox per rotation lane. No files touched besides this card.
