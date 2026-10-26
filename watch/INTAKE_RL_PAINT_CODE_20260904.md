# INTAKE — "RL a coding model to paint" open reproduction (adithya_s_k X post)

Date: 2026-09-04 | Intake seat: zcode (research-socratic genome, L0 contract)
Item (verbatim): https://x.com/adithya_s_k/status/2095434194591924630?s=20

## ITEM
X post (2026-09-03T08:50Z) by Adithya S K (@adithya_s_k, Indian AI/dev-tooling poster):
"Wake up ppl / A complete Open Source reproduction dropped on @huggingface blogs /
Anyone now can 'RL a coding model to paint' / RL Envs + Dataset + Training Code everything"
— quoting Surya Narreddi (@kickingkeys, 2026-08-23): "You can just RL a coding model to
paint with javascript btw" (21s video). Follow-up reply (15h ago) links the blog:
huggingface.co/blog/train-to-paint-with-code — "Absolute Amazing work by @SergioPaniego !!"
PROVENANCE NOTE: the poster is not a neutral booster — the artifact repo lives under
github.com/adithya-s-k (his own GitHub). He is an author signal-boosting his own
reproduction; the tweet credits collaborators honestly (blog: Sergio Paniego; idea:
Surya Narreddi; p5.brush library: Alejandro Campos Uribe).

Primary source, ingested verbatim (WebFetch of the blog, pub 2026-09-03):
- Base model Qwen/Qwen3.5-35B-A3B (36B MoE), LoRA (--all-linear, bf16, grad ckpt).
- GRPO via TRL GRPOTrainer (8 generations/group); env = OpenEnv "watercolour-env"
  wrapping p5.brush rendering in headless Chromium + a "gate" that rejects cheats.
- Reward = 4 weighted terms: gate 0.05 (compiles/paints/no-cheat), length 0.05,
  pairwise VL judge (Qwen3-VL-30B-A3B-Instruct vs 4 refs from a 178-painting
  hand-rated pool), HPSv3 (open 7B preference model). Three mixes trained:
  judge-led (0.60/0.30), hps-led (0.30/0.60), hps-only (0.00/0.90).
- Compute: 1x H200; 18h for 60 steps, ~34h for 110; a step (8 rollouts) 15-18 min,
  70-80% of it software-WebGL rendering (69-96 s/render). HPSv3 on an a100 Space;
  env on a cpu Space; judge on Inference Providers quota.
- Open-sourced: repo 02-watercolour (training scripts), datasets
  watercolour-reference-pool (178 paintings + source sketches) and
  watercolour-rollows-* (rollouts), Spaces watercolour-env + watercolour-hpsv3,
  LoRA adapters watercolour-grpo-{hps-only,judge-led,hps-led}, gallery, trackio
  Spaces, CSV curves — all in the "Paint with Code" HF collection.
- Results: model paints watercolour hibiscus as ~150-line p5.brush JS. Mean group
  reward hps-only +0.13, judge-led +0.27, hps-led +0.24; paint coverage ~2x in judge
  runs; biggest gain = eliminating bad paintings; judge lifts the top end.
- Stated limitations (author's own): no human painting in the pool ("a real
  limitation"); one subject → homogeneous output; blind single-turn painting (no
  image feedback to the policy); infra failures entered reward as zeros (~1.5% of
  rollouts, worst 5.2%); model ignores shape-count instruction; "The pool is the
  bottleneck, and it is the part of the pipeline with no principled answer."

## RECEIPTS
- Whole conversation fetched via web_reader (root post + quoted origin tweet + author
  follow-up reply). No community notes retrievable. Threads law satisfied — not scored
  from the root alone.
- Blog fetched whole: huggingface.co/blog/train-to-paint-with-code (WebFetch, verbatim
  claims above). Guessed URLs 404'd first (train-to-paint, train-to-paint-with-trl) —
  exact slug found by search: /blog/train-to-paint-with-code.
- $0 EXISTENCE FALSIFIER RUN (this session, curl): api.github.com/repos/adithya-s-k/
  HuggingEnvs = 200; .../contents/02-watercolour = 200 (README 13.5KB present);
  huggingface.co/api/datasets/HuggingEnvs/watercolour-reference-pool = 200;
  huggingface.co/api/spaces/HuggingEnvs/watercolour-env = 200. The tweet's
  "everything" completeness claim: Supported.
- Not run: training code execution (H200-class), rollout CSV inspection, human rating
  of the gallery. THE CROP names who sits next.

## SCORE
F:3 P:3 C:4 W:2 N:4 = 16/25 — BUILD WINDOWED

