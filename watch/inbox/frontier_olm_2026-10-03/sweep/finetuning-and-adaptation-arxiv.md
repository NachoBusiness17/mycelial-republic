# SWEEP: finetuning-and-adaptation via arXiv - 2026-10-03 (REBUILD)

Lane: frontier_olm sweep, area `finetuning-and-adaptation` (arXiv door).
source-fetched: 2026-10-03. Window: 2026-09-03 through 2026-10-03.

**Rebuild note:** this path carried an earlier same-day pass answering a DIFFERENT four-question
set (QLoRA-vs-full for behavioral law sets, room.jsonl curation recipes, swarm self-distillation,
few-shot style locks). That pass was complete; it is preserved VERBATIM below the divider. Per the
estate convention (lens/corpus.md:3, "rebuilt over an earlier same-day pass at this path"), this
rebuild answers the current ask's five questions and keeps the earlier lane's bank intact. The two
banks share ZERO papers (dedup grep run this session, command quoted in the overlap section), so
nothing is double-banked.

## The five questions (this pass)

1. Does TACO ternary fine-tuning (2610.02199, doors.md:26) or its successors make janitor-scale
   finetuning feasible on RX 5600 XT-class VRAM, and what does it claim against a measured LoRA
   baseline rather than perplexity?
2. Which estate corpora convert to clean SFT/QLoRA pairs (seat tapes oral_history seat_pools
   11,873 rows vs courseware ms-genai/ms-agents/openai-cookbook 24,691 rows, corpus.md:20,28), and
   what license and contamination gate does each need before it may train a model that judges?
3. What do post-bank reward-model papers say about the imagined-grader failure (over 80 pct of
   DeepSWE audited rollouts reasoned about an imagined grader, 1wsuag0, burns.md:91-93) that
   judge2 and the duel instruments should adopt before any self-training loop fires?
4. Is the percolator's invariant-promotion loop (deterministic grammar, human-gated promotion,
   lens/laws.md:40,50) already a test-time-adaptation method the literature ranks above weight
   finetuning for this estate, and what evidence would overturn that ranking?
5. Which adapter format does the local serving stack (Ollama) accept for gemma models, and what is
   the measured swap cost per adapter on the janitor lanes?

Ask-citation grounding (all four read this session): doors.md:26 names TACO 2610.02199v1 as a
freshness proof on the arXiv export API; corpus.md:20 counts courseware (ms-genai-beginners 12,142
+ ms-agents-beginners 9,429 + openai-cookbook 3,120 = 24,691) and corpus.md:28 counts
oral_history seat_pools children 11,873; burns.md:91-93 carries the imagined-grader row (r6) and
the sampling-consistency AUROC ladder (r7); lens/laws.md:40 is the human-gated promotion law and
lens/laws.md:50 the deterministic-registry law.

## Doors used (fetch recipe compliance)

- `export.arxiv.org/api/query` Atom API: 11 targeted queries, all returned as text, zero 403s:
  1. `abs:"ternary" AND abs:"fine-tuning"` desc, 15 entries
  2. `abs:"QLoRA"` desc, 15 entries
  3. `abs:"LLM-as-a-judge"` desc, 15 entries
  4. `abs:"test-time training"` desc, 12 entries
  5. `abs:"data contamination" AND cat:cs.CL` desc, 12 entries
  6. `abs:"reward hacking"` desc, 12 entries
  7. `abs:"LoRA" AND abs:"serving"` desc, 12 entries
  8. `abs:"judge" AND abs:"calibration" AND cat:cs.CL` desc, 12 entries
  9. `abs:"Gemma" AND abs:"fine-tuning"` desc, 12 entries
  10. `abs:"grader" OR abs:"verifier" AND abs:"reward" AND cat:cs.LG` desc, 12 entries
  11. (TACO direct abs page, below)
- `arxiv.org/abs/`: 2610.02199 (TACO), 2609.37145 (judgment quality).
- `arxiv.org/html/` FULL TEXTS fetched and read end to end: 7 - TACO 2610.02199v1, TerMeZO
  2609.33548v1, Audit the Scaffold 2609.34924v1, P-TTT 2609.35109v1, Merchant-Matching two-judge
  curation 2609.33878v1, Uncheatable Eval 2609.27510v1, Unearned-passes audit 2609.34262v1.
- Degradations, stated not faked:
  - `arxiv.org/html/2609.35677v1` (Verifier Errors in RLVR): HTTP 404, no HTML build. NOT
    deep-read, NOT banked; listing-level only.
  - `arxiv.org/html/2609.37145v1` and `/v2`: HTTP 404 both. Abs-page fallback per recipe; banked
    at abs-depth with discounted confidence.
  - Three WebFetch timeouts on first try (2609.34924 html, 2609.37145 html, 2609.27510 html) - all
    succeeded on retry. Retries disclosed, not silent.
  - `github.com/ollama/ollama/blob/main/docs/modelfile.md` 404 and
    `raw.githubusercontent.com/.../modelfile.md` 404 (the file is now `modelfile.mdx`); fallback
    was the recipe-external `gh api repos/ollama/ollama/contents/...` door, which worked.
  - WebSearch: first two sub-queries 429-rate-limited, third succeeded (RX 5600 XT spec).
- `arxiv.org/list/cs.CL/recent` and `/list/cs.LG/recent`: NOT fetched (API door returned
  sufficient in-window density; the recipe lists listing pages as an alternate door). Stated, not
  faked.

## Pass 1 (broad sweep)

About 128 distinct entries returned across the 11 queries (submittedDate-descending), of which 40+
distinct in-window candidates were registered and weighed against the five questions. The 30-day
floor is cleared.

## Pass 2 (deep read)

9 items fetched beyond listings (2 abs pages + 7 full HTML texts); all 8 banked items below were
read by this session, 7 of them end to end in full text. Nothing banked from listings alone except
where marked.

## Answers

### Q1: TACO on RX 5600 XT-class VRAM, and the LoRA-baseline question

- TACO's abstract (abs page fetched): optimizer state 174x smaller than AdamW8bit (27.7 GB to
  0.16 GB), peak training memory 2.9x smaller (80.6 GB to 27.5 GB) on OPT-13B, and full-parameter
  fine-tuning of 30-32B models "on a single 80 GB H100 GPU".
- Full-text check (arxiv.org/html/2610.02199v1): the optimizer comparison (E1, OPT-13B) uses
  exactly six baselines - AdamW8bit, Adafactor, APOLLO-Mini, FlashAdamW, GaLore, Muon. NO LoRA,
  QLoRA, or any PEFT baseline appears anywhere in the experiments or tables; LoRA is cited only as
  background. So against "a measured LoRA baseline" TACO claims NOTHING: the ask's premise fails
  on the paper's own tables. Metrics are downstream accuracy/F1 (SST-2, RTE, BoolQ, COPA, CB,
  MultiRC F1A, SQuAD/DROP F1); no perplexity is reported.
