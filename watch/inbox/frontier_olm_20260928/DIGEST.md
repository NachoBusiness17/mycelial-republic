# Frontier OLM mine: fold digest (second pass)

source-fetched: 2026-09-28. The window 2026-08-29 to 2026-09-28 bounds what the lanes enumerated
and fetched; individual finds carry their own dates and out-of-window items are dated and flagged
in place. Fold written 2026-09-29. This pass supersedes the same-path predecessor fold (written
earlier on 2026-09-29 from an 18-lane / 23-find / 9-card confirmation state; sizes and mtimes
measured before overwrite, see RECEIPT.md). Pass-over delta (added by the cold-read fix): 18 lane
reports became 32 sweep returns (the full 8-area x 4-door set, all ok:true); 23 confirmed finds
became 21 and 1 unconfirmed became 3 (the confirmation set was redrawn, not carried row-for-row;
the one predecessor verification carried forward is the PolAgentBench license refutation, now
register row 18's overlap note, while the Vals/RWKV/Jetson probe corrections come from this
pass's round-2 steal card); 9 steal cards became 5. Which specific lanes are new versus refreshed
cannot be reconstructed from this session (the predecessor digest's lane list was not read beyond
its header). Preservation: the predecessor text is NOT recoverable. The four fold outputs are
untracked in git (git status shows ?? for all four paths; git log on them returns nothing), so
the overwrite destroyed the only copy; its headline counts survive only in this note and in
RECEIPT.md's Supersession section. This pass folds the mine as handed to the fold ask:
32 sweep returns, 21 confirmed finds, 3 unconfirmed items with confirmation evidence, 5 steal
cards. Text law: ascii only, no em or en dashes; the one unicode math token in a source quote
(the REUSE paper's 1-minus-alpha) is normalized to "1-alpha" here and in register.jsonl.

## Fold mechanics and grounding

- Inputs: 32 sweep returns over 8 areas (open-and-local-language-models, quantization-compression,
  agent-memory-continuity, swarm-orchestration, finetuning-and-adaptation, kv-cache-context-engineering,
  evals-self-improvement, inference-efficiency) x 4 doors (arxiv, hn, reddit, x), all ok:true; a
  confirmation pass returning 21 confirmed finds and 3 unconfirmed items; 5 steal cards. Lane banks:
  sweep/<area>-<door>.md (32 files), raw fetch receipts sweep/_raw/, lens findings lens/, steal
  cards steal/.
- Outputs: DIGEST.md (this file), register.jsonl (21 rows, one per confirmed find),
  percolator_candidates.jsonl (5 rows, one per steal), RECEIPT.md (measured byte counts, counts by
  area and source, workflow gate row pointer).
- Grounding law: sweep and steal content below is lane-reported (sources fetched and read on
  2026-09-28; overlap greps and probes run by the lanes). What this fold verified itself this
  session is tagged "verified this session": the two percolator code reads (mag/percolator.py:264-272,
  mag/seed_percolator.py:6-16), the workflow registry rows (memory/workflows/REGISTRY.jsonl lines
  34, 36, 38), the directory walk and byte counts, the line-by-line json.loads parse of both
  registers, and the dash/non-ascii scan of all four outputs. Everything else is carried with its
  lane attribution, never asserted as this fold's own measurement.

## Executive summary

1. **The promote gate is a counter today; published instruments say it must be a certified
   decision.** Verified this session: mag/percolator.py:264-272 promotes an invariant on
   `count += 1` alone (returns status "repeat", compiled True; no behavior eval, no baseline, no
   rollback), while mag/seed_percolator.py:6-16 already holds the estate's own paired-blind gate
   (>=55% win rate, 30 pairs per epoch, 3 consecutive fresh-set epochs, null-variant canary halt)
   with "No scheduler wiring" at :15. Six confirmed papers define the upgrade path: certified
   decision-only acceptance under a global alpha budget (REUSE, arXiv 2609.33180: 0 false
   promotions vs up to 20.7% naive at matched performance; the metric is share of accepted
   modifications that were not genuine improvements, 75 false promotions in the naive best-of-K
   arm); held-out grade plus generalization
   benchmarks never fed back into selection (AIDE2, 2609.26457: 7 of 99 rewrites accepted, grade
   0.703 to 0.778, hacking 55% to 32%, non-monotone across checkpoints); fresh alternative-route
   closure tests for patched exploits (Unearned Passes, 2609.34262); paired-attribution ledgers
   (SEABench, 2609.35596: 316/720 evolved-arm safety failures vs 0/720 baseline, Fisher
   p=3.48e-13); verification budgeted by expected selection-regret per cost (PIVOT-KG, 2609.32677:
   a near-zero-MAE verifier still reversed up to 100% of proposed updates); change manifests with
   rollback where the updater cannot weaken its own gate (RegenHarness, 2609.27612, protocol only).
   Steal S1 carries the port and the falsifiable probe.

2. **Janitor fleet doctrine is published-backed end to end.** Untuned sub-2B checkpoints are
   components, not executors: only 5 of 1,000 raw tool responses strict-parse (arXiv 2609.07370,
   released 100-prompt battery github.com/Abrar051/sml_mcp_benchmark). Structure is a sampler
   property: grammar-constrained decoding buys 100% schema validity on 0.6B-4B at 1.6-3.7%
   throughput cost, and constrained 1B beats unconstrained 3B (arXiv 2609.23742). The quant cliff
   replicates while failure modes do not: everything collapses between Q3_K_M and Q2_K (aggregate
   task-success fraction on the PolAgentBench agentic tool-use suite: 11B 0.716 pre-cliff to
   0.045 at Q2_K, paired McNemar p<0.001), and 2-bit failures confabulate well-formed JSON, so the
   dangerous regime looks like success to a tool harness (arXiv 2609.32042); at 27B, Q4_K_M
   matches BF16 on agentic Terminal-Bench 2.1 and 1-bit is random chance
   (quesma.com/blog/qwen38-27b-quantizations-benchmarked/). Fleet shape: Q4_K_M default, 3-bit
   floor, constrained decode, parse-then-recover scoring, repair-layer hit rate as the per-model
   diagnostic. Steals S2, S3, S4.

3. **The deployment landscape moved under the estate (one headline item single-sourced).**
   "Hugging Face was acquired by NVIDIA" is SINGLE-SOURCED: one X post by Georgi Gerganov
   (x.com/ggerganov/status/2095897173376618881, register row 2); the fold's material names no
   press release, filing, or second source, and a second-source web search run this session hit
   Z.ai 1302 rate walls on most queries and returned no confirming hit on those that ran, so the
   acquisition line is uncorroborated: fetch a primary (HF blog or NVIDIA newsroom page) before
   anything rides on it. Independently usable from the same post: llama.cpp/ggml committing to
   hardware-agnostic independence. DeepSeek-V4.1-Flash is rolling out on Ollama cloud, Max/Team
   first (x.com/ollama/status/2098188014119985406). The Vals "#1 open-weight" headline was REFUTED at
   probe time: the live board saved 2026-09-29 puts V4.1-Flash 51.32 at #4 among open weights
   behind MiMo V2.6 Pro 55.20, GLM 5.3 53.51, and MiMo V2.6 Flash 53.23, still above Kimi K3
   50.70, with the $0.30/test price leg confirmed (steal S5; saved bytes sweep/_raw/vals_home_20260929.html
   and sweep/_raw/vals_model_v41flash.html). RWKV-7 G1j (Apache-2.0 RNN, 1.5B/2.9B) landed with
   only its author BlinkDL's own claim of being better at agent/coding/STEM, untested by any
   benchmark in the material until the estate's own battery re-ranks it; DeepSeek-V4-Flash-Vision-Exp
   (MIT) is a separate open-weights vision checkpoint the estate can pull and diff against the
   findings of its own v41_paces LANE5_vision lane. Steal S5.

4. **Cache law: the boring baseline wins until beaten at the real budget.** Replay of 68,266 real
   Claude Code requests plus 23,608 Mooncake requests through a prefix-cache simulator left
   radix-leaf LRU at an 83.48% prefix-hit rate (share of the 91,874 replayed requests served from
   prefix cache) at the simulator's 8k-block cache capacity, with every fancier policy losing;
   dominant waste is
   tight tool loops whose ~88k-token working sets exceed capacity, so the lever is budget and
   assembly, not a cleverer evictor (github.com/gauravapiscean/agentic-kv-cache). The estate
   should mint the same LRU null arm over its own tape corpus before believing any compaction
   claim, which its own law already demands (memory/research_polished/kv_cache_compaction.md:13).
   Byte-identical prefixes stay the load-bearing invariant. Steal S4, second mechanism.

5. **Door health, honestly.** Direct reddit doors and the site:x.com search backend degraded in
   every lane that touched them (403s, login walls, 429/1302 rate walls, welcome shells); the
   working doors were the archives and mirrors: pullpush and arctic-shift APIs, redlib mirrors
   (including one Anubis sha256 proof-of-work solve to read a thread), the fxtwitter JSON door,
   and smol.ai AINews issue indexes. HN Algolia and arXiv API ran clean except one 429 burst
   degraded to serialized curl (open-and-local-language-models-arxiv lane). That no lane claimed a
   fabricated fallback success is LANE-ATTESTED, not fold-verified: each sweep's own note asserts
   it and this fold did not audit lane fetch logs; it is consistent with the snippet-only items
   being flagged in place, and none of those is in the register.

6. **Honesty state of the register.** 21 confirmed rows bank. Two carry post-confirmation
   corrections recorded in their overlap fields (overlap is register.jsonl's free-text field for
   prior-holdings grep results and post-confirmation corrections; the full field list is in
   RECEIPT.md): the Vals #1-open leg refuted at probe (register
   row 1) and the PolAgentBench CC0 attribution refuted (register row 18: the repo README says MIT
   code and CC BY 4.0 release data; the CC0 on the arXiv page is the paper-text license). Three
   items are held unconfirmed with their evidence (end of this file) and none of them is cited as
   support anywhere in this fold.

## Top steals with estate maps

### S1. Promote gate for the percolator (evals-self-improvement via arxiv)

- Steal: a promote gate is a statistical instrument, not a counter. Decision-only feedback plus a
  global error budget alpha certifies, with probability >= 1-alpha over the whole run, that every
  promoted modification is a genuine population improvement (REUSE 2609.33180). Accept on a
  private held-out grade, then prove generalization on benchmarks never fed back into selection
  plus a held-out hacking instrument (AIDE2 2609.26457). Treat a patched exploit route as unclosed
  until a fresh alternative-route attempt fails (Unearned Passes 2609.34262). Run each promotion
  paired against a frozen baseline with attribution (SEABench 2609.35596). Spend scarce
  high-fidelity verification by expected selection-regret reduction per cost (PIVOT-KG 2609.32677).
  Wrap promotions in change manifests, fixed regression sets, and rollback, updater barred from
  weakening its own acceptance predicate (RegenHarness 2609.27612, protocol only, no experimental
  RSI results).
- Estate map: percolator is the organ. Verified this session: recurrence-only promote at
  mag/percolator.py:264-272; the estate's own designed paired-blind A/B gate sits dormant across
  mag/seed_percolator.py:6-16 (gate thresholds at :8-12; the ':15 No scheduler wiring' line sits
  at :14-16; range read this session). Port: wire the dormant seed gate onto
  the percolator repeat branch; add the REUSE decision-only accept predicate and alpha budget;
  grade acceptance on a frozen probe suite with one task family never fed back (AIDE2 tier 2);
  give rows manifest/regression/rollback fields (RegenHarness); log SEABench-shaped paired rows
  into the open emergence A/B ledger (lens/laws.md:69, lane-verified); PIVOT-KG's EVSI-per-cost
  rank decides which promotions earn funded-tier grades. Secondary organs: sovereign mirror
  (ternary violation test replaces binary reject at mag/improve.py:2721-2724, lane-verified) and
  the tripwire tier (fresh alternative-route attempt as the closure test after any tripwire fix).
- Probe: draw the 20 highest-count rows from memory/percolator/invariants.json; 5 fresh probe
  prompts per invariant (new phrasings, zero token overlap with the sentences that percolated
  them, half to trigger and half to not); blind-grade whether the prescribed behavior fires
  (~200 judgments, janitor tier plus a 20-prompt funded-tier spot check). Prediction from the
  verified numbers: 1 to 5 of 20 fail held-out. Decision rule (null branch restated by this fix;
  the card's "0 failures means empirically adequate" is unsupported at n=20, where 0/20 is also
  what a 10% true failure rate produces most of the time, P = 0.9^20 = 0.122, and it leaves a 95%
  one-sided upper bound near a 14% true rate): 6+ failures of 20 means the estate gate is worse
  than the published naive baseline and the REUSE-shaped predicate jumps the queue; 0 failures is
  INCONCLUSIVE at this sample size, not vindication, and only justifies scaling the probe up
  before any gate redesign. Not run by this fold.
- Run plan for the predicted operator ask (added by this fix): owner UNASSIGNED in the fold
  material (no named percolator owner exists in what this fold received; the ask must name one;
  the natural surface is the seat that owns mag/percolator.py); suite source: the 20 highest-count
  rows of memory/percolator/invariants.json plus fresh prompts authored at run time under the
  zero-overlap rule above; receipt path: watch/inbox/frontier_olm_20260928/probe/S1_promote_gate_probe_<UTC date>.md
  (the probe/ directory does not exist yet; the runner creates it); cost: about 200 janitor
  judgments plus a 20-prompt funded-tier spot check.

### S2. Constrained-decode the janitor fleet (open-and-local-language-models-arxiv)

- Steal: schema validity is a sampler property, not a parameter-count property (grammar-constrained
  1B beats unconstrained 3B; 4-8 ms compile and 1.6-3.7% throughput buys 100% schema validity on
  0.6B-4B), so buy structure at decode time and hold the smaller model. Janitors earn chore
  autonomy through a measured recovered-call score on the released 100-prompt tool-call battery
  with a mandatory JSON recovery stage (untuned sub-2B: only 5 of 1,000 raw responses
  strict-parse; 89.4% of 658 failures die at JSON recovery). Below gemma class the win is a
  narrow 270M fine-tuned specialist on one fixed schema catalog (FunctionGemma 29.3% to 76.5% on
  ~9,500 schema-validated conversations; 285.6 MB is the fine-tuned model's on-device size), a
  training-data problem the percolator can
  price. Quantization law: the Q3_K_M-to-Q2_K cliff replicates across models while failure modes
  do not, so set a 3-bit fleet floor and log repair-layer hit rate as the per-model diagnostic.
- Estate map: gopher fleet (janitor-agent seat mag/agent_state_router.py:41-48; call defaults
  mag/afk_loop.py:104 gemma:2b, mag/batch_scribe.py:45 gemma4; lane-verified) gains the 100-prompt
  trust gate before chore autonomy with mandatory parse-then-verify, plus a fleet law: no GGUF
  below Q3_K_M dispatched agentic chores, repair-layer hit rate banked per model+quant into
  memory/learn/sizing.jsonl, quantcheck acceptance gate on every pull. Quantizer as emission site
  (tools/thought_quantizer.py:258-259): grammar-constrained drafting of chore/instruction JSON via
  Ollama format=JSON-schema (0.34.3 live-verified by the lane). Percolator: bank the 270M
  chore-specialist candidate (FunctionGemma recipe, mag/lora_pipeline.py shell re-targeted, SFT
  spend net-new). Sovereign mirror and water graph get no direct port from these finds.
- Probe (lane-priced at $0; the lane verified gemma:2b installed via ollama list and the server
  live via curl /api/version): run 30 of the sml_mcp_benchmark prompts against gemma:2b on the
  live Ollama over HTTP, two arms: unconstrained vs format=<JSON schema>. Falsifiable
  predictions: arm b hits 100% schema-valid at under 4% throughput cost (per 2609.23742) and arm
  a strict-parses low, near the paper's 5 of 1,000 (per 2609.07370). Decision rule (dead zone
  closed by this fix; the card had only the 80% falsifier, so outcomes between the paper's 0.5%
  and 80% decided nothing): arm b missing 100% or costing over 10% throughput falsifies the
  constrained arm outright; arm a below 5% strict-parse lands on the paper's rate and confirms
  the trust gate as designed; arm a at or above 50% (working threshold pre-committed by this
  fix, fold-added, not lane-reported) means the unconstrained path is usable behind a cheap
  JSON-retry wrapper and the full gate is overkill for gemma:2b; between 5% and 50%, keep the
  gate and log both arms as gemma:2b's measured recovered-call score. Not run by this fold.

### S3. Quant floor plus free collapse detector (quantization-compression via arxiv)

- Steal: three mechanisms from PolAgentBench (arXiv 2609.32042, three GGUF k-quant models, Q8_0
  to Q2_K). (1) The collapse threshold replicates, the failure mode does not: exactly one thing
  transfers across a fourfold capability spread, the cliff between 3-bit and 2-bit, so a quant
  floor is keyed to role and never learned from one model's telemetry; at 27B the endpoints
  confirm it (Q4_K_M matches BF16 on agentic Terminal-Bench 2.1, 1-bit collapses to chance, per
  the Quesma post). (2) Below the cliff, failure looks like success to a tool harness: 2-bit
  failures keep the protocol well formed (a final_answer with no parse error and an empty tool
  log) while confabulating content, so harnesses must score protocol-shape and content separately.
  (3) A free zero-inference collapse detector from inverted token economics: failing trajectories
  cost more tokens at every precision except 11B Q2_K, where they are cheap (median 1,506.5 vs
  4,010 tokens) because the model answers before it looks; steps-to-final, tool-calls-before-final,
  and tokens-per-trajectory form an alarm that costs nothing at run time. Rider: scaffolding
  repair is precision-coupled, and per-model failure taxonomies are measured, never assumed.
- Estate map: the quantizer's GGUF weights side. Port moves: a quant floor law (any tool/JSON
  role floors at Q3_K_M-equivalent, Q2_K banned for those roles) hosted as a per-model quant
  census in mag/gguf_cartography.py, which already parses the GGUF dtype table with zero deps
  (Q2_K at mag/gguf_cartography.py:59, Q3_K at :60; lane-verified); the VRAM folklore at
  mag/vast_launcher.py:436 becomes a measured cliff law; the three free detector signals wired
  into the janitor run loop with the corollary to mag/auto_quantize.py:22 (anomalies are never
  quantized; below the cliff quantization itself manufactures anomalies shaped like successes).
  Delivery-chain note: the quantizer's thought packs (tools/thought_quantizer.py:74) are consumed
  by these same local models via mag/context_pack.py:392, so a sub-floor janitor corrupts the
  pack consumer, not just its own tasks.
