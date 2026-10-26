# BREAK-ACCURACY PASS (hostile second lens on accuracy.md)

Seat: break-accuracy, ractor run 2026-10-10. Laws honored: no fabrication
(unverified = OWED), no em-dash, every claim cited to what this seat read or
ran, absence claims scoped to the instrument actually run. No subprocess was
spawned from Python this sitting (direct CLI only), so the win32
CREATE_NO_WINDOW law was not triggered. The db is live: every count below is
a moment (census denominator law); message total read 231,532 (moonshot-2.md:33,
verified) at the siblings' moments and 232,137 at mine.

## Instrument log (everything this seat ran or read)

Read in full or at cited windows: accuracy.md, economics.md, moonshot-2.md:25-54,
operations.md grep hits (:13,:27,:30,:212), _probe_verify_tape_b.py,
_probe_verify_tape.py, _probe_count_tape.py, _tape_census.py,
configs/lane_profiles.yaml:1-8,25-30, watch/inbox/burn_reset_20260927/work/
w-selfplay-hardware_verify.md:8-16, mag/lora_pipeline.py:9-14,25-28,
mag/harness.py:474-500, watch/inbox/ASTRA_V4_STATUS.md:1-8,
memory/continuity/seat_memory_20260927/astra-v4-converged-training-brief.md:25-31,
tools/zknot_alarm.py:45-55, memory/zknot/LATEST.md:1-5,33-40 + grep (:209),
memory/rib/RIB_BEHAVIOR_CARDS_20260928.md:1-6,75-80, memory/rib/
RIB_LIVING_WEIGHTS_BY_NATURE.md:5-12,20-24, memory/rib/
RIB_DRIVING_LADDER_20260928.md:50, watch/inbox/ASTRA_REVIVE_VERDICT_20260926.md:15,28.

Ran: (1) `./.venv/Scripts/python.exe _probe_verify_tape_b.py` verbatim rerun
(read-only, mode=ro uri); (2) a read-only part-census group-by by
message origin and by message role (same db); (3) a shape-A content-field
count over real_user messages; (4) an independent sum of memory/runs/
hermes_burn/usage.jsonl (3,038 rows) by model, plus last-paid-row and
glm-5.3-prime row inspection; (5) recursive file counts of watch/salon_responses
and watch/salon_glm53 plus a listing of watch/inbox/frontier_olm_2026-10-09;
(6) two WebFetches (arxiv.org/abs/2610.12426, arxiv.org/abs/2610.09484);
(7) QUANTIFIER attack on the finding-5 absence claim: full-depth
`rg -il "simulat"` over mag/ tools/ configs/ scripts/ tests/ (~90 files)
plus `rg -in "user.?sim|simulated.?user|interlocutor|counterpart"` over
mag/ tools/ configs/ (5 files, all inspected at match lines, plus
head-of-file reads of mag/desk_local_simulator.py, mag/desk_dialogue.py,
mag/surrogate.py, mag/behavioral_lensing.py, mag/mindweave_eval.py).

## VERDICTS

### FINDING 1 (tape census double-instrumented): CONFIRMED

Rerun of the banked probe verbatim (moment 2026-10-10, this sitting):
19,026 real_user text parts / 51,782,785 chars / ~12.9M tokens at chars/4;
7d: 4,432 turns / 16,932,685 chars / median 2,584 / p90 4,721 / max 345,016 /
voice(<500c) 549 turns / 83,029 chars / ~20.8k tokens. The falsifier's own
thresholds clear with margin (19,026 vs the under-18k kill line; 51.78M vs
under-45M). Median and max still byte-exact to economics.md:36-37. My own
shape-A query returns 0 texts from message.data content, confirming the
moonshot adjudication; moonshot-2.md:36-38's "NOT MEASURED" quote byte-checks
("that count is NOT MEASURED, not zero"). Drift story checks: messages
231,532 (moonshot-2.md:33) to 232,137 (mine), monotone growth, real_user side
moving +29 turns since the lens's 18,997.

One wording defect, not a data defect: accuracy.md:41-43 attaches "(exact
match to economics.md)" to a 7d row where only 2 of 6 figures were exact
(median 2,584, max 345,016; turns 4,407 vs 4,402, p90 4,678 vs 4,673,
chars not comparable as printed). "Within drift" was the accurate phrase and
is the phrase the same report's header law demands; the accuracy seat
overstated its own agreement in the one place it claimed exactness.