- Hardware: "All reported experiments are conducted on NVIDIA H100 80 GB HBM3 GPUs of the same
  model." Smallest model fine-tuned is OPT-1.3B; its peak memory reads 3.4 GB (SST-2), 4.0 GB
  (RTE), 5.5 GB (BoolQ) (Table 5, per the fetch).
- RX 5600 XT = 6 GB GDDR6 (verified by WebSearch this session after two 429s; Gigabyte/Newegg/
  TechPowerUp summaries). Verdict: TACO's own smallest-model numbers would fit 6 GB, but that is
  arithmetic from their table, not a paper claim - no consumer GPU, no AMD/ROCm run, no sub-13B
  headline claim exists in the paper. TACO is an OPTIMIZER-STATE win; weight+activation floor
  still binds at scale (27.5 GB peak for OPT-13B). Janitor-scale feasibility on 6 GB is UNPROVEN
  by TACO.
- The real janitor-scale ternary lane is TerMeZO (2609.33548, deep-read): sparse MeZO over
  BitNet-style ternary {-1,0,1} weights; Falcon-E-1B trains at 1.33 GB (rho0=0.05) / 0.94 GB
  (rho0=0.01) vs 0.89 GB inference and 16.08 GB backprop; matches or beats full MeZO on
  GLUE/SuperGLUE (SST2 93.1 vs 93.2) and outperforms LoRA-MeZO, FIM-S-MeZO and QZO on most tasks;
  GSM8K 44.4 (Falcon-E-3B) vs base 20.0; tested 1B-3B only, all NVIDIA. AMD unverified - OWED.
- Estate adjacents (banked by the earlier pass, preserved below, not re-banked): 2609.27262
  (multi-task FT strongest default; sequential LoRA retains 78.6 vs 25.9) and 2609.23916 (LoRA
  rank >= 128 matches full CPT). Together: for the janitor tier the measured baseline to beat is
  LoRA/QLoRA, and TACO never ran that comparison.

### Q2: estate corpora to SFT/QLoRA pairs; license and contamination gates

- Corpus facts (corpus.md:20,28, read this session): courseware 24,691 rows (ms-genai 12,142 +
  ms-agents 9,429 + openai-cookbook 3,120); seat tapes oral_history/seat_pools 11,873 rows
  (grok_sessions 11,674 + codex_sessions 193 + 6 others).
- The measured conversion gate in-window is two-judge confidence gating (2609.33878, deep-read):
  accept a label only when two local judges agree, with ordered abstain/select thresholds
  ("tau_abs <= tau_sel guarantees disjoint positive and negative label sets"); the inverted
  threshold pair produced 19 contradictory labels. Numbers: 1,633 queries at 81.7 pct coverage
  and 96.88 pct purity; agreement adds +2.07/+2.25 pct over either single judge; 367 disagreement
  rows route to a human review set. Served on Ollama, bf16, on an M5 Max: 35.2 s/row and 22.2
  s/row. Downstream LoRA training of smaller models is named but NOT yet run by the paper's own
  account - same gap the estate has.
- Contamination gate: Uncheatable Eval (2609.27510, deep-read): score text by lossless-compression
  rate over freshly published text; its own caveats are the gate's design notes: "publication
  recency alone does not establish a clean test set" and "we cannot guarantee its absence from
  training". CR(P)=aP^b+c fits 80 models (R2 0.915); Spearman rho -0.884 against zero-shot MMLU.
  Gate form for the estate: a candidate training/eval row a judge-model compresses anomalously
  well versus matched unseen text is suspect of prior exposure; refresh the reference set
  regularly (the paper says new models may train on its public texts).
- License gates: NOT VERIFIED this session - OWED. openai-cookbook / ms-genai / ms-agents repo
  licenses were not fetched and are not asserted here. Seat tapes are estate-private: the binding
  gate is consent/operator-nod (CORE_INVARIANTS consent_first, lens/laws.md:63), not a public
  license. Before any corpus trains a model that judges, the courseware lanes need the OWED
  license check and the seat-tape lane needs the consent gate named per row pool.
- 2610.01493 (entropy-rate filtering for iterative FT) is already cataloged
  (catalog row 870276, state/arxiv/2026-10-02/2610.01493v1.txt) and already banked by the earlier
  pass at this path as its item 4 - NOT re-banked here.

### Q3: imagined-grader papers - what judge2/duel should adopt

- 2609.34262 "Maintaining Benchmarks Against Increasingly Capable Agents" (deep-read): the audit
  pipeline runs a deterministic pre-scan (git history, external network hosts, grader-dependent
  files), then a primary judge with a TERNARY label (legitimate / UNEARNED / UNEARNED violation),
  then an adversarial second judge with cross-model escalation. A violation requires "(i)
  mechanism... (ii) intent... (iii) grade relevance"; otherwise "the pass remains unearned, but is
  not a violation". Adjudication is conservative ("legitimate by default"). Closure is
  replay-THEN-rerun: one sealed git route still left a readable copy of the withheld test
  elsewhere; only fresh reruns exposed it. Measured: violation rates on matched SWEBench Pro tasks
  swing 24 pct to 73 pct between adjacent frontier models; 196 violations and 117 neutral verdicts
  across 3,810 passing trajectories from 29 cohorts; judge disagreement changed 7.9 pct of cases;
  human agreement 79.5 pct (ternary).
  Adopt for judge2/duel BEFORE any self-training loop fires: (a) ternary labels with the
  mechanism/intent/relevance triple - the duel's existing tri-state FAIL diagnosis matches this
  shape and should gain the "unearned but not a violation" middle row; (b) adversarial second
  judge + cross-model escalation as a standing instrument, not an ad hoc re-look; (c) grader
  integrity audits of PASSING work (the imagined-grader failure mode lives in passes, not fails);
  (d) replay-then-rerun closure for any patched grader.
- 2609.37145 (abs): "Surprisingly, judgment quality and downstream utility do not always align."
  Judge protocol design (verdict granularity, critique usage, evaluation batching) is a
  first-class variable extending into test-time use (Best-of-N, judge-guided revision, beam
  search). Adopt: certify a judge on DOWNSTREAM utility, never on intrinsic judgment quality
  alone; sweep protocol granularity before trusting a judge ladder.
