# WEEKEND BURN BOARD — 09-05 (from salon self_steal_moonshot_20260905)

Operator order: MORE CODE LESS PROSE · burn the free pool on hard builder work · Max reserved
for important/unblocking · long horizon. Source: memory/runs/salons/self_steal_moonshot_20260905/
(five seats argued, fold ranked by impact/effort with falsifiers). Pool cap law: ≤3 free windows
churn; 4th+ auto-launches on Max. Free pool opens 11:00 EDT today, Sep 3-20.

## B1 — ECONOMIST refeed-guard · 2h · FREE WINDOW 1 · gates Sep 8 Lite re-arm
The burn audit proved ~50% of the Lite pool died as re-feed tax (context re-sent on worker
restarts). Build `mag/refeed_guard.py`:
- Measure: per lane per day, refeed_ratio = tokens_in_restarted_contexts / total_tokens.
  Real sources: `~/.zcode/cli/db/db.sqlite` model_usage + turn_usage (status='completed',
  started_at ms-epoch) + fuel_feed lane logs in state/fuel/.
- Act: ratio > 15% for 2 consecutive days → CLAMP the lane (same clamp shape as the live
  1,228/day meter clamp) + one CONVO row. Wire into lite_guard tripwire.
- Falsifier: refeed >15% persists 2 days WITH the guard live → guard is vapor, delete it.

## B2 — LESSIG law-compiler · 6h · FREE WINDOW 2 · kills the death classes in code
25 prose-tier laws = uncompiled law. Build `mag/law_compiler.py`: parse the law lattice
JSON → executable guard registry (`@law.guard("L-xxx")` decorators + a `check_all()` binary
the night shift runs as step 0.5). First six compilations are the measured death classes:
window-source-lite (kill), 5.3-full-tick<600s (clamp), MSYS_NO_PATHCONV-missing (kill),
send-unconfirmed (retry), guest-deep-think (alert), 4th-free-window (redirect-max — the
operator's 09-05 ruling as compiled law). Resolution from the fold: law-guards run on FREE
lanes; paid Max only for the proof demo.
- Falsifier: no compiled law fires for real within 7 days → the lattice is decoration.

## B3 — BARD unblock-meter · 3h · FREE WINDOW 3 · receipts/day becomes the KPI
Build `mag/unblock_meter.py` + `state/unblock_events.jsonl` (append-only, chain-adjacent):
every stuck→unblocked transition gets one row {ts, worker, blocker_class, time_s, fix_ref}.
Blocker classes already named by the crash record: window-death, hung-call, path-mangle,
429-box, send-unconfirmed, wall-challenge. Night shift step 0.5 reads it; receipts/day =
unblocks+cards+seals, printed in every morning brief. No new sqlite tables — jsonl only.
- Falsifier: 0 unblock rows for 48h while a process is verifiably stuck → meter is blind.

## B4 — ELDER corpus-distiller · 9h · LONG HORIZON (Rocinante feed, post-B1/B3 or quiet window)

DOCTRINE MANDATE (operator, 09-05, as the 300M pool burned to zero): "it's all training data.
We're learning for free." The distiller harvests WHOLE TRAILS — this weekend's session
transcripts, tri-state cards, salon arguments, and crash-and-fix loops (captcha wall, MSYS
mangle, send-confirm) join the 9,305-part thought-bank as the seed corpus. Every burn arc ends
with a harvest step, not just a receipt.
The thought-bank exists (9,305 reasoning parts / 17.3M chars, db part type=reasoning).
Build `mag/corpus_distiller.py`: join reasoning parts → their sessions → build/verification
outcomes (passed builds only per the seat's thesis), emit QLoRA-format JSONL
(prompt=composer state, completion=thinking+answer, meta=lane/model/score) into
corpus/ft/. Extends the existing banked store — never re-harvests.
- Falsifier: QLoRA fine-tune doesn't beat base on the R-1 bench by Oct 27 → corpus is
  noise, the distiller dies by its own kill-switch.

## B5 — PONYTAIL Invariant Workbench · 8h · NEXT FREE SLOT (after B1-B3, cap law applies)
Unify the paste-checkers behind one `check(text, paste_type)` dispatch: CyberChef recipe
chains, OEIS detector mode, godbolt permalink receipts, witness rendering (steal pass:
watch/STEAL_PASTE_FALSIFIERS_20260904.md). Public-turn demo candidate. Ship as
/static/workbench.html + mag/workbench.py.
- Falsifier: <10 pastes/day after ship → nice-to-have confirmed, kill or shrink.

## Sequence
11:00 pool open → B1+B2+B3 fire as the three free windows → B5 takes the next freed slot →
B4 docked for long horizon. Sep 8: Lite re-arms THROUGH B1's guard, not before. Sep 20:
receipts/day curve is the proof artifact.

## T-SECTION — TRAJECTORY RIB (salon trajectory_rib_20260905, 7/7 shapes, 09-05 ~10:0x)
Operator order: incorporate the z.ai Trajectory window into our rib structures, adapt the
harvested thinking, extract from every seat — "should change the way we interact with z.ai
entirely." Sample preserved: corpus/training_materials/zai_trajectory_window_sample_20260905.txt
(sha256 efd424dd...858d517). Salon artifact: memory/runs/salons/trajectory_rib_20260905/.

**T1 — TrajectoryStep schema + rejoiner proof · FREE WINDOW (next builder slot)**
`mag/trajectory.py`: TrajectoryStep record (step_hash, channel ∈ {input, tool_result, output,
reasoning, system}, tool, timing_ms, schema_version:int, signature w/ version check) — LESSIG
frozen schema + PONYTAIL rejoiner SQL upgraded per the fold: schema_version field MANDATORY
(collision #2), sequence→step mapping validated not assumed (collision #3). PROOF LEG: run the
rejoiner on a 100-row subset of the 9,305-part thought-bank; zero data loss = Supported.
Falsifier: any joined chain missing a channel or reordering under replay.

**T2 — UniversalExtractor · after T1**
`mag/trajectory_extract.py`: per-door adapters (local db door + z.ai surface export door), with
BLOCKED/UNVERIFIED state flags (ELDER's artifact was truncated in-salon — the fold's build #1).
Token counts: vendor does NOT render them (collision #4) — envelope measurement comes from OUR
model_usage table join, not the surface. Falsifier: extractor misses a seat's schema version
without flagging UNVERIFIED.

**Orchestrator tri-state stamps on the fold** (primary sources the salon couldn't see):
the 24-hex step hash = SUPPORTED (preserved sample, e.g. 305501de0d7240dfab0e5d8f);
the 240:1 refeed tax = SUPPORTED (meter query 09-05: 122,403,057 in / 511,253 out on the free
plan). ELDER truncation = real, re-fire that seat's brief in T2's builder prompt.
