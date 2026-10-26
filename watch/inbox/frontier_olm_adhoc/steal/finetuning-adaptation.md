# STEAL CARD: finetuning-adaptation (frontier_olm_adhoc)

source-fetched: adhoc · seat: steal-finetuning-adaptation · moment: 2026-10-11
Inputs: 8 confirmed finds from the 2026-10-10 sweeps (3 reddit-door, 5 arxiv-door),
delivered by the round-1 ask with overlap verdicts attached. Source docs read this
session: watch/inbox/frontier_olm_adhoc/sweep/finetuning-adaptation-arxiv.md and
watch/inbox/frontier_olm_adhoc/sweep/finetuning-adaptation-reddit.md.

## The steal (one mechanism, not a link dump)

Adaptation is a gated and verified serving path, not a training run. The estate's JIT
fine-tuning law (memory/rib/RIB_TEN_MINUTE_SELF_20261010.md:24-28) already says feeding
is timed delivery; the frontier finds add the four organs any fold lane must have or it
silently degrades:

1. SELECT the supervision, not just the corpus. DIAL-OPD: token selection beats
   teacher scale (a 4B teacher with selection beats an 8B without, up to +1.76; random
   80% retention beats 100% on a 0.6B student) because low-agreement tokens soak 49.8%
   of reward while hindering learning (sweep doc lines 150-160). SGUID: fewer than 25%
   of retrieved skills carry signal; 6 selected skills match banks up to 11x larger, and
   a second co-evolution round DEGRADES without selection (Qwen3-4B HMMT25 -0.3 naive
   vs +1.1 selected; sweep doc lines 162-168). This is the rib's dead-salmon curation
   rider (RIB_TEN_MINUTE_SELF_20261010.md:50-51) with published numbers: curation is
   the difference between a loop that compounds and one that degrades.
2. GATE the invocation with a price. Agentic-TTT: without an explicit compute penalty
   the learned policy OVERUSES test-time training; a moderate penalty cuts compute
   about 30% while utility RISES (0.256 to 0.510 on Qwen2.5-7B; sweep doc lines 51-59).
   The estate's 03:00Z drain law (AGENTS.md:34) in weight-space form: adaptation
   without a priced valve is a drain.
3. VERIFY the serving leg. MedGemma oncology tune: merging the r=64 adapter at nominal
   scale lost most of the tune (83.8% output agreement; alpha=32 gave 93.2%) and bf16
   merge rounding erased 17-37% of delta elements (sweep doc lines 56-69). Replicated
   synthetically this session on CPU, see probes below: the erasure class is real at
   estate scale. A tune that dies in the merge is spend theater at the serving layer.
4. COMPILE the shed context. aTTT falsifier-2 clearance: the SAME update text scores
   54.3% as an adapter update vs 49.3% as in-context injection (below the 50.7%
   baseline) on Qwen3.5-9B ALFWorld; TT-SI independently: fine-tune 72.43% vs ICL with
   the same generated examples 68.36% (sweep doc lines 77-86). Under matched food,
   weights beat prompt because context is the scarce resource on long horizons. DPPM
   prices the compile door: a frozen hypernetwork compiles session history into LoRA
   adapters in ONE forward pass (no per-segment optimization), beating Full Context
   (+21.26 PersonaMem-v2) and Mem0 (+11.30 PrefEval) while running 62.7x faster than
   Full Context at flat 7.8 GiB (sweep doc lines 135-148). That is the ASTRA-class door
   RIB_LIVING_WEIGHTS_BY_NATURE.md:17 names, now with a cost ladder.

## Estate organ map (each find to the organ it feeds, concrete port move)

- MedGemma merge-scale discrepancy (reddit 1wywscq) -> mag/lora_pipeline.py (the LoRA
  training organ: config at mag/lora_pipeline.py:218, script gen at :298, status at
  :497; it has NO merge or serve-verification leg today) + mag/unsloth_seat.py:1-4
  (the Unsloth GPU seat the discrepancy was observed under). PORT: before any estate
  adapter is trusted, run a merge-fidelity check (bf16-merged vs fp32 delta element
  survival) plus an output-agreement probe (adapter-served vs merged on fixed probes);
  the JIT law's serving leg is adapter-only or verified-merge, never blind merge.
- MOLT fit tests + base-vs-adapter eval (reddit 1wyvc8k) -> mag/improve.py promote lane
  (promote_apply at mag/improve.py:2744, human gate at :2747, auto-promote refused at
  :2595). PORT: add two first-class gate rows to the candidate eval before
  promote --apply: (a) pre-run fit test (VRAM/thermal/microbatch sweep predicted
  against actual), (b) base-vs-adapter eval on a frozen quiz (the MedGemma post's
  paired McNemar on a frozen item set is the rigor template; 4B 56.0 -> 71.6 in 2h39,
  sweep doc lines 56-69).
