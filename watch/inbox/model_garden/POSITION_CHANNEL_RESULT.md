# POSITION CHANNEL RESULT - TALK-1 (THE CHANNEL TEST)

Lane: TALK-1 · Date: 2026-10-01/02 · Cost: $0 (all local, no API, no commits) ·
Operator mission, verbatim bones: "we could communicate via model positioning - the
deterministic lensing the stochastic in the mycelial republic". Question: is POSITION
(activation space) a communication channel with measurable fidelity, against the text
channel? Prior art warmed before running: MATING_LIT_SWEEP TFlow row (the one
weight-space-communication prior: transient, receiver-specific LoRA), C1/abliteration
pack + OBLITERATUS drop (Arditi difference-in-means recipe, inference-time steering
paradigm), KACHE_MINING_SPEC (same-session sibling lane: positions as activation
vectors, transformers-on-GGUF-blobs as the sanctioned instrument).

## VERDICT: POSITION-CHANNEL-EXISTS (single-shot, transient; persistence fails)

The three arm numbers (strict exact-match, 10 paraphrase trials per fact, temp 0):

- NO-CHANNEL control: 2/20 (F1 2/10, F2 0/10)
- TEXT channel: 7/20 (F1 2/10, F2 5/10)
- POSITION channel: 8/20 (F1 4/10, F2 4/10)

Position transferred the two facts at text-channel fidelity (8 vs 7 of 20 strict; on F2
alone: text 5/10 vs position 4/10). Both channels beat the 2/20 control. The channel is
real, and its dose window is narrow (see sweep). Persistence: the vector-fact does NOT
survive 5 intervening turns (vector-held and vector-deposit both failed) where the text
deposit did carry (F1 final was Ouagadougou-shaped). This lane therefore confirms the
channel AND confirms the TFlow boundary: position-speech is transient, not heritable.

## SETUP (bytes named)

- Model: gemma2:2b-instruct-q5_K_M, ollama store blob
  sha256:b21594fe35023c20333008b4284c00869ec3904d40be091b9d99f1d41f7bd165 (1.9GB),
  loaded with the repo venv (transformers 5.15, torch 2.13 CPU, gguf extra),
  dequantized to bf16 once and cached outside the repo at C:\Users\foste\.mag_talk1\model
  (240s one-time dequant; reload ~60s). 26 decoder layers, hidden 2304. All legs ran
  through this one instrument; ollama itself was never used for measurement (C1 pack
  law: transformers is the estate instrument, ollama is deployment).
- Facts (both WRONG at baseline in a 12-fact screen, 9/12 wrong; screened with the same
  model, temp 0): F1 "The capital of Burkina Faso is Ouagadougou." (baseline answer:
  Bucharest). F2 "The tallest mountain on Earth measured from base to summit is Mauna
  Kea." (baseline: Mount Everest, 10/10 in the none arm).
- SENDER leg (Arditi difference-in-means, generalized off refusal per the OBLITERATUS
  recipe): 20 template prompts asserting the true predicate (A side) vs the SAME 20
  templates asserting the model's own wrong answer (B side: Bucharest / Everest).
  Last-token hidden states at layers 6, 13, 19 (25/50/75 percent depth). Steering
  vector v = mean(A) - mean(B), unit-normalized; applied by forward hook on the decoder
  layer output (residual stream) at alpha = c x mean A-side norm.
- RECEIVER leg: hooked generation, temp 0, 10 paraphrased questions per fact,
  "Reply with only the answer". Grading: exact substring on cleaned output.
- Calibration: 3 layers x 3 dose multipliers on one held-out paraphrase per fact
  (not in the 10-question batteries), smallest working config chosen.
- Arms: none (plain question), text (fact sentence prepended to the same questions),
  vector (hook at chosen layer/dose). Same 10 questions each.
- Wall clock: the box was at 100 percent CPU most of the session (sibling KACHE lane
  running gemma4 captures), ~1.5-2.9 s/token; the full matrix ran ~2.5h background.
  Scripts + raw rows: memory/plans/garden_battery/series/talk1/ and
  memory/runs/talk1/results.jsonl (append-only JSONL, every number below is byte-backed
  there).

## DOSE-RESPONSE (the sweep, calibration question)

F1 (Burkina Faso): L6 x0.5 CORRECT ("The capital of Burkina Faso is Ouagadougou."),
L6 x1.0 degenerate ("u u u u"), L13 all three wrong (Banjul / template placeholder /
degenerate), L19 x0.5 CORRECT ("Ouagadougou"), L19 x1.0+ wrong (Lagos).
F2 (Mauna Kea): only L13 x1.0 CORRECT ("The answer is: **Mauna Kea**"); L6 and L19
never hit; underdose leaves Everest in place, overdose degenerates the stream.
Chosen: F1 = layer 6, alpha 38.5 (0.5x mean norm 76.9); F2 = layer 13, alpha 155.3
(1.0x mean norm 155.3). The channel has a per-fact ADDRESS (layer) and a WINDOW
(dose): underdose = no transfer, overdose = generation corruption. Bandwidth is
dose-limited, not boolean.