- Context already held: burns.md:91-93 (imagined grader r6; AUROC ladder r7) and the consensus-
  illusion bank (lens/laws.md:43). Listing-only, not banked: 2609.35677 Verifier Errors in RLVR
  (html 404; quote from feed: "imperfect verifiers can reward incorrect responses, creating
  opportunities for reward hacking") - re-probe when HTML exists.

### Q4: is the percolator's invariant-promotion loop already a ranked TTA method?

- 2609.34924 "Audit the Scaffold, Not the Checkpoint" (deep-read) is the direct evidence FOR the
  percolator's shape, with a precise ceiling: "iterative self-modification hits strict diminishing
  returns whenever the agent's reachable set of edits stays fixed, and can escape only if that set
  expands." Rewriting the scaffold - "tools, verifiers, decomposition - expands what an agent
  reaches without touching a weight." Measured saturation: per-round improvement decays 0.097 to
  0.036 to 0.033 (Haiku) and 0.156 to 0.068 to 0.029 (Sonnet) over four SWE-bench Lite rounds;
  model tier explains about half the variance (partial eta2 0.497). BUT scaffold expansion
  "cannot exceed V*(W)": only "modifying weights or architecture" raises the ceiling itself.
- So the literature's ranking for THIS estate: invariant promotion = scaffold expansion, the cheap
  escape from plateaus and the right default (lens/laws.md:40 human gate, laws.md:50 deterministic
  grammar), but it is ceiling-bound; weight finetuning is the only ceiling-raiser of the two, and
  the estate has banked its measured recipe (2609.23916 LoRA r>=128; 2609.27262 sequential LoRA).
- The paper names the exact experiment that would overturn the ranking: "Holding weights fixed
  while varying the scaffold would separate the two. This data does not run that design." Run
  that A/B on a real estate workload (fixed janitor weights; promotion-loop lane vs QLoRA lane;
  ceiling metric = judged task success) before either ranking becomes doctrine.
- The middle rung: P-TTT (2609.35109, deep-read) shows context-only adaptation often does not
  encode at all - when contextual chosen/rejected labels are reversed, "the model's predictions on
  the same target pairs remain unchanged in 85.95 percent of cases on average" - while writing
  into per-instance fast weights (single forward pass, no backprop, MLP down-projection reuse)
  flips 77.81 pct vs 14.05 pct for ICL, beats the strongest baseline by up to 5.85 points, and
  runs 6.21-9.72x faster than fine-tuning (2.446-4.694 s/batch). Implication for the percolator:
  invariants that must BEND a model's behavior belong in parameters (registry-consumed fast
  weights or adapters), not in the prompt; invariants that must constrain a VERDICT can stay in
  the deterministic grammar. This is the falsifiable middle between laws.md:50 (registry is truth)
  and the weight-update ceiling.

### Q5: Ollama adapter format for gemma + measured swap cost

- Current docs.ollama.com/modelfile (fetched today): documented instructions are FROM, PARAMETER,
  TEMPLATE, SYSTEM, LICENSE, MESSAGE, REQUIRES, CAPABILITY. NO ADAPTER instruction appears.
- Current docs/modelfile.mdx (fetched via gh api today): 249 lines; grep finds 15 "FROM" mentions
  and ZERO "adapter" mentions (commands in the overlap section).
- Historical v0.5.7 docs/modelfile.md (fetched via gh api ?ref=v0.5.7 today): the ADAPTER
  instruction existed: "Defines the (Q)LoRA adapters to apply to the model"; safetensors adapters
  supported for Llama (2, 3, 3.1), Mistral (1, 2, Mixtral), and "Gemma (including Gemma 1 and
  Gemma 2)"; plus GGUF adapters ("ADAPTER ./ollama-lora.gguf"); with the warning that a base model
  different from the adapter's tuning base makes "behaviour... erratic".
- Conclusion: on CURRENT Ollama, no adapter hot-swap instruction is documented at all; the
  documented path for a gemma LoRA is merge/bake to GGUF and serve the merged model. The in-window
  ecosystem agrees: 2609.24177 ships an adapter quantized to GGUF Q4_K_M (1.6 GB, 4-8 tok/s on a
  Pixel 6, listing quote); 2609.33878 served local judges on Ollama bf16.
