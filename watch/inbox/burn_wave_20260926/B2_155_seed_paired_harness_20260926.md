# B2-155 receipt (2026-09-26)

## Verdict

LANDED. The seed-paired uplift harness with the TARA gate exists and is testable: tools/seed_paired_uplift.py implements law D verbatim (paired means, k = min(5, n) fixed folds, per-fold re-pick between candidate and seed, held-out sum, auto-revert on refuse), and tests/test_seed_pinned_uplift.py (6 pins) plus the built-in replay prove the gate refuses what the single-delta gate would adopt. Amendment D is no longer spec-only; B2-58's F2 "untestable until a paired scorer exists" is cured. The F2 comparison metric is implemented: on the replay set the gate scores 0.0 mean seed regressions vs flag-only's 3.0, so the auto-revert clause is NOT vacuous.

## Evidence file:line quotes

- roblox/prompts/README.md law D (B2-200 upgrade, lines 96-118): "Adopt a candidate iff its seed-paired score beats the seed's AND the gain holds across folds ... split the seed set into k = min(5, n_seeds) fixed folds; re-pick the best candidate on all folds but one; score that pick on the held-out fold; sum across folds) and adopt only if the held-out sum beats the seed's."
- tools/seed_paired_uplift.py _folds: k clamped internally to min(FOLDS, n), fixed `random.Random(0).shuffle`, no empty folds (mirrors B2_59_dspy_reanchor_calibrate.py:50,214-221).
- tools/seed_paired_uplift.py gate loop: per candidate, per fold, "if _total(cscores, train) > _total(seed_scores, train): pick this candidate, add its held-out delta; else pick the seed, add 0" with the comment naming the B2-155 replay fix (a shared cross-candidate best-pick let a confined candidate hitchhike on another candidate's held-out gains, which would adopt exactly the shape law D refuses).
- Replay output (this lane, `--demo`, n=12): single_fold_gain aggregate_delta +3.0, heldout_delta_sum 0.0, REVERT, standing p0; two_fold_gain +3.0 / +3.0 ADOPT; broad_gain +0.96 / +0.96 ADOPT; pure_regressor -1.2 REVERT. f2_compare: flag_only_mean_seed_regressions 3.0 vs gate 0.0, gate_beats_flag_only true.
- tests/test_seed_paired_uplift.py: 6 pins, 6 passed (folds deterministic + cover + small-set clamp; single-fold refusal; two-fold adoption; broad adopt / regressor refuse; tie never adopts; gate beats flag-only).

## Work done

1. Read B2-58 F2, the README law D text as B2-200 upgraded it, and the B2-200 replay; confirmed no paired scorer exists anywhere in the repo (the F2-named B2-151 harness never landed; today's B2-151 row is an unrelated renumbered brief).
2. Built tools/seed_paired_uplift.py: gate() (law-D executor), flag_only_compare() (the F2 regression-rate metric), --scores JSON input for real eval runs and --demo replay needing no network; arithmetic only, it never generates (law C keeps generation cost zero).
3. Found and fixed two of my own defects via the replay before landing: a syntax slip in the pick loop, and the real mechanism bug (cross-candidate hitchhiking) which the first demo run exposed when a single-fold confined candidate was ADOPTED; the gate is now strictly per-candidate accept-or-revert against the seed, matching TARA's "adopts the repair iff s(x_hat)>s(x0) and otherwise reverts".
4. Tuned the demo to the true refusal shape (gain confined to exactly one fold of the fixed partition, computed from _folds itself) after observing that a gain spread over two folds legitimately recurs and must adopt; both shapes are now pinned.
5. Added the 6-pin test file; all pass. Ratchet check --changed over the touched files: NEW=0, PASS.

## Falsifier

The brief's falsifier (F2 restated): if the gate does not beat flag-only adoption on seed-paired regression rate, the auto-revert clause is vacuous. Pinned inverse: test_gate_beats_flag_only_on_seed_paired_regressions fails if a refactor makes the gate adopt the pure regressor or the single-fold candidate, since gate regressions would rise above 0 while flag-only stays 3.0. test_single_fold_confined_gain_is_refused fails if anyone reintroduces aggregate-only adoption (the pre-B2-200 law D). test_folds_deterministic_and_cover_all fails if the partition becomes run-dependent (a seed-paired gate with drifting folds is not re-runnable). Standing gap, honest: the harness consumes recorded per-seed scores; wiring it to a live judge loop over real prompt candidates is the next lane's generation run, not this file's job.

## Bibliography closed

- roblox/prompts/README.md (law D as upgraded by B2-200; amendments C/D context)
- watch/inbox/burn_wave_20260926/B2_58_prompt_amendments_20260926.md (F2 pre-registration)
- watch/inbox/burn_wave_20260926/B2_200_lawD_fold_check_20260926.md (fold-check upgrade + replay)
- watch/inbox/burn_wave_20260926/B2_59_dspy_reanchor_calibrate.py (vendored canon, lines 50, 214-252)
- tools/seed_paired_uplift.py (new, 190 lines region); tests/test_seed_paired_uplift.py (new, 6 pins)
- QUEUE.md row B2-155 (line 419/430 at lane time)