### FINDING 2 (economics assistant row "does not reproduce"): KILLED

The lens's own falsifier fired: "a stated-filter reproduction overturns this
correction and my number becomes the filter-artifact." My origin/role census
of type='text' parts (read-only, same db, same sitting):

- by origin: agent_runtime 125,336 parts / 59,401,588 chars; real_user
  19,026 / 51,782,785; NULL origin 132 / 99,315; system 3 / 933. There is
  NO origin='assistant' value in the db.
- by role: assistant 105,063 parts / 38,526,302 chars; user 39,436 /
  72,758,766.

role='assistant' at 38,526,302 chars is 9,631,575 tokens at chars/4, which is
economics.md:41-42's "~9.6M tokens" exactly, and 105,063 vs the banked 104,809
is +254 parts of ordinary live-tree drift (messages grew +605 in the same
window). The sibling family is monotone and convergent: 104,809 (economics.md:41)
then 104,971 (operations.md:30, produced by the role='assistant' query scripted
at _tape_census.py:26-29 in this same directory) then 105,063 (mine). The
filter economics ran is identifiable and stated-in-script by a sibling seat.

The lens's 125,132 was origin='agent_runtime': a real but DIFFERENT population
that includes roughly 20.3k agent-runtime USER-role parts (39,436 user-role
parts minus 19,026 real_user minus the NULL-origin remainder), i.e. subagent
and child-session turns, not "the estate's own half of the dyad" in the dyad
sense. So the headline "the estate's half of the dyad is ~50 percent larger
than banked" is a filter artifact, and "unreproducible as stated" is false.

Compounding instrument defects in the lens's own evidence chain, for the
record: (a) its banked script _probe_verify_tape_b.py:50-62 queries
origin='assistant', which returns 0 ("assistant text parts: 0" on my rerun),
so the banked script never validated the in-session agent_runtime query the
correction rode; (b) accuracy.md:71-72's "its banked _probe_count_tape.py
does not attempt it" conflates moonshot's probe (header line 2 of
_probe_count_tape.py: "moonshot-2 2026-10-10") with the sibling set, and the
directory did hold a stated assistant-count script (_tape_census.py, banked
by operations per operations.md:212) that the accuracy seat's instrument log
(accuracy.md:18-19) shows it never read.

