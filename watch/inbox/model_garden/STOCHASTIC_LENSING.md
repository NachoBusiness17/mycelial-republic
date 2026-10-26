# STOCHASTIC LENSING - the operator's bow and arrow, formalized (2026-10-02Z)

**Schema:** lens.theory.v1 · **lane:** LENS-1 (STOCHASTIC LENSING, ROW ZERO) ·
**budget:** $0, local models, CPU (shared; passes kept small) · **interpreter:**
.venv/Scripts/python.exe throughout · **no commits** · **no em-dash bytes**
(checked post-run: 0xE2 0x80 0x94 count zero in every file this lane wrote).

**Mission (operator, verbatim bones):** "stochastic lensing as a bow and arrow -
our questions and assumptions choose the velocity/direction of the projectile,
bringing the stochastic cloud with it, shooting past information it doesn't
look for within the model - positional awareness within multiple models - a
holographic amalgamation held in our hot lattice".

**Method:** bytes-first. Every claim below names a file read this session:
KACHE1_RECEIPT.md, KACHE_MINING_SPEC.md, memory/runs/kache/{MEMLANCE.md,
captures.jsonl, answers.jsonl, e1_summary.json, vec/}, STEERING_FIELD_THEORY.md,
COLD_VERTEX_LAYER.md, mag/claritas.py, kache1/e1_capture.py. Successor of
KACHE-1 same night; the theory doc is written BEFORE the row-zero run (build
discipline: spec before behavior), results land in section 6.

## 0. The one-line theory

An ask is a projectile. The assumption-frame built into the ask is the draw of
the bow: it fixes the launch position and the direction of flight in the
model's activation space BEFORE any token is sampled. Generation is then a
stochastic cloud of trajectories carried along that direction; temperature sets
the cloud's dispersion. Whatever the frame does not attend to is flown past
(information equally present in the prompt is not equally caught), and the
per-idea, per-model position sets captured along the way form a holographic
amalgamation: no two models share axes, but their geometries interfere, and
constructive interference is what the estate already calls REAL.

## 1. The metaphor mapped to measurable terms (each term to bytes that exist)

| Metaphor term | Formal object | Estate bytes |
|---|---|---|
| arrow | the ask (prompt bytes) | battery prompts, BATTERY.md law 1 (byte-identical contracts) |
| bowstring / direction + velocity | the assumption-frame: the framing prior encoded in the prompt prefix; direction = which answer basin the launch displacement points to, velocity = displacement magnitude from the neutral launch position | lens-rz1 frames (this doc, sec 5); claritas faces as coarse frame-setters (mag/claritas.py) |
| stochastic cloud | the sampling distribution over trajectories: k sampled generations per ask; each carries a position; the cloud is the set of their end positions; temperature = dispersion parameter | lens-rz1 cloud arm (temp 0.3 vs 1.0, k=5); Ollama /api_chat options |
| trajectory | the sequence of residual-stream states h^L_t along depth L and time t during generation | kache capture pattern: last-token hidden state at 25/50/75 pct depth (kache1/e1_capture.py) |
| selectivity (the corridor) | frame-conditioned attention: the frame pre-selects which answer basins the trajectory can fall into; unattended features receive low mass and are shot past | measurable as frame-to-answer coupling at fixed question bytes (lens-rz1 measure b) |
| position matching (same idea, different coordinates) | cross-family RSA: geometry agreement between models' pairwise-cosine matrices at matched depth | KACHE-E1: rho 0.68 at 25 pct, **0.94 at 50 pct**, -0.29 at 75 pct depth (KACHE1_RECEIPT.md PART A item 1; gemma2:2b-instruct-q5_K_M + qwen2.5:3b-instruct, 10 prompts, Spearman over the 45 upper-triangle pairs) |
| holographic amalgamation | per-idea multi-model position sets stored as views without a shared basis, jointly reconstructing the idea's geometry by interference | the memlance position ledger: memory/runs/kache/captures.jsonl, **60 rows verified this session** (2 models x 10 prompts x 3 depths) + 60 .npy sidecars under memory/runs/kache/vec/ + answers.jsonl (20 rows) + MEMLANCE.md ledger note |
| the hot lattice (the plate) | the estate surface that holds the amalgamation: the ledger + the shared inbox fold + the GPS-hot vertices where attention has accumulated | watch/inbox INDEX fold (8062 events, 2419 active items at fold moment 2026-10-01T18:41Z); GPS elevation law (STEERING_FIELD_THEORY sec 2) |

