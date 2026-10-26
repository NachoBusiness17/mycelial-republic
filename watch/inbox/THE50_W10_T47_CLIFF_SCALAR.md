# THE 50 · W10 T47 - CLIFF-SCALAR LAW, FORMAL SPEC + INSTRUMENT REGISTRY

Filed 2026-09-19 · finish line per `watch/inbox/THE_50_PROGRAM_20260918.md`
line 72: "47. Cliff-scalar law formal spec + instrument registry [LANE]".

**Gate status, stated first.** The cliff-scalar law is a CANDIDATE law,
unsigned. `watch/inbox/SESSION_CLOSE_20260919.md` lines 41-43 list "the law
signatures (DISTINGUISH, tombstone boundary, cliff-scalar)" under
OPERATOR-GATED items, and `rg -in "cliff" memory/rib_bus/doctrine.json`
returns nothing: the law is not in fleet doctrine. This spec files the
formalism and the registry. It does not sign the law, and nothing here is
fleet-binding until the operator signs it. The registry becomes a checkable
gate on the day of signature, not before.

## 1. The law as filed (verbatim, source of record)

From `watch/inbox/SELF_STEAL_CORPUS_SKILLS_20260918.md` lines 40-46:

> Law text for the gate: EVERY INSTRUMENT MUST NAME ITS CLIFF SCALAR: the
> integral of an extreme (not an average) whose unbounded growth the headline
> metric can mask. An instrument that cannot name its cliff scalar is
> decoration until it does.
> - fluids: integral of ||vorticity||_inf
> - fleet: thrash coefficient per lane; drift corr(dM,dR); ink coastline
>   dimension
> - corpora: countdown density against called-shot dates
> Pairs with I-12 (count against the sky): the cliff scalar is what you count
> against.

The mathematical anchor, as filed at lines 36-38 of the same receipt:
"Beale-Kato-Majda: a smooth flow dies only if the time-integral of PEAK
vorticity diverges. Translation: a system can look completely smooth while an
unwatched integral of an extreme grows silently toward a cliff. Cache-hit rate
is smoothness." (The literature form is the standard Beale-Kato-Majda 1986
blowup criterion, integral of the L-infinity norm of vorticity; the fleet's
operative form is the filed translation above. The literature was not
re-fetched this ask; the filed translation is what the law means here.)

Where the law is already applied on file: the ignorance budget is "the
cliff-scalar law applied to ontology" (`watch/inbox/COGNITIVE_CONTROL_PLANE_20260919.md`
lines 51-52); in the VERB DSL "the cliff-scalar law becomes the while-loop's
alarm clause" (`watch/inbox/VERB_DSL_STEAL_20260918.md:38`); thrash, cliff
scalars and the ink coastline are "orientation checks against the filed
future" (`watch/inbox/TIME_TRAVEL_QSTAR_20260918.md:53-54`); and it is "the
safety rail on all of it" (`watch/inbox/SOVEREIGN_JUDGMENT_STACK_20260919.md:78`).

## 2. Formal definitions

An INSTRUMENT is a standing procedure I that fires on a cadence and emits, at
each observation time t, a HEADLINE statistic h_t computed from observations
X_t. "Standing" means: fires on a schedule, on a corpus landing, or per gate
cycle, and writes a row or reading somewhere durable.

An EXTREME FUNCTIONAL E on observations is a sup-type functional: E(X_t) is
the supremum (or a fixed upper-tail quantile) of a local quantity phi over the
window or ensemble the instrument observes. Means, medians, modes, and shares
are not extreme functionals. The defining property: E dominates every local
sample, and a finite number of local samples cannot bound a growing
frequency-or-magnitude of peaks.

The CLIFF SCALAR of instrument I is

    C_I(t) = integral from 0 to t of E(X_s) ds

taken on I's native cadence (discrete instruments sum: C_I(n) = sum of
E(X_1..X_n) steps). C is monotone nondecreasing by construction when E >= 0;
where the danger is a deficit rather than an excess (stasis, not blowup), E is
the deficit functional E = max(0, floor - measured), and the same integral
form holds. Both directions are registered below; the law's sentence "integral
of an extreme" covers both, because a deficit floor is an extreme claim too:
it names the tail of a repeated-miss distribution, not the average.

