# w4-13: The Epistemic Gap Sensor: design grounded in tools/drift.py and the percolator invariants

Deep item, 2026-09-28, burn reset flash50. Everything below was read or run in this session. Files read in full: `tools/drift.py` (101 lines), `mag/percolator.py` (385 lines), `mag/epistemic_guard.py` (165 lines), `tools/drift_pairs_stamp.py` (681 lines). Checks run are named inline with their outputs.

## 1. The gap, stated from evidence rather than metaphor

The estate's "internal model" is not one thing. Reading the code, it is three belief strata, and each drifts from observable reality in a different way, which is why one sensor cannot be a single comparison.

Stratum A is the compiled belief layer: `memory/percolator/invariants.json`, measured live this session at **359 invariants, false_positives counter 13**. These are sentences that repeated often enough to be compiled (`mag/percolator.py:264-289`, recurrence = stable truth). Top of the registry by count: `[steer] Elevate with a deliberate ask...` at 232,214 recurrences, `false-success: claimed edits, wrote nothing` at 18. This layer drifts when reality changes shape and the invariant keeps asserting the old shape.

Stratum B is the measurement layer: the teleological drift pairs T1-T6 (`tools/drift_pairs_stamp.py:377-400`), stamped weekly into `memory/runs/adv_arc_50/teleo_drift_stamps.jsonl`. This layer drifts when its sources die under it.

Stratum C is the reflexive layer: the seals and self-reports (`memory/seals/`, briefs, state docs), which drift when a seat writes a claim no byte backs. The AGENTS.md trust-bytes law and the retired 1,341-test headline are this stratum's known failure mode.

The measured gap events in this session's reading:

- **A corpse stamped healthy, twice.** The W38, W39, and W40 stamps of pair T2 all read `ALIGNED corr=0.8839 deltas=12`, digit-identical across three weeks (ledger tally run this session). Cause verified: both T2 sources, `watch/inbox/mrpool_export/media_register.jsonl` and `ledger.jsonl`, last moved at `2026-09-18T14:27:47+00:00` (range check run this session). The window (`_aligned_window`, `drift_pairs_stamp.py:212-217`) ends at the newest observed date, so a dead source freezes the window and the sensor re-files the same correlation forever. Two of the three T2 ALIGNED stamps are false negatives of exactly the kind the sensor exists to catch.
- **Amnesia, healed 14 times.** `memory/percolator/heal.log` holds 14 auto-heal rows from 2026-09-06 to 2026-09-26, nine of them within eight minutes on 09-06 (the registry-wipe amnesia incident), and several from the `/app/...` Docker path spelling alongside the Windows path, proving both shared-surface contexts loaded and healed the same divergent registry. The GAP-2 comment (`mag/percolator.py:167-175`) records why the old detector was blind: a `>50%-by-count` gate cannot see the loss of ONE sealed generation, so a partially wiped registry loaded as "silently healthy." The fix was a per-generation ID diff against the newest seal.
- **Decoupling as the steady state.** Live tally of the 18 ledger rows: 13 DRIFTING, 5 ALIGNED, zero INVERTED, zero VACUOUS. The estate's motion metrics (lane trails, fold steps, training events) are largely not tracking their filed referents. The gap is not an anomaly here; it is the background condition the sensor must characterize, not merely detect.

## 2. What the sensor compares (the design)

The instrument the ask names, `tools/drift.py`, already contains the core insight and it is worth stating precisely. It does not compare a metric to a referent. It compares **movements**: `_deltas` (first differences, `drift.py:32-33`), then Pearson correlation of the two delta series (`drift.py:36-47`), with the verdict bands ALIGNED >= +0.5, INVERTED <= -0.5, else DRIFTING (`drift.py:77-85`), VACUOUS when the referent never moved (`drift.py:69-72`), INSUFFICIENT under 3 deltas (`drift.py:64-67`), DEGENERATE on zero variance. The module's own law (`drift.py:90-91`): "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers 'is it moving north'." This is Goodhart's law turned into a computable quantity: instead of asserting that a target degenerates when it becomes a metric, it measures whether the metric still points at the thing.

The design proposal is therefore not one sensor but a three-strata stack, because the three strata fail differently:

**Stratum 1, movement coupling (exists):** per pair, corr(dM, dR) over the pair's window (13 to 60 days by pair, `drift_pairs_stamp.py:224,243,264,314,334,359`). Comparing: estate motion (lane trail rows, fold steps, training events) against filed referent motion (LINKS filings, burn receipts, release milestones). Keep as is.

**Stratum 2, referent liveness (half exists, the measured hole):** newest-row date of every referent source versus its cadence. Today only one referent is watched: the B2-208 staleness tripwire (`drift_pairs_stamp.py:603-646`) reads `memory/improve/releases/gates.jsonl` for regime_*/graduation rows and alarms when 14 days pass AND the training metric still grows. T2 proved unwatched referents die silently. The extension is mechanical: a table of (source path, last-row date, expected cadence) covering all six pair sources plus the percolator registry, computed from bounded tail reads the way `_last_training_ts` does it (`drift_pairs_stamp.py:571-600`, reads a 2 MB tail rather than the 241 MB file). The tripwire's own live reading this session (`tools/drift_pairs_stamp.py --status`): gates fresh at 3 days, `alarm: false`.