- Probe: pin a 15-20 task deterministic tool-call suite in the janitor's own idiom (every task
  requires at least one tool call before a final answer; score protocol-shape and content
  separately). Run gemma:2b and gemma4 twice each: current ollama quant vs one Q2_K_M rebuild
  from the same base, temperature 0, fixed seed, roughly 40 short local calls per model. Sharpest
  falsifiable prediction: at Q2_K_M only, median failing-trajectory tokens drop BELOW median
  passing-trajectory tokens (paper: 1,506.5 vs 4,010 at 11B Q2_K). Falsification condition: if
  the estate stack fails by parse errors and failures cost more tokens than successes at Q2_K_M,
  the confabulation signature does not transfer and only the pass-rate collapse leg of the floor
  law survives. Not run by this fold; proposal.

### S4. Quesma quant floor plus the LRU null arm (quantization-compression via hn)

- Steal: two mechanisms, both source-verified by the card lane. (1) A measured quant floor law
  for agentic work: Q4_K_M is the safe default that holds agentic coding (17 GB Q4_K_M matches
  full Qwen3.8 27B on Terminal-Bench 2.1), 2-bit is the instruction-following floor (IFBench flat
  down to UD-Q2_K_XL), 1-bit is collapse (random chance on GPQA Diamond); quant selection must be
  judged on agentic task benchmarks, never perplexity or KL proxies (thread: KL is
  dataset-dependent with agentic traces diverging far worse than wikitext; quants are not uniform
  so 4-bit is not a true 4-bit). The suite has no tool-calling or JSON benchmark, which is exactly
  the estate-side eval slice to cover. (2) The kv steal is a method, not a number: replay real
  traces through a prefix-cache simulator with radix-leaf LRU at the real budget as the free null
  arm before believing any eviction candidate (68,266 Claude Code + 23,608 Mooncake requests;
  every fancy policy lost to LRU-leaf); when working sets exceed capacity (88k-token tight tool
  loops) the lever is budget/assembly, not a cleverer liveness predictor. This independently
  confirms the estate's own gap law at memory/research_polished/kv_cache_compaction.md:13.
