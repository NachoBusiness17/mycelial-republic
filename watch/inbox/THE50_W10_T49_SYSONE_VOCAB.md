# THE 50 · W10 T49 - SYSTEM-ONE QUESTION VOCABULARY (SYSONE-VOCAB-1)

Filed 2026-09-19 · finish line per `watch/inbox/THE_50_PROGRAM_20260918.md`
line 74: "49. System-One question vocabulary spec [LANE]".

This is a language specification, not a new organ. It codifies the typed
question vocabulary the fleet already speaks and that the gate already
ratified ("Jev Salon 2 ratified: sift / witness / vow / abide",
`mag/verb.py:317-320`) and the build order already adopted ("VERB stone
three: typed question vocabulary (Choice/Score/Noul naming adopted)",
`watch/inbox/COGNITIVE_CONTROL_PLANE_20260919.md:72`). Nothing here
publishes anything or answers the salon's open questions 1-8
(`watch/inbox/JEV_CONSOLIDATED_BRIEF_20260919.md:118-137`); those stay
operator/salon gates.

## 1. Ground truth the vocabulary is pinned to (verified spec, on file)

- Endpoint POST api.typesafe.ai/v1/systemone, model jev-1.13.0 (pin it).
  $0.042/MTok input, $0 out. 70-500ms. 64k context / 32k for state plus the
  longest question. Text-only state. Choice up to 255 options.
  (`JEV_CONSOLIDATED_BRIEF_20260919.md:10-12`)
- Three primitives, parallel and isolated, one judgment per question:
  CHOICE (pick one from your list), SCORE (position on your rubric), NOUL
  (boolean probability). (`JEV_CONSOLIDATED_BRIEF_20260919.md:12-15`,
  `COGNITIVE_CONTROL_PLANE_20260919.md:12-13`)
- Confidence is a spread statistic, C = (N*p_max - 1)/(N - 1), argued by
  independent audit to be normalized distance-from-chance, NOT a trained
  uncertainty head. Uncalibrated until the Fleet-Bench meter says otherwise.
  (`COGNITIVE_CONTROL_PLANE_20260919.md:17-19`,
  `JEV_CONSOLIDATED_BRIEF_20260919.md:22-25`)
- Key ablation: one 4-option Choice 48.3 percent vs four decomposed
  precondition Nouls in one request 98.3 percent. Decomposed atomic
  questions beat fat Choices by 50 points.
  (`JEV_CONSOLIDATED_BRIEF_20260919.md:43-45`)

## 2. The three families

Every System-One question is ONE of these three kinds. A question carries a
`kind` tag in kifu rows (the linter already emits it,
`mag/verb.py:362-363,368`).

### NOUL - boolean probability

One yes/no judgment over the state, answered with a probability, never
prose. The fleet's native family: `feels()` yes/no verdicts
(`mag/verb.py:186-219`), `witness()` packet votes where full agreement is
GREEN and anything else is PURPLE (`mag/verb.py:376-413`, live rows in
`queue/lanes/jev/trail.jsonl`), `abide()` per-rule violation reads
(`mag/verb.py:438-459`), `vow()` stop conditions (`mag/verb.py:416-435`),
and the Class-A kifu-link meter rows the standing drive farms
(`scripts/gopher_packs.py:40`).

Examples (all runnable shapes, verified this ask):

- "Is every meter row in the jev trail idempotent by id?" -> NOUL
- "Does the previous wave change this verdict?" -> NOUL with a state
  isolation warning (context belongs in state, never in the question)

### CHOICE - pick one from a closed list

Exactly one option out of a closed option set. The fleet speaks it as
`classify()` (`mag/verb.py:238-256`), `match()` doctrine routing
(`mag/verb.py:222-235`), the duty-fuzz closed option sets A-D
(`tools/duty_fuzz.py`, docstring lines 6-7), the SCS choice sets scored by
ordinary-code JSD (`tools/scs.py`, docstring lines 5-6), and the blind
condition classifier of the persona harness
(`JEV_CONSOLIDATED_BRIEF_20260919.md:98-100`).

Wire limits: hosted cap 255 options; FLEET COMPILER CAP 4
(`mag/verb.py:322`). A Choice over the cap is not an error, it is a
compile-time transform: it auto-decomposes into parallel Nouls, one per
option ("Is 'pol' the answer?"), the 50-point ablation enforced as a rule
(`mag/verb.py:357-360`, `JEV_CONSOLIDATED_BRIEF_20260919.md:92-93`).