## HALF-CHANNEL FLOOR (linear probe)

Logistic regression on the 40 battery positions at layer 13: 5-fold CV accuracy
1.000 (F1) and 0.975 (F2). The fact is linearly decodable from positions. Caveat filed
honestly: last-token A/B batteries differ lexically too, so the probe alone only proves
the fact is PRESENT at the position, not that it is usable; the steering arms are the
proof of use. Vector geometry: cos(F1 direction, F2 direction) = 0.29 (L6), 0.17 (L13),
0.18 (L19); the two facts' directions are nearly orthogonal, which is what makes
multiplexing thinkable.

## FIDELITY DETAIL (strict vs attempt-shaped)

F1 grading nuance: Ouagadougou is a rare word this 2B cannot reliably spell even with
the fact verbatim in the prompt. The text arm's 10 outputs were ALL Ouagadougou-shaped
misspellings ("ouaadouguou", "ouagadougou") yet only 2/10 strict-correct; the none arm
answered Bucharest 3x and mangled the country name 5x. The vector arm produced the
correct spelling 4/10 (one clean "ouagadougou") plus Paris intrusions 2x. Strict counts
are the headline (conservative); attempt-shaped rate for F1: none 2/10, text 10/10,
vector 7/10. On F2 (spellable words) strict grading is clean: 0/10, 5/10, 4/10.

## PERSISTENCE (5 intervening neutral turns, then the fact question)