- Estate map: floor law into the thought quantizer's input stream (memory/percolator/
  invariants.json) so it compiles into the packs delivered at mag/context_pack.py:1142; a
  quant-level axis (current vs Q4_K_M vs 2-bit) on the next tools/tier_probe.py run scored on
  real seat tasks; the LRU replay mints the measured null arm that gap-fold G1 already demands
  (gap-fold G1 = the estate law at memory/research_polished/kv_cache_compaction.md:13: any
  eviction/compaction claim must beat LRU/ARC/PBKV/Belady-MIN baseline arms or it is decoration),
  validated against the existing frozen-prefix machinery (mag/context_pack.py:489
  freeze_system_prompt, :548 Auto-repack tail; lane-verified). Doc-drift, re-verified this
  session by this fold: memory/research_polished/kv_cache_compaction.md:23 still says
  freeze_system_prompt() is never built with "grep: absent repo-wide", and :27 still lists
  building it as a next action, while mag/context_pack.py:489 defines it (both doc lines and the
  def read this session). Filed in: the S4 card's estate map
  (steal/quantization-compression via hn.md) and this digest line, which is the filing of
  record; no separate desk bullet or receipt exists in the fold's material.
- Probe (byte-cheap, local compute over files already on disk, no GPU, no API spend): compute
  radix-leaf LRU hit rate over the most recent 5,000 estate tape rows from
  dashboard/static/trails/ (12 .jsonl trail files, verified present this session); the card's
  second source, "db.sqlite transcripts", could not be resolved to a file this session (no
  db.sqlite at repo root or one to three levels deep; the only shallow .sqlite files are the
  catalog FTS indexes, and the phrase traces to kv_cache_compaction.md:28), so pin the
  transcript-store path at probe start or run on the trails alone. Budget: mag/context_pack.py
  pins per-mode max_chars budgets (mode-table comment at :52, janitor default 4,800 chars at
  :67, five more modes through :165), so the probe runs at the janitor default 4,800-char pack
  budget (chars, not tokens; the budget is char-denominated in code). Falsifiable claim: LRU at
  the estate's real budget achieves 80%+ hit (external reference: 83.48% prefix-hit at the
  source simulator's 8k-block capacity on its 40-session AgentX subset). If it holds, that number becomes the G1 null every future
  eviction/compaction proposal must beat; if per-session working sets blow past the budget, the
  correct fix is pack budget and assembly, not eviction policy. Either branch converts the
  doctrine into a measured fact. Secondary probe banked in the card: local worker at Q4_K_M vs
  2-bit over 30 prompts from memory/corpus/quantized_thought/instructions_flash.jsonl, graded on
  JSON-valid rate. Not run by this fold.