A MASK for C_I is a headline metric h such that h can sit in its healthy band
indefinitely while C_I grows without bound. Formally: for every horizon T and
bound M there is a trajectory with h_t in the healthy band for all t <= T
while C_I(T) >= M. Mask-ness is demonstrated by construction (a spike train
that a mean absorbs) or by a measured instance on file.

## 3. The law, formal statement

Instrument I is VALID on its domain only if all four hold:

- L1 NAMED. I's registration declares the triple (E, C_I, h), with E
  sup-type (or declared deficit-type), C_I its integral, and h not equal to E
  up to monotone transform. An h that is a rescaled E is not a mask; the law
  demands a genuinely average-shaped headline.
- L2 MEASURED. C_I is computed on I's own cadence and stored append-only
  next to h's readings (same row or same ledger).
- L3 SKY. The registration declares S_I: either (a) a finite ceiling s-star
  with a tripwire threshold tau strictly below it, or (b) a declared meaning
  for divergence, in which case the tripwire moves to the RATE dC/dt with a
  threshold. The sky is the I-12 pairing ("count against the sky"): every
  integral is counted against a named ceiling or a named meaning, never
  against the ledger's own growth.
- L4 RESPONSE. Breaching tau fires a filed, ordinary-code-or-inbox-row
  response (veto row, lane row, or operator notice). A tripwire with no named
  response is decoration wearing a uniform.

Corollary (the decoration rule, formalized): an instrument with no named
(cliff scalar, sky, response) triple is INVALID regardless of what h reads.
This is the filed sentence "an instrument that cannot name its cliff scalar is
decoration until it does", given a truth condition.

Soundness remark (why an extreme, not an average). For any mean-shaped
functional and any sup-shaped E on the same observations there exist spike
trajectories where the mean's integral stays bounded while E's integral is
arbitrary: place the peaks at growing height or growing frequency inside an
ocean of quiet samples; the average absorbs them, the sup does not. The
converse fails: a bounded sup-integral bounds every peak. So the
integral-of-an-extreme is the only universal blowup certificate available to
an instrument, which is exactly the BKM content translated at
SELF_STEAL lines 36-38. This remark is a construction argument, not a cited
theorem; it needs no citation.

## 4. Registration protocol (how an instrument names its cliff scalar)

Every instrument files one registration row with eight fields:

1. `id` - registry id (R1..R12 below).
2. `instrument` - name + tool/artifact path on disk.
3. `headline` - h, the average-shaped reading the instrument is trusted for.
4. `extreme` - E, what is sup'd (or deficit-floored) over what window.
5. `cliff_scalar` - C, the integrand and the integral, computable from files
   the entry names.
6. `mask` - the failure story: how h stays healthy while C climbs.
7. `sky` - s-star or divergence meaning; `tripwire` - tau + the named
   response. Thresholds filed here are PROPOSALS until the instrument's owner
   fires them; the signature gate owns promotion.
8. `status` + `current_reading` + `reading_source` - bytes on file, with the
   path, never a memory.

Machine-readable twin: `watch/inbox/THE50_W10_T47_CLIFF_SCALAR.registry.json`
(12 entries, same fields, valid JSON, checked this ask).

## 5. THE INSTRUMENT REGISTRY (12 entries, every path read or run this ask)

### R1 TELEO-DRIFT · teleological drift pairs · LIVE

- Tool: `tools/drift.py` (drift_check) + `tools/drift_pairs_stamp.py`
  (weekly, idempotent); ledger
  `memory/runs/adv_arc_50/teleo_drift_stamps.jsonl`.
- Headline: per-pair verdict label on each weekly stamp.
- Extreme: per-stamp decoupling deficit E = max(0, 0.5 - |corr(dM,dR)|) over
  each pair's delta window (0.5 is the ALIGNED floor proposal).
- Cliff scalar: C = sum over stamps of E, per pair. (This is the law's own
  "drift corr(dM,dR)" fleet example.)