Example (verified this ask): "Which verdict does the wave packet carry?"
options GREEN/PURPLE/RED -> kind CHOICE, passes at 3 options.

### SCORE - position on a rubric

A scalar on a declared rubric, not a free number. The fleet already emits
the de facto Score as the declared CONFIDENCE field ("End every answer with
exactly: CONFIDENCE: <0-100>", `mag/verb.py:127`), read only when explicitly
declared, never bluffed (`mag/verb.py:175-183`), aggregated as a predictive
distribution by `confident()` with honest n
(`mag/verb.py:280-313`). Calibration of Score fields is the oracle
calibration harness's job: binned reliability, ECE/MCE/Brier, temperature
fit, per decision-class thresholds
(`tools/oracle_calibration.py`, docstring lines 14-27). Planned rubric
uses on file: stylometric fidelity rubric and per-lens confidence for salon
verdicts (`JEV_CONSOLIDATED_BRIEF_20260919.md:95-97`,
`COGNITIVE_CONTROL_PLANE_20260919.md:31-33`), risk rubric in the
jev-router organ (`JEV_CONSOLIDATED_BRIEF_20260919.md:68-69`).

Example: "On a 0-100 rubric where 0 = prompt-only and 100 = fully
method-faithful, score this answer's fidelity" -> SCORE, rubric named in
the question, judgment still atomic.

## 3. Composition law: G26's missing types are NOT new primitives

G26 named four candidate additions: "ranking, comparison,
threshold-with-confidence, abstention" (`watch/inbox/GPS_BATTERY_20260918.jsonl:26`).
VOCAB RULING (naming only, per the adopted build order): all four are
compositions or verdict routes over the base three. No fourth primitive.

- RANKING = ordered pairwise NOUL comparisons. "Rank A, B, C" compiles to
  "Is A above B?", "Is B above C?" (n-1 questions), then code assembles the
  order. Never ask a fat ranking Choice.
- COMPARISON = degenerate two-option CHOICE ("A" vs "B"). Two Nouls if you
  also want the margin.
- THRESHOLD-WITH-CONFIDENCE = NOUL plus its declared confidence field plus
  a per decision-class tau gate from the calibration harness (escalate to a
  bigger model or a human below threshold; G31 rule,
  `tools/oracle_calibration.py`, docstring lines 26-27).
- ABSTENTION = not a question kind. It is a VERDICT ROUTE every family
  carries, with four named routes already compiled in
  (`mag/verb.py:332-333`): low -> PASS_UNVERIFIED, medium -> QUEUE_RETRY,
  high -> ESCALATE_MODEL, irreversible -> WAKE_HUMAN. Silence is a verdict,
  not a stop sign (`mag/verb.py:189-194`). The two-witness law is the
  abstention floor: a lane that dies in transit casts no vote, so a packet
  can never turn GREEN on partial attendance (`mag/verb.py:380-382,406-407`),
  and the meter stays honestly conservative: transport deaths count as
  misses (`mag/verb.py:462-484` idempotent rows; bias noted in the lane
  trail, `queue/lanes/jev/trail.jsonl` trigger rows).

## 4. The grammar (what makes a question legal at all)

The linter `sift()` is the vocabulary's syntax
(`mag/verb.py:336-373`). Four rules, exercised LIVE this ask with
`.venv/Scripts/python.exe -c "from mag import verb; print(verb.sift([...]))"`:

1. ATOMICITY: no compound predicate (and/or/but). "Is the ledger broken
   and the channel silent?" -> REJECTED, reason "atomicity: compound
   predicate (and/or/but)".
2. ONE JUDGMENT: one "?" per question. "Is the meter valid? Is the trigger
   above 0.880?" -> REJECTED, reason "one-judgment: two questions in one".
3. CHOICE CAP: more than MAX_CHOICE_OPTIONS=4 options auto-decomposes into
   parallel Nouls. The 6-option board question -> decomposed dict with six
   "Is 'x' the answer?" entries.
4. STATE ISOLATION: the question may not reference other context
   (previous/earlier/above); context lives in the state block, never in the
   question. "Does the previous wave change this verdict?" -> WARNING
   "state isolation: question references other context" (passes, tagged).

Plain boolean questions compile to kind NOUL, option sets within cap
compile to kind CHOICE. Batch legal questions in one request; they evaluate
in parallel and in isolation (`JEV_CONSOLIDATED_BRIEF_20260919.md:14-15`).

## 5. Registry and versioning (G34's schema question, answered as law shape)

G34 asked: typed answers with schema evolution, who registers, what happens
to old traces (`watch/inbox/GPS_BATTERY_20260918.jsonl:34`).

- This file is SYSONE-VOCAB-1. Three kinds, four grammar rules, four
  silence routes, one compiler cap (4), one composition list (section 3).
- WHO REGISTERS: the module that owns lane plumbing registers question
  vocabulary; the gate already ruled no parallel organ re-implements it
  (`mag/verb.py:317-320`). A vocabulary change is an amendment to
  `mag/verb.py` plus a new version line here, never a side module.
- OLD TRACES: the kifu is append-only and hash-chained
  (`mag/verb.py:72-82`); rows are never rewritten, corrections travel as
  new rows (duty D2, `tools/duty_fuzz.py` D2 text). A kind tag added later
  does not invalidate old rows: pre-vocab rows are simply untyped and
  count as legacy, exactly as pre-chain rows do in `verify_trace()`
  (`mag/verb.py:91-94`).
- NEW KINDS: enter only through the composition list. A proposed fourth
  primitive must first show a live judgment that NOUL/CHOICE/SCORE cannot
  express without losing the one-judgment or isolation property. That bar
  is the ignorance budget applied to language
  (`COGNITIVE_CONTROL_PLANE_20260919.md:48-52`).

## 6. Worked examples, one per family (the payload contract)

State block (text-only, the 64k/32k rule): the packet text under judgment.
Questions (one request, parallel, isolated):

- NOUL: "Does this packet's cited link resolve?" -> probability on YES;
  GREEN only on witness agreement (`queue/lanes/jev/trail.jsonl`
  A-harvest rows are this shape, live).
- CHOICE: "Which class is this packet: A, B, or C?" -> exactly one label;
  the gopher wave rows carry class A/B/C today.
- SCORE: "On the 0-100 CONFIDENCE rubric, score the grounding of this
  packet's claim" -> declared scalar, routed by the per-class tau after
  calibration.

Routing after answers is DETERMINISTIC CODE with tau gates
(`mag/verb.py:332-333`, `tools/oracle_calibration.py`); the oracle never
owns control flow.

## 7. Do-not-use list (negative capability, binding on question writers)

- No counting, arithmetic, or date math questions
  (`JEV_CONSOLIDATED_BRIEF_20260919.md:39-40`).
- No free-text generation, open planning, or long chain-of-thought
  (same source).
- No fat taxonomies: a Choice over 4 options is written as fan-out Nouls,
  never as one big Choice (section 2, compiler-enforced).
- No composite weighted scoring of uncalibrated Scores until the Fleet-Bench
  meter shows ECE below the bar (`JEV_CONSOLIDATED_BRIEF_20260919.md:70-72`).
- No doctrine-adjacent judgment through the hosted oracle: fresh-domain
  packets yes, judge-suitable doctrine stays local
  (`JEV_CONSOLIDATED_BRIEF_20260919.md:112-114`).
- Model jev-1.13.0 pinned; never jev-latest
  (`JEV_CONSOLIDATED_BRIEF_20260919.md:10-11`).

## 8. What this file does not decide

Salon open questions 1-8 (adopt organs now, replica threshold, silence
branch default route, Fleet-Bench publication, ignorance budget
ratification, the A/B/C falsifier pre-registration) remain open and
operator/salon-gated (`JEV_CONSOLIDATED_BRIEF_20260919.md:118-137`). This
spec adopts names and composition law for question types already ratified
and already running in `mag/verb.py`; it files the language, it opens no
gate.


## 9. Re-verification (2026-09-25, seat T49 re-check)

All citations above re-read from disk this date and confirmed current:
mag/verb.py (sift 336-373, cap 322, routes 332-333, two-witness 380-382 and
406-407, meter 462-484, chain 72-82, legacy 91-94), the JEV brief, the
control-plane stone, G26/G34 rows of GPS_BATTERY_20260918.jsonl, the
tools/duty_fuzz.py, tools/scs.py, tools/oracle_calibration.py docstrings,
scripts/gopher_packs.py:40, and live rows in queue/lanes/jev/trail.jsonl
(6 rows, class A/B/C packets, trigger rows present). Grammar re-exercised
live with

.venv/Scripts/python.exe -c "from mag import verb; print(verb.sift([...]))"

over all six shapes of sections 2 and 4: plain boolean compiled kind NOUL;
compound predicate rejected (atomicity); double question rejected
(one-judgment); 6-option Choice decomposed into six Nouls; 3-option
GREEN/PURPLE/RED compiled kind CHOICE; previous-wave question warned (state
isolation) and passed tagged. Every result matched section 4 exactly.
