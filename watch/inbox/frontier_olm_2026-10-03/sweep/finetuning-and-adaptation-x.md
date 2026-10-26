# SWEEP: finetuning-and-adaptation via x - 2026-10-03

Seat: sweep-finetuning-and-adaptation-x (frontier olm). Area: finetuning-and-adaptation. Door: x (fxtwitter recipe), with named degradation and arXiv fallback per recipe.

## Door status (honest accounting)

- WebSearch with site:x.com was NOT honored by the search backend (6 phrasings tried); x.com status URLs are essentially unindexed. A direct mirror attempt (twstalker.com/Teknium1) 403'd on Cloudflare. alphaXiv and HuggingFace papers pages for the anchor paper carried zero X embeds.
- The fxtwitter door itself WORKS: resolved https://api.fxtwitter.com/GoodfireAI/status/2070181051801235463 to full JSON (author, date 2026-06-25, 307k views, 6-tweet thread) on the first attempt; cross-verified the full 7-tweet unroll on threadreaderapp.com/thread/2070181051801235463.
- Because X post DISCOVERY is the broken leg (not resolution), 7 of 8 banked items are arXiv abstract pages fetched and read directly this session. This is the recipe's named fallback; the search-result-snippet route was not needed because the primary pages fetched clean.

## Pass 1 (broad sweep, 2026-09-03 through 2026-10-03)

Candidates considered (42+), pulled from export.arxiv.org API listings this session:

- RQ1 vein (LoRA/forgetting, 24 entries): 2610.02148 Omni-Embed-Mini, 2610.01702 TORA, 2609.39839 DLEPEM, 2609.39550 HyPro, 2609.39390 TALON, 2609.39367 Dynamical Theory of LoRA (forgetting grows with rank), 2609.38591, 2609.38251 Fisher-weighted LoRA gradient surgery, 2609.34453 SPACE-LoRA, 2609.32818 first-order forgetting bounds, 2609.25618 NB-LoRA (reasoning-preserving SFT), 2609.24678 Muon beats dedicated continual learning, 2609.23989 ACLArena, 2609.23916 Time-Incremental CPT, 2609.23594 BOD, 2609.18444 DR.WILSS, 2609.11310 soft prompting (no forgetting), 2609.06986 composed mechanisms 1.2 pct to 34.9 pct retention; near anchor 2602.04998 "Vanilla LoRA May Suffice" (Feb 2026, window violation, noted).
- RQ3 vein (collapse/self-distillation, 14 entries): 2610.01493 entropy-rate filter, 2610.01318, 2609.40295 AI-token scaling law, 2609.35512, 2609.34257 recursive biomedical degradation, 2609.32987, 2609.18878 Fisher-Rao human-data ratio (already in catalog), 2609.18560 population-genetics collapse, 2609.15314 implosion threshold, 2609.12353 SynthSentry, 2609.11149 Break Step, 2609.11146 oligarch steering (already in catalog).
- RQ2 vein (agent-trajectory corpora, 15 entries): 2610.00949 PG-SFT (turn-level info-gain SFT), 2609.36588, 2609.32795 AgentHabit, 2609.20715 Don't Mask the Environment, 2609.18417 dependency-DAG trajectory refinement (minus 48 pct inference tokens), 2609.04148 Terminal-Universe, 2609.28554 Pistis, 2609.07782 TrajectoryDB; near-window: 2608.30147 CAST, 2608.29357 LiteSearch-VL, 2608.27449 SWE-Prime (10 pct selected subset beats full SFT data by up to 24.2 pct), 2608.24188 Paritok-4B (67,074 real OpenHands trajectories distilled).
- RQ4 vein: 2609.05111 ICL/SFT/KL-RL Bayesian unification, 2609.07334 AAS-RAIL, plus the Goodfire X thread (minimal-data behavioral edit).

## Pass 2 (deep reads, 9 items read end to end this session)

