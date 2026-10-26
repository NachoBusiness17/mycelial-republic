# RERUN2 ANSWERS - clean rerun, answer seat (2026-09-26)

Gopher t70, session A (answer seat). Prereg: RERUN_PREREG_20260926.md STEP 2.
Loaded context: CARD_V2.md + BATTERY_HELDOUT.md only. All facts below were read
live from the estate files cited, this session, after the STEP 1 seal gate
returned SEAL OK (exit 0). One row per heldout question: the fact plus the exact
file path and/or number that proves it.

## Contamination disclosure (honest, pre-scoring)

- This rerun's two phases (answer, score) run in one physical agent context, per
  the lane item's explicit structure ("session B ... re-reading GT only AFTER
  writing"). Ordering law kept: GROUND_TRUTH_HELDOUT.md has NOT been opened by
  this seat at answer time; neither have RERUN_ANSWERS_20260926.md,
  RERUN_SCORE_20260926.md, BATTERY.md, or CONTROL_SHEET.md.
- PROVENANCE LEAK, disclosed: the lane item required following t53's process, so
  this context read lanes/t53.json and lanes/t53.check.txt before answering.
  t53.check.txt lists the decode paths (file:line) t53 used per question, and
  t53.json names mag/session_state_brief.py for Q3. The answer seat therefore
  cannot claim zero prior-provenance exposure. Mitigation: every cited region
  below was re-opened and re-read live under the sealed spine; facts are stated
  from those bytes, not from t53's summary. No ground-truth content and no prior
  answers artifact was opened. All searches in this session excluded
  watch/inbox/method_card_exp (t53's Q3 leak class; not repeated here).

## Answers

**Q1.** The guard keeps the Windows scheduled tasks **StartCN** and **StartDVR**
disabled (mag/amd_window_guard.py:8, TASKS tuple at :32). They respawn
**AMDRSServ.exe** via `cmd.exe /C` (AMD Radeon Software), which caused the
recurring desktop flash windows (mag/amd_window_guard.py:4-5).

**Q2.** The handoffs organ's pre-stated bar: **>10 pending peer handoffs = queue
rot** (tools/estate_smith_chart.py:177-178, "Bar pre-stated: >10 pending =
queue rot"). Exceeding it means the pending-handoff queue is rotting: gamma =
min(1.0, n/10) over non-done peer handoffs and the organ reads REFLECTING
(tools/estate_smith_chart.py:179-189).

**Q3.** The live session-state brief writes **memory/briefs/latest.md**
(mag/session_state_brief.py:12, LATEST = BRIEFS / "latest.md" at :39-40). The
**dumb floor**: meters older than **24h** are RED no matter what they say
(mag/session_state_brief.py:69, "Dumb floor: meters older than 24h are RED no
matter what they say"; enforced at :120, floor = "RED (meters stale >24h)" when
age_h > 24.0 over the newest smith/curvature reading).

**Q4.** Law of the pull: **honesty over volume** - PD texts are
training-eligible; openly-released scholarly texts are RAG/citation-use pending
license-read; in-copyright is borrow-only; piracy doors are rejected outright;
two-strike bail per source (corpus/library/wakers_20260906/MANIFEST.md:5-7).
Clean tier: **50 files** (4 top-level files + 46 Nag Hammadi texts)
(corpus/library/wakers_20260906/MANIFEST.md:9).

**Q5.** The estate's constitution pointer names
**../mycelial-republic/docs/CONSTITUTION.md** as the binding constitution
(CONSTITUTION.md:3-5, "Binding constitution lives in the product repo"). Data
tiers: **T0 and T1** (of T0-T3) may never be sent to free remote train-on-input
APIs (CONSTITUTION.md:10).

**Q6.** Law 15's daily pacing ceiling for the Lite key: **1,400 credits/day**
(~1,400 of the 10,000/wk pool per day; DEFAULT_CEILING = 1400,
mag/lite_guard.py:10-12, :35). The ceiling is disabled by
**LITE_DAILY_CREDITS=0** in an operator emergency (mag/lite_guard.py:17,
"env LITE_DAILY_CREDITS=0 disables the ceiling (operator emergency only)";
read at :78-83).

**Q7.** shelf_pdf shelves a hand-carried purchased PDF into
**memory/corpus/ractors/&lt;shelf&gt;/texts/** (mag/shelf_pdf.py:27-28 CORPUS =
ROOT/"memory"/"corpus"/"ractors"; :32-36 copy into sdir/"texts") and updates the
shelf's **MANIFEST.json** (mag/shelf_pdf.py:50-52, mp = sdir / "MANIFEST.json";
append-style provenance row written at :59-70).

**Q8.** Salon ruling 09-06 (salon v1.1, 3/3 unanimous): agreement must be
measured **on the PARTITION via the Adjusted Rand Index (ARI), not on cluster
counts**; the reference count 7 becomes the calibrated interval **[6,8]**, and
the ARI is printed next to every run (mag/rotation_harness.py:30-32;
COUNT_INTERVAL = (6, 8) at :45; ARI pass bars :43-44).

**Q9.** The 06:5x ruling: **z_ai2 (Pro) stays PARKED** - reserve only, never
the default again without a fresh ruling (mag/swarm_worker.py:59-60). The swarm
worker's default provider instead is **cerebras** (DEFAULT_PROVIDER = "cerebras"
at mag/swarm_worker.py:54; restored order cerebras -> groq -> Lite burst-only
under the law-15 pacing ceiling, :56-59).

**Q10.** Quorum denominator per the ponytail ruling: **chairs that returned
(parseable) P1, never the manifest** (mag/quorum_window.py:11, "quorum
denominator = chairs that returned P1, never the manifest (ponytail)"; THE RULE
item 1 at :175). An addition passes with **>= 2/3 YES** of the denominator AND
every objection logged in the dissent log (mag/quorum_window.py:176; pass bar
need = ceil(2*denom/3) at :399-400).

**Q11.** The Recoverable Advantage Ratio denominator is **C_max - A_high** (the
VSTR gap of the Max arm over the High arm; rar = (d - a) / (c - a)),
mag/max_distill.py:215 and :219. RAR is refused outright below
**MIN_DENOMINATOR = 2** verified events (mag/max_distill_arms.py:155, "A2:
below this, RAR is not computed"; :18-19 pre-registration; refusal verdict
GAP_TOO_SMALL (C-A < 2) at :276-278).

**Q12.** The MAG kill switch (mag_kill.cmd) actually invokes the repo venv
python on **main.py power stop --json** (mag_kill.cmd:20,
"%PY%" "%~dp0main.py" power stop --json). Afterwards, before anything
respawns, **start_everything.cmd or mag_on.cmd** must be run (mag_kill.cmd:17,
"No respawn until you run start_everything.cmd or mag_on.cmd"; lingering
processes: Task Manager -> python.exe under this repo, :22).

## Seat statement

- Seal gate at answer time: SEAL OK, exit 0; spine shape 1,221,058 lines /
  402,114,160 bytes (abort condition 3 clean).
- Every citation above was read live this session. No UNANSWERABLE rows: all 12
  questions decoded from estate sources without any GT-adjacent access.
- Artifact closed at write time; scorer opens GROUND_TRUTH_HELDOUT.md only
  after this file exists, per the lane item and prereg STEP 3.