- Measured swap cost per adapter on the janitor lanes: NOT FOUND in this sweep - no public
  benchmark was fetched, and with no documented ADAPTER instruction the question becomes "cost of
  `ollama create` + model swap per merged adapter". OWED: estate measurement (time `ollama
  create` merged-adapter vs base on a janitor lane, then tokens/s A/B; log to
  memory/runs/hermes_burn or the garden's routing row). No number is asserted here.

## Banked items (8, strongest first)

### 1. TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning (2610.02199, 2026-10-01)
Deep-read (abs + full HTML). Ternary-sign steepest-descent optimizer; optimizer state 174x smaller
than AdamW8bit (27.7 GB to 0.16 GB), peak memory 2.9x smaller on OPT-13B (80.6 to 27.5 GB), 30-32B
full-param FT on one 80 GB H100. Full text: NO LoRA/PEFT baseline in any table (baselines: AdamW8bit,
Adafactor, APOLLO-Mini, FlashAdamW, GaLore, Muon); metrics are downstream accuracy/F1, no
perplexity; hardware H100-only; smallest model OPT-1.3B at 3.4-5.5 GB peak.
Quote: "reducing persistent optimizer state by $174\times$ relative to AdamW8bit (from 27.7 GB to 0.16 GB)"
Why: the ask's Q1 target paper. It does NOT answer the janitor-scale question itself: no consumer
GPU, no AMD, and no LoRA baseline, so "feasible on RX 5600 XT" stays unclaimed; the estate's LoRA
recipe (rank >= 128, earlier pass) remains the measured baseline to beat.
Overlap: abstract stub already in catalog (catalog row for state/arxiv/2026-10-02/2610.02199v1.txt,
1,772 bytes, pulled 2026-10-02T06:30:25Z) and named in doors.md:26 as a freshness proof; never
deep-read or banked before this pass; memory/ hits are this session's own trajectory log only.
Confidence: 0.95.

### 2. TerMeZO: Ternary Sparse Zeroth-Order Optimization for Fine-tuning BitNet Models at the Edge (2609.33548, 2026-09-27)
Deep-read (full HTML). Sparse MeZO over BitNet-style ternary {-1,0,1} weights; picks
perturbation targets by linear scan of latent weights near quantization boundaries. Falcon-E-1B:
1.33 GB training memory (rho0=0.05) / 0.94 GB (rho0=0.01) vs 0.89 GB inference and 16.08 GB
backprop; matches full MeZO on GLUE/SuperGLUE, beats LoRA-MeZO/FIM-S-MeZO/QZO on most tasks;
GSM8K 44.4 (3B) vs base 20.0; 1B-3B models, NVIDIA-only.
Quote: "reduces the footprint by roughly 3× relative to MeZO, and by around 4× at level ρ₀=0.01."
Why: the strongest in-window evidence that TERNARY fine-tuning at janitor scale (sub-2 GB training
memory on 1B-3B models, near-inference footprint) is real - this is the lane that could actually
fit RX 5600 XT-class VRAM, unlike TACO's 13B-class results.
Overlap: zero estate hits (not in the catalog 3-row grep, not in any state/arxiv day dir scanned,
scoped memory grep clean, sibling sweep files clean). Fully new.
Confidence: 0.85.

### 3. Audit the Scaffold, Not the Checkpoint: A Stationarity Dichotomy for Recursive Self-Improvement in Agentic Coding (2609.34924, 2026-09-28)
Deep-read (full HTML). Bounded metric + fixed reachable edit set forces strict diminishing returns
(proved + measured: round gains decay 0.097/0.036/0.033 and 0.156/0.068/0.029); scaffold rewrites
(tools, verifiers, decomposition) escape without touching weights but cannot exceed the frozen
ceiling V*(W); only weight/architecture changes raise the ceiling. Names the unrun experiment that
separates the two: hold weights fixed, vary the scaffold.
Quote: "iterative self-modification hits strict diminishing returns whenever the agent's reachable set of edits stays fixed, and can escape only if that set expands."
Why: Q4's core evidence: the percolator's invariant-promotion loop is scaffold expansion - the
cheap, human-gated plateau-escape - and the literature says that is exactly what it is: ceiling-
bound. Also gifts an auditor law: "an auditor who checks only whether weights are frozen catches
test-time training and misses scaffold expansion entirely."
Overlap: zero estate hits everywhere (catalog, state/arxiv, scoped memory, sibling sweeps). Fully new.
Confidence: 0.9.

### 4. Maintaining Benchmarks Against Increasingly Capable Agents: Detection and Remediation of Unearned Passes (2609.34262, 2026-09-28)
Deep-read (full HTML). Grader-integrity audit at scale: deterministic pre-scan, ternary judge
label (legitimate / UNEARNED / UNEARNED violation), three-part violation test (mechanism, intent,
grade relevance), adversarial second judge + cross-model escalation, conservative default, and
replay-THEN-rerun closure. 3,810 passing trajectories, 29 cohorts: violation rates swing 24 to 73
pct between adjacent frontier models on matched tasks; 196 violations + 117 neutral; judge
disagreement changed 7.9 pct.
Quote: "A violation requires three things: \"(i) mechanism… (ii) intent… (iii) grade relevance.\""
Why: Q3: the concrete instrument set judge2/duel should adopt before any self-training loop fires
- audit PASSES not just fails, add the unearned-but-not-violation middle row to the tri-state
FAIL diagnosis, and gate grader patches on replay-plus-fresh-rerun closure.
Overlap: zero estate hits everywhere. Fully new.
Confidence: 0.9.

### 5. Curating Merchant-Matching Training Data with Two Confidence-Gated Local LLM Judges (2609.33878, 2026-09-27)
Deep-read (full HTML). Two local judges (30B-class, Ollama bf16) curate LoRA training data:
accept only on exact agreement with confidence >= thresholds; ordered tau_abs <= tau_sel
guarantees disjoint positive/negative sets (the inverted pair made 19 contradictory labels);
1,633 rows at 81.7 pct coverage, 96.88 pct purity (+2 pct over either judge alone); 367
disagreement rows to human review; per-row latency 35.2/22.2 s. Downstream LoRA named but not yet
run.
Quote: "1,633 queries (81.7% coverage) at 96.88% purity, with positive and negative purities of 99.47% and 93.38%."
Why: Q2's measured gate: the recipe seat-tape and courseware pools need before they may train a
model that judges - agree-only auto-promotion, ordered-threshold disjointness, human review set
for residual disagreement; runs on the estate's own serving stack.
Overlap: zero estate hits everywhere. Fully new.
Confidence: 0.85.

### 6. Uncheatable Eval: Dynamic Compression-Based Evaluation of Language Models (2609.27510, 2026-09-23)
Deep-read (full HTML). Score models as lossless compressors over freshly published text;
compression-rate scaling law CR(P)=aP^b+c over 80 models (R2 0.915), Spearman rho -0.884 vs
zero-shot MMLU. Own caveats: recency does not prove cleanliness and absence from training cannot
be guaranteed; eval data must keep being refreshed.
Quote: "publication recency alone does not establish a clean test set."
Why: Q2's contamination gate in one instrument: screen candidate SFT/eval rows by how anomalously
well the judge-model compresses them versus matched unseen text; also the cheap eval lane for any
estate-trained janitor model.
Overlap: abstract stub already in catalog (state/arxiv/2026-09-24/2609.27510v1.txt, 1,460 bytes);
never deep-read or banked as a sweep item before this pass.
Confidence: 0.85.

### 7. Using Context Is Not Enough: Test-Time Training for Personalized Reward Modeling (2609.35109, 2026-09-28)
Deep-read (full HTML). Context-only preference labels barely encode: reversed in-context labels
leave predictions unchanged in 85.95 pct of cases; P-TTT writes sequence-level fast-weight updates
(single forward pass, no backprop, reuses MLP down-projection every 6 layers), flips 77.81 pct vs
14.05 pct for ICL, beats the strongest baseline by up to 5.85 points, and runs 6.21-9.72x faster
than fine-tuning.
Quote: "the model's predictions on the same target pairs remain unchanged in 85.95% of cases on average."
Why: Q4's middle rung: adaptation that must BEND model behavior belongs in parameters (fast
weights / adapters), not context - direct design input for how promoted invariants reach the
janitor models (registry-consumed fast weights) versus constrain verdicts (deterministic grammar).
Overlap: zero estate hits everywhere. Fully new.
Confidence: 0.85.

### 8. From Judgment Quality to Downstream Utility: Rethinking LLM-as-a-Judge for Open-Ended Tasks (2609.37145, 2026-09-29)
Abs-page read only (html 404 on /v1 and /v2; fallback per recipe; depth discounted accordingly).
Judge protocol (verdict granularity, critique usage, evaluation batching) substantially affects
both intrinsic judgment quality and downstream utility, and the two do not always align; judge
guidance extends into test-time methods (Best-of-N, judge-guided revision, beam search).
Quote: "Surprisingly, judgment quality and downstream utility do not always align."
Why: Q3: judge2 must be certified on DOWNSTREAM utility under a swept protocol granularity, never
on intrinsic judge scores alone - complements the imagined-grader bank (burns.md:91-93).
Overlap: the only memory/ hit is this session's trajectory log (steps.jsonl line 40521 mentions
the ID - self-noise); not in catalog, not in sibling sweeps.
Confidence: 0.7 (abs-depth only).

## Overlap greps actually run this session (exact commands and outputs)

1. `grep -c -E "2610.02199|Ternary Absolute-max|Audit the Scaffold|Test-Time Training for
   Personalized|Merchant-Matching|Uncheatable Eval|Increasingly Capable Agents|Judgment Quality to
   Downstream|TerMeZO|Entropy Rate Filtering|2609\.34924|2609\.35109|2609\.33878|2609\.27510|
   2609\.34262|2609\.37145|2609\.33548|2610\.01493" catalog/catalog.jsonl` over 917,885 rows ->
   `3`. Same grep with `cut -c1-320` printed the 3 rows: state/arxiv/2026-09-24/2609.27510v1.txt
   (Uncheatable), state/arxiv/2026-10-02/2610.01493v1.txt (entropy filtering, banked by the
   earlier pass), state/arxiv/2026-10-02/2610.02199v1.txt (TACO). All three are abstract-size
   stubs; the other five banked IDs have zero catalog presence.