- AgileRL Arena manifest validation (reddit 1wdjk0y) -> corpus/CURRICULUM.md:85-88
  clone queue (trl first, verl second per sweep RQ3) + mag/lora_pipeline.py:218
  generate_training_config. PORT: validate every training manifest with a schema
  (Pydantic-class) BEFORE any GPU minute; bad configs must fail in milliseconds, not
  40 minutes in. The find's verbatim: "Validation is Pydantic, so bad configs fail
  before training instead of 40 minutes in."
- aTTT (arxiv 2607.03441) -> the JIT law card itself,
  watch/inbox/frontier_olm_adhoc/lens/burns.md:119 (the aTTT row; the
  fine-tuning-JIT law mention sits at :82; REV-2 fix: the round-1 anchor :103 was
  wrong, that line is a FREE-RESOURCE SCOUT commit-log row, verified by sed) +
  RIB_TEN_MINUTE_SELF_20261010.md.
  PORT: stamp the published bound onto the card so fold designs target the right
  regime: latency is solved (sub-100 ms hot-swap via vLLM runtime LoRA API, 1.9x
  wall-clock, K=5-step cadence; sweep doc lines 33-49), the ten-minute budget is 4
  orders loose, and the bound is that aTTT "mainly preserves existing competence
  rather than teaching new abilities" with the smallest model gaining least - feed the
  workers (gemma4-class), not the scut (gemma:2b), per the rib's own tier law.
- Agentic-TTT (arxiv 2610.12002) -> the invocation gate. Organs: the improve lane's
  human gate (mag/improve.py:2744) for fold promotion, and the flow-pricing organ
  mag/water_graph.py:11-12 (waste basin holds overflow; routing as physics) as the
  shape for pricing adaptation calls. PORT: when the fold lane exists, every adapter
  fold invocation routes through a priced valve (a lambda penalty on the water-graph
  line), never always-on; the published result says the penalty PAYS for itself
  (compute down ~30%, utility up).
- DPPM (arxiv 2610.11776) -> mag/context_pack.py shed ledger (PACK_OFFLOAD_FILE at
  mag/context_pack.py:17, tolerant reader read_pack_offload at :266, stub listing at
  :326) + RIB_LIVING_WEIGHTS_BY_NATURE.md:17 (ASTRA door). PORT: the pack's shed
  volume IS the demand meter for the context-to-weights compiler; when shed chars per
  session trend up, the DPPM shape (frozen hypernetwork, one forward pass, no training
  loop at serve time) is the port, and it must keep the estate's two-tier form (living
  ledger, receipt-backed - RIB_LIVING_WEIGHTS_BY_NATURE.md:9).
- DIAL-OPD (arxiv 2610.11659) -> mag/percolator.py (partition into signal/theater/noise
  at mag/percolator.py:213-223, noise file writer at :342-344) as the corpus-selection
  organ the fold feeds from. PORT: when building the pitfall-bypass corpus, weight
  supervision toward the fix hunk (pitfall-adjacent tokens), not the whole commit; a
  small local teacher with selection beats a big dumb one.
- SGUID (arxiv 2610.12367) -> the same percolator + the fold's skill bank. PORT:
  re-SELECT the pitfall/skill bank each fold round (percolator's
  repeatables-to-invariants compile is the selector); never append-only, because round
  2 without selection degrades (sweep doc lines 162-168).

## Probes RUN this session (receipts, not claims)

1. Synthetic bf16 merge-erasure bench (the MedGemma class, at estate scale, CPU,
   $0). Command: ./.venv/Scripts/python.exe with torch 2.13.0+cpu. REV-2 ENV
   CORRECTION (round 1 falsely claimed the venv "also holds numpy 2.4.6,
   transformers 5.15.0, peft 0.21.2"): numpy and peft are ABSENT (import fails
   for both; torch itself warns "Failed to initialize NumPy"), transformers
   5.15.0 is pip-installed but NOT importable while numpy is absent, and
   safetensors 0.8.0 is present and importable (all verified by import this
   session). The synthetic bench needs none of the missing packages (pure torch),
   which is why it ran and replicated. Setup: 2560x2560 gemma-4B-class
   weight, W ~ N(0, 0.02) (absmean 0.016), LoRA r=64 alpha=32 (the post's config,
   scale 0.5), adapter factors A std 0.008, B std swept. Metric: fraction of positions
   where bf16(W+delta) == bf16(W) exactly, i.e. the merge changed nothing there.
   Result at B std 0.008 (delta absmean 2.04e-4): 13.64% of delta elements erased.
   Sweep: B std 0.002 -> 41.45% erased, 0.004 -> 25.16%, 0.008 -> 13.69%, 0.016 ->
   7.05%, 0.032 -> 3.52%. The MedGemma 17-37% band sits inside this sweep; the
   erasure class replicates at estate magnitudes and is strongly adapter-scale
   dependent: SMALL trained adapters lose the most to a bf16 merge.