### S5. Open-model landscape, round-2 mechanism card (open-and-local-language-models via x)

- Steal: eight finds with six probes already run by the card lane. (1) Vals probe falsified the
  find's headline as of fetch: saved bytes (sweep/_raw/vals_home_20260929.html, 1,297,267 B;
  sweep/_raw/vals_model_v41flash.html, 305,311 B) show DeepSeek V4.1 Flash 51.32 ABOVE Kimi K3
  50.70 in both embedded tables and $0.30 per test on the model page, but #4 among open weights
  behind MiMo V2.6 Pro 55.20, GLM 5.3 53.51, MiMo V2.6 Flash 53.23 (#1 leg REFUTED as of
  2026-09-29; board movement vs tweet error indistinguishable). (2) HF-as-NVIDIA supply chain:
  live server provably pulls an hf.co-prefixed GGUF; port is one per-model register (license from
  vault manifest + pull source + second source), tag count read at probe time with the instrument
  named (14 round-1, 16 this round; B2-216 = the estate's census-denominator law: a count is a
  snapshot of one tree at one moment; name instrument, moment, and delta before comparing counts;
  carried in the AGENTS.md Clippy block, receipt
  watch/inbox/burn_wave_20260926/B2_216_collect_delta_20260926.md). ARTIFACT GAP (cold-read fix):
  the provably-pulls claim names no pull log, manifest, or registry row in the fold's material,
  and the default ollama manifests path (~/.ollama/manifests) does not exist on this seat
  (checked this session), so the artifact must come from the card lane's environment; attach the
  manifest or pull-log line naming the hf.co/-prefixed model id before the register port is
  scheduled. (3) RWKV-7 G1j date corrected from raw
  provenance (ONE tweet, not two: fxtwitter created_at for status 2094785763129151677 is
  2026-09-01T13:53:39Z; the sweep's 2026-08-31 was the HF weight-filename stamp on the same
  release) and the sweep's
  missing raw landed (sweep/_raw/hf_rwkv7g1.json: apache-2.0, 22,917 downloads, 4 G1j files
  ctx16384). (4) Nemotron recipe now rerunnable: full verbatim capture landed
  (sweep/_raw/nemotron35_fastino_article.md; Recipe I numbers verbatim: 27,542 trajectories,
  rank 32, 2e-4 override of the ~1e-4 default, 2 epochs, 48.00 to 71.18 overall, 51.42 to 81.88
  single-turn, multi-turn under half a point). (5) Agent Arena rank banked as a stored input to
  the warm memory/runs/fleet_round/burn2b_pack.md:7299 comparison, inert A/B cut. (6) Jetson
  pointer probe ran (sweep/_raw/jetson_unsloth_on_jetson.html, 92,055 B, both models named
  verbatim; Qwen3.5-4B existence now vendor-page-confirmed), zero-port. (7) Ollama cloud gate
  proven (registry 404 MANIFEST_UNKNOWN + cloud library page). (8) Vision-Exp MIT-confirmed via
  landed HF raw (sweep/_raw/hf_v4flashvision.json). Landing: 8 register rows (validated, 0 bad),
  1 merged percolator row (validated), 2 desk bullets in watch/inbox/DESK_DSV41FLASH_20260911.md,
  8 raw receipts on disk.