- Mask: any rate metric ("is it moving") - lane activity counts look healthy
  while coupling decays. The tool's own filed law line says exactly this:
  "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers
  'is it moving north'" (stamped verdict rows, read this ask).
- Sky/tripwire (proposal): two consecutive stamps of a pair below 0.5 fires a
  lane row demanding re-registration of the pair's referent (the filed-future
  side, per T1-T3 definitions in the tool header).
- Current (read this ask): T1 lane_activity_vs_filed_knowledge corr 0.4118
  DRIFTING; T2 mrpool_video_density_vs_message_density corr 0.8839 ALIGNED;
  T3 anchored_proofs_vs_lane_activity corr -0.1385 DRIFTING. Weeks stamped
  2026-W38; 3 v1 rows + 3 v2 rows (`tools/drift_pairs_stamp.py --status`).
  Under the proposal, T1 and T3 are already one tripwire stamp in.

### R2 THRASH · multi-front thrash meter · LIVE

- Tool: `tools/thrash_meter.py` (6h trajectory window) + lane register
  `memory/runs/adv_arc_50/thrash_register.json` (ADV-I-7).
- Headline: lane trail success share (absence of CYCLE_FAIL rows). The meter
  itself flags this: pre-fix lane-down days "are success-shaped lies in the
  trail" (register note, on file).
- Extreme: per-lane retraction-equivalent events (CYCLE_FAIL, rollback,
  rewrite); C = per-lane thrash coefficient, fails/rows, with the n-squared
  scaling watch. The law's own fleet example ("thrash coefficient per lane").
- Mask: a lane looks productive (rows accumulate) while its rewrite integral
  climbs; also the meter's trajectory-mode reading is itself masked by
  parallelism (below).
- Sky/tripwire: ceilings are already on file in the register's law field:
  "<0.05 shared grounding suffices; >0.3 with n^2 scaling proves private
  channels required". Response on breach (proposal): coordination review row,
  not silent lane split.
- Current (on file, read this ask): fleet max harvest 0.125 (n=16), night
  0.0667, research 0.029 (n=1343) - broadcast-only coordination healthy at
  current scale. Live run this ask, `tools/thrash_meter.py`: score 84
  THRASHING over a 6h window (1,480 events, 261 fronts, 56 sessions) - the
  declared THE 50 parallel burn, which the tool's own filed bias note predicts
  ("parallel sessions interleaving in the shared log raise switch_rate").
  Registered response: during declared parallel burns the trajectory reading
  is interpreted with the session count attached, never muted.

### R3 COUNTDOWN · Pool urgency density · LIVE (analysis-pass cadence)

- Tool: the cadence pass, `watch/inbox/RIDDLE_TRIAD_CADENCE_20260918.md`
  (registration section lines 46-51); term list on file there.
- Headline: post volume, steady 50-207/month - named on file as the metric to
  distrust (line 49: "Mask-metric to distrust: post volume (steady = looks
  healthy)").
- Extreme: monthly urgency-term share peaks; C = integral of countdown density
  above the ~10% baseline band, aligned against called-shot dates. The law's
  own corpora example ("countdown density against called-shot dates").
- Mask: the channel looks alive and prolific while the urgency integral
  ratchets.
- Sky/tripwire (proposal): density is bounded above by 100% (saturation =
  all speech is countdown); tripwires: any month above the prior 64% peak
  (2025-11), or three consecutive months above the 56% band top, fires a
  scoring pass of the flagged posts into the called-shot ledger plus a
  reaction-signature re-run (T23 tool exists).
- Current (on file): elevated band 27-56% over 18 months, peaks 64 (2025-11)
  and 56 (2026-07); Sep-2026 partial month 18%, do not read the dip (caveats
  section on file). Q contrast: urgency never exceeded 10% and decayed to ~0
  before termination.

### R4 Q-URGENCY · Q urgency curve (T22) · CLOSED

- Tool: `scripts/the50_w5_t22_urgency_curve.py`; artifact
  `memory/runs/the50/w5_t22_urgency_curve.json` (4,705 Q-authored rows,
  2017-11 to 2022-11, read this ask).