2. Shed-ledger demand-meter read (the DPPM mapping's ground truth). Command:
   ./.venv/Scripts/python.exe -c using mag.context_pack.read_pack_offload(tail=None)
   and list_shed_stubs. watch/inbox/PACK_OFFLOAD.jsonl on disk: 7.7 MB, 35,974
   readable rows + 1 torn row (line 13499: non-UTF8 bytes, tolerated with a note by
   the reader at mag/context_pack.py:266), spanning 2026-09-28T07:12Z to
   2026-10-09T00:18Z. v2 stub rows with per-stub chars exist for ONE day only
   (2026-10-08): 691 stubs, 858,048 chars total (build 229,877 / route 199,230 /
   plan 190,628 / audit 169,244 / janitor 69,069). Two honest estate findings: (a)
   the demand meter has a single day of v2 data then goes dark - the instrumentation
   gap is itself the first thing to fix; (b) the ledger carries one torn row, and the
   tolerant reader already handles it (the nothing-lost law holds, but the tear is
   worth a patrol look).

## The falsifiable probe for this week (cheap, decisive)

Merge-fidelity + agreement bench on a real adapter. On the next adapter the estate
trains (mag/lora_pipeline.py output) or any public small LoRA adapter: (a) elementwise
bf16-vs-fp32 merge survival of the delta (the synthetic bench above, run on the real
tensors, minutes on CPU); (b) identity-probe agreement: 20 fixed probes answered by
adapter-served weights vs merged weights. Falsify: if merged outputs agree >=99% with
adapter-served outputs AND delta survival is >96%, the MedGemma discrepancy does NOT
replicate in the estate stack and verified-merge is safe; if agreement <95% or
survival <90%, the JIT law's serving leg must be adapter-only (vLLM runtime-LoRA
  class, per aTTT) and blind merge is banned from the fold lane. REV-2 PROBE
  REWRITE (round 1 said "the venv already has torch+peft": false, peft and numpy
  are absent): leg (a) merge-fidelity reads the adapter's adapter_config.json
  (stdlib json) and adapter_model.safetensors via safetensors.torch.load_file,
  then does delta/merge/survival math in pure torch. This path is VERIFIED LIVE
  this session: a hand-written safetensors file round-tripped through load_file
  with maxdiff 0.0 and no numpy anywhere in the process. Leg (b)
  output-agreement needs a serving stack (peft/transformers, or an Ollama
  GGUF-merge path) and stays blocked until the venv is repaired; that repair is
  the venv owner's call, logged here rather than silently made by this seat.
  Cost: leg (a) minutes, $0, torch+safetensors only.

## OWED (never asserted as done)

- The repo-wide search for an existing on-disk LoRA adapter (adapter_config.json /
  *.safetensors) was started and stopped before completion (the find over the whole
  tree exceeded the command budget); no real-adapter bench ran, only the synthetic one.
- The MedGemma ~2x effective alpha/r scale claim under Unsloth remains unverified
  (the author's own open reproduction request; probe script in Zenodo
  10.5281/zenodo.23134374; one seed, no CV, versions outside declared ranges).
- The Agentic-TTT compute-penalty port names mag/water_graph.py as the pricing shape;
  no valve was implemented this session - mapping only.
- v2 shed-stub instrumentation continuity (why 2026-10-08 is the only v2 day) was not
  diagnosed, only measured.

## Overlap verdict (from the round-1 ask's find rows, all run by the sweep seats)

- MedGemma 1wywscq, MOLT 1wyvc8k: 0 catalog hits on catalog/catalog.jsonl at
  card time; genuinely new. REV-2: AgileRL 1wdjk0y's "genuinely new" is WITHDRAWN
  as overstated: it sat in the 10-04 ranked candidate pool, not deep-read
  (watch/inbox/frontier_olm_2026-10-04/sweep/finetuning-and-adaptation-reddit.md:44,
  verified by sed this round); the find's Pydantic-validation detail is the new
  part.
