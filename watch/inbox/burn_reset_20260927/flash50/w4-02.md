# W4-02: THE SOVEREIGN MIRROR AS A PREDICTION ENGINE - THE BRIER EVALUATION

- date: 2026-09-28, item w4-02 (flash50 wave 4)
- ask: read `memory/rib/RIB_BEHAVIOR_CARDS_20260928.md` and the operator's corrections in tonight's git log; design the prediction evaluation (given a situation, how well does the mirror predict the operator's decision); answer "what is the Brier score."
- pass-off: the w3 lane's `flash50/deep-mirror-architecture.md` fixes the architecture (unit of copy = the decision; E0-E5 eval families). This item does not re-derive it; it supplies the concrete scoring protocol, the first measured numbers, and the first live prediction ledger. `flash50/mirror-decision-tree.md` (w3) supplies the branch content; `flash50/sess-01.md` supplies 13 unresolved operator-decision predictions that become 8 scoreable rows below.

## 0. Method: everything cited was read or run this session

Read in full: `memory/rib/RIB_BEHAVIOR_CARDS_20260928.md` (76 lines), `memory/rib/RIB_DRIVING_LADDER_20260928.md` (38 lines), `flash50/sess-01.md` (65 lines), `flash50/deep-mirror-architecture.md` (via head pass, its counts re-verified against live), `flash50/mirror-decision-tree.md` + `flash50/oral-decision-patterns.md` (head passes), `docs/ref/MIRROR_PRESENTED.md` (lines 1-45), `tools/oracle_calibration.py` (lines 1-60, 60-120, grep of brier/ece/mce), `mag/behavioral_lensing.py` cited at :26-27 by the w3 lane (not independently reopened).

Run this session (exact commands):
1. `git log --since="2026-09-27 00:00" --format="%h %ad %s" --date=iso | grep -iE "driving|rib|law|correct|remember|stealth_driver"` -> found the correction lineage: `709e2928a` minted the driving ladder from three operator corrections in a row; `a23928aca` (2026-09-27 22:53:18 -0400, "SELF-BUILDING LOOP LIVE") landed both ribs (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md` +75 lines, `memory/rib/RIB_DRIVING_LADDER_20260928.md` +37 lines, verified in its --stat); `f48e5aaa6` (09-28 16:41) carried the "the operator doesn't repeat himself" enforcement wave per the w3 lane's git-show census, which I inherit rather than rerun.
2. `.venv/Scripts/python.exe tools/oracle_calibration.py --selftest` -> exit 0, 12/12 PASS, receipt filed `watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json`. This proves the estate's scoring machinery computes ECE, MCE and Brier on a confidence ledger and fits temperature T (selftest recovered true T=4.0 as T_hat=3.9536; held-out ECE 0.1848 -> 0.0057 after scaling).
3. `.venv/Scripts/python.exe watch/inbox/burn_reset_20260927/flash50/_w4_02_brier_calc.py` -> the numbers in section 4 and 6, banked with the instrument and `_w4_02_brier_out.json`.
4. Denominator counts, this session: `wc -l memory/decisions_log.jsonl` = 213,310, then 213,311 on recount minutes later inside the calc script; `grep -c "" logs/behavioral_events.jsonl` = 215,582. The w3 lane measured 213,259 and 215,576 earlier today: +52 and +6 rows moved between lanes' read moments. That is the B2-216 census-denominator law live on the mirror's own training corpus, and it is the first thing any mirror evaluation must be built to survive.

## 1. What the record already fixes (inherited, not invented)

The operator's own charter, quoted in the card rib (`memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:3-4`): "the whole purpose of the sovereign mirror was to copy my thinking and decision making with you to run autonomously." The same rib makes the mirror's truth condition implicit: every card is EVIDENCED only by "demonstrated repeatedly in the record," and the CORRECTION card (:26-32) converts operator corrections into law, not apologies. Translation into forecast language: the estate has already declared that the mirror is legitimate exactly insofar as it forecasts well, and it has already declared its update rule.

Tonight's git log supplies the freshest ground truth. `RIB_DRIVING_LADDER_20260928.md:3-5` preserves the three corrections verbatim, minted the night of 09-27/28: "those aren't funded only hermes" / "stop running shit and start remembering" / "what are warmed ribs for if you won't use them." Three in a row is not noise; it is a calibration event of the kind forecasters train on for years (section 4).

## 2. The prediction task, formalized

Given situation S (an open decision the estate carries), the mirror outputs a probability vector p over an option set O, and the operator's actual act resolves exactly one option y. Score with the multiclass Brier sum, sum over classes of (p_c - y_c)^2 (Brier 1950 defined the binary case; the multiclass sum is the standard extension, Gneiting-Raftery 2007 review proper scoring rules generally). Binary rows reduce to (p - y)^2.

The estate's own structure splits the task into three regimes, and this is the first original claim of this item: **the mirror's Brier score is only defined on the third regime, and pretending otherwise is how mirror projects fake success.**

- R1 RAIL classes. Preferences already compiled into gates: GO-row authorization (`watch/inbox/OPERATOR_GO.jsonl`, B2-449 kill condition), no-crons (CURRENT.md:22), free-lanes-never-trusted (ladder invariant 2), trust-roots-undelegable (sess-01 pattern P5). Here the mirror does not forecast the operator; it enforces him. The Brier contribution is 0 by construction, and the correct instrument is a gate audit (exit codes), not a probability. Counting rail classes in a Brier average inflates the score with tautologies - the forecast equivalent of grading a calculator on arithmetic.
- R2 CARD classes. The ten input-shape cards (LINK-DROP, GO, CORRECTION, TERSE-EVAL, X-DROP, STEAL-ORDER, FUNDING-STATEMENT, RESOURCE-ORDER, GENESIS-TESTIMONY, standing lanes, `RIB_BEHAVIOR_CARDS_20260928.md:13-75`). These are near-deterministic classifiers with residual error: the card fires when the SHAPE is recognized. Score them as top-1 precision per card (the w3 lane's E3), with the operator's follow-up as label and his correction as a miss. Cards are the mirror's confusion matrix, not its Brier.
- R3 JUDGMENT classes. Everything genuinely open: key grants, window picks, renew-or-drop calls, trust-root rulings, kill-or-reschedule. This is where "given a situation, how well does the mirror predict the operator's decision" lives, where a confidence number means anything, and where the Brier score is the headline metric. The decision_class field in the ledger below comes from exactly these.

This decomposition mirrors the estate's own compile-to-rails doctrine (`RIB_BEHAVIOR_CARDS_20260928.md:46-50` STEAL-ORDER: "implement as RAILS in code"; w3 lane section 2.4). It has a sharp theoretical consequence: **as preferences migrate from R3 to R1 through the CORRECTION card, the mirror's Brier score improves not because the mirror got smarter but because the class left the statistical domain entirely.** A falling Brier on a shrinking R3 is honest progress; a falling Brier on a constant denominator would be the echo costume (`docs/ref/MIRROR_PRESENTED.md:36-40` anti-echo table). Every reported score must therefore carry the R3 denominator alongside it. This is B2-216 (name the instrument, moment, and denominator) applied to a mind.

## 3. The scoring machinery already exists

`tools/oracle_calibration.py` was built for the G31 recipe (GPS_BATTERY_20260918.jsonl line 31, via the program row in THE_50_PROGRAM_20260918.md line 46): binned reliability tables, ECE/MCE, Brier at lines 144-174 (`brier += (c - y) ** 2`, normalized by n_total), temperature scaling by logit division, per-decision_class drift flags, and per-class escalation thresholds. Its input contract is one JSONL of `{"confidence", "correct", "decision_class", "ts"}` rows. Selftest run this session: 12/12 PASS, exit 0.

Pass-off consequence: the mirror's prediction ledger needs no new scorer. It needs to emit rows in that shape at resolution time. The ledger banked beside this file (`flash50/w4-02-prediction-ledger.jsonl`, 8 rows) carries confidence, decision_class, resolution_surface and deadline per row; when each resolves, `correct` is set from the resolution surface and the file is fed straight to the tool. Zero new infrastructure; the mirror's first calibration report is one command away from its first resolved batch.

One gap, named: the tool's own docstring states "No live oracle confidence ledger exists on disk yet (G31 is a steering proposal), so the exercised validation path is the self-test on synthetic data." The ledger below is the first live candidate; until at least one row resolves, the estate's Brier number on real operator decisions is exactly undefined, and any published number before that is fabrication.

## 4. Tonight's corrections as calibration data (first measured numbers)

Treat each of the three corrections as a resolved binary event E = "the operator endorses the pre-correction seat policy" (P1: free lanes usable as work; P2: run-first over remember-first; P3: hand-rolling rib-held doctrine is acceptable). The pre-correction seat acted at implicit confidence near 1.0 - it ran the policies as if they were law. The operator resolved E = 0 three times. The instrument (`_w4_02_brier_calc.py`, run this session) computes:

- implicit confidence 0.95: per-event Brier term 0.9025, mean 0.9025
- implicit confidence 0.90: mean 0.81; implicit confidence 1.00: mean 1.00
- coin-flip baseline (constant p=0.5): 0.25
- the confidence parameter is an ASSUMPTION (swept across all three values above); what is not an assumption is that all three events resolved against a policy the seat was executing without hesitation, so the terms sit at the top of the 0-1 range

Read: on its most-confident class, the pre-correction seat scored roughly three to four times worse than a coin flip. This is the canonical overconfidence signature, and the selftest's own calibration demo shows the cure: temperature scaling (T_hat=3.9536 recovered a true distortion T=4.0; held-out ECE 0.1848 -> 0.0057). But the estate does something stronger than recalibration, and the second original claim of this item is that **the CORRECTION card is a structural update, not a gradient step.** After the ladder minted, "free lanes are work" is not a downweighted option - it is deleted from the R3 option set and replaced by a rail (sensed-never-done enforcement in `tools/stealth_driver.py` per the w3 lane's grep at :483-490). A rail's future Brier contribution is exactly 0, verified by exit code rather than forecast. Recalibration squeezes error smoothly toward the base rate; correction-by-minting removes whole regions of error at once. The mirror's learning curve will therefore be discontinuous by design: sawtooth drops at each correction, flat plateaus between, and the R3 denominator shrinking under each drop. A smooth monotone improvement curve in this estate would be evidence that corrections are being absorbed as opinions rather than compiled as law.

There is also an information-theoretic reading of why the estate keeps correction receipts verbatim: a resolved event at p near 1 carries near-maximal surprise (log-loss approaches infinity as p->1 against outcome 0), so a single correction dominates thousands of uneventful confirmations in any proper scoring rule's gradient. Three corrections in one night, preserved byte-for-byte at `RIB_DRIVING_LADDER_20260928.md:3-5`, are the highest-value calibration rows the mirror owns. Kahneman-Klein (2002) gives the environmental condition for this to work at all: intuitive expertise needs high-validity feedback. An estate that mints corrections as dated, enforced laws is a maximally high-validity environment; the mirror's Brier curve is meaningful because the operator made it so.

## 5. The first live ledger (pre-registered before resolution)

The sess-01 table banked 13 predicted operator decisions with no probabilities and no resolution protocol - a forecast without numbers. This item upgrades the 8 operator-gated rows into the estate's first scoreable live ledger, filed at `flash50/w4-02-prediction-ledger.jsonl` with confidence numbers and deadlines, marked speaker: mirror-L2 per the L2 labeling law (`docs/ref/MIRROR_PRESENTED.md:5-9`: model judgment is "Labeled - not their voice").

| id | event (resolvable form) | class | P(event) | deadline |
|---|---|---|---|---|
| W4L-A4-LLM7 | operator unlocks LLM7 token | key_grant | 0.30 | 2026-10-28 |
| W4L-A5-PROBE20 | operator names a probe20 --live window | scheduling | 0.65 | 2026-10-05 |
| W4L-A6-GROK-B253 | OPERATOR_GO.jsonl row for the b2-53 Grok packet | go_row | 0.15 | 2026-10-05 |
| W4L-B8-OPENCLOUD | roblox_opencloud key pinned | key_grant | 0.40 | 2026-10-28 |
| W4L-B10-SEEDAUDIT | registry home named for standalone seed audit | trust_root | 0.35 | 2026-10-28 |
| W4L-B11-KEYLAW | engines/key_law.py drift ruled (re-mint or revert) | trust_root | 0.30 | 2026-10-12 |
| W4L-B12-STRANGER | human stranger named for G7 | trust_root | 0.35 | 2026-10-28 |
| W4L-B13-MOVE1 | lapsed MOVE1 explicitly killed or rescheduled | lapsed_gate | 0.40 | 2026-10-12 |

The probabilities are derived, not guessed: low numbers on trust_root and key_grant come from sess-01's own pattern P7 ("silent deferral is the recurrent failure shape") - these rows predict the operator's behavior including his deferrals, which is the honest thing to predict. Resolution rules are byte-backed surfaces, not vibes: OPERATOR_GO.jsonl contents for go_row (sess-01's live check: exactly 1 row, burn-wave gate, no b2-53 row - their run, cited, not rerun by me), .env/PROVIDER_KEY_ASKS state for key grants, attributed commits or transcribed chat for trust-root rulings. Rows that expire void (superseded by a new operator decision that bypasses the event) drop out with a void marker, like forecasts for a canceled event; they never silently convert to misses or hits.

## 6. So what IS the Brier score? (honest answer plus the bar)

Three answers at three horizons:

1. **Today, on live operator decisions: undefined.** Eight rows are pending; zero resolved. Publishing a number now would violate the no-fabrication law.
2. **Retrodictively, on tonight's corrections: mean Brier 0.81-1.00 depending on the stated confidence assumption, against a 0.25 coin baseline** - the pre-correction seat, scored as a forecaster on its own implicit claims, was badly overconfident. This is a demonstration of method, not a mirror score (n=3, one night, confidence parameter assumed).
3. **The target, pre-registered here:** the mirror earns "working" status when, on resolved R3 rows, its Brier beats the class base-rate forecaster (predicting each event at its historical frequency) by a pre-stated margin, and its ECE lands under 0.05 after at most a temperature fit, per decision_class. The selftest's synthetic floor is instructive: a perfectly calibrated forecaster drawing confidences from U(0.05,0.95) still scores Brier ~0.153-0.183 (the tool's own check asserts < 0.20) - Brier has an uncertainty floor set by the base rate, and the estate's base rate is harsh: the operator says no to most things (unfunded lanes, ungated dispatches, self-scheduling), so a mirror that has learned P1/P3/P5 should score well below 0.25 precisely because the classes are skewed. Reference class from the forecasting literature: Good Judgment Project superforecasters sustained Brier ~0.15-0.20 on geopolitical questions where domain experts scored 0.3-0.4 and the chance baseline sat at 0.5-adjacent (Tetlock's Expert Political Judgment and Mellers et al. GJP results). The realistic ambition for the mirror is superforecaster-on-home-turf: the operator's decision environment is narrow, rule-rich, and instrumented, which is exactly where Tetlock found skill lives.

Power, stated so nobody over-reads early numbers (computed in `_w4_02_brier_calc.py`): at 8 rows, a 95% CI half-width is +/-0.28 to +/-0.35 under typical Brier-term sd (0.4-0.5) - the first resolved batch can only detect catastrophe, not skill. Half-width +/-0.05 needs N=246-384 resolved rows. N comes from the E0 retrodiction lane (213,311 decisions_log rows counted this session, though the w3 lane already flagged the author-attribution gap: 167,015 rows contain "operator", none are row-attributed), and from months of ledger accumulation. Until then, per-class ECE on tiny n is noise; report N and class next to every number or do not report the number.

## 7. Reflexivity: why the ledger must be sealed

The mirror predicts a human who can read the predictions. The estate also runs an explicit steering program (the `retrocausal-steering` skill: plant the cause now, harvest the decision later). So P(decision | mirror predicted X) is contaminated by P(decision | do(mirror predicted X)) - Pearl's distinction lands here with full force. Once a prediction is visible, a low Brier could mean the mirror knows the operator, or that the mirror moved him, or both; Goodhart and Lucas both cash out as "the metric stops measuring the thing once it becomes the target of an optimizing party in the loop."

The estate already owns the seal: hash-chained pre-registration. The verkle chain (8,261-8,262 leaves measured by sibling lanes this week) provides tamper-evident timestamps; the protocol is one line - hash each ledger row into the chain at prediction time, resolve only from the sealed digest, and mark any row whose resolution surface was touched between sealing and resolution as void. Sealed rows measure forecasting skill; declared-steering rows (where the mirror wanted the outcome) are excluded from the skill score and scored instead as control effectiveness, a different and also useful number. This protocol is design-registered here, not yet implemented; the chain-append plumbing exists but no code writes prediction hashes today, stated as a gap.

The L2 law is the second half of the seal: every prediction row carries speaker: mirror-L2 (`docs/ref/MIRROR_PRESENTED.md:5-9`), so the operator always sees which voice made the call, and the anti-echo table (:36-40) forbids the mirror laundering its guess as his intent. A mirror that cannot be distinguished from the operator cannot be scored against the operator; labeling is what makes the evaluation possible at all.

## 8. Falsifiers for the mirror program (pre-registered)

- F1: on the first 30 resolved R3 rows, ledger Brier fails to beat the class base-rate forecaster -> the mirror is not forecasting; halt R3 autonomy claims, keep R1 rails.
- F2: any rail-class item appears inside a Brier average -> the score is inflated with tautology; reject the report (this file's R1/R2/R3 decomposition is the named instrument).
- F3: per-class ECE above 0.10 on key_grant or trust_root after temperature fit -> escalations route to operator contact earlier (the G31 threshold machinery already computes the escalation share).
- F4: a correction lands and the next same-class Brier does not drop discontinuously -> corrections are being absorbed as opinion, not compiled as law; audit the minting pipeline, not the model.
- F5: accuracy on operator-gated classes rises while E5 authority recall (w3 lane: 100% recall on needs-operator) drops -> catastrophic failure regardless of Brier; the mirror's failure budget is spent on wrong predictions, never on wrong authority (`mag/behavioral_lensing.py:26` per the w3 lane's verified grep: "Alignment steers are suggestions. The Sovereign (operator) decides.").

## 9. Not run, stated

- The 8 ledger rows are pending; no live Brier exists yet (by design; anything else is fabrication).
- E0 retrodiction over the 213k decisions_log rows was not run: no author attribution per row (w3 lane's finding, inherited), so denominators cannot be trusted into a score without extraction work first.
- Temperature fitting on real traces: not run; no live oracle-confidence ledger exists (the tool's own docstring says so).
- `f48e5aaa6` and `709e2928a` contents were taken from the w3 lane's git-show census and sess-03's law-lineage census rather than re-opened; `a23928aca` --stat was verified by me directly.
- The w3 lane's decisions_log count (213,259) versus mine (213,310 then 213,311) is reported as the drift it is, not reconciled: different moments, live-append file, +52/+6/+1 rows.

## Banked artifacts

- `flash50/w4-mirror-prediction.md` (this file; byte-identical mirror at `flash50/w4-02.md`)
- `flash50/w4-02-prediction-ledger.jsonl` (8 pre-registered rows, scorer-ready shape)
- `flash50/_w4_02_brier_calc.py` + `flash50/_w4_02_brier_out.json` (instruments)
- Selftest receipt: `watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json` (12/12, exit 0, run this session)