1. Goodfire thread (fxtwitter + threadreaderapp, 7 tweets): removed a 67M-param model's German by tuning ONE scalar factor on one weight subcomponent using 4 German tokens; benchmarked vs LoRA: their edit left other languages almost untouched, "The LoRAs often wrecked French, Spanish, Italian, and sometimes English"; they concede the decomposition step already spent tokens (amortizes across future edits); posted a correction for an off-target-effect plotting error.
2. arxiv.org/abs/2609.23916 (Time-Incremental CPT, 2026-09-20): 6 open models (1B to 8B: OLMo2, Llama-3.1/3.2, Gemma-3-1B) on post-cutoff FineWeb-Edu: knowledge acquired with NO catastrophic forgetting (macro drift within 0.01 of base across 13 tasks); "data quality dominates quantity" (a 6B curated slice matched a 40B broader one); knowledge-vs-capability optimal learning rates differ by roughly an order of magnitude; LoRA at sufficient rank matches full CPT; gains survive SFT.
3. arxiv.org/abs/2609.11149 (Break Step, 2026-09-10): recursive fine-tuning diversity collapse traced NOT to gradual error accumulation but to vLLM shared-batch sampling: "every request receives the same random draws, and a fixed seed replays them every generation"; removing either sharing or replay holds unique-4-gram fraction near 0.98; keeping both drops it to 0.045-0.38 within three generations; a per-request seed fixes it; a peer-reviewed Gemma-2-27B collapse pipeline was affected.
4. arxiv.org/abs/2610.01493 (entropy-rate filter, 2026-10-01): model-free Kontoyiannis entropy-rate estimator h_k as a training-data filter; in a 6-generation QLoRA collapse run on Llama-3.1-8B, logprob filtering gave no significant diversity benefit (p > 0.23) while h_k filtering gave +42 pct unique trigrams, +30 pct vocabulary, minus 19 pct repetition (all p < 0.001); needs no model, no oracle, no human reference set.
5. arxiv.org/abs/2609.04148 (Terminal-Universe, Qwen team, 2026-09-03): replays recorded file operations from code-agent trajectories to restore pre-modification file states, a completion agent fills gaps, then synthesizes 37.3k task-sufficient environments scaled on breadth (cross-workspace) and depth (multi-round with a user agent); SFT of Qwen3.5-27B gained +11.9 on Terminal-Bench 2.1, +13.8 on EvoCode-Bench v2 MT@4.
6. arxiv.org/abs/2609.23989 (ACLArena, 2026-09-21): framework for agent continual learning; compares multi-teacher on-policy distillation, self-distilled fine-tuning, and model merging for stacking capabilities; proposes offline replay over high-quality trajectories plus routed LoRA experts each specialized via RL; analyzes forgetting at model AND token level.
7. arxiv.org/abs/2609.20715 (Don't Mask the Environment, 2026-09-17): ActObs supervises observation tokens in SFT instead of masking them; identical after SFT, diverges after GRPO: Qwen3-8B +3.4pp at pass@16, +4.2pp pass@1 cross-domain at 4B; action-only SFT degrades environment prediction below the base model.
8. arxiv.org/abs/2609.32795 (AgentHabit, 2026-09-26): 23-axis behavior taxonomy over 408 trajectories / 18 models; fine-tuning on ANOTHER model's trajectories changes only part of a model's behavior profile and leaves much of it intact; prompting shifts some axes readily, others barely; profiles stay recognizable across task sets.
9. arxiv.org/abs/2609.39390 (TALON, 2026-09-30): per-task LoRA-Teachers distilled into one LoRA-Student, 33x fewer deployment parameters, minus 41.7 pct inference time vs ASP; honorable mention (vision FSCIL, weakest estate transfer, cut from top 8).

## Answers to the four asks

- RQ1 (QLoRA vs LoRA vs full finetune with measured retention): 2026's converged answer is that method choice matters less than learning rate, rank, and data quality: vanilla LoRA matches variants once lr is tuned (2602.04998), LoRA at sufficient rank matches full CPT with measured non-forgetting (2609.23916), and forgetting grows with rank in theory (2609.39367). For teaching narrow law sets to small open models: LoRA/QLoRA at adequate rank with curated data is the retention-safe default; full FT is not the retention win folk doctrine claims.
- RQ2 (curation recipes for session-tape corpora): the session-tapes-to-environments recipe (Terminal-Universe) plus supervision-design changes (ActObs: keep observations as loss targets; PG-SFT: weight turns by information gain; SWE-Prime near-window: a 10 pct selected subset beats full data) is the published mold for the room.jsonl organ.
- RQ3 (swarm self-distillation): measured improvement conditions exist (ACLArena compares self-distilled FT against multi-teacher on-policy distillation and merging; its winning recipe is offline replay over HIGH-QUALITY trajectories plus routed experts) and the degradation conditions are now mechanism-named: shared and replayed sampler seeds collapse diversity within ten generations (Break Step), and unfiltered self-data loses rare patterns (the entropy-rate filter fixes this model-free). Self-distillation degrades by sampler and by filter, not by self-reference per se.
- RQ4 (few-shot style lock): the extreme point is Goodfire's parameter decomposition (a behavioral edit from 4 tokens); the measurable-profile instrument is AgentHabit's 23 axes (which also bounds what a style lock can transfer cross-model); TALON shows per-task teacher distillation into one adapter as the lock-and-merge pattern. The estate's song style-lock (SEED SAVER 831936fb6) matches the Goodfire lesson: lock style onto a narrow, identified component rather than the whole weight surface.

## Overlap checks (grep, this session)

- catalog/catalog.jsonl: "Terminal-Universe" 2 hits (state/arxiv/2026-09-06/2609.04148v1.txt plus watch/INTAKE_TERMINAL_UNIVERSE_20260904.md via @dair_ai); "Time-Incremental" 1 (state/arxiv/2026-09-22/2609.23916v1.txt); "Observation Supervision" 1 (state/arxiv/2026-09-18/2609.20715v1.txt); "model collapse" 2 (including 2609.18878 Fisher-Rao raw abstract); "self-distillation" 18; "LoRA" 131. Zero hits: Break Step, AgentHabit, ACLArena, Goodfire, Kontoyiannis, TALON-as-paper (the 6 TALON hits are WoW zone files: stonetalon_mountains.cpp and boss_talon_king_ikiss.cpp), ActObs.
- memory/ (rg, excluding state/arxiv raw mirrors): Terminal-Universe 3 files (watch_mining inventory and timeline, decks snapshot); Goodfire 7 files but all about the company's SAE/steering work (reward-hack probes, persona salon, living_map research-pack note), NOT the June 25 LoRA-degradation benchmark; self-distillation 1; ouroboros 18 (descent-protocol concept known); zero: Break Step, AgentHabit, ACLArena, Kontoyiannis.
- Verdict: 5 of 8 banked items are genuinely new to the estate; 3 (Terminal-Universe, Time-Incremental CPT, Don't Mask) are held as raw abstracts only, and this sweep's value there is the deep-read numbers the raw abstracts lack.

---

# SECOND PASS (different gopher, same area, same day): optimizer-feasibility + grader-gates + adapter-format vein

source-fetched: 2026-10-03
Gopher: sweep-finetuning-and-adaptation-x (second run at this path; items below are DISJOINT
from the first pass above - no overlap in banked items, both passes preserved).

## Door health this session (recipe compliance)

- **X discovery: DEGRADED.** 9 WebSearch attempts; 6 returned MCP 1302/429 rate-limit storms
  (some after internal retries), and the 3 that succeeded returned zero resolvable
  x.com status URLs (one gave bare `https://x.com` with no status ID; one surfaced a
  @kafkaup TACO post as a Chinese snippet with no status ID). Per the fetch recipe the
  fallback is to bank the snippet with its URL and say so: neither snippet carried a URL
  resolvable through the fxtwitter door, so neither is banked as an item. No in-area X post
  was resolved through api.fxtwitter.com this session. The door itself was verified OPEN
  earlier today by the lens (doors.md:54-60, fixture jack/status/20); the degradation is in
  discovery (search 429s), not resolution - consistent with the first pass's finding that
  resolution works when you hold an ID.
- **arXiv export API: OPEN** (12 queries, ~75 candidates scanned).
- **GitHub raw/API: OPEN** (gh api: licenses, Ollama code at pinned refs, release notes).
- **One hook intercept:** a Bash file-redirect writing fetched source code to disk was
  blocked by the Mimosa seat hook; the check was re-run as a pipe instead. Same data, no
  file bypass.

## Pass 1 (breadth): 34+ candidates considered, last 30 days

arXiv descending-submittedDate scans: ternary fine-tuning (15 returned, 5 in-window
relevant), reward-model + hallucination (15), test-time adaptation + language model (15),
benchmark contamination (15 of 25), LLM-as-a-judge + reliability (12). WebSearch (degraded)
added: Unsloth/Gemma finetuning results, RLVR reward-hacking discussions, the Allternit
weekly mention of TACO. Notable candidates NOT banked (outside window or weaker): Low-Rank
Ternary Adaptation 2608.24469 (2026-08-25, 39 days), Benchmark Contamination Taxonomy
2608.29463 (2026-08-29, 35 days), Hallucination Self-Play 2607.07993 (Jul),
Category-Aware Iterative Expert Training 2609.23377 (09-20; the abstract does NOT contain
the evaluator-hacking sentence the search snippet claimed - snippet/abstract mismatch,
demoted), Pair Difficulty 2609.37577 and LLMAdBench 2609.32533 (abstract-level reads only;
not deep-read, not banked).

## Pass 2 (deep reads): 7 items read end to end

### 1. Ollama removed LoRA adapter support in v0.35.0 (RQ5) - silent breaking change

- URL: https://github.com/ollama/ollama/blob/v0.35.1/cmd/cmd.go (read via gh api raw at
  refs v0.30.0, v0.31.0, v0.32.0, v0.33.0, v0.34.0, v0.35.0, v0.35.1, main; plus
  docs/modelfile.mdx at main and its commit history).
- Quote (cmd/cmd.go:293 at v0.35.1): `errAdaptersUnsupported = errors.New("LoRA adapters are no longer supported")`
- Checks run this session: (a) current docs/modelfile.mdx (main, 13,006 bytes) contains ZERO
  occurrences of "adapter"/"ADAPTER"/"lora"/"merge"/"quantize"; instruction set is now FROM,
  PARAMETER, TEMPLATE, SYSTEM, LICENSE, MESSAGE, CAPABILITY, REQUIRES. (b) parser/parser.go
  still lexes "adapter" as a valid command (lines 114, 446, 472, 732) - it parses, then:
  (c) cmd/cmd.go:335-336 rejects any Modelfile carrying an adapter command with
  errAdaptersUnsupported at create time. (d) Bisect: error string absent at
  v0.30.0-v0.34.0, present at v0.35.0 (release published 2026-09-28T21:23:22Z) and
  v0.35.1 (2026-09-29, current latest). (e) None of the last 15 release-note bodies mention
  adapters (rg over the releases JSON returned nothing) - undocumented in release notes.
- Findings against RQ5: the local serving stack at current release accepts NO adapter format
  at all, for any family including Gemma. The historical answer (ADAPTER ./lora.gguf in the
  Modelfile, safetensors QLoRA import) is dead code on v0.35+. "Measured swap cost per
  adapter on the janitor lanes" is therefore moot on v0.35+: the only remaining path is
  merge adapters offline into base weights and ship a merged GGUF/safetensors via FROM, so
  per-adapter cost becomes a full model swap (GGUF load time), not an adapter hot-swap.
  NOT RUN this session: any local measurement (no janitor lane touched, no ollama
  create/swap executed) - the measured number is OWED, and only meaningful if the estate
  pins an Ollama version or adopts merge-then-ship.
- Estate action implied: `mag/lora_pipeline` and `training_packager` assumptions need a
  re-check against v0.35 semantics before any training_packager output is pointed at
  `ollama create`; the v0.35 line also adds CAPABILITY/REQUIRES instructions (PR #18708,
  2026-09-29) worth a separate read. OWED if pursued.
- Overlap: `rg -c -i "adapters are no longer supported"` over catalog/catalog.jsonl +
  memory/: zero rows; `errAdaptersUnsupported`: zero rows. Genuinely new to the estate.

### 2. TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning (RQ1)

- URL: https://arxiv.org/abs/2610.02199 (v1, 2026-10-01, UCF + Mohammed VI Polytechnic;
  24 pp; code github.com/Jichao2357/TACO_optimizer). Full text also read:
  https://arxiv.org/html/2610.02199v1.