- aTTT 2607.03441: 0 catalog rows at card time; only the sweep session's own
  trajectory steps. REV-2: a catalog re-read TODAY returns 3 rows, all this
  sweep's own fetch byproducts under frontier_olm_adhoc/sweep/
  (_ft_2607.03441.html, _ftread_2607.03441.txt, _ftfull_2607.03441.html), not
  prior holdings; future overlap greps must exclude own-byproduct rows or they
  will misread as prior banks (grep re-run this round).
- Agentic-TTT 2610.12002: REV-2 CORRECTION, round 1's "stub row only" verdict was
  false: the 10-10 bank HELD it and deep-read it that session
  (watch/inbox/frontier_olm_2026-10-10/sweep/finetuning-adaptation-arxiv.md:28-33,
  catalog id 6ae1751acd00); the adhoc numbers (0.256 to 0.510, the ~30 pct
  compute cut, the overuse finding) are genuinely new depth, that bank carries
  none of them.
- DPPM 2610.11776, DIAL-OPD 2610.11659, SGUID 2610.12367: one automated-ingest
  stub row each (state/arxiv/2026-10-09/<id>v1.txt, abstract only); verified this
  round that the 10-10 bank carries no rows for these three (grep of that bank,
  zero hits); the full reads and this estate mapping are the sweep's and this
  card's.
- REV-2 methodology note: this round-1 section grepped catalog only, which
  violates the run's own standing law (watch/inbox/frontier_olm_adhoc/DIGEST.md:31:
  frontier overlap checks must also grep watch/inbox/frontier_olm_* and
  frontier_olm_adhoc, because catalog + memory/ cannot see untracked sweep prose);
  the corrections above are what that omission hid.

---

# ADDENDUM (round 2, same day): the HN-door finds, 5 items

seat: steal-finetuning-adaptation · moment: 2026-10-11 · The round-1 card above
(8 finds, arxiv+reddit doors) stands untouched; this addendum banks the 5 HN-door
finds delivered confirmed by the round-2 ask. Amended, not rewritten (nothing-lost
law, RIB_TEN_MINUTE_SELF_20261010.md:18-20). Provenance of the find material: the
ask's confirmed rows, cross-consistent with the adhoc sweep seat's own banked items
in watch/inbox/frontier_olm_adhoc/sweep/finetuning-adaptation-hn.md ("Banked items"
section; that doc's Pass 2 note says the raw fetches are on disk under _ft2_*). I did
not re-fetch the five URLs this session; every repo path:line below I read myself.

## The steal this round (one mechanism, not a link dump)

Adaptation moves are gated swaps. The estate's standing position is living ledger +
frozen weights (RIB_LIVING_WEIGHTS_BY_NATURE.md:9); these five finds supply the gate
stack any weight-side or assignment-side move must pass, and every gate is already
running in production somewhere public:

1. ROUTE on semantic entropy at janitor scale, never token entropy (arxiv
   2609.20824: token entropy is measured blind below 3B, 91 pct of dataset-model
   combos; the working signal is multi-sample + cluster-by-meaning, worth up to
   +50pp routed, and the climb target should be cross-family: +22.0 pct vs +6.8
   same-family).
2. SWAP models or adapters only on a pre-registered non-inferiority verdict
   (illate/parity: paired bootstrap, 10k resamples, same items both models, margin
   agreed before results, PASS/FAIL/INCONCLUSIVE, INCONCLUSIVE means label more and
   never guess, exit 0 only on PASS).
3. REFINE supplemental state as small evidence-backed amendments over an immutable
   base with snapshot rollback (Prime Agent /refine: never rewrites the base system
   prompt; snapshots support rollback), which is the estate's amend-never-rewrite
   law returned to us as a competitor's contract shape.
4. TRAIN on a peer box, SERVE on the weak box, promote only on no-regression
   (ASTRO on a Pi 5: LoRA trained on an RTX-4060-class peer, served on the Pi,
   promotion only after tools/chain/chat gates pass with no regression vs baseline).
5. INSTRUMENT retention before intervening (Learner 1.0 ten-skills: per-skill
   held-out panels scored at own-teach AND every later checkpoint, plus a base
   sentinel battery at every checkpoint; final per-skill deltas as small as 0/+1/-1
   are only readable because the panel design exists).

## Find-by-find: mechanism, organ, port move, probe

### 1. Do small language models know what they don't know? (arxiv 2609.20824)
- URL: https://arxiv.org/abs/2609.20824 (submitted 2026-07-21; HN 49801865,
  2026-09-22, in-window).