- Estate map: sovereign mirror takes finds 1, 2, 7, 8 (desk tri-state now carries two dated
  bullets appended after their probe gates landed with saved bytes). Gopher fleet takes finds 3,
  4, 5, 6: finds 3 and 4 name the estate's OWN abliterate-p1 battery (watch/inbox/ball2/abliterate-p1.md,
  tools/abliterate_p1_probe.py, 20 fleet-shape prompts x 3 runs = 60 inferences) as re-rank
  instrument and test rig instead of hand-rolled prompt sets; find 5 is a banked fact wired to the
  already-warm comparison; find 6 is a zero-port named-recipe pointer. Quantizer: find 4's
  tape-selection law (multi-turn competence needs real multi-turn trajectories). Context pack:
  find 1 secondary. Percolator: the merged register. Water graph: declined for all 8
  (mag/water_computer.py:1-9, hydraulics keep).
- Probe: run the abliterate-p1 battery unchanged (tools/abliterate_p1_probe.py, same 20
  fleet-shape prompts, same 3-run shape) against qwen2.5:3b-instruct (the cache-identity primary,
  mag/cache_identity.py:78-80) and test the captured Nemotron asymmetry on the estate's own
  instrument: interface-shape prompts close faster than multi-step prompts. Falsifier: if the two
  gap classes come out equal or inverted, the curriculum law has no purchase on this stack; if
  the asymmetry reproduces, the quantizer's tape-selection rule (weight real multi-turn seat
  tapes over synthetic pairs) is earned. Receipt path: watch/inbox/ball2/abliterate_p1_runs_qwen25-3b.json.
  Cost: 60 local CPU-class calls. Not run by this fold.