- Registration is historical: the corpus is dead. The cliff scalar reached its
  terminal state honestly: urgency decayed to ~0 while volume collapsed - the
  curve shows death by silence, not by cliff. Kept in the registry so the
  closed shape stays comparable against R3's climbing shape (the succession
  note, RIDDLE_TRIAD lines 41-44).

### R5 LEDGER-PENDING · called-shot ledger horizons · LIVE (scoring passes)

- Tool/artifact: `watch/inbox/mrpool_export/called_shot_ledger.jsonl` (16/16
  BROKEN), the 107-row unscored caption pool with horizons through 2028-03-01,
  per `watch/inbox/THE50_W8_T38_LEDGER_PUBLIC_SPEC.md` section 1 (read this
  ask); Q ledger 3 claims, BG 0 (`watch/inbox/SESSION_CLOSE_20260919.md:19`).
- Headline: scored-row count and verdict mix - 16/16 BROKEN looks complete.
- Extreme: per-row age of unresolved PENDING/un-scored claims against their
  own horizons; C = sum of horizon-clock ages over the pool.
- Mask: the ledger looks settled while its unresolved pool ages silently.
- Sky/tripwire: each row's own target_date is its local sky (built into the
  artifact); global tripwire (proposal): any row past its horizon left
  unscored > 30 days fires a scoring pass. Publication stays operator-gated
  (T38 section 8); scoring does not.

### R6 MISS-ENTROPY · cache-miss diversity (G13, T28) · FILED, wiring owed

- Tool/artifact: `memory/runs/the50/w6_t28_miss_entropy.json` (read this ask);
  claim on file: "99 percent prefix cache hit rate is necessary but dangerous:
  it proves stability but also proves nothing new is being asked. The health
  metric is not hit rate but the ENTROPY of misses."
- Headline: prefix cache hit rate - the law's own smoothness example
  (SELF_STEAL line 38: "Cache-hit rate is smoothness").
- Extreme: the repeat-tail of the miss distribution; deficit form E =
  max(0, H_max - H_miss(t)); C = stagnation integral of the deficit. Direction
  note: this cliff grows toward STASIS (asking nothing new), the mirror of
  R3's blowup; the law's deficit form covers it.
- Mask: 99% hit rate reads as perfect efficiency while the system stops
  asking anything that would miss.
- Sky/tripwire (proposal): rolling-week deficit budget; breach fires a forced
  novelty pass (new question classes into the queue). Landing site matches the
  standing-drives-stop-on-instrument-conditions law already on file
  (COGNITIVE_CONTROL_PLANE item 5).

### R7 COVERAGE · stego / spectro / vision scan coverage · LIVE (batches)

- Tools: `scripts/the50_t13_stego_detectors.py`,
  `scripts/the50_t08_spectro.py` (390-video corpus per its header), vision
  triage batches; receipts `memory/runs/the50/w2_t08_spectro_receipt.json`,
  `memory/runs/the50/w2_t08_spectro.jsonl`.
- Headline: "scan clean" verdicts on covered sets - the smoothness reading
  ("full stego scan clean", SESSION_CLOSE line 11).
- Extreme: uncovered population share; C = item-days of backlog (integral of
  uncovered count over time).
- Mask: zero findings in the measured subset masks the unmeasured remainder;
  840/2,011 vision-triaged (SESSION_CLOSE line 11) means 1,171 rows the
  "clean" language does not describe.
- Sky/tripwire: sky is 0 backlog (full coverage); tripwire (proposal): two
  consecutive weeks of growing backlog integral raises batch size. Honest
  status: 1,171 images pending as of the last filed count. (2026-09-26 note:
  the mrpool media_full universe itself reads fully triaged, 1,980/1,980 with
  0 remaining per T44's 09-25 re-measure, recounted this date; this registry
  line tracks the older 2,011-image denominator and reads staler than the
  estate it registers. Cause: wave-2 audit batch 8.7.)

### R8 ORACLE-CAL · oracle calibration (G31, T29) · FILED, wiring owed