- Mechanism: mean token entropy is near zero regardless of answer correctness in
  91 pct of dataset-model combinations at small scale, so any token-based
  confidence channel is unusable below the paper's 3B line; semantic entropy
  (multi-sample, cluster-by-meaning) remains informative, and routing on it gains
  up to +50pp, with cross-family routing averaging +22.0 pct vs +6.8 pct
  same-family (all numbers from the ask's confirmed find row).
- Estate organ: the gopher fleet's dispatch confidence + the routing rib. The
  estate's routing law says route by question-class first, family explains only
  3.6 pct of variance (RIB_ROUTING_CLASSES_20261002.md:11-15); this find amends the
  rib's climb rule: when a janitor's confidence channel fires, the climb target
  should be cross-family, and the confidence signal itself must be semantic, not
  token-entropy. It also bounds the banked itsodeleo direct-scoring pattern
  (banked at watch/inbox/frontier_olm_2026-10-10/sweep/finetuning-adaptation-hn.md:36-40,
  replication proposal at :66): gemma:2b and gemma4 sit under the 3B line, so a
  logits/token-entropy confidence baseline does not transfer to them without the
  semantic wrapper.
- Port move: before any janitor answer is trusted without climbing, the dispatch
  path (the model-gates fire path that mag/inference_budget.py:8-11 owns for
  per-animal recipes) gains one semantic-entropy leg: N samples, cluster by
  meaning, route on cluster spread. Never a single-pass token-entropy read at
  janitor scale. The rib amendment is filed against RIB_ROUTING_CLASSES_20261002.md
  whose own falsifier clause (:28-30) invites exactly this amend-on-new-evidence.
- Probe (cheap, falsifiable): 100 fixed items from an estate QA fixture, gemma:2b,
  10 samples each on local Ollama; score correct vs incorrect separation two ways:
  (a) mean token entropy, (b) semantic-entropy cluster spread. Falsifier in both
  directions: if (a) separates cleanly, the paper fails to transfer to the
  estate's stack and token-entropy routing stands; if (a) is flat and (b)
  separates, the amendment is confirmed and the port is justified. Cost: $0,
  local, one sitting.

### 2. Parity: non-inferiority testing before you swap models (illate-parity)
- URL: https://github.com/illate/parity (2026-10-06; HN 49976362 per the find's
  overlap row).
