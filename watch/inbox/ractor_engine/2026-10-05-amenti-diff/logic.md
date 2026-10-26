# LOGIC LENS - Amenti diff adjudication (2026-10-05, ractor dwfrun-b8b718fd)

Seat: lens-logic, instrument theorist. Everything below was checked this sitting
with the repo venv python (filesystem census + targeted reads); no model probes
were fired, so every adjudication is instrument-shape analysis, not measurement.

## 0. What I read and ran

- memory/research_packs/20261005_agent_mesh_salon/DIFF_TARGETS.md (all 36 lines)
- watch/inbox/AMENTI_TRANSLATION_20261005.md, watch/inbox/MESH_V2_SELFSTEAL_LANDED_20261005.md,
  watch/inbox/AMENTI_DIFF_RACTOR_20261005.md, .agents/skills/swarm-search/SKILL.md
- state/CURRENT.md, mag/operator_mode.py, mag/realign.py, tools/refold_gate.py,
  tools/query_broker.py + tools/gps_mcp/server.py + mag/mesh/door.py (freshness lines)
- Census commands run: file count under memory/runs/salons (558 excl .mimosa);
  SALON_ARTIFACT parseability census (53 artifacts, 38 with per-seat engine lines,
  48 with fold sections, 7 with tri-state verdict tables, fold-fate grep = 1 hit);
  hermes_burn usage.jsonl field census + ok:false by model (716 rows false);
  operator_mode.jsonl trail census (415 rows); scoped greps for operator_state
  (mag/ + tools/), sycophancy, filter_trip (mag/: zero hits).

## 1. Per-target adjudication

### T1 operator-state feed: steal REAL but the map cell is WRONG, and the cheapest falsifier already sits on disk

DIFF_TARGETS.md:15 grades "nothing typed; operator state lives only in prose | ABSENT".
That is a grading error. The estate has a typed operator-state organ:
mag/operator_mode.py:9-26 (schema operator_mode.v1, modes running|paused, scopes,
atomic state file + append-only trail) read by mag/realign.py:54-55 and
mag/realign.py:248-258; the trail state/operator_mode.jsonl holds 415 rows and the
state file is live (mode=running, changed_at 2026-10-04T02:57:31Z). What is
genuinely absent is the somatic dimension (sleep/energy/focus) and the mesh writer
"operator". So the steal is narrower than claimed: extend schema v1, do not build
a first channel. Cheapest falsifier is NOT the diff's two-week prospective A/B;
it is a retrospective join run today: memory/runs/hermes_burn/usage.jsonl
(3010 rows, fields ts/model/ok/cost_usd/turn) x operator_mode.jsonl trail (ts/mode/
scope), testing whether burn outcomes (ok rate, cost per ok turn) differ across
operator mode windows. Zero delta on the binary channel is evidence the somatic
extension is ceremony; delta is the first body-state-adjacent measurement the
estate has ever had. Order: FIRST, before any feed is built.

### T2 harmonic profiles: vertex is COLDER than graded; the named base is the wrong instrument

The graded base (DIFF_TARGETS.md:16, "Nous authority-override filter laws (filter
trips)") resolves to the ok:false rows of the burn ledger (watch/inbox/
PROCESS_IMPROVE_WAVE1_20261003.md:36 names them "the banked Nous content-filter").
Two problems I verified: (a) construct mismatch - ok:false measures a PROVIDER
refusing, T2's target is the MODEL not yielding (unprompted disagreement, authority
survival, verdict under pushback); those are different constructs; (b) cause
mixing - usage.jsonl carries no reason field, and 483 of the 716 ok:false rows are
anthropic models the driving ladder (AGENTS.md) says are UNFUNDED, so filter trips
cannot be separated from key failures in the ledger as it stands. Sovereign-voice
retention has ZERO measurements in the estate. T2 is therefore a cold vertex, not
a PARTIAL extension.

### T3 repetition-binding: steal REAL, and the harness already exists

mag/arena_bench.py is a scored two-lane bench: live mode against ollama-compatible
endpoints (arena_bench.py:456-464, :511-515), per-claim CONFIRM/REFUSE verdicts,
and a synthetic sycophancy ceiling already built (fixture_maru_sycophant,
arena_bench.py:482-492, which CONFIRMS every claim including lies). The existing
sycophancy surface is otherwise lore only (regex in mag/field_steal.py:63-64,
risk knob in mag/guardrail_sentinel.py:53), consistent with the diff's "never
measured". T3 = inject N repetitions of a contrary assertion into the challenge,
same candidate, measure verdict drift per N per family. The sycophant fixture is
the drift ceiling and fixture_honest_ghost (arena_bench.py:468-479) is the floor;
real seats land between. One sitting on free lanes.