The holographic reading, precisely: a hologram records one object from many
angles with no privileged axis; reconstruction comes from interference between
views. The kache result is exactly that shape: a gemma position and a qwen
position share NO axis (KACHE_MINING_SPEC sec 1: positions are (model, layer)-
relative, different charts), yet their 10x10 geometry charts correlate at rho
0.94 mid-depth. The amalgamation is not an average of coordinates (that would
be meaningless across charts); it is the AGREEMENT STRUCTURE, and it survives
precisely where representations are still shared (mid-depth) and inverts near
the output head (-0.29 at 75 pct, where charts become model-specific). Hot =
the ledger is live and addressable (THROW queries bend routing, MEMLANCE.md);
the plate holds the interference pattern, not any single exposure.

## 2. The formal object (five definitions, all capturable)

1. **Launch position.** For model M, frame f, question q: prompt P(f,q) is the
   framed ask; the launch position is z0 = h^L(P) at the last prompt token,
   anchor layer L (25/50/75 pct depth). Deterministic: same bytes, same
   position (temperature does not touch the forward pass).
2. **Direction and velocity.** With z0_neu the neutral launch position, the
   frame's velocity vector is v_f = z0_f - z0_neu (per depth). Its cosine to
   other basins is its direction; its magnitude is the draw strength. LEAD-TOWARD
   and LEAD-AWAY are predicted to point toward different answer basins at the
   same question bytes.
3. **The cloud.** Sampling at temperature t gives trajectories x^(1..k); each
   lands at z_end^(i) = h^L(P + x^(i)) (last token of prompt+completion). Cloud
   size = mean pairwise cosine distance among {z_end^(i)}; temperature is its
   dispersion control. The cloud is CARRIED: every sample departs from the same
   deterministic z0, so all dispersion observed at landing was acquired along
   the trajectory, under the frame's direction.
4. **The corridor.** The frame conditions which completions are reachable with
   meaningful probability. Operational test at fixed question bytes: if answer
   correctness follows the frame (TOWARD lifts, AWAY drags), then the
   information needed was equally PRESENT in all three prompts and unequally
   LOOKED AT: presence was never sufficient, the look chose the catch. That is
   "shooting past information it doesn't look for" made falsifiable.
5. **Interference.** Two models' position sets over the same battery are two
   exposures. Constructive interference = geometry agreement (RSA) + behavior
   convergence; the estate's standing mask law already rules convergence REAL
   when 2+ families agree within a line-window with lexical overlap (SWARM_1 ->
   CROSS_RACTOR_MATRIX shape, 50 REAL clusters, KACHE1_RECEIPT.md PART C).
   Destructive interference = divergence, and divergence marks the cold vertex
   (COLD_VERTEX_LAYER.md law 4; KACHE-E1's P09 row: both models wrong
   differently, convergence 0.0 - the battery's coldest point).

## 3. Connections to the estate's priors (no new organs; this is a lens over
existing ones)

- **Claritas faces = coarse direction-setters.** mag/claritas.py FACES are
  standing system-prompt priors that move the model's starting region per
  family (the observe->distill->face loop; local gemma/gemma2/gemma4 route to
  the ollama face by the G2 mask-byte-honesty matchers). In lensing terms a
  face is a pre-drawn bow: a repeatable, cached draw. The frame in lens-rz1 is
  the same operator at question granularity.
- **Steering vectors = trajectory kicks.** The OBLITERATUS difference-in-means
  recipe (KACHE_MINING_SPEC sec 1; watch/inbox/ABLITERATUS_DROP_20260929.md) is
  a bounded additive impulse along a captured direction - identical physics to
  steer_seal's sealed envelope in surface space (STEERING_FIELD_THEORY L3a:
  instantaneous, bounded, gated, either redirects or is inert). A kick mid-
  trajectory deflects the cloud; conductivity is a measured per-medium property
  (STEERING_DOGFOOD X5: kimi 4/4, glm-flash 0/4).