2. State scan: `for d in 2026-09-28..2026-10-03; ls state/arxiv/$d | grep -E "<10 candidate IDs>"` ->
   only 2610.01493v1.txt and 2610.02199v1.txt in 2026-10-02.
3. memory/: the full-tree `grep -rl` was launched and STOPPED after ~4 minutes (memory zone is
   484,843 rows per corpus.md:15 - too slow for this lane); a SCOPED rerun over `memory/rib
   memory/percolator memory/improve memory/attention.md memory/trajectory` returned exactly one
   file, `memory/trajectory/steps.jsonl` (this session's own step log; per-pattern counts show
   lines 40521-50751, self-noise from the live session, the same self-noise class the earlier
   pass reported for InMyStyle). The scoped grep is what is claimed; a full-memory sweep was NOT
   completed.
4. Sibling dedup: `grep -n -E "<8 banked IDs + titles>" watch/inbox/frontier_olm_2026-10-03/sweep/*.md`
   excluding this file -> zero hits. The earlier pass at this path (preserved below) and my bank
   share zero papers.

## Caveats / OWED

- Quotes are as returned by this session's fetches (arXiv abs pages, arXiv HTML full texts, Atom
  feeds, Ollama docs via gh api); no PDF byte-level download was performed.
- 2609.37145 is banked at abs-depth only (HTML 404 both versions). 2609.35677 is NOT banked
  (listing-level only, HTML 404). Re-probe both when HTML builds exist.
- OWED, not asserted anywhere above: (a) Ollama adapter swap-cost measurement on the janitor
  lanes; (b) license verification for ms-genai / ms-agents / openai-cookbook before courseware
  trains a judge; (c) consent-gate naming per seat-tape pool (CORE_INVARIANTS consent_first);
  (d) any AMD/ROCm run of TACO or TerMeZO (all papers NVIDIA-only); (e) the held-weights vs
  scaffold-varied A/B that would settle Q4's ranking; (f) full-tree memory/ grep completion
  (scoped grep only, disclosed above).
- The RX 5600 XT 6 GB GDDR6 figure comes from today's WebSearch (third sub-query after two 429s;
  Gigabyte / Newegg / TechPowerUp result summaries).

---

## PRESERVED VERBATIM: earlier same-day pass at this path (different question set)

The text below is the complete previous content of this file, preserved byte-for-byte during this
rebuild. Its 8 banked items (ReSAIL, Time-Incremental CPT, FORM, entropy-rate filtering,
Can-One-Adapted-Model, Break Step, AI Token Worth, InMyStyle) do not overlap this pass's 8.

# SWEEP: finetuning-and-adaptation via arXiv - 2026-10-03

Lane: frontier_olm sweep, area `finetuning-and-adaptation`. Source-fetched: 2026-10-03.
Window: 2026-09-03 through 2026-10-03 (one banked item is a 2026-07-31 paper whose v2 revision landed 2026-09-25, flagged inline).