- Mechanism: each model scored with a bootstrap confidence interval, then a
  non-inferiority test: does the new model stay within an agreed margin of the
  current one, with 95 pct confidence; 10k resamples, same items both models,
  PASS/FAIL/INCONCLUSIVE where INCONCLUSIVE means label more and never guess;
  margin agreed before results; exit-0-only-on-PASS so it can gate CI. NumPy-only,
  Apache 2.0 (all from the ask's confirmed find row).
- Estate organ: the promote/swap gate. The estate's promote lane is already
  human-gated and refuses model-seat auto-writes (mag/improve.py:2744-2747), and
  the standing card above demands base-vs-adapter evals before any fold promotion
  (its MOLT row). What is missing is the verdict CONTRACT: the estate's blind
  audits grade but carry no pre-registered margin, no INCONCLUSIVE state, and no
  exit-code semantics. Note the kinship law: an honest instrument must be able to
  LOSE (mag/mirror_control.py:8); parity's three-state verdict is that law in
  decision form.
- Port move: a parity-class verdict row becomes a required input beside
  promote_apply (mag/improve.py:2744) for any model or adapter swap on a
  fire-path lane: frozen paired panel, margin declared in the row before the run,
  verdict PASS/FAIL/INCONCLUSIVE, exit 0 only on PASS, INCONCLUSIVE routes to more
  labeling (gopher label-farm rows are the natural panel food,
  mag/gopher_lite.py:14-16). The find's driver context also prices the status quo:
  OpenAI kills gpt-4.1-nano/o4-mini/gpt-3.5/gpt-4 fine-tunes on 23 October 2026,
  so swap-decision debt is about to be collected industry-wide.
- Probe (cheap, falsifiable): clone parity, freeze a 200-item paired panel, run
  gemma:2b vs gemma4 with a pre-agreed margin, plus two controls: a deliberately
  degraded arm (temperature 2.0) and a half-labeled set. The gate is real only if
  the degraded arm returns FAIL and the half-labeled set returns INCONCLUSIVE; if
  the degraded arm PASSes, the port is theater and must not gate anything.

### 3. Prime Agent: a self-improving RLM harness (PrimeIntellect-ai)
- URL: https://github.com/PrimeIntellect-ai/prime-agent (HN 50046425, posted
  10-11; MIT, funded org; Continual Harness paper arxiv 2605.09998 named in the
  find's why row).
- REV-2 PRIOR-BANK AMENDMENT: the find row's "New" verdict is withdrawn as
  overstated. The Prime Agent WORK was already banked 10-05, blog fetched end to
  end, including the immutable base prompt, evidence-logged CRUD refinements,
  and revert-by-ID
  (watch/inbox/frontier_olm_2026-10-05/sweep/evals-self-improvement-reddit.md:76;
  thread and fetch provenance at :33, :35, :39 of that bank; verified by grep and
  sed this round). What is genuinely new in the round-2 find: the GitHub repo
  itself (HN 50046425, posted 10-11, MIT), the /refine command's scope over
  supplemental state (prompts/memories/skills/subagent-specs), snapshot-based
  rollback, the bounded autonomous mode with its gate-honesty caveat, and the
  Continual Harness paper link (2605.09998).
- Mechanism: /refine reviews the current trajectory and applies small,
  evidence-backed updates to supplemental harness state (prompts, memories,
  skills, subagent-specs) as durable state; it never rewrites the immutable base
  system prompt; recorded snapshots support rollback; bounded autonomous mode
  carries the caveat that a passed gate checks only what that gate verifies (all
  from the ask's confirmed find row).
- Estate organ: the sovereign-mirror side, i.e. the estate's self-refinement
  ledger. The two-tier law is already ours (living ledger + frozen weights,
  RIB_LIVING_WEIGHTS_BY_NATURE.md:9, with SUPERSEDED reversibility at :13), and
  the workflow REGISTRY already runs amend-not-rewrite, and the 10-05 bank already
  carried this contract in prose (immutable base, evidence-logged CRUD,
  revert-by-ID; see the REV-2 note in this find). The repo-level steal is the
  reference implementation of that shape: refinement updates are (evidence
  pointer, snapshot id, rollback path) triples over an immutable base, and the model-gates
  distillability law already agrees in principle (a recipe changed without its
  observation + receipt is void, mag/inference_budget.py:25-26).
- Port move: audit and, where missing, stamp every supplemental-state mutation
  path (improve candidates, rib edits, context-pack mode configs) with the triple:
  evidence pointer, snapshot id, rollback path. The gate-honesty caveat gets
  quoted into the gate docs verbatim; it is the estate's own law said back to us.
- Probe (cheap, falsifiable): read the last N promotion receipts and REGISTRY rows;
  count how many carry an evidence pointer AND a rollback path. Falsifier: if more
  than half lack either, the ledger tier has the exact hole Prime Agent's
  snapshot-rollback closes and the port is urgent; if all carry both, the steal
  downgrades to confirmation-only and gets banked as such.

### 4. ASTRO: self-hosted, self-improving voice AI agent (Raspberry Pi 5)
- URL: https://github.com/mobium-app/ai_astro_public (v1.0.0, MIT, 2026-09-29).
- Mechanism: a full self-improvement loop BELOW estate-hardware scale: hears,
  speaks, sees, runs commands on its own device, learns while working, trains its
  own LoRA models (README quote, Polish verbatim, gloss per the find); lessons
  banked to SQLite, trajectories distilled, LoRA adapters trained on a peer
  RTX-4060-class box and served on the Pi; promotion only after tools/chain/chat
  gates pass with no regression vs baseline; E1-E9 quality gates; layered offline
  degradation; Ollama as the only hard dependency (from the ask's confirmed find
  row).
- Estate organ: the fold lane's train/serve split. The training organ exists
  (mag/lora_pipeline.py, config generator at mag/lora_pipeline.py:218) and the
  estate serves janitors through Ollama today. ASTRO's steal is the topology:
  training compute is borrowed (peer box), serving stays sovereign (weak box), and
  the promotion gate is no-regression, which is find 2's non-inferiority test with
  the margin set at zero.
- Port move: the fold lane adopts the split explicitly: adapters train wherever
  GPU capacity exists (peer box, hired GPU, unsloth seat), serve on the estate's
  weak boxes through Ollama, and no adapter reaches the serve path without the
  parity-class no-regression verdict. This kills the compute excuse for the
  estate's RDNA1-class box: if a Pi 5 can run the loop, the estate's box can
  serve it.
- Probe (cheap, falsifiable): serve-side bench on the weakest estate box: load one
  small LoRA-serving path under Ollama (an existing adapter, or the smallest
  public one if the estate has none trained yet; the standing card's OWED notes
  the on-disk adapter search never completed), run 20 fixed prompts, measure load
  time and tokens/s against the bare base model. Falsifier: if adapter-serving
  fits the estate's cadence budget, the compute excuse is dead and the split
  ports as-is; if it does not, only the serving claim amends (training stays
  peer-side either way).

### 5. Ten skills, one model, one pass (Learner 1.0 continual learning demo)
- URL: https://learnerlabs.ai/demos/skills/ten-skills (HN 49803321, 2026-09-22).
- Mechanism: 1.14B trainable parameters fixed, ten unrelated skills taught
  sequentially at one example per update, 63,282 updates, no replay, no task
  labels; every skill has a 225-row held-out panel scored at its own teach AND at
  every later checkpoint (final deltas 0,+1,-1,-3,0,0,-2,0,+2,0); a 498-item base
  sentinel plus a 16,481-item likelihood battery runs at every checkpoint; one
  H200 total; the page bounds its own claim to this stream and budget (all from
  the ask's confirmed find row, consistent with the adhoc sweep doc's banked item
  in watch/inbox/frontier_olm_adhoc/sweep/finetuning-adaptation-hn.md).
- Estate organ: the sovereign mirror's falsifier instrument. The ten-minute-self
  rib's falsifier 2 demands that a fold beat prompt-only on held-out pitfalls
  (RIB_TEN_MINUTE_SELF_20261010.md:58-60); Learner's design is the exact
  measurement pattern that demand was missing: per-skill panels at every LATER
  checkpoint (forgetting made visible) and a base sentinel at every checkpoint
  (collateral damage made visible). It is also the living-weights side of the
  two-tier law demonstrated with ledger-grade instrumentation
  (RIB_LIVING_WEIGHTS_BY_NATURE.md:17 puts the ASTRA distillation door in exactly
  this queue position).
- Port move: freeze the instrument BEFORE any fold runs: a base sentinel panel
  (the blind-audit fixture class is the natural source,
  RIB_ROUTING_CLASSES_20261002.md:3-4) plus a per-pitfall-class held-out panel
  template that scores at own-fold and every later fold. The fold falsifier
  becomes: per-class panels must not degrade at later folds AND the sentinel must
  hold, else the fold is distillation wearing a clock (the rib's own phrase,
  RIB_TEN_MINUTE_SELF_20261010.md:59-60).
- Probe (cheap, falsifiable, run BEFORE any training): build the sentinel, run it
  twice on the SAME unchanged model, measure test-retest agreement. Falsifier: if
  agreement is below roughly 95 pct, the instrument is too noisy to read the
  0/+1/-1-scale deltas Learner reports and must be enlarged before any fold claim
  is allowed; if it is stable, the estate owns a working forgetting meter for $0.

## Overlap verification re-run this session (commands and outputs)

- Catalog: grep -l -i -E "2609\.20824|illate|PrimeIntellect|ai_astro|learnerlabs"
  catalog/catalog.jsonl catalog/tags.jsonl catalog/junctions.jsonl → no file
  matched, exit 1. All five finds are unbanked in the catalog, confirming the
  catalog half of the find rows' overlap verdicts (the bank half is the REV-2
  bullet below; round 2 originally grepped catalog only, the same omission the
  round-1 section was corrected for).
- REV-2, the full-law bank grep the standing law requires
  (watch/inbox/frontier_olm_adhoc/DIGEST.md:31; run over the 09-30 through 10-10
  sweep .md banks with precise tokens: the SLM paper's arxiv id, illate,
  PrimeIntellect, ai_astro, learnerlabs, and the Learner, parity, and prime-agent
  HN story ids exactly as the find rows above state them): it changes one
  verdict, now
  corrected inside find 3 above (Prime Agent work prior-banked 10-05). The
  remaining PrimeIntellect hits (10-05 kv-cache bank :35 and :49, 10-07 swarm
  bank :52, 10-09 agent-memory bank :18) are org-name noise: tweet ids, NVFP4
  latent storage, a Goodfire case study; none are the prime-agent repo.
  parity (illate, 49976362): zero hits across all banks, genuinely new.
  2609.20824: prior candidacy now stated explicitly: HN id 49801865 sits on the
  10-03 daily candidate list at
  watch/inbox/frontier_olm_2026-10-03/sweep/finetuning-and-adaptation-hn.md:104
  ("Do SLMs know what they don't know (09-22)", verified by grep this round;
  round 2 had checked prior candidacy for Learner but not for this find, an
  asymmetry the review named).
  ASTRO: the find row's claim of "an unbanked candidate row in the 10-05 and
  10-06 evals-self-improvement sweeps" is NOT reproducible at bank scope: grep
  for ai_astro, mobium, astro, raspberry over all eight evals-self-improvement
  .md banks in 10-05 and 10-06 (reddit, hn, x, arxiv per day) returns zero
  (astroturf false-positives excluded). The row may live in the raw pools this
  law excludes from bank greps; catalog remains 0. Claim OWED, not asserted.
- Prior-candidate evidence for Learner 1.0 (the find claimed candidate-not-banked):
  sed -n '28p' watch/inbox/frontier_olm_2026-10-01/sweep/finetuning-adaptation-hn.md
  shows "Considered, not deep-read: Continual learning on a 28B Learner 1.0 model
  (HN 49803321)"; sed -n '52p' watch/inbox/frontier_olm_2026-10-02/sweep/finetuning-adaptation-hn.md
  shows "Learner 1.0 (49803321) ... cataloged as candidates but NOT deep-read".
- The 10-03 daily candidate list exists at
  watch/inbox/frontier_olm_2026-10-03/sweep/finetuning-and-adaptation-hn.md:104
  (verified by sed this session; it is a raw candidate listing, no analysis).
- The itsodeleo pattern the find amends is banked at
  watch/inbox/frontier_olm_2026-10-10/sweep/finetuning-adaptation-hn.md:36-40
  with the replication proposal at :66 (located by grep this session; earlier
  greps over corpus/steal, memory/corpus/LINKS.jsonl and
  memory/lenses/corpus_index.json returned zero, so the sweep bank is its home).

## OWED (never asserted as done)

- The five source URLs were not re-fetched this session; the finds arrived
  confirmed in the ask and were consistency-checked against the adhoc sweep doc's
  banked items only. Numbers inside the finds (91 pct, +50pp, +22.0 vs +6.8 pct,
  63,282 updates, 16,481-item battery, E1-E9) are the find rows' claims, not
  re-derivations.
- Prime Agent's /refine contract fields and ASTRO's E1-E9 gate contents were not
  read firsthand; the contract-shape steals rest on the find quotes.
- No probe above was executed this session: all five are designed, not run. The
  rev-2 JSON companion row's probe (appended to
  watch/inbox/frontier_olm_adhoc/percolator_candidates.jsonl this round, curing
  the "only steal card without a .json companion on disk" flag that
  watch/inbox/frontier_olm_adhoc/DIGEST.md:17 recorded at fold time) is the
  parity negative-control run, the cheapest decisive first move.