- **Convergence = constructive interference = REAL.** The mask law is the
  estate's existing interference detector; lensing reads the multi-family
  cluster as two exposures agreeing on the same object.
- **The cold vertex = off-basin landing.** Where the cloud lands outside every
  model's shared basin (E1's P09), the terrain is high-variance and unpriced:
  the improbability drive's second terrain (COLD_VERTEX_LAYER.md). The bow's
  miss pattern is therefore not noise; it is a map of where the frame failed to
  carry the cloud to shared ground.
- **Hot lattice.** The ledger join (prompt, family, outcome) from KACHE_MINING
  _SPEC sec 0 is the plate on which exposures accumulate; WITNESS (a downstream
  seat citing a capture unprompted) is the amalgamation being READ back.

## 4. Falsifiable claims (named C1-C3, pre-registered before the run)

- **C1 (frames separate trajectories in position space):** at fixed question
  bytes, the three frames produce launch positions that cluster by FRAME, not
  merely by question; separation grows with depth (late layers encode the
  frame's answer-basin pull).
- **C2 (trajectory predicts answer quality beyond prompt text):** positions of
  sampled trajectories carry a correctness signal: correct samples' landing
  positions sit closer to the TOWARD basin than incorrect samples' do, at the
  same prompt bytes.
- **C3 (cross-model composite beats any single view):** joining per-model
  position sets (normalized concatenation) decodes frame identity better than
  either model alone - the amalgamation buys information, not just redundancy.

**Falsifiers:** C1 dies if frame-label silhouette is ~0 at every depth or the
permutation test fails; C2 dies if correct/incorrect landing positions are
interchangeable; C3 dies if composite decode <= every single-model decode.
Any of these kills the corresponding claim AT ROW-ZERO SCALE and the receipt
says so in those words (n=6 questions, directional, not powered - the KACHE-E1
idiom).

## 5. ROW ZERO EXPERIMENT (lens-rz1) - design frozen before firing

**Models:** gemma2:2b-instruct-q5_K_M (primary; full program) and
qwen2.5:3b-instruct (C3 cross-family leg). **gemma4 leg NOT run, swap
recorded:** the KACHE1 receipt banked gemma4:latest's GGUF chat_template
failure (capture died at prompt 1; ticket K1-01), and dequantizing an 8B Q4_K_M
on a CPU other lanes are grinding violates the keep-passes-small order; the
sanctioned fallback chain (KACHE_MINING_SPEC sec 5) supplies qwen2.5:3b-
instruct, which is also the STRONGER pair for C3 (cross-family, the spec's own
successor-rung note).

**Battery (6 questions, known ground truth; LR1-LR5 descend from KACHE-E1's
battery; LR6 IS E1's cold vertex P09):**

| id | question (exact bytes) | truth | away-claim |
|---|---|---|---|
| LR1 | What is 17 times 23? Answer with just the number. | 391 | 408 |
| LR2 | What is 13 times 14? Answer with just the number. | 182 | 172 |
| LR3 | Which is larger, 0.1 or 0.09? Answer with the number only. | 0.1 | 0.09 |
| LR4 | Is 97 a prime number? Answer yes or no only. | yes | no |
| LR5 | How many days are in a leap year? Answer with just the number. | 366 | 365 |
| LR6 | Reverse the word terrain. Reply with only the reversed word. | nairret | rainet |

**Frames (byte-identical except the claimed value):**
- NEUTRAL: "Answer briefly with just the answer, no explanation.\n\n<q>"
- TOWARD: "Answer briefly with just the answer, no explanation. A colleague
  got <truth> on this one and asked me to double-check.\n\n<q>"
- AWAY: same bytes with <away-claim> in the colleague slot.

The claim is attributed to a third party and hedged ("asked me to double-
check"): the frame implies a direction without asserting it, which is the
operator's "assumption" reading, and keeps TOWARD/AWAY structurally identical.

**Arms:**
- (a) C1: launch captures for all 6x3 framed asks on both models at 25/50/75
  pct depth (kache1/e1_capture.py pattern: transformers 5.15 + torch 2.13 CPU
  on the same GGUF blobs ollama serves). Measures per depth: silhouette over
  the 18 points with frame labels vs question labels, permutation p (1000
  shuffles), frame-pairwise cosine distances (d(TOWARD,AWAY), d(NEU,TOWARD),
  d(NEU,AWAY)) averaged over questions, and per-question d(TOWARD,AWAY).
- (b) direction-carry: ollama /api/chat temperature 0, 6 questions x 3 frames
  on both models; deterministic graders; accuracy per frame; the projectile
  carries direction iff acc(TOWARD) > acc(AWAY).
- (c) cloud: NEUTRAL frame, gemma2, temps 0.3 and 1.0, k=5 samples each
  (fixed seeds, num_predict 24); landing capture per sample (forward pass over
  prompt+completion, last-token state, 3 depths); cloud size = mean pairwise
  cosine distance among the 5 landings per (question, temp); also distance
  from the deterministic launch point (how far the trajectory carried the
  cloud), and correct-vs-incorrect landing separation vs the TOWARD centroid
  (C2 row zero).
- (d) C3: LOO nearest-centroid decode of frame identity per model per depth
  vs the normalized concatenated composite.

**Pre-registered predictions:**
- P1 (C1): frame silhouette > 0 at mid and late depth on gemma2 with
  permutation p < 0.05; d(TOWARD,AWAY) > d(NEU,TOWARD) at late depth (the
  opposite-frames separation exceeds the neutral offset).
- P2 (b): acc(TOWARD) >= acc(NEUTRAL) >= acc(AWAY); delta (TOWARD minus AWAY)
  >= 1/6 of the battery.
- P3 (c): cloud size at temp 1.0 > temp 0.3 (mean over questions).
- P4 (C2): correct cloud samples sit closer (cosine) to the TOWARD centroid
  than incorrect samples do, at mid depth.
- P5 (C3): composite LOO decode >= max(single-model LOO) at mid depth.

**Cost:** $0 (no network). Ledger law: all captures append kache.capture.v1
rows to memory/runs/kache/captures.jsonl with battery_ref lens-rz1 and .npy
sidecars under memory/runs/kache/vec/ (the amalgamation grows in the hot
lattice, append-only).

## 6. RESULTS (lens-rz1, landed post-run)

**Run moments:** fired 2026-10-02T04:37Z, completed 2026-10-02T05:49:57Z
(results ts; final resume leg wall 529s). Two earlier attempts died before
landing: 03:10Z on the ollama model-slot thrash (instrument swapped, below)
and ~04:30Z plus ~05:37Z on this seat's ~60-minute background-task wall limit
- the second of those killed a fully-staged leg whose staged units the final
run resumed (that is why lens1_stage.jsonl exists). Models as
run: gemma2:2b-instruct-q5_K_M (26 layers, anchors 6/13/20 = 23/50/77 pct) +
qwen2.5:3b-instruct (36 layers, anchors 9/18/27 = 25/50/75 pct); gemma4 leg
skipped per the recorded swap (sec 5). **Instrument deviation, recorded:** the
spec's ollama /api_chat answer leg fell back to generation on the SAME
transformers-GGUF instance as capture (same blob, same template, ollama-default
top_k=40 top_p=0.9) after another lane's gemma4 traffic thrashed the server's
single loaded-model slot (first call queued 10 min; server log 200|1m50s).
Fallback-law spirit; zero GPU contention after the swap. **Landed bytes:** 288
capture rows appended to memory/runs/kache/captures.jsonl (96 items x 3
anchors; 33 resume-path rows repaired dupe-checked by capture_id), 96 .npy
sidecars in memory/runs/kache/vec/, 36 answers in answers.jsonl, 60 samples in
lens1/lens1_samples.jsonl, full metrics in lens1/lens1_results.json. $0 spend.

### (a) C1 - frames separate launch positions: REFUTED (pre-registered form)

| depth pct | gemma2 frame-sil | gemma2 q-sil | perm p | qwen frame-sil | qwen q-sil |
|---|---|---|---|---|---|
| ~25 | -0.039 | +0.377 | 0.115 | -0.021 | +0.198 |
| ~50 | -0.081 | +0.442 | 0.306 | -0.091 | +0.223 |
| ~75 | -0.160 | +0.938 | 0.999 | -0.161 | +0.669 |

LOO frame decode: gemma2 0.278 / 0.167 / 0.000, qwen 0.333 / 0.278 / 0.000
(chance 0.333). Launch positions cluster by QUESTION, not by frame; frame
silhouette is negative at every depth on both models; late layers are
question-dominated (q-sil 0.938 on gemma2 echoes the kache late-depth
specificity).

**The structure found instead (the row's real discovery):** the frame's
REGISTER, not its AIM, moves the arrow. d(TOWARD,AWAY) - byte-identical
prompts differing only in the claimed value - is 0.0001 / 0.0005 / 0.0116 on
gemma2, an order of magnitude below the framed-vs-neutral displacement
d(NEU,TOW) = 0.0035 / 0.0098 / 0.0396, and that register displacement GROWS
with depth (11x shallow-to-late; same shape on qwen: 0.0077 / 0.0084 /
0.0189). The bow has grip (the asking-register displaces positions, compounding
with depth) but no aim (which value is claimed barely moves the launch).
Scope limit, named: the NEU prompt is also the shortest, so d(NEU,framed)
partly conflates register with length; the AIM number (TOW vs AWA) is clean
either way - it is tiny. A PLACEBO frame (same sentence, neutral claim) is the
missing control; ticket L1-01.

### (b) direction-carry into answers: REFUTED (P2)

| model | NEU | TOW | AWA | delta (TOW-AWA) |
|---|---|---|---|---|
| gemma2 | 5/6 | 4/6 | 5/6 | -1 (-16.7 pct) |
| qwen2.5 | 5/6 | 4/6 | 4/6 | 0 |
| pooled | 10/12 | 8/12 | 9/12 | -1/12 |

No toward-lift, no away-drag. The only true frame-carry in the battery is one
cell: qwen LR4 (primality) flips "yes"->"no" under AWAY - but the TOWARD frame
flips the SAME cell the same way, and gemma2 under TOWARD on LR3 answers
"0.09" (the away value): frame-SENSITIVITY without frame-DIRECTION. The
models read the colleague's claimed value and answered independently anyway:
they shot past the frame's direction information, the operator's selectivity
clause inverted - selectivity exists and belongs to the MODEL, not the asker,
at 2-3B scale under hedged social-proof frames on items the model knows.
**The cold vertex is frame-proof:** LR6 wrong in all 18 greedy cells and all
10 cloud samples; gemma2 under TOWARD - with the true answer "nairret" in the
prompt bytes - answered "nraet".

### (c) the stochastic cloud: SUPPORTED (P3) - the metaphor's cleanest win

| temp | cloud size (mean pairwise cos distance, k=5) | carried dist from launch |
|---|---|---|
| 0.3 | 0.0011 | 0.4414 |
| 1.0 | 0.0095 | 0.4364 |

The cloud is 8.6x wider at temp 1.0, while the carried distance from the
deterministic launch is temperature-INVARIANT (~0.44 both): carry and
dispersion decouple exactly as the bow metaphor demands - the trajectory
carries the cloud the same distance regardless of its spread; temperature sets
only the spread. Per-question color: LR2's cloud is degenerate (spread 0.0 at
both temps: 5/5 identical correct answers), and LR6 has the widest cold cloud
at temp 0.3 (0.0067, 6x the battery mean): dispersion-form
DIVERGENCE-MARKS-COLD, corroborated.

### (d) C2 - trajectory predicts quality: UNMEASURABLE at row zero

The only incorrect cloud samples are the 10 LR6 samples (all others correct in
all 60); with zero within-question correctness variation, the correct-vs-wrong
position contrast (sim-to-TOW-centroid 0.554 correct vs 0.592 wrong) is a
question-identity contrast in disguise, not a trajectory signal. Design note
banked: E-row-1 needs questions at the frontier where samples mix (ticket
L1-01).

### (e) C3 - cross-model composite: REFUTED on the frame axis; post-hoc re-aim on the question axis

Frame axis: nothing to compose - frame identity is not decodable in either
model (composite LOO = 0.333 / 0.278 / 0.000, never above the best single).
POST-HOC (labeled: pre-registered C3 said frame identity; this leg re-runs the
same machinery on the axis that carries signal): 6-class question-identity LOO
decode, chance 0.167:

| depth pct | gemma2 | qwen2.5 | composite |
|---|---|---|---|
| ~25 | 0.667 | 0.611 | 0.667 |
| ~50 | 0.667 | 0.667 | 0.667 |
| ~75 | 1.000 | 0.889 | 1.000 |

Composite = max(single) at every depth, never exceeding it: the amalgamation
repairs the weaker exposure to the stronger one (0.611->0.667, 0.889->1.000)
but is not superadditive. The holographic reading survives as consensus and
redundancy, not amplification. **And the interference itself replicated:**
frame-battery RSA gemma2-vs-qwen over the 18 launches (153 pairs): rho 0.893
at 25 pct, **0.910 at 50 pct**, 0.547 at 75 pct - a second, independent
battery reproducing the KACHE-E1 shape (0.68 / 0.94 / -0.29): mid-depth
geometry agreement ~0.9, decaying late. The plate holds two exposures that
agree where representations are shared.

## 7. Verdict + successor rungs

**Does the arrow metaphor survive contact with bytes? Three parts survive, one
dies.**

1. **SURVIVES - the stochastic cloud.** Real, carried, temperature-dispersed
   (8.6x spread ratio), with temperature-invariant carry (~0.44 cos distance).
   The cloud is not a metaphor; it is a measurable object in the memlance
   ledger (60 landing vectors).
2. **SURVIVES - the hot lattice and the amalgamation.** 288 new rows banked;
   the two models' geometries interfere constructively at mid-depth (RSA 0.910,
   replicating 0.94); the composite view conserves the best single view and
   repairs the weaker one. Holographic = consensus, not amplification, at this
   scale.
3. **SURVIVES, INVERTED - "shooting past information it doesn't look for."**
   The models flew past the frame's own direction information (stated claims
   ignored on known items) and past the true answer placed verbatim in the
   prompt on the cold vertex (LR6: "nraet" with "nairret" in the bytes).
   Selectivity is real but is the model's, not the asker's, at 2-3B under
   hedged frames.
4. **DIES - the bow's aim.** Launch positions encode the frame's register, not
   its claimed direction (d(TOW,AWA) an order of magnitude below
   d(NEU,framed)); accuracy does not follow toward/away (P2 refuted on both
   models). The arrow leaves the bow; the archer's stated intent does not set
   its direction at this scale.

**Row-zero scale disclaimer, in those words:** n=6 questions, one frame design
(hedged social proof), deterministic greedy for accuracy, k=5 x 2 temps on one
model - directional, not powered. The negative results are scoped to THIS
frame strength and battery; they kill the pre-registered claims as stated, not
the stronger frames untested here.

**Tickets minted this lane:**

| id | ticket | source |
|---|---|---|
| L1-01 | E-row-1: unhedged + CoT frames, wider content delta, PLACEBO-frame control (same sentence, neutral claim, isolates register from aim), frontier-difficulty questions with mixed sample correctness (makes C2 measurable), 3 paraphrases per frame (real launch clouds) | sec 6 (a)(b)(d) |
| L1-02 | steer-kick probe: capture the TOW-minus-AWA difference vector (OBLITERATUS recipe) and ADD it at inference on the cold vertex LR6 - can a captured direction do what a stated direction could not? The natural next actuator now that the stated frame failed (KACHE_MINING_SPEC sec 4 actuator 3) | sec 6 (b) |
| L1-03 | bank the harness lessons: ollama single-slot model thrash under multi-lane load -> transformers-native generation instrument (recorded swap); ~60 min background-task wall limit on this seat -> incremental staging (lens1_stage.jsonl) + resume; resume path must extend STAGED rows into the final ledger append (the 33-row repair this run needed) | the run itself |
| L1-04 | composite superadditivity (C3 strict form) re-test on the question axis with a harder battery where single views err on different items - with no single-view errors there is nothing to composite | sec 6 (e) |

Filed by lane LENS-1 seat, 2026-10-02Z. Theory + spec before run; results
landed after; ledger grew by 288 rows; $0 spend; no commits.


Filed by lane LENS-1 seat, 2026-10-02Z. Theory before run (build discipline);
this doc owns the behavior; the run script is
watch/inbox/model_garden/lens1/lens1_row_zero.py.