- Quote (full text, Sec 6): "Figure 3 compares TACO with memory-efficient and conventional
  first-order optimizers across eight downstream tasks."
- Findings against RQ1: (a) abstract claims 174x optimizer-state reduction vs AdamW8bit
  (27.7 GB to 0.16 GB) and 2.9x peak training memory reduction (80.6 GB to 27.5 GB) on
  OPT-13B; 30-32B finetuning on a single 80 GB H100. (b) NO LoRA/QLoRA experimental baseline
  anywhere: E1 compares "six baseline optimizers" - AdamW8bit, Adafactor, APOLLO-Mini,
  FlashAdamW, GaLore, Muon - all full-parameter; LoRA appears only as intro related work.
  So its claim structure is vs memory-efficient full-parameter optimizers, NOT vs a measured
  LoRA baseline. (c) Metrics are downstream accuracy/F1 (SST-2, RTE, BoolQ, COPA, CB,
  MultiRC-F1A, SQuAD-F1, DROP-F1), not perplexity - that half is the right claim shape.
  (d) Models: OPT-1.3B/6.7B/13B/30B, Qwen3-8B/14B/32B, Pythia-12B, Llama-3.1-8B,
  Mistral-24B. No Gemma of any size, no janitor-scale (2B/4B) memory numbers, no consumer
  GPU claims. Even the 13B peak (27.5 GB) is roughly 2-3x above an RX 5600 XT 16GB card,
  and the RX 5600 XT (RDNA1) CUDA/ROCm story was not verified this session (OWED: check
  TACO_optimizer repo hardware requirements before any trial).
