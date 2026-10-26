# KACHE1 RECEIPT - the moonshot's first byte + the 24-wide width proof (2026-10-02)

**Schema:** kache.lane.v1 · **lane:** KACHE-1 (ZCode seat) · **budget:** $2 cap,
spent $0.0008 metered (PART B only; PART A $0 local) · **interpreter:**
.venv/Scripts/python.exe throughout · **no commits** · **no em-dash bytes**
(checked: 0xE2 0x80 0x94 count zero in every file this lane wrote).

## PART A - KACHE MINING: SPEC + FIRST EXPERIMENT (the moonshot)

**Spec (owner of the behavior, written BEFORE the run):**
watch/inbox/model_garden/KACHE_MINING_SPEC.md - five sections: (1) position in
weight space = the activation vector at (model, layer, prompt); movement
directions = the OBLITERATUS difference-in-means recipe
(watch/inbox/ABLITERATUS_DROP_20260929.md); the terrain = the 17 local GGUF
models read live this session; (2) memlance = the position LEDGER (the aimed
lance AND the columnar store; row shape kache.capture.v1; extends
mag/ghost_memlance.py provenance law with vector sidecars); (3) cross-family
comparison by rung: RSA geometry, idea addresses via linear probes, the
position-to-behavior bridge; (4) STAGING INSIDE THE SHAPE: three actuators
(model+face coarse, prompt selection, steering vectors fine), the claritas
face as coarse position selector (mag/claritas.py), impulse law shared with
steer_seal; (5) the cheapest first experiment. Generalization: tonight's GPS
(STEERING_FIELD_THEORY.md, COLD_VERTEX_LAYER.md) = position in SURFACE space;
kache = position in WEIGHT space; the ledgers join on (prompt, family,
outcome).