- Tool: `tools/oracle_calibration.py`; receipt
  `watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json` (selftest 12/12
  pass, read this ask).
- Headline: per-read confidence plausibility - a confidence number always
  looks calibrated to its own reader.
- Extreme: per-decision-class calibration residual peaks (ECE/Brier by class);
  C = integral of the class residual deficit from calibration, per class.
  Recipe names this: "per-domain drift" (receipt's recipe_source, G31).
- Mask: reads keep arriving with plausible-looking confidences while a class's
  residual integral drifts.
- Sky/tripwire: per-decision-class threshold (G31, on file); breach escalates
  that class's reads to a bigger model or a human - the G31 rule verbatim.
  Thresholds are per-class and owned by the escalation ladder when the wiring
  lands.

### R9 SCS · choice-set diversity scorer (T17, I-11) · READY, experiment unrun

- Tool: `tools/scs.py` (Jensen-Shannon over choice sets, stdlib only);
  battery `watch/inbox/ADVERSARIAL_ARC_BATTERY_20260918.jsonl`.
- Headline: task pass rates.
- Extreme: choice-set collapse (pairwise JSD toward 0 = uniform echo);
  deficit form C = integral of (1 - SCS) over battery administrations.
- Mask: high pass rates mask an echoing chooser that always picks the same
  shape of answer.
- Sky/tripwire: SCS decision rules are pre-registered on file (I-11,
  `watch/inbox/DEEPSEEK_ADVERSARIAL_ARC_20260918.md` lines 262-264); the
  instrument is built but the four-condition experiment is unrun - the
  fleet's #1 unrun falsifier per I-11. Not standing yet; registers READY.

### R10 DUTY-FUZZ · held-out gate-cycle fuzzing (T18) · READY

- Tool: `tools/duty_fuzz.py` ("HELD-OUT edge-case dilemmas per GATE CYCLE",
  its header, read this ask).
- Headline: gate cycle pass share.
- Extreme: gate cycles elapsed since the last held-out batch; deficit form
  C = staleness integral over cycles.
- Mask: a gate looks sound while its spec goes un-fuzzed cycle after cycle
  (retrospective compliance, the wave-2 flaw the tool exists for).
- Sky/tripwire: the tool's own design is the sky - staleness ceiling of 1
  gate cycle; breach holds the gate's promotion decisions until a fresh batch
  runs. Threshold is the tool's design intent, not yet wired.

### R11 COASTLINE · ink coastline dimension (ADV-I-12 falsifier side) · DEFINED, UNBUILT

- Definition on file: "ink coastline (fractal dimension of the record)
  distinguishes discovery from self-agreement" (ADV-I-12,
  `memory/corpus/quantized_thought/adversarial_arc_invariants.jsonl` row 12;
  also `watch/inbox/DEEPSEEK_ADVERSARIAL_ARC_20260918.md:268`). The law names
  it a fleet cliff scalar (SELF_STEAL line 44).
- Headline: record row counts - growth reads as discovery.
- Extreme: straight-line self-agreement streaks vs fractal turns of the
  trail; deficit form C = self-agreement integral (straightness over time).
- Mask: an ever-longer record that is a straight line masks that nothing new
  is being found in it.
- Sky/tripwire: defined on file ("straight ink = consensus"), unbuilt. Honest
  status: no tool on disk computes it (search run this ask); the "Coastline
  Index" named in `watch/inbox/NIGHT_MEMORY_AUDIT_20260911.md` and
  `watch/inbox/DESK_DEFENSE_FACTORY_20260911.md` is a Water Arena game chart,
  not this instrument, and is not conflated here. UNBUILT means the law's
  own sentence applies to the fleet: this one is decoration until built.

### R12 BOARD-DRIFT · vocabulary drift across 10 boards (T25) · ONE-PASS

- Tool/artifact: `scripts/the50_w5_t25_board_drift.py`;
  `memory/runs/the50/w5_t25_board_drift.json` (6,242 drops, 105,628 tokens,
  read this ask).