- Verdict for the estate: TACO does NOT establish janitor-scale finetuning on RX 5600
  XT-class VRAM. It makes 8-32B full-parameter finetuning fit an 80 GB H100. The honest use:
  if a funded H100 lane ever opens, TACO-style ternary optimizer state is the memory shape;
  on local janitor hardware the open question stays LoRA/QLoRA - and item 1 changes that
  question entirely.
- Overlap: abstract already on disk (catalog row 582bd1b23b9b,
  state/arxiv/2026-10-02/2610.02199v1.txt, 1,772 bytes); zero hits for "Ternary Absolute-max"
  in memory/ and zero in today's DIGEST.md - raw pull, never mined. This banking adds the
  no-LoRA-baseline, no-Gemma, and memory-floor findings.

### 3. ImpossibleRubrics: Stress-Testing Generated Rubrics as Reward Signals (RQ3)

- URL: https://arxiv.org/abs/2609.16816 (v1, 2026-09-15; Qin, Xie, Liu, Yang).
- Quote (from the abs page): "The problem is not that rubrics are vague; it is that they
  are specific about the wrong things."
- Findings against RQ3: 169 impossible tasks across six categories, each with an "oracle
  certificate" defining what an honest answer may claim, plus 48 answerable controls. On an
  unbiased 150-of-169 cut, "Eleven generators are exploited 8--26% of the time"; the
  strongest generator still loses 36% on a stress cut while a certificate-faithful rubric
  scores 0%; a generic "be decisive, penalize hedging" rubric is exploited 64%.