Residue that survives the kill: economics.md:41 still should name its filter
(role='assistant'), and the agent_runtime population (125,336 parts /
59.4M chars / ~14.85M tokens) deserves its own labeled row. The lens's MOVE
(amend economics' assistant row to 125,132) inverts: the amendment would have
replaced a correct dyad number with a different population's count.

### FINDING 3 (arXiv 2610.12426 overstated; MIMESIS quotes byte-check): CONFIRMED

My two fresh fetches this sitting reproduce every element. 2610.12426:
title "Lyapunov spectrum of random neural networks", author David G. Clark;
AI sentence verbatim "This work was done in collaboration with the AI models
GPT-6 Astra and Claude Opus 5.5"; NO seed/ansatz mention; NO amplify/suppress
mention; the application sentence is "This result establishes that the chaos
in this network is extensive and gives access to diffeomorphism-invariant
properties of the dynamics", matching the lens's paraphrase at accuracy.md:94-95.
2610.09484: all five load-bearing quotes verbatim ("our 9B model achieves a
SOUL-Index of 65.7", "13 realistic behavioral patterns derived from real user
interactions", "Across eight environments, training with MIMESIS yields better
agent performance than training with GPT-5.5" holding "under all nine unseen
user simulators", the coach sentence, "simulator-generated private reasoning
traces"); v1 2026-10-07, v2 2026-10-08; NO affiliations shown anywhere, so
Meta SIL stays correctly OWED.

One narrowing the lens missed (see additions): the page DOES list ten author
names (submitted by Hoang Phan), so the OWED is affiliation-only, not
attribution-at-page-level.

### FINDING 4 (funded-lane hoarding byte-backed; probe needs no GPU): CONFIRMED

My independent sum reproduces every figure to the cent: 3,038 rows; lifetime
$94.74; anthropic $93.11 (claude-opus-5.5 $59.83 over 1,248 rows,
claude-fable-5.1 $18.30 over 418, claude-sonnet-5.5 $12.31 over 693,
claude-haiku-4.5 $2.67 over 672); z-ai/glm-5.3-prime 7 rows / $1.64 / last
call 2026-10-03T19:33:24.686865Z. Last paid row of any kind is exact:
sonnet-5.5, 49,942 prompt tokens, $0.0999, 2026-10-07T09:21:35Z. Both
falsifier conditions checked: no prime rows exist after 2026-10-03 (the
hoarding claim stands), and no rate card was read by me either (price
exactness stays OWED, as the lens itself scoped). Every hardware cite
byte-checks: lane_profiles.yaml:1 "RX 5600 XT actor pool (6 GB VRAM, AMD,
no CUDA)", :27-29 single 7B Q4 inference-only; w-selfplay-hardware_verify.md:14
"No consumer-GPU minimum exists anywhere published"; lora_pipeline.py:10-13
hands box 3090 "the local 24GB rung, $0 rent"; lora_pipeline.py:26-27
Qwen2.5-1.5B-Instruct "fits on 6GB with QLoRA 4-bit". The SPEND falsifier
quote byte-checks at RIB_DRIVING_LADDER_20260928.md:50.

One price nit (does not overturn): the ledger's own prime rows imply
~$3.5/M prompt + ~$6.2/M completion (59,476pt + 16,000ct = $0.3073;
29,948pt + 14,759ct = $0.2137), so a lean 30-turn session is ~$0.14-0.41
and a 30-to-100-session calibration spans ~$4 to ~$41: "single-digit
dollars" (accuracy.md:133-134) holds only at the lean 30-session end. The
lens scoped all prices as scale arguments, so this is a band to attach, not
an error to strike.

### FINDING 5 (spine, gap, realism meter, rubber stamp): CONFIRMED (scope upgraded by this pass)

Every cite byte-checks: ASTRA_V4_STATUS.md:5-6 spine verbatim
("harness_audit -> curator (sealed-first) -> validate -> QLoRA SFT ->
RS-DPO+HyPO -> GRPO+ACR/AVSPO -> budget-matched eval -> canary promotion");
astra-v4-converged-training-brief.md:28 reward law verbatim including
"clarification_zero" and "no learned reward model, no model-as-judge";
zknot_alarm.py:49-50 holds SELF_STEAL_RE / FORGOT_RE at exactly those lines;
memory/zknot/LATEST.md:3 meter row exact (last 7d 98 = 34 self-steal +
10 forgot of 448; target <75); LATEST.md:35-38 carries the redirection
register including "I don't understand" seems to be a trend haha at :38
("meet me where i am" is also real, at LATEST.md:209);
RIB_BEHAVIOR_CARDS_20260928.md:3-4 operator order verbatim, the 2026-10-05
MOUNTED AT BOOT amendment at :77+, and mag/rib_boot.py:84 mounts it;
ASTRA_REVIVE_VERDICT_20260926.md:28 gives T-SUBSTRATE window ~Oct 20 and
LEXICON Rocinante = 4x Mac Studio, Oct 27; harness.py:495 is exactly
"# Simulate operator confirm" setting AUTHORIZED inside test_scenario_3
(def at :478; the cited :479 is the docstring line, one line off, immaterial).

My QUANTIFIER-LAW attack on the absence claim ("the only operator simulation
in code") FAILED to break it and instead upgraded it: full-depth
`rg -il "simulat"` over mag/ tools/ configs/ scripts/ tests/ returns ~90
files, all game/cost/system/protocol simulators (campaign_simulator,
cost_simulator, k8s_water_sim, prefix_cache_sim, prospect_sim,
hydro_xor_sim, hero_simulation, game_emulator, race_harness, and kin) or
docs/tests; the counterpart-pattern grep (user.?sim|simulated.?user|
interlocutor|counterpart over mag/ tools/ configs/) returns five files, all
benign: agentic_test_steal.py:44 (a benchmark-description row for tau-bench,
not an organ), dissector.py (a "counterpart" VOICE classifier for pasted
debate respondents in operator input), duty_fuzz.py:94,451 (scenario
strings), thrash_meter.py:14 and quorum_window.py:13 (docstring/protocol
metaphors). The nearest thing to a simulated counterpart in the code tree,
mag/desk_local_simulator.py, is a deterministic stub that "Return[s]
protocol-shaped output" simulating the AGENT seat for Desk protocol tests
(docstring line 1), not the operator. No interlocutor organ exists in the
code tree at any depth.

One scoping note: "the clarification_zero term pays the agent for never
asking" is the natural parse of the term name, but the term appears exactly
once in the brief (the reward formula, brief:28) and is defined nowhere
else in the two scoped docs, so the "pays for never asking" reading is an
interpretation (the only sensible parse of a multiplicative factor named
clarification_zero, but the lens states it as fact without flagging the
inference, the exact phantom class its own finding 3 polices). Weakened by
nothing, scoped by this note.

## ADDITIONS (what the lens missed)

1. THE FINDING-2 INVERSION ITSELF (the highest-value miss): the correction
   was the artifact. Any downstream seat that had executed accuracy's MOVE
   would have overwritten economics' correct dyad number (role='assistant',
   ~9.63M tokens) with the agent_runtime population count (125,336 /
   ~14.85M tokens) containing ~20.3k subagent user-role parts. Evidence: the
   origin/role group-by census above; operations.md:30 + _tape_census.py:26-29;
   probe B rerun printing "assistant text parts: 0" for origin='assistant'.
   Falsifier: an economics-banked script surfacing a different stated filter
   that also returns ~104,809, or a db snapshot where role='assistant' parts
   sit below 104,809 (breaking the drift story). Move: revert the finding-2
   amendment in accuracy.md (correction header, not silent edit); economics.md:41
   names its filter; bank the agent_runtime count as its own labeled row:
   10 min, $0.
2. Filter-law for the tape db: the assistant half of the dyad exists ONLY as
   role='assistant' (origins are agent_runtime / real_user / NULL / system;
   there is no origin='assistant'). Evidence: the origin group-by (125,336 /
   19,026 / 132 / 3, summing to the same 144,497-part total as the role
   split 105,063 + 39,436 within rounding of NULL-role stragglers). Falsifier:
   a future db schema adding an assistant origin (the law then expires).
   Move: the tools/ tape-census script both lenses proposed should print BOTH
   group-bys (origin AND role) so a filter mismatch self-reveals instead of
   producing a confident wrong census: +5 min on the already-costed script.
3. The salon-vault blind spot resolves in economics' favor: recursive counts
   are exactly 19 files (watch/salon_responses, 3 subdirs) and 22 files
   (watch/salon_glm53), and watch/inbox/frontier_olm_2026-10-09 exists with
   lens/ steal/ sweep/ percolator_candidates.jsonl as economics.md:43-46
   describes. Evidence: find -type f | wc -l this sitting. Falsifier: none
   meaningful (a moment count on a live tree). Move: none; the blind-spot
   line can be closed.
4. Honest probe price band from the ledger's own prime rows: ~$3.5/M in +
   ~$6.2/M out implies ~$0.14-0.41 per lean 30-turn session and ~$4-41 for
   the 30-to-100-session calibration. Evidence: the two prime rows quoted in
   the finding-4 verdict. Falsifier: a quoted rate card contradicting the
   implied per-token prices. Move: put the band (not "single-digit") in the
   probe spec's spend gate before firing: 5 min, $0.
5. MIMESIS's OWED is narrower than stated: the arXiv page lists ten author
   names (Hoang Phan et al., submitted by Hoang Phan); only the AFFILIATIONS
   are absent. Evidence: my 2610.09484 fetch this sitting. Falsifier: a fetch
   of the paper body / author list showing Meta or SIL. Move: scope the OWED
   line to "affiliations not shown on abstract page": 2 min, $0.

## Not run (stated, not guessed)

- Paper bodies of 2610.09484 and 2610.12426 remain unread (my fetches were
  abstract-level, same as the lens's): SOUL-Index methodology, CSD mechanics,
  per-environment numbers, any AI-derived seed in the body, and the Meta SIL
  affiliation all remain OWED.
- No external verification of Open Env Arena or TensorFold "Living Weights"
  (rib-internal only, RIB_LIVING_WEIGHTS_BY_NATURE.md:7-9 and :22, both
  byte-checked as rib text).
- No simulator session and no paid API call fired by this pass either; all
  prices above are ledger-row-derived.
- The .agents/skills tree and docs/ specs were not part of the finding-5
  code sweep (its claim was scoped to code: mag/ tools/; mine widened to
  configs/ scripts/ tests/).