### T4 photocopy A/B: steal REAL, but the falsifier as written conflates two variables

The freshness header is verified live in all three doors (tools/query_broker.py:234-247,
tools/gps_mcp/server.py:142-155, mag/mesh/door.py:51-67) but frozen is TIME-DERIVED
(30 days without growth), so "corpus live vs frozen:true" mixes content staleness
with the label effect. The cheapest machine-checkable falsifier separates them:
same corpus bytes, forced-frozen header (a knob that does not exist yet; monkeypatch
or env override on _freshness), fixed question battery, diff answers + citation
resolvability. Nobody has this number; the header landed today with zero behavioral
evidence, so the vertex is cold and the probe is cheap once the knob exists.

### T5 condensation threshold: KILLED AS SPECIFIED (no outcome labels exist); redefined, not dead

The archive is input-rich, outcome-poor. Census: 53 SALON_ARTIFACT files, 38 carry
per-seat engine lines (cross-family diversity real: deepseek 52, hermes 43, zai 38,
cohere 38, anthropic 37, xai 25 mentions), 48 have fold sections, but only 7 have
parseable tri-state convergence tables, and a fold-fate grep over all 558 files
found exactly ONE artifact mentioning falsification language
(memory/runs/salons/planning_chord_test_20260903/SALON_ARTIFACT.md) and it is a
DESIGNED prospective falsifier, not post-hoc fate tracking. "Folds that later got
falsified vs held" cannot be mined from labels that were never recorded. T5's
cheapest honest form: wire a fold-fate ledger now (every banked fold claim sampled
and re-checked at +7d/+30d by a free-lane verifier, tagged held/falsified) and let
the dew point accumulate; the n=7 input-side mining (agreement density vs judge
confidence tag) is a methods dry-run, underpowered as a measurement. Note
tools/refold_gate.py is a DIFFERENT fold (JS index fold host pins, its own docstring
lines 1-23); do not let the name collision fool the probe writer.

## 2. Free-lane order (cheapest instrument first)

1. T1-RETRO join (local ledgers only, ~60 min, zero model calls; adjudicates
   whether the T1 build is worth building at all).
2. T3 then T2 as ONE arena grid with two dials (repetition N x authority register
   across family/temperature on free endpoints) - same harness, two columns.