- Adoptable by judge2 / duel instruments BEFORE any self-training loop fires: (a) every
  grading surface gets an oracle certificate (what an honest pass may claim) generated
  separately from the rubric; (b) an adversarial impossible-task suite audits any generated
  rubric for exploitability before it grades real work - the ratchet/citation-lint pattern
  applied to judges; (c) a rubric that leaks which claims to fabricate is worse than a vague
  one, so judge2 must audit its own prompts the way the paper audits generators. This slots
  next to the imagined-grader find already banked (burns.md:91-93, r6): DeepSWE rollouts
  reasoned about an imagined grader; ImpossibleRubrics shows even the real grader's rubric
  can be gamed at 8-26%.
- Overlap: abstract already on disk (catalog row cf236e13417c,
  state/arxiv/2026-09-16/2609.16816v1.txt, 1,924 bytes); zero memory/ + DIGEST hits - not
  mined. This banking adds the certificate-gate mechanism.

### 4. Designing Reliable LLM-as-a-Judge Measurement Systems for Multi-Turn Business Agents (RQ3)

- URL: https://arxiv.org/abs/2609.33955 (v1, 2026-09-27; Luo, Gao).
- Quote (from the abs page): "Independent human audits estimate measurement fidelity, renew
  tiered reference sets, and route disagreements to label correction, guideline revision, or
  judge improvement."
- Findings against RQ3: production-grade judge reliability is run as a measurement SYSTEM,
  not a prompt: atomic judges sharing versioned evidence through an explicit aggregation
  graph; an intent-preserving user simulator gated by task-preservation and stability checks
  before release; recurring independent human audits; tiered reference sets renewed over
  time; disagreement routing to three destinations (label correction, guideline revision,
  judge improvement). The authors flag their own evidence honestly: "these findings
  demonstrate operational usefulness rather than causal or universal superiority."