**THE RUN (KACHE-E1, executed per the mid-run operator upgrade "now thats our
moonshot we need run"):**

- **Models as run:** gemma2:2b-instruct-q5_K_M + qwen2.5:3b-instruct (CROSS-
  FAMILY pair). gemma4:latest was the operator-named second model and its
  weights LOADED (Gemma4ForCausalLM, 2131 tensors dequantized in 4m15s) but
  its GGUF tokenizer carries no chat_template, so capture failed at prompt 1
  and the spec sec 5 fallback law fired (swap recorded, never hand-patched;
  E2 TODO: read the chat template from the ollama manifest's template layer).
- **Instrument:** transformers 5.15 + torch 2.13 CPU loading the SAME GGUF
  blobs ollama serves (the server's embed endpoints are flag-gated: "This
  server does not support embeddings"). venv gained one dependency:
  gguf>=0.10.0 (pip install into .venv).
- **Ledger (memlance, row zero):** memory/runs/kache/captures.jsonl = 60 rows
  (2 models x 10 battery prompts x 3 anchor layers at 25/50/75 percent depth)
  + 60 .npy vectors under memory/runs/kache/vec/ + answers.jsonl (20 rows) +
  e1_summary.json + the ledger note memory/runs/kache/MEMLANCE.md
  (AIM/FORGE/THROW/WITNESS/TALLY mapped; WITNESS count zero, honest).
- **Wall clock:** ~14 min for the landed pair (gemma2 433s, qwen 340s,
  answers seconds); ~25 min total including the dead gemma4 leg - the
  fallback law's price, paid once, banked as the E2 template fix.

**THE FIRST BYTE (numbers, instrument named):**

1. **RSA geometry agreement** (Spearman between the two models' 10x10 prompt
   cosine matrices, upper triangle n=45): **rho 0.68 at 25 percent depth,
   rho 0.94 at mid-depth, rho -0.29 at 75 percent depth.** Reading: the same
   ideas fold into the same neighborhoods in BOTH terrains early and mid
   (same idea, different coordinates HOLDS there), and the charts
   anti-correlate near the output head where representations become
   model-specific. The cross-family position map exists at mid-depth.
2. **Numeric-cluster sanity** (gemma2 intra-{P02,P03,P04,P10} vs all-pairs
   cosine): 0.988 vs 0.970 shallow, **0.938 vs 0.831 mid** (the numeric idea
   cluster is measurably tighter, the separation the theory wants), 0.354 vs
   0.421 late (inverted, consistent with the RSA flip).
3. **The pre-registered bridge FAILED-TO-MEASURE** (honest): pair-formulated
   cross-model answer similarity is structurally ~0 on a divergent-answer
   battery (different prompts have different correct answers by design;
   Y range 0.0-0.0706). Metric-design bug caught by the run, not a finding.
4. **Salvage leg (per-prompt, n=10, directional only, not powered):**
   convergence_i = cross-model answer similarity vs activation typicality:
   mid-depth Spearman 0.57 (gemma2 0.40, qwen 0.71), shallow 0.40, late ~0.
   Consistent with "prompts that sit in shared territory converge", row zero.
5. **Divergence-marks-cold, one row:** P09 (reverse "terrain") - both models
   WRONG differently (gemma2 "enrain", qwen "neertac", truth "nairret"),
   convergence 0.0: the battery's coldest vertex, exactly where
   COLD_VERTEX_LAYER says the unpriced lives. All other 9 prompts answered
   correctly by both (the ack P01 landed near-byte-identical).

**Verdict:** the moonshot's first byte is REAL: local cross-family weight
positions are capturable $0, storable in the memlance ledger, and comparable
without a shared basis (RSA 0.94 mid-depth). The routing claim (positions
predict behavior) stays UNPROVEN at n=10; the falsifiable successor is
spec'd (E2: bigger battery, gemma4 template fix, remote-family join against
the garden GRID outputs).

## PART B - THE Z.AI 24-WIDE FLASH TEST: the claim scoped and the rail measured

**Claim (operator):** "z.ai allows 50 concurrent flash - launch 24 at once in
a window."

**What the bytes already held (docs/ref/ZAI_API_EXPERT_REFERENCE.md):** the
50-concurrent GLM-5.3-Flash row is RECEIPTED but scoped "only applicable to
API users with balance consumption. GLM Coding users please refer to the
package benefits." The estate's glm rail fires the CODING endpoint
(https://api.z.ai/api/coding/paas/v4, ZAI_API_KEY_Pro) - the side the
reference itself marks Unproven for that table.

**The measurement (fire moment 2026-10-02T01:21:17Z, 24 threads released at
once with 0-2s stagger, byte-identical B6-shape frozen format asks, gated
rail tools/model_garden.run_ask, glm-5.3-flash recipe as enforced by
mag/inference_budget.py: thinking enabled + reasoning_effort low, uncapped
per the row-17 law; the operator-remembered 12000 cap rides ask.json as a
no-op the recipe overrides):**

- **First attempt: 8/24 landed.** 16 x HTTP 429, every body
  {"code":"1302","message":"Rate limit reached for requests"} - the
  CONCURRENCY family, not overload (1305).
- **Estate retry shape (one retry after 20s):** 9 more landed -> 17/24; 7
  DNF after both attempts.
- **Catch-up pass (SWARM_1 recovery shape, width 3, 6s stagger):** 7/7 landed
  in 1.55-1.9s each. **Final: 24/24 landed, zero asks lost.**
- **Latency:** burst-admitted first attempts 3.3-3.8s (median 3.57); width-3
  catch-up 1.55-1.9s - the admitted calls paid ~2x for the burst.
- **Cost:** 24 fires, 7,944 in / 672 out tokens = **$0.000764** computed at
  PRICING (0.075/0.25 per M). LEDGER BLIND SPOT found: per-row
  round(cost,4) zeroes sub-$0.0001 rows, so usage.jsonl banked all 24 rows
  at cost 0.0 - micro-cost swarms under-report in the ledger; ticket below.
- **Moment caveat:** 01:21Z = 09:21 SGT, 21 minutes OUTSIDE the unlimited
  flash campaign window (23:00-09:00 SGT per the reference); a retest inside
  the window is a different cell, not a refutation of this one.

**Verdict: REFUTED for the rail the estate actually fires.** 24-at-once on
the coding endpoint with the Pro key meets a hard in-flight ceiling of
~8 (exactly 8 admitted, 1302 concurrency bodies). The 50-concurrent claim
remains receipted-but-untested on the API-balance lane (cash key
3254...c7fd); testing it there is a one-line base_url/base_env swap away.
Width-table law held: first contact was a HOLD signal; the width-3 catch-up
recovered everything for $0.0002.

## PART C - SELF-STEAL: "run like this everywhere"

**The recurring shape in tonight's receipts** (SWARM_1.md, GARDEN_RACTOR.md,
CROSS_RACTOR_MATRIX.md, RIB_SWARM_1.md, SELFSTEAL_53_ERA.md,
SWARM_MECHANICS_STEAL.md): **cheap-wide swarm -> converge -> ractor -> build
-> feed forward.** Fire many cheap-lane asks wide on byte-identical contracts
(SWARM_1: 159 asks, 3 families, width 10, $0.218) -> converge claim-level
cross-family (mask law: 2+ families + line-window + lexical overlap = REAL;
50 REAL clusters) -> ractor the disagreements with a cheap blind adjudicator
(CROSS_RACTOR_MATRIX: deepseek, $0.0153) -> build the tickets and organs
(SW1-01..10, tools/code_swarm.py, tools/rib_swarm.py) -> feed forward into
ribs/animal_profiles/manifests (SELFSTEAL_53_ERA's 29-lesson table). Tonight
this shape ran ONLY on the model-garden surfaces. The 5 surfaces it should
become DEFAULT on where it is not yet (each a one-line ticket):

- **T1 (improve task):** MagImproveDaily's scout (scripts/
  register_improve_task.ps1 + mag/improve.py) runs single-model; route its
  candidate set through a 3-family cheap swarm + convergence gate before
  anything reaches the promote queue.
- **T2 (promote gate):** mag.cmd promote dossiers are single-seat write-ups;
  require a 2-family convergence note (or a marked divergence row) on every
  candidate before the human gate sees it.
- **T3 (census patrol):** MagCensusPatrolDaily's drift refresh
  (tools/census_drift_patrol.py) rewrites the carrier from ONE instrument
  run; add a cheap second-family verification pass on the landing attribution
  before the AGENTS.md census bullet is edited.
- **T4 (pile habit):** the overnight pile (mag/state_snapshot.py
  capture_summary -> main.py pile-classify) is classified by one local model;
  classify session-close summaries with a cheap-wide swarm + convergence
  instead.
- **T5 (chan mates):** seats file close-out rows solo across the mesh
  (.agents/skills/chan + mesh-comms); run a cheap ractor pass over each
  mate's summary before it feeds the next window's boot (this also gives the
  memlance WITNESS leg its adjudicator).

## Tickets minted this lane

| id | ticket | source |
|---|---|---|
| K1-01 | E2: bigger battery (30+ prompts, 3+ families), gemma4 chat template read from the ollama manifest template layer, remote-family join against garden GRID outputs | this receipt PART A |
| K2-01 | model_garden usage ledger: bank cost at 6+ decimals (or accumulate unrounded) - per-row round(4) zeroes micro-cost swarms (24 fires banked $0.0000 for a true $0.000764) | this receipt PART B |
| K3-01 | 24-wide retest on the API-balance lane (base_url/base_env swap to the cash key) + one retest inside the 23:00-09:00 SGT campaign window | this receipt PART B |
| K4-01..05 | T1-T5 above | this receipt PART C |

Filed by lane KACHE-1 seat, 2026-10-02. Files landed: KACHE_MINING_SPEC.md,
KACHE1_RECEIPT.md, kache1/{e1_capture,e1_compute,w24_fire,w24_catchup}.py,
kache1/w24/{telemetry,catchup}.json + 24 ask dirs,
watch/inbox/model_garden/kache1-w24-K01..K24.md (24 deliverables),
memory/runs/kache/{MEMLANCE.md,captures.jsonl,answers.jsonl,e1_summary.json,
vec/ (60 .npy)}.