**Stratum 3, claim resampling (missing entirely):** the 359 invariants are beliefs with no re-verification loop. The design: a rotating audit that draws a bounded sample (20 per week, oldest-last_seen first) and re-tests each compiled operational claim against the live tree, the way the estate already ad-hoc verifies (the c2e38d6c9 oral-02 receipt counted 60/63 cited modules existing; the s2-13 receipt fact-checked DNA.md 21 verified / 8 partial / 2 contradicted). Verdicts write back as annotations, never mutating the invariant text: a compiled belief that fails resampling twice gets flagged DRIFTED in a sidecar ledger, and the flag itself is fed to `false_positive()` (`percolator.py:252-261`) so the calibration counter learns. What cannot be mechanically resampled (steer advice, social claims) is marked UNTESTABLE and excluded from the rate, so the sensor's denominators stay honest.

## 3. Cadence

Three clocks, each matched to its failure rate:

- **Weekly, idempotent:** the existing stamp contract (`drift_pairs_stamp.py:45-49`: one stamp per ISO week per pair, safe to fire daily because it writes at most once weekly). W38, W39, W40 stamped per the `--status` run.
- **Daily liveness tails:** the B2-465 scheduled-task pattern already proven in this repo (MagFtsIndexDaily). Tail reads are milliseconds; a dead referent is known within one day instead of surfacing at the next weekly stamp.
- **Per-call, $0:** the percolator runs on every ingested text with no LLM (`percolator.py:8-24`), so its calibration is continuous at zero marginal cost.