- Adoptable: judge2's promotion path maps 1:1 - seats draft verdicts (volume unbounded),
  the operator audit renews the reference set (authority bounded, lens/laws.md:38-40), and
  judge disagreement routes to corpus fix, spec fix, or judge swap. The duel instruments
  should record which destination each disagreement was routed to, making judge drift
  measurable over time.
- Overlap: no catalog rows, zero memory/ hits - new.

### 5. Harness Learning Enables Generalizable Test-Time Adaptation (RQ4)

- URL: https://arxiv.org/abs/2609.35738 (v1, 2026-09-28; authors include Salakhutdinov,
  Khashabi, Zanette).
- Quote (from the abstract): "At test time, the proposer uses feedback from successive
  executions on a new task to refine the harness, without performing any parameter-space
  update."
- Findings against RQ4: this IS the literature's version of the percolator loop - a proposer
  model revises the harness (the executable program organizing model calls, tool use,
  information flow) from execution feedback, trained by RL with revised-harness task
  performance as reward, explicitly framed as "meta-learning over executable programs, with
  harness revisions playing the role of weight updates in gradient-based adaptation."
  Benefits transfer to unseen tasks. The percolator's invariant-promotion loop (deterministic
  grammar, human-gated promotion - lens/laws.md:40,50) is the same shape with the promotion
  gate where this paper puts the RL reward. What the paper has that the percolator lacks:
  an RL-trained proposer and a measured transfer claim. What the percolator has that the
  paper lacks: human authority on promotion and a deterministic grammar - exactly the safety
  property the paper gives up. Overturner for the ranking (TTA/promotion above weight
  finetuning for this estate): a cheap adapter-sampling method (item 6's shape) matching or
  beating promoted-invariant gains on estate tasks at comparable cost, or evidence that
  harness revision saturates where weights move the needle.
- Overlap: abstract already on disk (catalog row dcbc53d4aa9f,
  state/arxiv/2026-09-29/2609.35738v1.txt, 1,572 bytes); zero memory/ + DIGEST hits - not
  mined. This banking adds the percolator mapping and the overturner criteria.

### 6. Learning to Predict Distributions over Weight Updates for Test-Time Adaptation (RQ4)

- URL: https://arxiv.org/abs/2610.01934 (v1, 2026-10-01; Khan, Ramji, Naseem, Anwar,
  Fernandez Astudillo).
- Quote (from the abs page): "instead of spending additional compute only by sampling more
  token sequences from a fixed model, we sample weight updates, yielding multiple adapted
  models for the same query"
- Findings against RQ4: the newest move on the TTA-vs-finetuning axis dissolves the binary -
  a query-conditioned hypernetwork predicts a DISTRIBUTION over LoRA updates from the query
  alone (no demonstrations), and test-time compute buys sampled adapters instead of sampled
  token sequences. Weight-update sampling beats "corresponding token-sampling adaptation
  baselines"; even the distribution mean beats deterministic hypernetworks; generated
  updates transfer across queries (reusable adaptation structure). For the estate: this is
  the concrete shape of evidence that would move the ranking toward weight-space adaptation
  - if a small hypernetwork can emit per-task janitor adapters cheaply, the invariant bank
  stops being the only cheap adaptation channel. It is also, notably, an adapter format
  question again (LoRA updates) - which item 1 shows the estate's serving stack can no
  longer consume at runtime.
- Overlap: abstract already on disk (catalog row 3d0895ceda4b,
  state/arxiv/2026-10-02/2610.01934v1.txt, 1,745 bytes); zero memory/ + DIGEST hits - not
  mined.

### 7. TerMeZO: Ternary Sparse Zeroth-Order Optimization for Fine-tuning BitNet Models at the Edge (RQ1)

- URL: https://arxiv.org/abs/2609.33548 (v1, 2026-09-27; Sifaou, Katti, Rajendran, Simeone).
- Quote (from the abstract): "TerMeZO matches or exceeds the performance of full-parameter
  MeZO while substantially reducing the fine-tuning memory footprint."