## Confirmed finds

21 register rows (20 distinct sources; rows 18 and 19 are the same paper, arXiv 2609.32042,
independently confirmed from two lanes). Row 4's date is outside the window and stated as the
source shows it. Row 1's headline leg was refuted at probe time (see S5); row 18 carries the
PolAgentBench license correction (CC0 attribution refuted: MIT code, CC BY 4.0 release data).
Titles and quotes are verbatim from the sources, so row 1's title still carries the refuted #1
claim; the bracketed tags on rows 1 to 3 exist so the table cannot be skimmed as asserting them.
Row 3's date is the HF weight-filename stamp; the tweet itself is one post with created_at
2026-09-01T13:53:39Z, not two tweets (see S5 item 3).

| # | Title | URL | Date | Area |
|---|-------|-----|------|------|
| 1 | DeepSeek V4.1 Flash is the new #1 open-weight model on the Vals Index [VERBATIM TWEET TITLE; #1-open leg REFUTED at probe 2026-09-29, see S5 and register row 1 overlap] | https://x.com/ValsAI/status/2098125164072554545 | 2026-09-10 | open-and-local-language-models via x |
| 2 | Hugging Face has been acquired by NVIDIA (Georgi Gerganov) [SINGLE-SOURCED: one X post; second source not held, see exec summary 3] | https://x.com/ggerganov/status/2095897173376618881 | 2026-09-04 | open-and-local-language-models via x |
| 3 | RWKV-7 G1j (100% RNN) release | https://x.com/BlinkDL_AI/status/2094785763129151677 | 2026-08-31 (weight-filename stamp; tweet created_at 2026-09-01T13:53:39Z, see S5 item 3) | open-and-local-language-models via x |
| 4 | Small Model, Big Leverage: What We Learned Fine-Tuning NVIDIA Nemotron 3.5 Lightning with an Agent | https://x.com/i/article/2088303137182679378 | 2026-08-14 (out of window, stated) | open-and-local-language-models via x |
| 5 | Qwen3.8-Flash-Next lands in Agent Arena at #7 among open models | https://x.com/arena/status/2094566204488962483 | 2026-08-31 | open-and-local-language-models via x |
| 6 | Fine-tune and quantize AI models directly on NVIDIA Jetson | https://x.com/NVIDIARobotics/status/2094480283135316182 | 2026-08-31 | open-and-local-language-models via x |
| 7 | DeepSeek-V4.1-Flash is now being rolled out on Ollama's cloud | https://x.com/ollama/status/2098188014119985406 | 2026-09-10 | open-and-local-language-models via x |
| 8 | DeepSeek V4 Flash Vision weights open (Zizheng Pan) | https://x.com/zizhpan/status/2094386230675062836 | 2026-08-31 | open-and-local-language-models via x |
| 9 | Which Self-Improvements Should We Trust? Reliable Self-Improvement When Agents Reuse Their Benchmarks | https://arxiv.org/html/2609.33180v1 | 2026-09-27 | evals-self-improvement via arxiv |
| 10 | Recursive self-improvement of AI research agents | https://arxiv.org/html/2609.26457v1 | 2026-09-22 | evals-self-improvement via arxiv |
| 11 | Maintaining Benchmarks Against Increasingly Capable Agents: Detection and Remediation of Unearned Passes | https://arxiv.org/html/2609.34262v1 | 2026-09-28 | evals-self-improvement via arxiv |
| 12 | SEABench: Benchmarking Endogenous Misalignment In Self-Evolving Agents | https://arxiv.org/html/2609.35596v1 | 2026-09-28 | evals-self-improvement via arxiv |
| 13 | When Better Gets Worse: Improvement Fidelity for Self-Improving Agents in Adaptive Worlds | https://arxiv.org/html/2609.32677v1 | 2026-09-26 | evals-self-improvement via arxiv |
| 14 | RegenHarness: A Robot Agent Harness with Evidence-Gated Recursive Self-Improvement | https://arxiv.org/html/2609.27612v1 | 2026-09-23 | evals-self-improvement via arxiv |
| 15 | Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B Small Language Models for Edge Deployment | https://arxiv.org/abs/2609.07370 | 2026-09-07 | open-and-local-language-models-arxiv |
| 16 | Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap | https://arxiv.org/abs/2609.23742 | 2026-09-20 | open-and-local-language-models-arxiv |
| 17 | Extending FunctionGemma for Practical On-Device Mobile Function Calling | https://arxiv.org/abs/2609.25373 | 2026-09-21 | open-and-local-language-models-arxiv |
| 18 | Quantization Thresholds Replicate, Failure Modes Do Not: A Three-Model Study of Agentic Tool Use in Polish from 8-bit to 2-bit | https://arxiv.org/abs/2609.32042 | 2026-09-25 | open-and-local-language-models-arxiv |
| 19 | Quantization Thresholds Replicate, Failure Modes Do Not (same paper, second lane) | https://arxiv.org/abs/2609.32042 | 2026-09-25 | quantization-compression via arxiv |
| 20 | Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses | https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/ | 2026-09-08 | quantization-compression via hn |
| 21 | LRU is harder to beat than the KV-cache papers suggest (agentic-kv-cache) | https://github.com/gauravapiscean/agentic-kv-cache | 2026-09-10 | quantization-compression via hn |