3. T4 forced-frozen knob + fixed battery (one sitting for the knob, one for the run).
4. T5-redefined fate ledger (wire now; the dew point is a delayed dividend, and it
   is also the loop's cure, see F5).

## 3. The loop itself: real on rails 4-6, broken at three joints

EXTERNAL SYSTEM -> invariants -> self-map -> diff -> ractor -> probes -> bank is
genuinely repeatable: station 4 fired for real (this run, gate-checked per
SKILL.md:25-28), station 6's propose -> adjudicate -> knot cycle is proven with
blob #1 (MESH_V2 receipt section 3). What breaks it:

- Joint A, self-map integrity: station 2's honesty law ("PRESENT cells cite the
  organ (file path)", SKILL.md:22-23) has NO tripwire, and run #1 already contains
  a grading error (T1 cell, section 1 above). The estate's own prior art is the
  census-carrier tripwire pattern; the fix is a map-lint that re-greps each map
  row's claimed organ and flags ABSENT cells whose concept keywords hit code.
- Joint B, single-family adjudication: the loop banks a witness law (cross-family
  agreement only, SKILL.md:41-42) but does not apply it to its own ractor; this
  lens itself runs GLM-5.3 on the zai account, and workflow children ride that
  same account (AGENTS.md fan-out law), so ractor agreement is intra-family echo
  by the loop's own definition. Mitigation: count ractor verdicts as SENSING and
  climb kills/promotions to a funded different-family seat (grok-4.7 / Hermes
  primes), exactly as the driving ladder already orders for judgment.
- Joint C, no fate tracking: station 6 banks laws and station 7 re-diffs, but
  nothing ever re-tests a banked fold claim, so PRESENT cells rot silently - the
  same demotion-gap disease the mesh audit already banked ("no decay = cannot
  forget = cannot learn", commit 7b3ee99ec). The T5 fate ledger is simultaneously
  a target fix and the loop's own cure; that doubles its priority.

## 4. Blind spots

- No live probe was fired; all numbers above are ledger/archive censuses, and the
  actual drift, variance, delta, and dew-point values remain unmeasured (OWED).
- I read 3 salon artifacts in detail and censused the rest by pattern; subtle
  formats a regex census misses could raise the n=7 figure somewhat, though the
  fate-label absence is a structural gap no parser can cure.
- I cannot see sibling lenses' engines from this seat; the single-family claim is
  scoped to what I can verify (this account's children + my own engine).
- The ok:false anthropic interpretation (unfunded-key failures mixed with filter
  trips) is inference from the driving ladder; the ledger has no reason field,
  which is precisely the finding.

## 5. Convergence

The Joint C critique independently re-derives the demotion gap already banked in
the mesh audit (commit 7b3ee99ec) - flagged CONVERGENT, and it outranks my novel
map-lint point because two runs now name the same disease from different doors.

## 6. CORRECTIONS after the hostile second pass (2026-10-05, same sitting)

Every correction below was re-executed by me before accepting it.

### T1-RETRO falsifier WITHDRAWN (my own join kills it)

I ran the join power check myself: state/operator_mode.jsonl yields 205 paused
events totaling 333.7 s (0.0039 days; mean 1.6 s, max 300.6 s), and ALL 3010
hermes_burn usage rows classify into running windows, 0 into paused windows.
Burn dispatch is gated on running, so paused windows mechanically contain no burn
rows; the join has zero contrast and cannot adjudicate anything. T1's only honest
falsifier is the diff's original prospective A/B (DIFF_TARGETS.md:23). The
schema-extension finding (section 1, T1) stands; the cheap pre-adjudication move
does not.

### T2 evidence CORRECTED (three errors of mine; the conclusion stands)

- Family aggregation: 714 of 716 ok:false rows are anthropic-family (483 opus-5.5
  + 164 fable-5.1 + 67 sonnet-5.5); my "483 of 716" quoted one model as the family.
- "No reason field" was WRONG: my first census read only the first row's schema.
  Full-key census across 3010 rows: refused (89), finish_reason (332), note (2)
  all exist. Within ok:false: 214 finish_reason=content_filter, 89 refused rows
  carrying full Anthropic policy-refusal text (sample: "This request triggered
  restrictions on violative cyber content..."), 2 substance-floor notes = 305 of
  716 separable, zero overlap between refused and content_filter.
- The "unfunded-key failures" reading is contradicted for all 305 labeled rows:
  they are genuine provider-side refusals, matching PROCESS_IMPROVE_WAVE1_20261003.md:36-39
  (opus-5.5 combat-beat filter voids, void-not-crash as designed). The 2 glm rows
  are length-stubs, not refusals.
- Conclusion unchanged and now byte-solid: the banked signal is provider-side
  refusal, not model-side sovereign-voice retention; arena receipts census:
  144 files under memory/arena_bench, the ONLY live receipt ever is
  receipt_run_glm-5-3-flash_20260905T034941Z.json with verdict ERROR_LANE_DOWN
  ("flash lane unavailable") - no live seat has ever been scored, so the
  sovereign-voice vertex has zero measurements. (This also shades section 1's T3
  cost estimate: the arena live lane has never completed a run.)

### F4 reclassified: T5 is MIS-SCOPED, not unrunnable (my absence claim failed quantifier law)

My original grep was a fold-anchored composite pattern and I reported its count
as fate-language absence. Re-censuses I ran:
- Strict 'falsif' pattern: 322 of 558 files, 51 of 53 SALON_ARTIFACTs (most are
  designed falsifiers, which still falsifies my "exactly one" count).
- A genuine post-hoc fate record EXISTS in-archive:
  memory/runs/salons/long_horizon/SALON_ARTIFACT.md:5-7 - the 08-26
  "5.3-flash doesn't cache" finding OVERTURNED with the overturning measurement
  inline (99.52 percent cache hit, 7040/7074 tokens, novel-prefix controls 0).
- Fate language lives outside the archive at scale (capped census, files >2MB
  skipped): 278 occurrences / 136 files under watch/inbox, 298 / 196 under
  memory/; 3 RETRACT commits in git history (1693dd2ad, 2093ca518, 46ce3bc41).
- The tri-state input-side count is instrument-dependent and must be named with
  its instrument: 7 of 53 under the strict table-cell pattern, 50 of 53 under a
  broad verdict-vocabulary pattern, 19 of 53 per the second pass's pattern.
Corrected instrument for T5: a cross-surface join (fold claims in the salon
archive x overturning evidence in receipts/commits) can mint the first
fate-labeled dataset NOW; the fate ledger (section 1, T5) remains the standing
instrument for forward accumulation. The refold_gate.py name-collision warning
survives.
