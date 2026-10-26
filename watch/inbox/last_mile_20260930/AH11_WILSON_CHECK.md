# AH11 Wilson-bound G3-flooding adjudication (2026-09-30)

Mission (operator): extract deepseek's sharpest v1mf find from the duel
ledger, read the current BASELINE_SPEC.md including AD4's AMENDMENT 6,
adjudicate whether A6 closes it, draft AMENDMENT 7 if not (apply only if
a one-line spec clause), name the verifier math. Lane: last_mile_20260930.

## 1. The flaw, extracted from the v1mf deepseek rows

Source: `watch/inbox/last_mile_20260930/v1_contenders_20260930.jsonl`
keys ds#r1 / ds#r2 / ds#r3 (banked answers behind the 18 v1mf-* rows in
`logs/duel/duels.jsonl`; the receipt V1_MULTIFAMILY_DUEL.md names
deepseek-v4.1-flash's Wilson find as its sharpest).

ds#r1, section 3.1 KILL, the core: "lb95: Wilson 95% lower bound on the
weighted pass-rate" while "sample_size counts raw verdicts". Fixture:
1 G0 FAIL + 100 G3 passes. Weighted passes = 25, weighted fails = 1,
p_hat = 25/26 = 0.9615. Spec feeds the Wilson formula n = 101 (raw):
lb95 about 0.904, clears 0.85. Honest weighted evidence mass
n_eff = 1 + 100*0.25 = 26: lb95 about 0.811, correctly fails. "The spec
uses raw sample_size in the Wilson formula, so G3 flooding can qualify a
cell despite a deterministic G0 fail. The G3 cap only requires one
non-G3 verdict, not one non-G3 pass, and does not cap G3 weight share."

ds#r2 confirms the cap half: "The hard rule blocks only the all-G3 case,
not G3 domination." ds#r3, run against the spec WITH AMENDMENT 6 already
in it, confirms the flaw survives A6 and adds the deeper point: a Wilson
formula over weighted non-integer counts is not a valid exact interval
anyway (its missing-predicate 3 proposes a bootstrap cross-check).

## 2. Current spec state read

`watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md`, batch AD4
(2026-09-30) present: AMENDMENT 5 (n_min retired, m = 50 single
boundary), AMENDMENT 6 (eight per-class raw counters in the DDL; atomic
closed-form recomputation; cap as 4.1 rule 4 n_non_g3 >= 1).

## 3. Adjudication: MISSES ENTIRELY (statistical content untouched)

AMENDMENT 6 fixed the kill it names: the schema/enforcement gap
(denormalized JSON mix, unspecified first-G3 behavior, non-atomic flip).
It did NOT touch the Wilson denominator. Its own text preserves the
flaw verbatim: part 2 says "sample_size = sum of raw counts over
classes" and "pass_rate_lb95 by the section 2 Wilson formula on the
weighted counts (v1 convention unchanged)"; part 3 restates the cap as
"a composition gate on qualification, not a claim about the eff_lb95
arithmetic", which concedes the arithmetic is ungoverned. The flooding
cell qualifies byte-for-byte under the amended spec: n = 101 >= m = 50
(rule 2 boundary, raw), lb95 = 0.9041 >= 0.85 (rule 2 bound, raw n),
n_non_g3 = 1 >= 1 (rule 4): a cell holding a deterministic G0 FAIL has
routing authority. Credit where due: A6's eight counters make n_eff =
passes + fails available at routing time with zero new state, so A6
built the substrate for the repair without applying it.

## 4. Verifier math (item 5)

Wilson lb95(p_hat, n) is monotone increasing in n at fixed p_hat
(half-width shrinks as 1/sqrt(n); verified numerically: 0.8713 / 0.9286
/ 0.9634 / 0.9905 at n = 26 / 50 / 101 / 400 for p_hat = 0.9615). A G3
verdict adds 1 to n_raw but 0.25 to evidence mass, so each G3 pass
tightens the interval toward p_hat without adding proportional
evidence; the bound converges to the weighted rate on the strength of
raw volume. Since all weights <= 1, n_eff <= n_raw always, hence
lb95(p_hat, n_eff) <= lb95(p_hat, n_raw): the honest bound can only
demote. The rule 4 cap is orthogonal to this arithmetic (it counts raw
non-G3 verdicts, not weight), so it cannot see flooding: the single G0
fail satisfies the cap AND seeds p_hat just below 1 (25/26), after
which G3 volume alone carries the bound over threshold. Numbers
(via .venv/Scripts/python.exe, this lane's run):

- Case A, 1 G0 fail + 100 G3 passes: spec lb95(n_raw=101) = 0.9041
  (qualifies); honest lb95(n_eff=26) = 0.8111 (fails). Delta 0.0930 is
  entirely manufactured by the denominator.
- Case B, 1 G0 pass + 999 G3 passes: 0.9962 vs 0.9849, both qualify:
  the pure weight-share variant (no failure evidence) survives any
  denominator; that is the cap-strength residual, a different flaw
  (deepseek's share-cap predicate), NOT the Wilson flaw.
- Invariance: pure-G0 cells have every weight 1.0, so n_eff = n_raw
  and their bounds are byte-identical under the fix.
- Boundary interaction with AMENDMENT 5: 1 G0 pass + 49 G3 passes has
  raw n = 50 >= m but lb95(n_eff = 13.25) = 0.7752 < 0.85: correctly
  blocked on the bound conjunct even with rule 2's boundary still
  reading raw n.

## 5. AMENDMENT 7

Landed (the operative fix is one clause, satisfying the mission's
apply-only-if-one-line condition; appended to BASELINE_SPEC.md as batch
AH11, append-only per the file's own amendment law): the Wilson
denominator everywhere (pass_rate_lb95, therefore eff_lb95) is
n_eff = passes + fails, the weighted evidence mass AMENDMENT 6's closed
form already maintains; sample_size stays a raw audit column and is
never a bound input again.

Drafted but NOT applied (operator's call, each independent):

1. 4.1 rule 2's boundary (n >= m) reading n_eff instead of raw n
   (coherence hardening; the bound conjunct alone already blocks every
   flooding fixture above).
2. Honesty note: a Wilson bound on weighted counts is a conservative
   approximation, not an exact interval; measure the gap with ds#r3's
   bootstrap predicate in the harness (tolerance 0.02 UNPROVEN).
3. G3 weight-share cap (deepseek ds#r1 predicate 2 / ds#r3 predicate 1):
   addresses case B, the residual named above; thresholds (0.5 share,
   n_non_g3 >= 5) UNPROVEN until calibrated.

## 6. Verification (bytes, not reports)

- Wilson arithmetic recomputed independently (section 4 numbers, .venv
  interpreter); matches deepseek's 0.904 / 0.811 claims exactly.
- BASELINE_SPEC.md read in full post-edit; amendment block appended,
  body and batches 2 / AD4 untouched; em-dash count in new text: 0.
- No code touched (ledger.py / router.py are v0, already superseded).