## Honest gaps

Lane-reported gaps and OWED items that survived folding (each tagged with its lane; none of these
is asserted as verified by this fold):

1. The eval cell the estate cares about most is empty in the public literature: no in-window
   published eval isolates 2-4 bit weight quantization on 2B-8B tool-call JSON validity
   (quantization-compression via arxiv and hn notes). The estate-side probe is designed in S2,
   not run.
2. No public structure-vs-prose (memweave) measured experiment exists; the proposed estate A/B
   (same-byte prose vs structured packs on the gemma:2b battery, measuring cached-prefix reuse,
   accuracy, and needle recall) is designed, not run (kv-cache-context-engineering reddit and x
   notes).
3. The lens corpus.md 97,865-row scrape was never located in-repo; the figure rides the ask
   (open-and-local-language-models-arxiv note). Catalog row counts also disagree across lanes
   (581,477 on 09-28 vs 674,146 measured 09-29): different instruments at different moments on a
   growing file, named per the B2-216 census-denominator discipline (glossed at S5 item 2), not
   reconciled by this fold.
4. License primaries unread: Kimi K3 / Qwen 3.8 license terms rest on the HF blog summary plus
   one UNVERIFIED reader comment claiming a $20M/year serving cap; MiniMax M2.7 and Kimi K3
   license threads are snippet-grade only (open-and-local-language-models arxiv and reddit notes).
5. The Anthropic threat-intelligence report behind the Moonshot relay story (nearly 300,000
   relayed customer requests) was not fetched; the story is single-sourced to Anthropic and
   contested in-thread (open-and-local-language-models hn note).
6. The smol.ai AINews archive truncates at Sep 10, so Sep 11-28 X coverage is under-sampled in
   three x lanes (open-and-local-x, swarm-x, inference-x notes).
7. The V4.1-Flash total-parameter conflict (ArtificialAnalysis 552B vs smol-recap 763B) is
   reported unresolved; the desk-verified primary number is 552B (open-and-local-language-models
   via x note).
8. Reddit enumeration was door-limited: pullpush listing 429s capped the open-and-local reddit
   census at about 59 candidates (8 verifiably in-window); the quantization-compression reddit
   lane found ZERO in-window threads and reports the 30-day constraint as FAILED, not papered
   over; the evals reddit lane leaned on one redlib mirror with intermittent 429s (three reddit
   lane notes).
9. Swarm: no published design on provider-429 dispatch shapes or 50-wide fan-out retry topology
   surfaced in the window, so the estate's retry-on-shape and first-contact-as-HOLD laws stand
   unchallenged but uncorroborated; six leads were seen at feed-gist level only and are flagged,
   not banked (swarm-orchestration via arxiv note: 2609.12746, 2609.12404, 2609.07247, 2609.16491,
   2609.30293, 2609.22573).
10. Agent-memory negatives stated as findings: no published longitudinal next-session-success
    study from transcript mining surfaced in the window; no merkle or verkle-chained
    agent-memory log design exists outside the estate's own chain (agent-memory-continuity hn and
    reddit notes).