- Headline: vocabulary totals per board.
- Extreme: neologism share peaks per board-month; C = integral of new-term
  share against the event calendar (the drift family's law form).
- Status ONE-PASS: an analysis artifact, not a standing instrument;
  re-registers standing if a re-run cadence is ever wired (trigger proposal:
  new corpus landings).

## 6. What this filing is NOT

- Not a signature. The law stays a candidate (section 0).
- Not a threshold grant. Every tau/s-star above marked "proposal" is spec
  text; firing one is the instrument owner's or the operator's act, and L4
  requires the response to be ordinary code or an inbox row, never a silent
  judgment.
- Not new measurement. Every current reading above is quoted from a file
  read this ask or a command run this ask (section 7); no corpus was
  recomputed, no term list revised, no backlog burned.

## 7. Checks actually run this ask

1. `rg -in --glob "*.{md}" "cliff[-_ ]?scalar" watch/inbox docs` - 13 hits;
   origin (SELF_STEAL lines 34-46), applications (COGNITIVE_CONTROL_PLANE 40,
   52; VERB_DSL_STEAL 38; TIME_TRAVEL_QSTAR 53, 70, 137; INTERPRETER_LAYER
   48; SOVEREIGN_JUDGMENT_STACK 78; SESSION_CLOSE 18, 41-43;
   RIDDLE_TRIAD_CADENCE 21, 46), and the program line itself.
2. `.venv/Scripts/python.exe tools/drift_pairs_stamp.py --status` -
   `{"v1_rows": 3, "v2_rows": 3, "weeks_stamped": ["2026-W38"]}`.
3. Read `memory/runs/adv_arc_50/teleo_drift_stamps.jsonl`,
   `drift_stamps.jsonl`, `thrash_register.json` in full - corr values and
   verdicts quoted in R1/R2 are byte-quoted from these files.
4. `.venv/Scripts/python.exe tools/thrash_meter.py` - live reading, score 84,
   THRASHING, 1,480 events / 261 fronts / 56 sessions / 6h window (exit 0).
5. Read heads/bodies of `memory/runs/the50/w5_t22_urgency_curve.json`,
   `w6_t27_thrash_reading.json`, `w6_t28_miss_entropy.json`,
   `w5_t25_board_drift.json`, `watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json`
   (12/12 selftest), the T38 public-artifact spec, RIDDLE_TRIAD_CADENCE,
   SESSION_CLOSE, SELF_STEAL_CORPUS_SKILLS, DEEPSEEK_ADVERSARIAL_ARC (I-11,
   I-12 sections), COGNITIVE_CONTROL_PLANE, SOVEREIGN_JUDGMENT_STACK,
   VERB_DSL_STEAL, TIME_TRAVEL_QSTAR, INTERPRETER_LAYER.
6. Tool headers read for R7, R8, R9, R10, R12 (scripts/ and tools/ listed
   above); `memory/runs/the50/` artifact census run.
7. `rg -in "cliff" memory/rib_bus/doctrine.json` - no rows: law unsigned.
8. `memory/percolator/invariants.json` inspected: it is the behavioral
   n-gram percolator (counts over steer text), NOT the law register; the ADV
   arc's 12 invariants live at
   `memory/corpus/quantized_thought/adversarial_arc_invariants.jsonl`
   (ADV-I-12 row read).
9. Registry twin `THE50_W10_T47_CLIFF_SCALAR.registry.json` validated with
   `.venv/Scripts/python.exe -c "import json; json.load(...)"` and both files
   grep-checked for the em-dash character (U+2014) after writing: zero hits.
10. Not run (honest gaps): no BKM literature fetch (the anchor stands on the
    fleet's own filed translation); no corpus recomputation (R3/R7 numbers
    are the filed values, not fresh counts); no tripwire wired (L4 responses
    await owner/operator acts); R11 remains unbuilt.

## 8. Falsifier for this spec

1. Any registry entry whose cliff scalar cannot be computed from the files
   its own row names - a registration that names an unmeasurable integral
   violates the law it registers.
2. Any entry whose "extreme" is a mean, median, or share in disguise (a mask
   registered as a cliff).
3. Any current reading in section 5 that fails to reproduce from its named
   file (bytes, not reports).
4. A standing measurement instrument on disk, firing on a cadence, that is
   missing from the registry (the completeness claim: section 5 covers every
   standing instrument found on disk this ask).
5. Any claim here or later that the law is signed, fleet-binding, or
   enforcing. Until the operator's signature, every tripwire is a proposal.

## 9. Provenance

- `watch/inbox/THE_50_PROGRAM_20260918.md:72` - the task; line 78 - receipts
  to watch/inbox/.
- `watch/inbox/SELF_STEAL_CORPUS_SKILLS_20260918.md:34-46` - the law text,
  the BKM anchor, the four named scalars, the I-12 pairing.
- `watch/inbox/RIDDLE_TRIAD_CADENCE_20260918.md` - Pool/Q/BG readings and the
  first per-corpus registrations (lines 46-51).
- `watch/inbox/SESSION_CLOSE_20260919.md:18-19` - instruments live on file;
  lines 41-43 - the operator signature gate this spec respects.
- `watch/inbox/COGNITIVE_CONTROL_PLANE_20260919.md:51-52` (ignorance budget),
  `watch/inbox/VERB_DSL_STEAL_20260918.md:38` (alarm clause),
  `watch/inbox/TIME_TRAVEL_QSTAR_20260918.md:53-54,70` (orientation checks,
  registrations as the instrument the wild machines lack),
  `watch/inbox/SOVEREIGN_JUDGMENT_STACK_20260919.md:78` (safety rail),
  `watch/inbox/INTERPRETER_LAYER_20260918.md:48` (testing readings against
  the instruments).
- `watch/inbox/DEEPSEEK_ADVERSARIAL_ARC_20260918.md:262-268` +
  `memory/corpus/quantized_thought/adversarial_arc_invariants.jsonl` - I-11
  (pre-registration) and I-12 (count against the sky) verbatim.
- `memory/runs/adv_arc_50/` (teleo stamps, drift stamps, thrash register),
  `memory/runs/the50/` (t22, t25, t27, t28 artifacts),
  `watch/inbox/THE50_W6_T29_ORACLE_CALIBRATION.receipt.json`,
  `watch/inbox/THE50_W8_T38_LEDGER_PUBLIC_SPEC.md` - every current reading.
- Tools on disk: `tools/drift.py`, `tools/drift_pairs_stamp.py`,
  `tools/thrash_meter.py`, `tools/oracle_calibration.py`, `tools/scs.py`,
  `tools/duty_fuzz.py`, `scripts/the50_w5_t22_urgency_curve.py`,
  `scripts/the50_w5_t25_board_drift.py`, `scripts/the50_t08_spectro.py`,
  `scripts/the50_t13_stego_detectors.py`.
- House style and gate discipline:
  `watch/inbox/THE50_W8_T38_LEDGER_PUBLIC_SPEC.md` (receipt pattern, section
  9 checks-honesty pattern).

## 10. Re-verification 2026-09-25 (second seat, same task T47)

The artifact stood complete from the 2026-09-19 filing. Before submitting it,
this seat re-ran the load-bearing checks, per the rule that a check counts
only if run in the ask that claims it. Section 7's items remain the record of
the filing seat; this section is the record of this seat.

1. Registry twin re-validated: `.venv/Scripts/python.exe -c "import json;
   json.load(...)"` - JSON OK, schema `the50.w10.t47.cliff_scalar_registry.v1`,
   12 entries R1-R12 at check time (15 after item 8 below).
2. Em-dash scan re-run on both files (rg for U+2014): zero hits, still.
3. `rg -in "cliff" memory/rib_bus/doctrine.json`: no rows. The law is still
   unsigned; the gate status in section 0 stands unchanged.
4. Citation re-checks: `THE_50_PROGRAM_20260918.md` line 72 exact; SELF_STEAL
   lines 36-38 (BKM anchor) and 40-46 (law text) verbatim; SESSION_CLOSE
   operator-gated signature item on file (cited as "lines 41-43"; the item
   sits at lines 40-42 in current bytes, same text); SESSION_CLOSE line 12
   (840/2,011 vision-triaged) and the instruments line (Q 3 / Pool 16+107 /
   BG 0) verbatim.
5. Reading reproduction (falsifier 3): R1 corr 0.4118 / 0.8839 / -0.1385
   reproduce byte-exact from `teleo_drift_stamps.jsonl`; R2 register lanes
   harvest 0.125 / night 0.0667 / research 0.029 (n=1343) byte-exact from
   `thrash_register.json`, ceilings line verbatim in its law field; R3
   baseline ~10%, peaks 64 (2025-11) and 56 (2026-07), band 27-56%, Sep-2026
   18% partial - all verbatim in RIDDLE_TRIAD lines 13-29; R4 rows_q_authored
   4705 in `w5_t22_urgency_curve.json`; R5 recounted 16/16 BROKEN from
   `called_shot_ledger.jsonl`, pool 107 / horizons through 2028-03-01 in the
   T38 spec; R6 claim verbatim in `w6_t28_miss_entropy.json`; R8 tests_passed
   12 in the oracle receipt; R12 rows_loaded 6242 / total_tokens_analyzed
   105628 in `w5_t25_board_drift.json`; I-11/I-12 text verbatim at
   DEEPSEEK lines 262-268 and ADV-I-12 row in
   `adversarial_arc_invariants.jsonl`. All ten cited tool/script paths exist.
6. `.venv/Scripts/python.exe tools/drift_pairs_stamp.py --status` re-run:
   now `{"v1_rows": 3, "v2_rows": 6, "weeks_stamped": ["2026-W38",
   "2026-W39"]}`. A W39 stamp landed after filing. From the ledger: T1 corr
   -0.0271 DRIFTING, T2 0.8839 ALIGNED, T3 -0.0759 DRIFTING. Under R1's
   PROPOSAL tripwire, T1 and T3 now have two consecutive stamps below the 0.5
   floor (T1: 0.4118 then -0.0271; T3: -0.1385 then -0.0759). The proposal's
   condition is met; it is NOT fired. Firing is the pair owner's or the
   operator's act (section 6).
7. `.venv/Scripts/python.exe tools/thrash_meter.py` re-run: score 85,
   THRASHING, 2,284 events / 389 fronts / 152 sessions / 6h window, exit 0.
   Same verdict shape as the filed reading (84 on 2026-09-19); R2's declared
   parallel-burn caveat still applies.
8. Census re-run behind falsifier 4 found standing instruments that postdate
   the filing (the meters_nightly era, landed 2026-09-22 per its header and
   `watch/inbox/DOGFOOD_OPERATING_ENVIRONMENT_20260922.md`). The registry is
   expanded 12 -> 15 rather than left falsified by its own standard:
   - R13 SMITH-GAMMA: `tools/estate_smith_chart.py`, nightly via
     `tools/meters_nightly.py` JOBS[0]; reading
     `watch/inbox/ESTATE_SMITH_CHART_20260922.json` (bar 0.5, 8 organs, 5
     prose_bar_violations incl. ollama_lane gamma 0.895, 0 dark).
   - R14 CURVATURE: `tools/curvature_scan.py`, nightly via JOBS[1]; reading
     `watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260922.json` (6 regions, 5
     SADDLE, 1 DARK).
   - R15 USAGE-SWEEP: `scripts/usage_meter_sweep.py`, night-shift wired;
     readings `watch/usage_sweeps/USAGE_SWEEP_20260904.md` and
     `USAGE_SWEEP_20260906.md` (0906 header: FLAGS (5)).
   - Reviewed and NOT registered: `tools/lattice_build.py` (JOBS[2]) - a map
     compiler (`memory/lattice/latest.md`), not a measurement instrument; no
     headline statistic to mask. `tools/meters_nightly.py` itself is the
     wrapper, not an instrument.
9. Not run this ask: no BKM literature fetch (unchanged from section 7); no
   corpus recomputation (R3/R7 numbers remain the filed values); no tripwire
   fired or wired; R11 still unbuilt; the W39 proposal condition (item 6)
   deliberately left to its owner; R15 sweep bodies not re-parsed (headers
   and file census only).
