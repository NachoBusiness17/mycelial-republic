# RERUN ANSWERS - method-card heldout battery (2026-09-26)

Answer seat: gala afterparty gopher t53, fresh context, holding CARD_V2.md +
BATTERY_HELDOUT.md + live read access to the sealed estate. Seal gate passed
(SEAL OK, exit 0) immediately before this answer phase; spine shape verified
(1,221,058 rows / 402,114,160 bytes). GROUND_TRUTH_HELDOUT.md was NOT opened by
the answer seat.

## Disclosure (honesty over volume)

One search grep ("dumb floor", estate-wide) printed two excerpt lines from
GROUND_TRUTH_HELDOUT.md (its Q3 block) into the answer seat's terminal BEFORE the
answers below were written. The Q3 answer was then decoded independently from the
source file mag/session_state_brief.py, but the leak means the Q3 row cannot count
as uncontaminated evidence at scoring. No other ground-truth content was surfaced
(all later searches excluded the method_card_exp directory). Filed here per law 10
instead of silently patched.

## Answers (one row per question: fact + proving path/number)

- Q1. The AMD window guard keeps the Windows scheduled tasks **StartCN** and
  **StartDVR** disabled; they respawn **AMDRSServ.exe** (AMD Radeon Software) via
  `cmd.exe /C`, which caused the recurring desktop flash windows
  (mag/amd_window_guard.py:4-6, TASKS = ("StartCN", "StartDVR") at :32).

- Q2. The estate smith chart's handoffs organ pre-states the bar **>10 pending
  peer handoffs = "queue rot"**; exceeding it flips the organ to REFLECTING
  (gamma = min(1, n/10)), i.e. the pending handoff queue is rotting and needs
  drains, not new work (tools/estate_smith_chart.py:177-185).

- Q3. The live session-state brief writes to **memory/briefs/latest.md**
  (mag/session_state_brief.py:39-40, write_brief :350); the dumb floor rule is
  that **meters older than 24 hours read RED no matter what the meters say**
  (mag/session_state_brief.py:69; m["floor"] = "RED (meters stale >24h)" if
  age_h > 24.0 at :120).

- Q4. The wakers intake manifest (corpus/library/wakers_20260906/MANIFEST.md)
  states the law of this pull at its top (lines 5-6): **"honesty over volume. PD
  texts are training-eligible; openly-released scholarly texts are RAG/citation-use
  pending license-read; in-copyright is borrow-only; piracy doors are rejected
  outright."** The clean tier pulled **50 files** (4 top-level + 46 Nag Hammadi
  texts) (MANIFEST.md:9).

- Q5. The estate's constitution pointer (CONSTITUTION.md, repo root) names
  **../mycelial-republic/docs/CONSTITUTION.md** as the binding constitution
  (CONSTITUTION.md:3-5); the data tiers that may never be sent to free remote
  train-on-input APIs are **T0 and T1** (CONSTITUTION.md:10, "Data tiers T0-T3
  (T0/T1 never to free remote train-on-input APIs)").

- Q6. Law 15's daily pacing ceiling for the Lite key (z_ai3) is **~1,400 credits
  per day** (DEFAULT_CEILING = 1400, "law 15: 10,000/wk pool paced over 7 days",
  mag/lite_guard.py:10-11, :35); the environment variable **LITE_DAILY_CREDITS=0**
  disables the ceiling, operator emergency only (mag/lite_guard.py:17, :80).

- Q7. The operator's hand-carry door shelf_pdf shelves a bought PDF into
  **memory/corpus/ractors/<shelf>/texts/** (mag/shelf_pdf.py:27 CORPUS, :33
  tdir = sdir / "texts") and updates the shelf's **MANIFEST.json**
  (mag/shelf_pdf.py:52, stored_pd provenance rows).

- Q8. Salon ruling 09-06 (salon v1.1, 3/3 unanimous, recorded at
  mag/rotation_harness.py:30-32): **agreement in the rotation harness must be
  measured on the PARTITION via the Adjusted Rand Index (ARI), not by comparing
  cluster counts**; the fixed reference cluster count was replaced by the
  **calibrated interval [6, 8]** (COUNT_INTERVAL = (6, 8) at
  mag/rotation_harness.py:45; ruling text watch/ROTATION_TOLERANCE_RULING_20260905.md,
  consensus points 1-5).

- Q9. The 06:5x ruling **parks the z_ai2 (Pro) key in the swarm worker: reserve
  only, never the default again without a fresh ruling**
  (mag/swarm_worker.py:59-60); the swarm worker's default provider is instead
  **cerebras** (DEFAULT_PROVIDER = "cerebras", Lite unhooked from the default,
  mag/swarm_worker.py:54-56).

- Q10. In the quorum window, the quorum denominator per the ponytail ruling is
  **the chairs that returned a parseable P1, never the manifest**
  (mag/quorum_window.py:11, restated :175), and an ADDITION passes with
  **>= 2/3 YES** of that denominator plus every objection logged in the dissent
  log (mag/quorum_window.py:176).

- Q11. In the max_distill RAR math the denominator of the Recoverable Advantage
  Ratio is **the C-A gap: vstr(C_max) - vstr(A_high)** (denominator = c - a,
  mag/max_distill.py:215; denom = gaps["C_max"], mag/max_distill_arms.py:275),
  and RAR is refused outright below **MIN_DENOMINATOR = 2** verified events
  (mag/max_distill_arms.py:155, GAP_TOO_SMALL verdict :276-278).

- Q12. The MAG kill switch (mag_kill.cmd) invokes
  **`.venv\Scripts\python.exe main.py power stop --json`** (mag_kill.cmd:21),
  and afterwards **start_everything.cmd or mag_on.cmd** must be run before
  anything respawns (mag_kill.cmd:17, "No respawn until you run
  start_everything.cmd or mag_on.cmd").

## Answer-seat verification notes

- Every cited path was read under the sealed spine this session; cited line
  numbers were read with grep -n / sed -n against the live files, not recalled.
- Raw decode evidence: watch/inbox/gala_20260925/afterparty/lanes/t53.check.txt