- The routing rib amendment (cross-family climb + semantic-entropy signal) is
  mapped, not filed: filing it is the rib owner's edit, not this card's.

---

## REV-2 FIXES (receipt; reviewer verdict was "demand fixes, then bank")

All four blocking defects amended in place above, nothing rewritten away. Each
fix names its evidence:

1. ENV CLAIM (the false venv inventory): corrected in the probes section. My own
   import run this round: torch 2.13.0+cpu importable; numpy ABSENT; peft
   ABSENT; safetensors 0.8.0 importable; transformers 5.15.0 pip-installed but
   import fails on the missing numpy (ModuleNotFoundError inside the import).
   The decisive probe was rewritten to the safetensors-direct path per the
   review's option B, and that path is proven live: a hand-written safetensors
   file round-tripped through safetensors.torch.load_file with maxdiff 0.0, no
   numpy in the process (a first attempt also proved save_file DOES need numpy;
   the probe only loads, never saves). Serving-leg repair (numpy+peft) left to
   the venv owner, logged not silently done.
2. OVERLAP METHODOLOGY: the round-1 section's false verdicts corrected (AgileRL
   candidate-listed 10-04 at frontier_olm_2026-10-04/sweep/finetuning-and-adaptation-reddit.md:44;
   Agentic-TTT held AND deep-read by the 10-10 bank at
   frontier_olm_2026-10-10/sweep/finetuning-adaptation-arxiv.md:28-33; aTTT's
   today-catalog rows are own byproducts), the standing law cited
   (watch/inbox/frontier_olm_adhoc/DIGEST.md:31), and the full-law grep run for
   the round-2 five as well, which surfaced the Prime Agent prior bank (10-05
   evals bank :76, blog fetched end to end; find 3's verdict amended in place)
   and killed the ASTRO candidacy claim's reproducibility (OWED). The 2609.20824
   candidacy asymmetry is fixed (49801865 verified on the 10-03 list :104).
3. JSON COMPANION: a rev-2 row is appended to
   watch/inbox/frontier_olm_adhoc/percolator_candidates.jsonl (schema matched to
   the existing rows: area, claim, source_url, estate_map, probe), and the
   addendum's probe pointer now names that row, so a downstream JSON consumer
   sees the parity probe. The DIGEST.md:17 "no .json companion" flag described
   the fold-time state and is superseded by this append.
4. WRONG CITE: the aTTT anchor lens/burns.md:103 (a FREE-RESOURCE SCOUT
   commit-log row, verified by sed) is corrected to :119 (the aTTT row) with the
   fine-tuning-JIT law mention at :82.

Checks re-run after these fixes (this session, exact commands in the sections
above): citation lint exit 0 blocking 0; em-dash count 0; char counts in the
submit payload. Not done, stated plainly: the venv repair, the rib filing, and
every designed probe.