Any new wiring that spawns subprocesses on win32 carries `creationflags=CREATE_NO_WINDOW` per the ghost-modules law (the c2e38d6c9 receipt's spawn-sites correction).

## 4. What triggers an alarm

The existing trigger set, with this session's live state:

1. **INVERTED (corr <= -0.5):** the hard alarm in `drift.py:17,80-82`. Fired 0 times in 18 ledger rows. This is the "stop trusting the metric" verdict.
2. **Dashboard breach (B2-225):** DRIFTING streak >= 14 days OR referent age >= 30 days (`tools/drift_dashboard.py:326-334`), producing `watch/inbox/DRIFT_ALARM_<date>.md` and exit 2, explicitly a proposal surface that never mutates the ledger (`drift_dashboard.py:337-358`), honoring the model-text-proposes/switchboard-authorizes boundary. Computed live this session via `build_table` + `alarm_breaches` (no write): **0 breaches**; nearest is T1 at streak 10 days DRIFTING, T3 also 10 days but with a 0-day referent (alive).
3. **Staleness conjunction (B2-208):** referent silent >= 14 days AND metric still growing (`drift_pairs_stamp.py:634-638`). The conjunction is deliberate false-positive suppression: the stale-but-also-dead branch files NO alarm because "no growth to measure against a dead referent" (`drift_pairs_stamp.py:639-643`). Live: `alarm: false`, fresh.
4. **Seal diff (GAP-2):** any sealed generation missing from the live registry triggers auto-heal (`percolator.py:173-198`). This is the one trigger that acts rather than proposes, and its 14-fire history includes a same-hour nine-fire burst, which argues for a heal-rate alarm on top: more than N heals per day means two surfaces are diverging, not that one wipe happened.
5. **Proposed, from the T2 measurement:** a frozen-window tripwire. If a pair's `window.end` fails to advance between consecutive stamps, the stamp is VACUOUS-STALE, not ALIGNED. T2 would have been caught at W39 instead of being stamped healthy twice. This is strictly cheaper than correlation: compare one date to the previous row's.

## 5. False-positive rate, with denominators named

The census-denominator law (B2-216) applies to sensor claims too: name the instrument and the moment.

**Percolator as signal sensor, measured:** `rg -c '"pattern_tags": \["percolator"\]' memory/training/events.jsonl` returns **190,060** percolator-tagged training events; `rg -c '"false_positive": true'` returns **15** rows, and the three sampled (lines 95914, 95945, 393979) are all percolator `no_signal` FPs. In-feed FP rate: **15 / 190,060 = 0.0079%**. But the registry counter says 13, not 15: two instruments of the same quantity disagree by 2. The max-merge in the heal path (`percolator.py:189-190`, `max(seal, live)`) can drop a surface's count when the other surface is higher, and Docker-side FPs before a merge are invisible. The divergence is small and unreconciled; I did not verify a 1:1 mapping between the 15 feed rows and registry increments, and say so.

**Drift stamp sensor, measured:** 15 v2 stamps, 0 INVERTED, 0 aging-guard downgrades, 0 dashboard breaches. The measured FP rate is effectively 0/15 on the alarm paths. The measured FN rate on referent death is the damning number: 2/2 unwatched dead referents (T2 at W39 and W40) stamped ALIGNED. The sensor is currently biased toward silence, and the structural reason is visible in the code: every alarm requires a conjunction (staleness AND growth), a threshold (14 or 30 days), or a correlation band (0.5), and none of them watch source liveness for five of the six pairs. The fix is the Stratum-2 liveness table, not tighter thresholds: tightening corr bands on 20-delta windows would manufacture FPs, because a Pearson r on ~20 daily-count deltas has a wide confidence interval; T1's W38 corr 0.4118 versus W39 corr -0.0271 shows how far the same pair moves week to week near the boundary.

**Structural suppressors already in the code** (these are why the FP rate is low and why FN bias is the live risk): the INSUFFICIENT gate refuses verdicts under 3 deltas (`drift.py:64-67`); the aging guard downgrades ALIGNED to FRAGILE-ALIGNED rather than alarming when the referent has under 7 days of life (`drift_pairs_stamp.py:418-441`, threshold `REFERENT_MATURE_DAYS = 7` at line 147); FRAGILE-ALIGNED is rendered amber-green as ALIGNED-provisional, never as unknown (`drift.py:19-25`, `drift_dashboard.py:203-207`). One honesty note from the ledger: the guard has **0 live firings** (all v2 rows `downgraded=False`; the W39 rows predate the fields with `referent_age_days: None`, and history is append-only with no backfill, `drift_pairs_stamp.py:82-87`). Its named boundary case (W39 T6, age 2) is covered by unit tests, which pass this session (`pytest tests/test_drift_pairs_stamp.py tests/test_drift_dashboard.py -q` → **25 passed**), but the guard has never yet caught a real young ALIGNED in the wild. Confirmed tested, not yet confirmed fielded.

## 6. Two meta-gaps the sensor should also watch (found, not designed in)

- **Two definitions of "age" live side by side.** The stamp's `referent_age_days` is birth-based (T2 = 1246 days, from first row); the dashboard's `ref_age` is recency-based (T2 = 11 days, from newest row, `_ref_age_days` parsing "11d" at `drift_dashboard.py:316-323`). Same word, different referents, a 100x difference on the same pair. The B2-218 vocabulary sweep fixed this class of drift for verdicts; the age fields need the same treatment or one of the two alarms (streak vs referent-age) can be argued about with the wrong number.
- **The sensor's own sources are shared-surface files.** The heal.log's `/app/` rows mean a second context writes the same registry the Windows context heals. Any liveness table built on mtimes must pin which surface's clock it reads, or a Docker write and a Windows read will manufacture a staleness alarm (the time equivalent of the 09-06 double-heal).

## 7. Anchors in the literature (named as analogies, verified only as far as the code)

- **Goodhart/Campbell:** the drift law at `drift.py:90-91` is the operational form: do not legislate against proxies, measure their correlation with the referent.
- **Ashby's requisite variety:** the sensor distinguishes 7 verdict states (drift.py docstring) but, before the proposed fix, only 1 referent-liveness state (gates.jsonl). A regulator must have at least as many distinguishable states as the disturbances it must counter; T2's corpse is the missing variety showing up as a blind spot.
- **Calibration practice:** the percolator's FP ledger ("logged, never carried forward as truth", `percolator.py:23-24`) is Brier-style scoring in miniature; Stratum 3's resample feeds the same habit.
- **State-divergence detection:** the GAP-2 per-generation seal diff (`percolator.py:167-175`) is the same shape as a merkle-membership check against a checkpoint, which is presumably why the estate calls the seals verkle; the count gate it replaced is the classic anti-pattern of summarizing a set by its size.

## 8. One-sentence design

A weekly corr(dM, dR) stamp (exists, keep), a daily liveness tail over every pair source plus the invariant registry (extends B2-208; would have caught T2 ten days early), a rotating bounded resample of compiled invariants against live bytes (new; closes the loop on the 359), alarms only on INVERTED, 14-day DRIFTING streak, 30-day referent age, frozen stamp windows, or seal-diff heals, all firing as proposal-surface inbox rows with exit 2 and never as state mutations, with FP calibration counted in the same ledgers the percolator already keeps.

## Receipts

Commands run this session: `tools/drift_pairs_stamp.py --status` (18 rows, W38-W40, tripwire fresh); ledger verdict tally (13 DRIFTING / 5 ALIGNED, T2 corr 0.8839 x3); invariants.json load (359 invariants, 13 FP counter); heal.log cat (14 rows); rg counts on memory/training/events.jsonl (190,060 / 15, 3 rows sampled); live `build_table`+`alarm_breaches` (0 breaches, T1 streak 10d); MrPool date ranges (both last 2026-09-18); `pytest tests/test_drift_pairs_stamp.py tests/test_drift_dashboard.py -q` (25 passed). Files read in full: tools/drift.py, tools/drift_pairs_stamp.py, mag/percolator.py, mag/epistemic_guard.py; drift_dashboard.py read in part (lines 316-375 + symbol scan). Not run: the weekly stamp itself (W40 already stamped; avoiding a ledger write from an analysis item), and no bootstrap CI on the corr bands (proposed, not computed).
