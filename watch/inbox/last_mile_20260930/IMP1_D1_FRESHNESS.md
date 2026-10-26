# IMP1 D1: freshness kill amendment landed as AMENDMENT 8 (2026-09-30)

Status: LANDED. Spec-only amendment appended to
watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md (batch
IMP1-D1), no code touched. Lane: IMP1, delta D1 of the AA1 kill list
(watch/inbox/last_mile_20260930/AA1_OPUS_REFIRE.md section 4 kill 1:
"drift invisible inside our own budget - fail verdicts refresh
freshness, collapse needs ~21 fails vs K3's 10-verdict ceiling").
Amendment number 8 was reserved for this lane by the IMP3 batch header
and the operator's D1/D2/D3 allocation; it lands after 9 and 10 because
batches append in landing order (sibling lanes touched the file mid-
draft; re-read before append, zero collision).

## 1. What the amendment does

One mechanism on the 4.1 decay clock, replacing age-since-any-verdict:

- Asymmetry 1: only PASS verdicts refresh the clock (new
  last_pass_utc; last_verdict_utc stays a raw audit column).
- Asymmetry 2: each FAIL advances the clock by fail_age_days DEFAULT
  1.0 (new fail_age_days_accrued, zeroed by any pass). Freshness decays
  on fails at a faster, verdict-driven rate.
- Demote-only clamp: eff_lb95 = min(w * lb95 + (1 - w) * 0.5, lb95).
- THE INVARIANT: a cell whose last k verdicts are all fails is demoted
  by the 8th consecutive fail for ANY lb95 (worst case 1.0), inside
  K3's 10-verdict ceiling with margin 2; fail_age_days floor 0.7204
  days keeps that bound legal under tuning.
- T4 conjunct: staleness requires fail_age_days_accrued = 0, so
  evidence-driven demotion is never mislabeled a knowledge gap.
- AMENDMENT 4 predicate 3 carve-out: passes never lower eff_lb95; a
  fail lowering it IS the designed demotion path.

## 2. Arithmetic verification (repo venv, script below)

Wilson z = 1.96; pure-G0 cell so n_eff = n_raw (AMENDMENT 7); w =
2^(-k * fail_age_days / 14).

```
== kill: 285/300 cell, all-fail streak, v1 w=1 ==
v1 k=20 lb95=0.8517   (still qualifies vs 0.85)
v1 k=21 lb95=0.8486   (first demotion: 21 fails, K3 ceiling breached by 11)
== A8 on the same cell ==
k=3  eff=0.8517  k=4  eff=0.8318   (demotes at 4th fail, matches the
                                     frontier's "4th fail in last 10")
== worst case lb95=1.0 ==
k=7  eff=0.8536   k=8  eff=0.8365   (ANY cell demoted by 8th fail)
== floor: fail_age_days >= 0.7204 for bound <= 10 at lb95=1.0 ==
== one ordinary fail: w=0.9517; post-fail lb95 >= 0.8678 requalifies ==
== healthy 0.92 cell, no pass: k=3 eff=0.8613 survives, k=4 demotes ==
```

The ~21 headline from the AA1 verdict is confirmed byte-exact (21st
fail, 0.8486); the fix's 4th-fail detection on the same cell lands on
Opus's independently derived guard constant.

## 3. Coherence with the sibling amendments

- AMENDMENT 10 (identity): the two new columns attach to the
  four-tuple cell (model_id, model_fingerprint, shape, version); a
  vanished machine accrues wall-clock age on last_pass_utc exactly as
  A10's grouping law expects.
- AMENDMENT 9 (calibration) clause 2: gated-stop fails are ordinary
  fails, so they advance the fail clock (a real fail is a real fail);
  noted in-amendment.
- AMENDMENT 6: the pass/fail clock updates ride the same atomic commit.

## 4. Bytes and laws

- BASELINE_SPEC.md: 50,775 -> 57,508 bytes (+6,733), batch IMP1-D1
  appended after IMP2-D2; body and in-place DDL untouched (AMENDMENT 3
  and 10 part 3 precedent).
- Em-dash count: 0 in the amendment and in this receipt; whole-file
  count re-measured 0 after the append.

## 5. Residuals (named in the amendment, not papered)

One curated pass zeroes k accrued fail-days (lb95 damage persists;
probe_log + F5 clustering bound it); boundary cells transiently demote
on a single fail (fail-closed, one-pass recovery); the K3 promise
covers all-fail streaks only.