## READ (the honest why)
FIT 3: docks to three live arcs — the QLoRA campaign's Oct-27 training arm (same
TRL/OpenEnv ecosystem; OpenEnv's own tutorial is GRPO-via-TRL), the shader/light-codec
arc (model writes ~150 lines of JS that paints = code-to-pixels, our visual corpus IS
this shape, 377 shader knots in chain), and the verified eyes receipt (their judge is a
VL model; ours read exact end-to-end). But nothing in live ops consumes it before CUDA
exists; it does not serve the Sep 20 proof deadline. PULL 3: their admitted #1
limitation — "the pool is the bottleneck... no principled answer" — is a problem the
fleet has already solved for its own domain: the signed chain, 52K shaders, and the
explore-228 signal tape ARE principled reference pools. COST 4: intake and falsifier
ran at $0; datasets/env/adapters are usable read-only today; any training run is
H200-class, Rocinante-gated. WINDOW 2: one day old, ecosystem moving fast
(delta-weight-sync, OpenEnv tutorials), but our consumption date is Oct 27 — filing
preserves the option, nothing decays before then. NOVELTY 4: RL-post-training over
visual taste on code outputs is corpus-absent (MAX_DISTILL is distillation, percolator
judges prompts not pixels) — and it CONVERGES with two filed organs: WHALE card 27
(alternating harness mixes around fixed weights; their judge-led vs hps-led vs hps-only
ablation is a harness-composition result, second lane arriving at the same organ), and
wedge class #3 "gate-pass ≠ alive" (their infra-failures-scored-as-zero-reward bug is
our named failure class, verbatim, in a different lab — repetition is emphasis).

## TRI-STATE
- "A complete open-source reproduction exists (RL env + dataset + training code +
  adapters)": SUPPORTED — blog verbatim + all four artifact endpoints return 200
  (receipts above).
- "Anyone now can RL a coding model to paint": DISPUTED as stated — compute-gated
  (1x H200 18-34h + an a100-class scorer Space); the fleet itself has no CUDA until
  Rocinante (Oct 27); "anyone" = anyone with a datacenter GPU. Evidence: blog compute
  section; memory: GLM 5.3-flash campaign "no CUDA → QLoRA Rocinante-gated".
- "RL over taste works": UNPROVEN beyond a narrow frame — rewards rose only in curves
  graded by the same VL-judge family used in training (circularity risk); one subject,
  blind single-turn, author admits no human paintings in the pool and no human
  preference validation. Narrow-frame honest version: "eliminating bad paintings via
  a gate + preference judge lifts mean reward on self-graded curves" — Supported.

## VERDICT (three verbs, exhaustive)
- BUILD — WINDOWED, docked to the Oct-27 training arm as an amendment candidate routed
  through the DRIVER (WHALE precedent: touches locked order, not self-executed).
  Candidate thesis: our corpus as the reference pool the pipeline lacks; HuggingEnvs
  shape as the env harness for signal-replay training.
- CALIBRATE — now, $0: their reward-design findings calibrate seed_percolator + gate
  v2 doctrine (gate kills hacks, pairwise judge lifts top end, learned scorer has a
  ceiling ~0.771, infra-failures must never enter reward — wire our WAL-before-side-
  effect law into any reward path).
- REMEMBER — p5.brush (Alejandro Campos Uribe) and the HuggingEnvs env library on the
  watch-list; possible lite-lane "dumb model with eyes judges paintings" dogfood
  surface for the dungeon, only if a consumer claims it.

## ROUTE
Card → intake register. BUILD dock → campaign driver (locked order owner, Sep 3-20
QLoRA campaign). CALIBRATE rows → percolator doctrine + gate v2 notes. Kill condition
(falsifiable, executable cold): if the published CSV curves show reward gain explained
mostly by gate/length terms rather than the aesthetic terms, OR a 30-pair human rating
(operator = calibrator, decimation doctrine) of gallery vs base-model output shows no
preference, the "RL over taste" claim is Disputed and the Oct-27 dock is dead.
[SOCRATIC] assumption attacked: "complete open reproduction ⇒ anyone can do it";
instrument: $0 existence probes of all four claimed artifacts + verbatim blog pull;
what survives: the artifacts are real and complete — the universality claim and the
taste claim do not survive at fleet-facing strength.
Two counters: FORBIDS any training-run spend or quota pull before CUDA exists / before
the Sep 20 proof deadline. PAID RENT: external confirmation of two fleet laws at $0
(wedge class #3; paired-preference judging) + a named answer to their stated
bottleneck (our corpus is the principled pool).
Receipt: artifact = watch/INTAKE_RL_PAINT_CODE_20260904.md; room row ready to commit:
{"kind":"intake.verdict","item":"x:adithya_s_k/2095434194591924630","score":16,"band":"BUILD WINDOWED","build":"windowed:dock-oct27-training-arm-via-driver","calibrate":"percolator+gate-v2-reward-design","remember":"p5.brush+huggingenvs-watchlist","tri_state":{"completeness":"Supported","anyone_can":"Disputed","rl_over_taste":"Unproven"},"receipt":"watch/INTAKE_RL_PAINT_CODE_20260904.md"}

## THE CROP
Not seen: the rollout CSVs and trackio curves (whether gate/length terms, not taste,
explain the gain); the full 02-watercolour tree and whether the training scripts run
as-documented; p5.brush itself unexamined; OpenEnv's wider env library unswept for a
signal-replay env fit; no human-preference rating of the gallery. Next chairs: the
campaign DRIVER (does the Oct-27 arm absorb the dock?), the salon economist (does any
RL-in-the-loop belong in the Sep 20 proof plan — current answer no), and the operator
as taste-calibrator on a 30-pair gallery rating if the dock ever activates.