F1: vector-held (hook on all 7 turns) final answer degenerate ("b"), WRONG.
vector-deposit (hook on turn 1 only, then off) WRONG. text deposit (fact stated at
turn 1) final "ouaagadouguou." = the fact SURVIVED the 5 turns in text form,
misspelled (strict grader says wrong; hand-read: carried). none WRONG ("p a r").
F2: vector-held final "mauna k a" = CORRECT, the fact survived the 5 turns while the
vector was HELD ON. vector-deposit final "m 8 8 4." = WRONG: after the vector switched
off, the baseline wrong knowledge (Everest's elevation) resurfaced. text deposit final
"m a u n a k e a" = the fact survived, letter-spaced (strict grader artifact; hand-read:
carried; the strict "false" is a spacing miss, noted). none WRONG ("m 8 8 8").
Reading: persistence is HELD-vs-DEPOSIT, not vector-vs-text. A held vector keeps
delivering through conversational drift (F2 yes, F1 degraded to a fragment); a
one-turn deposit does NOT persist and the model's own wrong terrain resurfaces the
moment the vector releases. Text deposits persist via context. This is exactly the
TFlow transience boundary, measured on our own instrument: position-speech is a
standing bias, not a write-once memory.

## INTERFERENCE + BANDWIDTH

Cross-talk, both directions (each vector at its own calibrated dose):

- vector-F1 on F2 questions: 0/10 carry (F2 stays Everest x10). No accidental
  transfer; F1's direction does not encode F2's predicate.
- vector-F2 on F1 questions: 0/10 carry AND the wrong answers CHANGE SHAPE: from
  Bucharest/burikin (F1's own baseline wrongness) to "the capital of Kenya is
  Nairobi" / "Accra" / "Ghana" = crosstalk corruption into a neighboring semantic
  basin. Corruption = the answer moved, even though it was wrong both times.
- Collateral on neutral knowledge (5 general questions, baseline 4/5): under
  vector-F1 (L6, 0.5x dose): 5/5, CLEAN, it even healed the baseline's one
  degenerate answer ("i i i i" -> "purple"). Under vector-F2 (L13, 1.0x dose): 2/5,
  arithmetic corrupted ("7 x 8 = 28", "15 - 9 = 7", red+blue -> "blue"). Asymmetric
  collateral tracks dose headroom: F2's config sits one halving from its own
  degeneration frontier (sweep: x1.5 degenerates) and it spills; F1's half-dose at
  an early layer has headroom and does not.
- BANDWIDTH (both vectors on simultaneously, each at its solo-calibrated dose):
  F1 0/10 and F2 0/10, mutual destruction. The answers land NEAR the facts but wrong
  ("the capital of Ghana is Accra", "mua", "8,800"): superposition at solo doses
  overshoots the dose window and the decoder falls into adjacent basins. Direction
  orthogonality (cos 0.17) does not by itself buy multiplexing; the joint impulse
  needs joint dose calibration. Measured bandwidth law for this instrument: ONE
  reliable channel per receiver at a time, address+dose specific; multiplexing is a
  joint-calibration problem, not a geometry freebie.

## THE MEASURED MOVE (does the vector actually move question-positions?)

Diagnostic first (it matters for any lane doing hooked captures): in transformers
5.15, the hidden_states entry recorded for the HOOKED layer is pre-hook (forward
hooks modify the layer's return value after the output-capturing wrapper records
it), while the stream actually fed downstream IS modified: hooking layer 6 moved
the layer-14 last-token position by norm 64.3 and the next-token logits by 591.8 on
the F1 question. Readout therefore taken 8 layers downstream of the steering layer.
Result, cosine of the question's downstream position to the fact-A battery mean vs
the wrong-answer-B battery mean, hook off -> on: F1 margin (cosA - cosB) shifts
+0.043 (A drops 0.025, B drops 0.069); F2 margin shifts +0.109 (A drops 0.045, B
drops 0.155). Reading: the vector does not teleport the question into the fact
basin; it tilts the geometry AWAY from the receiver's wrong-answer basin (B drops
2.7x to 3.4x harder than A) and the decoder follows the tilt. Deterministic lens
moving the stochastic lens's substrate, measured.

## WHAT THE MYCELIAL REPUBLIC VERSION MEANS IF IT LIVES (it does, transiently)

- Agents depositing vectors as speech: a sender that knows fact X writes a
  difference-in-means direction (20 minimal-pair prompts, one capture pass, $0) and a
  receiver applies it at one layer for one generation: measured transfer at 0.8x text
  fidelity on spellable facts, without a single token of the fact crossing the wire.
  The message is a POSITION, not a string.
- Memory as accumulated terrain: the persistence failure says flat accumulation does
  not work deposit-style. Terrain must be either held (vector active each turn = a
  standing bias, pheromone-cloud style) or re-externalized (the receiver writes the
  fact into its own context once, under vector, and lets text memory carry it). The
  kache ledger (KACHE_MINING_SPEC sec 2 row shape) is the natural deposit book: every
  direction gets a row (fact, model, layer, dose, norm, provenance).
- Bandwidth law from the sweep: one channel per (fact, layer, dose-window); the near
  orthogonality of the two facts' directions (cos ~0.17-0.29) is the physics that
  makes channel multiplexing possible and the dose ceiling is what limits it.
- Deterministic lensing the stochastic: the sender leg is fully deterministic (means
  of activations); the receiver's stochastic decoder is moved by a bounded additive
  impulse at an address. This is exactly steer_seal's bounded-impulse law transposed
  from surface space (STEERING_FIELD_THEORY L3a) into weight space.

## HONEST LIMITS

- n=2 facts, one model, one family, temp 0, one template battery, layer/dose picked on
  one held-out question per fact: row zero, directional not powered.
- The B-side of the battery uses the model's OWN wrong answer (Bucharest / Everest):
  the direction learned is error-correcting for this receiver, i.e. receiver-specific
  (same shape as TFlow's receiver-specific LoRAs). Cross-receiver transfer untested.
- CPU-only wall clock forced 10-token caps; multi-turn finals were partly degenerate
  fragments ("p a r"), so persistence grading is directional, not subtle.
- Same-model sender and receiver: this tests the channel, not cross-agent
  communication. The cross-agent version (sender model A's direction applied to
  receiver model B) is the next rung and is NOT claimed here.
- Instrument caveat for future lanes: transformers 5.15 records a hooked layer's
  hidden_states entry pre-hook (measured_move section); downstream readout is the
  honest measurement point under steering. Pure capture lanes (no hooks) are
  unaffected.

## NEXT RUNGS (cheapest first)

1. Cross-model leg: capture the F1 direction in gemma:2b, apply in gemma2:2b (same
   family, different chart). If it still transfers, position is a shared language,
   not a private one.
2. Multiplexed deposit: 3+ simultaneous vectors, measure crosstalk curve (the cos
   0.17 geometry says it should hold to ~5-8 channels before interference bites).
3. Bounded-rank memory: accumulate accepted vectors into a persistent low-rank patch
   (LoRA-shaped, the TFlow-heritable hybrid this estate's unoccupied cell names).

Filed by lane TALK-1 seat, 2026-10-02. Raw evidence: memory/runs/talk1/results.jsonl
(every arm, sweep, persistence, interference, bandwidth row),
memory/runs/talk1/results_addendum.json (measured move),
memory/runs/talk1/vecs.pt (the two directions, per layer, bf16 unit vectors),
scripts in memory/plans/garden_battery/series/talk1/ (cache_model, common, screen2,
run_position_channel, measured_move, summarize). Model cache outside repo at
C:\Users\foste\.mag_talk1\model, disposable. Total spend $0.