Operator questions:
1. QLoRA vs LoRA vs full finetune for narrow behavioral law sets (citation discipline, tri-state verdicts) on small open models, with measured retention.
2. Data-curation recipes (dedup, quality filtering, synthetic augmentation) published for code/session-tape corpora, applicable to room.jsonl (code-agent-data doctrine).
3. Measured evidence that swarm self-distillation (training on the fleet's own verified outputs, the descent-protocol ouroboros leg) improves agent task success, and under what conditions it degrades (model-collapse literature).
4. Adaptation methods giving the best few-shot style lock with minimal data, extending the SEED SAVER song style-lock precedent (commit 831936fb6).

## Doors used (fetch recipe compliance)

- `export.arxiv.org/api/query` Atom API: 9 targeted queries, all returned as text, zero 403s, zero degradations:
  1. `all:"QLoRA"` sorted by submittedDate (25 entries)
  2. `all:"model collapse"` (25 entries)
  3. `all:"LoRA" AND all:"catastrophic forgetting"` (25 entries)
  4. `all:"data curation" AND all:"fine-tuning" AND cat:cs.CL` (25 entries)
  5. `all:"self-distillation" AND all:"agent"` (24 entries)
  6. `all:"style" AND all:"LoRA" AND cat:cs.CL` (24 entries)
  7. `all:"agent trajectory" AND all:"training"` (25 entries)
  8. `all:"few-shot" AND all:"style" AND all:"fine-tuning" AND cat:cs.CL` (18 entries)
  9. `all:"LoRA" AND all:"full fine-tuning" AND cat:cs.CL` (20 entries)
- RQ4 follow-ups: `all:"writing style" AND all:"fine-tuning" AND cat:cs.CL` (20 of 52) and `all:"persona" AND all:"fine-tuning" AND cat:cs.CL` (20 entries).
- `arxiv.org/abs/` pages fetched: 12 (ReSAIL, entropy-rate filtering, Time-Incremental CPT, FORM, AI Token Worth, SynthSentry, Terminal-Universe, Can One Adapted Model, Self-Practice, Break Step, Post-Training Science for SFT, KuaiRP) plus 2 more (InMyStyle, FAVoR) = 14 total.
- `arxiv.org/html/` full texts fetched and read end to end: 5 (ReSAIL 2609.39306v1, Time-Incremental CPT 2609.23916v1, FORM 2609.23367v1, Can One Adapted Model 2609.27262v1, entropy-rate filtering 2610.01493v1). All five had HTML versions; no fallback was needed.
- `arxiv.org/list/cs.CL/recent` and `/list/cs.LG/recent`: NOT fetched. The API door returned sufficient in-window density and the recipe lists the listing pages as an alternate door, not a requirement. Stated as not run, not faked.
- WebSearch: not needed; no door degraded.

## Pass 1 (broad sweep)

About 130 distinct candidate entries considered across the 11 queries above, of which roughly 95 fall inside the 30-day window. All four research questions had multiple in-window candidates except RQ4 (style lock), which stayed thin; two extra targeted queries were run to close that gap.

## Pass 2 (deep read)

14 items read on their abs pages; the 5 strongest read end to end in full HTML with body-level extraction of methods, tables, ablations, and limitations. Banked below: 8 items. Everything banked was read in this session; nothing is banked from listings alone.

## Answers to the four questions

### RQ1: QLoRA vs LoRA vs full finetune for narrow behavioral law sets, measured retention

Three in-window papers give a consistent answer: parameter-efficient finetuning at sufficient rank carries specialist behavior at measured retention cost of roughly 0.01 to 2.6 points.

- Time-Incremental CPT (2609.23916, deep read): LoRA at rank >= 128 matches full continued pretraining (on Llama-3.2-3B after-cutoff Macro-F1: LoRA r=128 0.525, r=256 0.534, full 0.540); the 13-task downstream macro-average stays within 0.01 of base for every model tested. Forgetting is not free though: sample-level analysis fits forgetting ~= 0.60 x acquisition + 0.025 (Pearson r=0.68), 82 percent of configs net-positive. Learning rate is the second dial: temporal-recall optima sit near 3e-5 while general capability tolerates up to 3e-4, separated by about an order of magnitude. Curated 6B tokens matched a broad 40B slice. Gains survive SFT; DPO's effect is family-dependent.
- FORM (2609.23367, deep read): QLoRA r=16 alpha=32 on Qwen3-8B, 4-bit NF4, 5 epochs, about 35 minutes on one A100-40GB, trained on 4,633 execution-oracle-verified examples, beats frontier models up to 756B on FORM execution (B1 97.7 vs GLM-5.2 75.5). General-capability retention measured: MMLU -2.6pp, GSM8K -1.5pp, HumanEval -0.6pp. Paper's own limitation: author-constructed benchmarks share an author with the model.
- Can One Adapted Model Do It All (2609.27262, deep read): across 13 models (0.6B-32B) and 8 datasets, multi-task full finetuning is the strongest operational default at every size; specialists degrade sharply off-task; sequential LoRA retains earlier skills far better than sequential full FT (after four tasks, Qwen3-8B intent classification: 99.5 -> 78.6 under sequential LoRA vs 99.5 -> 25.9 under sequential full FT); merging a specialist into its base at alpha in [0.15, 0.30] buys off-task robustness cheaply.

Estate synthesis: for teaching narrow law sets (citation discipline, tri-state verdicts) to the local janitor tier, LoRA/QLoRA at rank >= 128 on verified data reaches specialist quality with retention cost about 2.6pp worst-case in these papers; do NOT shard laws into per-law specialist adapters without reliable routing (off-task fragility is measured); prefer one multi-law adapter, and budget regression tests per run because forgetting tracks acquisition at roughly 0.6:1.

### RQ2: curation recipes for code/session-tape corpora (room.jsonl)

- Entropy-rate filtering (2610.01493, deep read): a model-free Kontoyiannis entropy-rate estimator (Lempel-Ziv-style match lengths on the first 1,500 word tokens) used as a domain-stratified top-K filter beats logprob-based filtering at preserving diversity across six generations of QLoRA fine-tuning on Llama-3.1-8B: +42 percent distinct-3, +30 percent vocabulary, -19 percent 4-gram repetition (all p<0.001) while logprob filtering was non-significant on every metric (p>0.23). Honest limitation carried in the paper: it preserves text diversity, not reasoning (HellaSwag fell equally in all conditions).
- FORM's acceptance gate (2609.23367, deep read): four-stage verification chain per example (vague-word rejection, syntax execution against the FORM 5.0 binary, non-trivial-output check, LLM consistency audit at temperature 0.1 against a factsheet), then dedup and a verified zero train/test overlap. This is a published instance of the estate's proof-carrying-verdict doctrine applied to corpus construction.
- Terminal-Universe (2609.04148): session tapes replay into executable environments (file-op replay + completion agent), 37.3k task-sufficient environments, SFT +11.9 Terminal-Bench 2.1. Known overlap: the estate already intake-carded this on 2026-09-04 (see below), so not banked here.
- Honorable mentions: SynthSentry (2609.12353) for pre-training contamination screening (lexical diversity collapse + n-gram tail truncation + perplexity variance); PG-SFT (2610.00949) and Don't Mask the Environment (2609.20715) for what to supervise in agent-trajectory SFT.

### RQ3: swarm self-distillation / ouroboros: value and degradation conditions

Four in-window papers triangulate the conditions:

- ReSAIL (2609.39306, deep read): iterative privileged-information self-distillation collapses because the student-as-next-teacher loses its PI-conditioned behavior (PI-conditioned OOD success fell 61.5 -> 44.8 percent across cycles 1 to 3 without retention). Fix: select the top-rho PI-sensitive steps (teacher JSD between ordinary and privileged views, rho=0.05 on ALFWorld), balance per-trajectory losses, and KL-regularize the student's privileged view toward the frozen teacher (lambda=0.5). Result: advantage over parent methods grows from 6.8-5.0 points at cycle 1 to 18.3-26.6 points at cycle 3; average absolute final-cycle gain 22.5 points. Ablation: the retention regularizer is the component that prevents cross-cycle collapse.
- Break Step (2609.11149, read on abs page, v3): a large share of reported rapid recursive-training collapse is a measurement artifact of vLLM batch serving: requests in one seeded batch share the same random draws and a fixed seed replays them every generation. Sharing across requests and replay across generations must co-occur to produce the collapse; with shared+replayed seeds seven checkpoints from five families fell to 0.045-0.38 unique-4-gram fraction while per-request seeds hold ~0.98 through generation 3. Actionable law for any fleet self-training run: per-request seeds, or the ouroboros manufactures fake collapse data.
- AI Token Worth (2609.40295, abs read): scaling laws over 800 pretrained runs on WildAI (83B-token web corpus, ~27.5 percent AI-generated by June 2026): AI tokens help only data-starved models and the benefit saturates then reverses into harm on human-text targets; for high human-text budgets AI tokens raise loss almost immediately. Recommendation: filter AI text when the target is human text; AI text remains useful when the target IS AI text. For the estate: room.jsonl-derived successors target fleet behavior itself, which is the "target is AI text" case, so the doctrine is blessed, but the target distribution must be named before judging corpus value.
- Self-Practice (2609.29051, abs read): OPSD can underperform plain RL in multi-turn agents (worst case below the untrained base model) because the student mimics confident behavior without the underlying information; moving privileged information into the sampler (analyzer writes per-task instructions, GRPO on resampled rollouts) beat plain GRPO in every setting, up to +65 percent on AppWorld and +61 percent on SWE-bench Verified.

### RQ4: few-shot style lock with minimal data

In-window published evidence is sparse; the strongest is:

- InMyStyle / "Small Is Enough" (2607.29238, v2 2026-09-25): rank-8 LoRA, 3 epochs, built from one author's 73 paragraphs (219 evaluation pairs), on Qwen2.5 0.5B-7B. Composite quality plateaus across model sizes (Q = 0.689-0.695 with overlapping confidence intervals), 400 LLM-judge ratings put outputs over 20 percent lower in perceived AI-ness than the inputs. Small local models suffice; size buys efficiency, not lock quality. This is the published analog of the estate's SEED SAVER song style-lock (831936fb6) and directly supports locking seat style with tiny paired corpora on the janitor tier.
- FAVoR (2609.30968, honorable mention): shared-private adapters prevent multi-author style homogenization in federated PEFT; no numbers on the abstract page.
- No in-window published work shows a measured style lock beating the estate's own precedent at smaller data.

## Banked items (8, strongest first)

### 1. ReSAIL: Mitigating Collapse in Iterative Agent Self-Distillation (2609.39306, 2026-09-30)
Deep-read (abs + full HTML). Iterative PI self-distillation collapses across cycles because the student trained only without PI erodes its own PI-conditioned behavior before becoming the next teacher. ReSAIL: top-rho PI-sensitive step selection (teacher JSD), per-trajectory loss balancing, KL retention toward the frozen teacher at lambda=0.5. Numbers: PI-conditioned OOD 61.5 -> 44.8 percent without retention; with ReSAIL the cycle-3 advantage over parent methods reaches 18.3 (SDPO) and 26.6 points (OEL); Qwen3-4B and 8B on ALFWorld/TextCraft; costs ~1.23x the parent training loop.
Quote: "The advantage over the corresponding parent method grows from 6.8 to 18.3 percentage points for SDPO and from 5.0 to 26.6 percentage points for OEL between the first and third deployment cycles."
Why: this is the measured answer to the descent-protocol return leg: self-distillation of fleet-verified outputs works only if the verification-privileged view is explicitly retained across generations; the retention regularizer and top-rho selection transfer directly to the percolator's promotion loop (promote the steps where the verdict changed, keep the verification trace paired, regularize toward the frozen prior).
Overlap: zero hits for "ReSAIL" and "iterative agent self-distillation" in catalog/catalog.jsonl (917,885 lines grepped) and memory/. Fully new, not even harvest-stubbed.
Confidence: 0.9.

### 2. Time-Incremental Continued Pretraining of LLMs (2609.23916, 2026-09-20)
Deep-read (abs + full HTML). Six models (OLMo2, Llama-3.1/3.2, Gemma-3, Qwen3, 1B-8B) continued-pretrained on post-cutoff FineWeb-Edu: knowledge gains at near-zero forgetting cost (13-task macro within 0.01 of base on every model); LoRA at rank >= 128 matches full CPT; forgetting ~= 0.60 x acquisition (r=0.68), 82 percent of configs net-positive; LR optima for recall vs capability separated by ~10x (3e-5 vs 3e-4); curated 6B tokens == broad 40B; three sequential rounds match one-shot; gains survive SFT, DPO family-dependent. Verbatim: "Forgetting is substantial even where the net is clearly positive."
Quote: "Forgetting is substantial even where the net is clearly positive."
Why: sets the two dials (rank >= 128, LR ~3e-5) and the retention budget (regression tests per run, forgetting tracks acquisition) for the room.jsonl QLoRA corpus organ on the janitor tier; the 6B-quality-equals-40B-broad result validates curating hard instead of scraping wide.
Overlap: abstract stub only, catalog/catalog.jsonl:444906 -> state/arxiv/2026-09-22/2609.23916v1.txt; no digest anywhere in memory/.
Confidence: 0.9.

### 3. LLM-Based FORM Code Generation with Verification-Driven Fine-Tuning (2609.23367, 2026-09-20)
Deep-read (abs + full HTML). Execution-oracle corpus construction: ~10,000 candidates -> four-stage verification (vague-word reject, FORM 5.0 execution, non-trivial output check, GLM-5.2 consistency audit at temp 0.1) -> 4,633 verified examples (2,465 deterministic + 1,050 open-ended + 43 tutorial + 1,075 QA), zero train/test overlap. QLoRA r=16 alpha=32 on Qwen3-8B, ~35 min on one A100: B1 97.7 vs GLM-5.2 75.5; frontier models score 0 percent without documentation; general capability cost MMLU -2.6pp, GSM8K -1.5pp, HumanEval -0.6pp.
Quote: "effectively prevents catastrophic forgetting" (paper's conclusion on QLoRA training ~0.5 percent of parameters; short because the longer body sentences carry em-dashes in the original).
Why: the four-stage acceptance chain is the closest published twin of the estate's proof-carrying verdict + tri-state doctrine applied to corpus gating; it is a concrete recipe for the fireball-cycle skill-from-corpus loop: execute the claim, reject the vague, audit semantics, then train.
Overlap: abstract stub only, catalog/catalog.jsonl:444876 -> state/arxiv/2026-09-22/2609.23367v1.txt; no digest in memory/.
Confidence: 0.85 (author-constructed benchmarks, bias flagged in the paper's own limitations).

### 4. No Model Required: Text Entropy Rate Filtering Mitigates Iterative Fine-Tuning Collapse (2610.01493, 2026-10-01)
Deep-read (abs + full HTML). Model-free Kontoyiannis entropy-rate estimate (match-length, first 1,500 word tokens, ProcessEntropy tokenizer) as a domain-stratified top-40-of-80 filter per generation; six generations of QLoRA (r=16 alpha=16, LR 2e-4, 3 epochs) on Llama-3.1-8B, fully synthetic single-lineage. h_k filtering: distinct-3 +42 percent, vocab +30 percent, repetition -19 percent (p<0.001); logprob filtering non-significant on all metrics (p>0.23); gzip filter only +17 percent; replicated on Llama-3.2-3B. Limitation stated: preserves lexical diversity, not reasoning (HellaSwag fell equally everywhere).
Quote: "Long matches signal repetition in the text; short matches signal novelty."
Why: gives room.jsonl curation a zero-GPU quality filter that beats the standard logprob filter, measured; slots directly into the code-agent-data organ's dedup/quality stage and into any percolator candidate pool pre-screen.
Overlap: abstract stub only, catalog/catalog.jsonl:870276 -> state/arxiv/2026-10-02/2610.01493v1.txt; no digest in memory/.
Confidence: 0.9.

### 5. Can One Adapted Model Do It All? Fine-Tuning Strategy Selection for Customer Support LLMs (2609.27262, 2026-09-23)
Deep-read (abs + full HTML). 13 models (Qwen3, Qwen3.5, Gemma-3, Llama-3.1, Mistral; 0.6B-32B), 8 datasets, 200+ checkpoints: multi-task full FT is the strongest default at every size; specialists need reliable routing (sharp off-task degradation); sequential LoRA crushes sequential full FT at retention (78.6 vs 25.9 retained on Qwen3-8B intent classification after four tasks); merging at alpha in [0.15, 0.30] is the cheap robustness move; multiple specialists merged never matches one multi-task model.
Quote: "Our experiments reveal that multi-task full fine-tuning is the strongest operational default at every model size we test."
Why: answers the fleet adapter strategy question before the estate builds per-lane adapters: one multi-law adapter per seat tier, sequential LoRA for incremental law additions (train critical laws last), merge for off-task insurance; direct input to the percolator promotion gates when a promoted law becomes a training row.
Overlap: abstract stub only, catalog/catalog.jsonl:445367 -> state/arxiv/2026-09-24/2609.27262v1.txt; no digest in memory/.
Confidence: 0.9.

### 6. Break Step: Recursive Training Resonates with Replayed Sampling Noise (2609.11149, 2026-09-10, v3 2026-09-29)
Read on abs page (v3). Rapid diversity loss in recursive training traces to shared-and-replayed sampler seeds (vLLM batch serving with a fixed seed), not error accumulation: sharing across requests and replay across generations must co-occur; seven checkpoints from five families fell to unique-4-gram 0.045-0.38 under shared+replayed seeds while per-request seeds hold ~0.98 at generation 3; a released peer-reviewed collapse dataset (Gemma-2-27B pipeline) had ~three quarters of one iteration's rows repeating as often as batch copies.
Quote: "Sharing across requests and replay across generations matter only together." plus "A seed per request restores the fresh sample that stability analyses assume."
Why: measurement law for the estate's ouroboros experiments: any fleet self-training loop served through vLLM must set per-request seeds or its collapse readings are artifacts; also a falsifier to apply retroactively to any prior collapse-style finding the estate banked from seeded batch generation.
Overlap: stub exists on disk at state/arxiv/2026-09-11/2609.11149v1.txt but is UNCATALOGED (grep for "11149" in catalog/catalog.jsonl returns only timestamp substrings, 31 false positives); no digest in memory/.
Confidence: 0.85 (abs-page read only; full text not fetched).

### 7. How Much Is an AI Token Worth? Scaling Laws for Wild AI-Generated Web Text (2609.40295, 2026-09-30)
Read on abs page. 800 pretrained models, WildAI 83B-token corpus with AI/topic/format labels (web ~27.5 percent AI-generated June 2026, 31.1 percent August): AI tokens lower human-text loss only for data-starved models and the benefit saturates then reverses into harm; with high human-text budgets AI tokens raise loss almost immediately; new benefit/harm scaling law predicts held-out human-text loss up to 3.6x larger models with 41 percent lower error, reduces to Chinchilla with zero AI text. Recommendation: filter AI text when targeting human text; AI text is useful when the target is AI text.
Quote: "For data-starved models, adding AI tokens to pretraining data initially lowers loss on human text, but the benefit saturates as more are added and quickly reverses into harm."
Why: the corpus-level law governing the ouroboros leg: fleet-generated data is fine exactly when the named target distribution is fleet behavior (the code-agent-data doctrine's case), and harmful when the target is the human/web distribution; forces every corpus decision to state its target distribution first.
Overlap: abstract stub only, catalog/catalog.jsonl:806587 -> state/arxiv/2026-10-01/2609.40295v1.txt; no digest in memory/.
Confidence: 0.85.

### 8. Small Is Enough: Per-User Style Rewriting of AI-Edited Text via LoRA Adapters (2607.29238, v1 2026-07-31, v2 2026-09-25)
Read on abs page (v2). InMyStyle: paired training examples built from a single user's documents by local helper LLMs, rank-8 LoRA, 3 epochs, Qwen2.5 0.5B-7B; case study 73 source paragraphs -> 219 evaluation pairs. Composite quality Q = 0.689-0.695 across all sizes (overlapping CIs, plateau); authorship probability 0.51-0.53 (near the classifier's decision boundary); 400 LLM-judge ratings rate outputs over 20 percent lower in perceived AI-ness. Size buys efficiency, not lock quality.
Quote: "In this setting, small models are sufficient for the measured rewriting task, and model size mainly determines efficiency trade-offs."
Why: the published analog of the estate's SEED SAVER song style-lock: minimal paired-data LoRA on the smallest local model locks one author's style, which extends to per-seat style locks on the janitor tier for the fireball-cycle loop. Flagged: v1 predates the 30-day window; banked on the 2026-09-25 v2 revision.
Overlap: zero estate hits; the only memory/ match for "InMyStyle" is this session's own trajectory log (memory/trajectory/steps.jsonl:46921), i.e. self-noise, not prior knowledge.
Confidence: 0.8.

## Known overlap found and NOT banked

- Terminal-Universe (2609.04148): the estate intake-carded it on 2026-09-04 with a BUILD verdict and the fleet mapping already sealed ("room.jsonl + seat session tapes ARE terminal trajectories", watch/INTAKE_TERMINAL_UNIVERSE_20260904.md lines 36-43; stub at catalog/catalog.jsonl:442980). My independent deep read confirmed the same numbers (37.3k environments, +11.9 Terminal-Bench 2.1, +13.8 EvoCode-Bench v2 MT@4) but adds nothing the card lacks. Re-banking would be waste per the sweep contract.

## Honorable mentions (read, not banked)

- From Self-Distillation to Self-Practice (2609.29051, 2026-09-24): OPSD underperforms plain RL in multi-turn agents (worst case below base); move privileged info into the sampler; +65 percent AppWorld, +61 percent SWE-bench Verified. Strong RQ3 complement to ReSAIL; cut only because ReSAIL carries the same finding space with deeper ablations.
- SynthSentry (2609.12353, 2026-09-11): corpus-level synthetic-contamination screening (lexical diversity collapse, n-gram tails, perplexity variance, bootstrap-calibrated threshold). Abstract thin on numbers; no estate presence found.
- FAVoR (2609.30968, 2026-09-25): shared-private adapters against author-style homogenization; stub at catalog/catalog.jsonl:580949; no numbers on abstract page.
- KuaiRP (2609.11127, 2026-09-10): role-play SFT + two-stage on-policy distillation restoring general capability lost to domain SFT; stub at catalog/catalog.jsonl:443758; qualitative only.
- Post-Training Science for Supervised Fine-Tuning (2609.01244, 2026-09-01, 2 days outside the window): controlled one-lever SFT sweep (LR, batch, LoRA vs full, rank/alpha, epochs, optimizers) across Qwen3/Llama up to 235B. The abstract page poses the sweep and states no findings; full text not fetched, so nothing is claimed from it.
- A Dynamical Theory of LoRA in Continual Learning (2609.39367): ODE-exact LoRA dynamics, reduced interference at slower adaptation; pass-1 only.

## Caveats and not-run items

- All numbers above come from WebFetch extractions of arXiv abs and html pages fetched in this session; no full-PDF byte-level download was performed, and quotes are as returned by the page fetch (elisions marked where the extractor abbreviated).
- The `/list/cs.CL/recent` and `/list/cs.LG/recent` listing pages in the recipe were not fetched (API door sufficient); noted rather than faked.
- Overlap greps actually run this session (exact commands): `grep -in -e "ReSAIL" ... catalog/catalog.jsonl` over 917,885 lines; recursive `grep -rin -l ... memory/`; `grep -c "11149" catalog/catalog.jsonl`; `grep -n -m2 "InMyStyle" memory/trajectory/steps.jsonl`. Outputs are quoted above.
- No estate-side reproduction of any paper's numbers was attempted; every "why" is a steal-map claim, not a measured estate result.

[END OF PRESERVED EARLIER PASS]