- Findings against RQ1: the successor line to TACO on the ternary axis, aimed at exactly
  janitor scale - BitNet models 1B-3B fine-tuned via forward-pass-only zeroth-order updates
  that exploit ternary quantizer geometry to pick which latent weights will move ("identify
  the latent weights that are more likely to change values during fine-tuning" at no extra
  cost). Measured on classification, instruction-following, and math reasoning. Honest gaps:
  no concrete memory numbers or edge hardware in the abstract ("the Edge" lives only in the
  title), baseline is full-parameter MeZO only - again no LoRA baseline - and BitNet
  ternary checkpoints are not the estate's janitors (gemma:2b / gemma4 are quantized GGUF
  animals). Relevance: it proves the ternary-training line is marching toward janitor-scale
  on-edge finetuning; nothing in it yet makes the RX 5600 XT a training target.
- Overlap: no catalog rows (the 09-27 arXiv pull missed it), zero memory/ hits - new.

## Cross-question synthesis (what this pass returns to the estate)

1. **RQ1 (TACO feasibility):** NO on RX 5600 XT-class VRAM, on the paper's own numbers
   (13B peak 27.5 GB; no sub-3B measurements; no Gemma; no consumer/AMD claims), and it
   claims against AdamW8bit/GaLore/Muon, never against a measured LoRA baseline - though
   its metrics are task accuracy/F1, not perplexity, which is the right claim shape. The
   ternary line's janitor-scale hope is TerMeZO-shaped (1-3B, forward-only), not
   TACO-shaped (30-32B, H100).
2. **RQ5 (adapter format) is this pass's hardest find and it invalidates part of the
   estate map:** Ollama v0.35.0 (2026-09-28) removed LoRA adapters entirely
   (cmd/cmd.go:293,335-336 at v0.35.1; docs scrubbed; release notes silent). The
   lora_pipeline/training_packager estate map needs an ollama-version gate: any "swap cost
   per adapter" plan now decomposes into merge-offline + full-GGUF-swap. Measured swap
   cost: OWED (no lane touched this session).
3. **RQ3 (imagined graders):** the two adoptables are ImpossibleRubrics' oracle-certificate
   adversarial audit (8-26% exploit rates on generated rubrics; 0% for certificate-faithful)
   and the judge-measurement-system cadence (atomic judges, versioned evidence, recurring
   human audits, tiered reference renewal, disagreement routing). Both are preconditions
   for any self-training loop; both match existing estate law (volume unbounded / authority
   bounded, lens/laws.md:38-40).
4. **RQ4 (percolator as TTA):** the literature's newest work (harness learning, 09-28;
   weight-update sampling, 10-01) independently converges on "adapt the program/adapters,
   not the weights, with execution feedback as the signal" - the percolator ranking is
   currently aligned with the frontier, and the named overturner is a cheap
   adapter-sampling result matching promoted-invariant gains at estate task granularity.
5. **RQ2 (corpora to SFT pairs):** license facts verified this session via gh api:
   microsoft/generative-ai-for-beginners = MIT (pushed 2026-10-01),
   microsoft/ai-agents-for-beginners = MIT (2026-09-19), openai/openai-cookbook = MIT
   (2026-10-03). The courseware block (~24,691 rows, corpus.md:20) is license-clean for
   SFT/QLoRA training; the seat tapes (oral_history/seat_pools 11,873 children,
   corpus.md:28) are estate-owned with no license friction but need a secret/PII scrub
   gate, and carry a self-contamination risk the courseware does not: a judge trained on
   seat tapes learns the graders it will later judge (the same failure class the
   imagined-grader find names). Contamination gate shape for a model that judges:
   certificate-style eval-set exclusion (item 3) + near-dup scan of training rows against
   every eval set the judge will be scored on, before promotion - promotion stays
   human-gated (lens/laws.md:40) regardless of what the data looks like.

## OWED (could not verify this session)

- Any in-area X post resolved through fxtwitter (discovery degraded; no status IDs surfaced;
  the first pass holds the one successful fxtwitter resolution of the day, GoodfireAI).
- TACO_optimizer repo hardware requirements / AMD support (not fetched).
- Measured adapter or merged-GGUF swap cost on the janitor lanes (no lane touched; on
  v0.35+ adapter swap is unsupported, making the old measurement target undefined).
- Whether any ollama release note ever documented the adapter removal (none of the last 15
  release bodies mention it; older notes not exhaustively swept).