11. Evals RQ5 (the evals lane's fifth research question, code-to-doctrine linking: tying each
    filed law to the module that enforces it) remains OPEN with no new in-window evidence; Population
    Physics HTML 404'd (abs-page read only, confidence marked lower); FutureX stayed unverified
    and was deliberately not banked (evals-self-improvement arxiv and x notes).
12. Inference efficiency: no Windows head-to-head llama.cpp/Ollama/vLLM benchmark in-window
    (nearest is an InventiveHQ Windows Server 2025 run with stated gaps: no warmups, no prefill,
    no concurrency); rib Q9 (lens/laws.md:76, verified this session: per-lane Windows GPU/RAM
    process attribution without psutil) stays open; ETW / uberAgent /
    CHAOS energy leads are search-sourced only, primaries not read; the Q7 cool/heat-map question
    (lens/laws.md:74, verified this session: the per-lane free-tier yield map) got nothing
    in-window (inference-efficiency arxiv, hn, reddit, x notes).
13. Quote provenance: several hn-lane quotes ride the WebFetch reader model, so verbatim fidelity
    is high-confidence but not byte-guaranteed; byte-verification is OWED before any become laws
    (kv-cache hn and swarm hn notes; the swarm hn lane did byte-verify 8 titles/dates via the
    Algolia items API).
14. Single-item OWEDs carried in lane notes: LensVLM paper arXiv 2605.07019 (its model card
    carries zero benchmark numbers); XGrammar-2 MLC blog and Willison grammars TIL surfaced but
    unread; the nvidia-smi sampling energy paper never located via arXiv API; fraserpricee's SSD
    streaming recipe follow-up not published in-window; the belindmo co-writing article 404'd
    through every door (snippet-only, parked); the cyi12 "1.5B on 200-500 examples" status id
    unresolved.

## Unconfirmed items (kept honest, with confirmation evidence)

None of these three is in register.jsonl and none is cited as support anywhere in this fold.

### U1. "Pre-caching context overhead (system prompt, tools, skills, ...) ?" (reddit 1wlazxc, kv-cache-context-engineering)

The banked item claimed a byte-identical-prefix quote, drift enemies (timestamps, working dir,
MCP/skills blocks), and a hash-the-overhead verification instrument. The confirmation pass reached
the live thread via safereddit (redlib v0.36.0) after solving its own Anubis sha256
difficulty-2 proof-of-work (nonce 270; solver in %TEMP%), then fetched the thread (HTTP 200,
21,425 bytes). Page facts: post by u/butterfly_labs, 13 comments, 8 comment blocks rendered. The
OP's TTFT anecdote is verbatim real: "strips the date/time from its system prompt. Tested
manually, and the TTFT is now very acceptable (5-10 seconds)". But the claimed quote ("the idea
works, but only if the prefix is byte-identical every time...") appears NOWHERE: the word "byte"
has 0 hits in the raw HTML; the nearest real text is split across two different commenters
("make sure that the harness you're using is actually using 100% identicall..." and "and yes the
prefix must match character by character."); "working dir" has 0 hits; "hash"/"checksum"/"sha"
have 0 hits. Verdict: the quote is paraphrase-as-verbatim and two of the named claims are absent
from the page. The underlying practice (byte-identical prefix, strip timestamps) stands on other
banked evidence (the doug.sh vLLM post, the cache-engineering X article), not on this thread.

### U2. "Qwen 3.6-35B-A3B KV cache bench: f16 vs q8_0 vs turbo3 vs turbo4 from 0 to 1M context on M5 Max" (reddit 1sy7srk)

The post exists: the exact URL and title are search-indexed, and one indexed body snippet shows
measured tables ("At 256K turbo3 wins prefill +27% over turbo4 (128 vs 101 t/s)..."). But the
confirmation pass reached only Reddit shells and 403s through every door (www/old/api reddit,
r.jina.ai, curl with a browser UA returned a 189,908-byte refusal), the single Wayback snapshot
captured Reddit's verification interstitial rather than content, and archive.ph 404'd. The claimed
quote and every specific sub-claim (3 reps / 8h wall clock; q8_0 holding ~95% of f16 decode to
128K then OOM past 256K; turbo3 13.3/6.5 tok/s at 512K/1M; q8_0 as the safe default at normal
agent depths) are UNSEEN and marked OWED. Nothing from this thread may be cited as support.

### U3. "What Stops a Small Language Model From Driving a Database Agent" (arXiv 2609.21341)

Re-fetch of the abs page and HTML v1 confirmed the quote in substance ("Five server changes,
touching no model, prompt or sampling setting, moved six models by 6 to 21 cells out of 30"), the
75.7% tool-invocation share of 2,100 model-attributed losses across 39 locally served models and
8,199 runs, transport (36.2%) vs capability (17.3%) as the largest and smallest failure classes,
and both the unbounded-context (7.1 GB resident at 51 GB with a 262,144-token context on a 64 GB
machine) and swap confound sections. NOT confirmed as banked: "qwen3:4b is the cheapest full-lock
agent" is the estate's inference; "cheapest" appears nowhere on the page and the paper never
ranks models by cost (Table 5 lists qwen3:4b among five full-lock models). The banked claim also
omits the paper's own caveat that the transport>capability ordering "is a property of this corpus
rather than a general finding" (holds in only 74.5% of model-clustered resamples). Held with
these corrections; metadata verified (authors, 2026-09-18 submission, cs.SE/cs.DB, dataset at
doi 10.57967/hf/10485).
