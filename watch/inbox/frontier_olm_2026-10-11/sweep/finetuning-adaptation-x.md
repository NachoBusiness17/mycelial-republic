# Sweep: finetuning-adaptation via X (frontier_olm_2026-10-11)

Seat: sweep-finetuning-adaptation-x. Doors used: WebSearch (site:x.com phrasing per recipe) plus the
fxtwitter JSON door for post resolution. Everything banked below was fetched and read this sitting,
2026-10-11. House laws held: ascii only, no em or en dashes in my own prose (verbatim quotes keep their
source bytes), every claim cites what was read or run.

## Pass 1: broad sweep, instruments and the window finding

24 WebSearch queries run this sitting (query strings like `site:x.com LoRA fine-tuning adapter`,
`site:x.com test-time training LLM`, `site:x.com interpretability probing random network dead salmon`,
`site:x.com Metan Recuris recursive self-improvement agents`, `site:x.com "2610.12002" OR "2610.11776"`,
`x.com UnslothAI post LoRA October 2026`, and 17 more). The backend honored the x.com restriction only
intermittently; roughly a third of queries surfaced real x.com rows, the rest fell back to generic web
noise (arXiv, Wikipedia, vendor blogs).

Candidates considered (30+ tallied from the 24 queries):

- X-native, resolved or date-decoded (17): dair_ai/1911444965458162088, TheAITimeline/1911633298704552301,
  emrecanacikgoz/1976686817177911653, askalphaxiv/2006079289163399451, ValerioCapraro/2009607652372840525,
  askalphaxiv/2010630950431195308, stanfordnlp/2010807762893349067, zhuokaiz/2017450185933439063,
  omarsar0/2036828723878793335, tianle_cai/2041705054886097155, sheriyuo/2061382777623519284 (article),
  ssi_trending/2087551605553901958 (trending page, not a single post), fchollet/2087823167049920721,
  TheTuringPost/2096173534439465268, plus three profile/loose rows (StevenDillmann reposts page,
  Hiroaki Hayashi thread, the kemkomdigi noise row) considered and rejected as off-topic or non-items.
- Off-domain surfaced and considered (~25, strongest): TTT-E2E (arXiv, Tandon et al.), Test-Time Training
  Done Right (arXiv 2505.23884), NVIDIA blog "Reimagining LLM Memory: Using Context as Training Data",
  ICLR 2025 Weight Space Learning workshop, EvolveR (arXiv 2510.16079), A Taxonomy of Self-evolving Agents,
  Self-Improving LLM Agents at Test-Time (arXiv 2510.07841), Critique-GRPO, Projection-Guided
  Cross-Tokenizer Knowledge Distillation, Low-Rank Clone, AdaKD, Hyperagents (arXiv 2603.19461),
  Sebastian Raschka LoRA tips, MLflow QLoRA guide, Fine-Tuning Increases LLM Vulnerabilities (HN 2024
  thread), vktr fine-tuning alignment note.

FINDING (instrument-tagged): every X-native candidate was date-verified two ways, snowflake decode
(`./.venv/Scripts/python.exe` run this sitting: `(id >> 22) + 1288834974657` over all 14 status IDs) and
fxtwitter's `created_at` on all 11 resolved posts. ZERO sit inside the 30-day window 2026-09-11..2026-10-11.
The newest is TheTuringPost 2026-09-05. This backend's x.com index carries no finetuning-adaptation posts
from the last 30 days. That is the same disease the estate already banked: X surface OWED carries per
commit e8eedd8eb and the burns lens names the x-history miner as the cure
(watch/inbox/frontier_olm_2026-10-11/lens/burns.md:127-128, :235-236). This sweep is more evidence the
cure is needed: discovery-by-search-engine cannot see the last 30 days of X.

## Pass 2: deep reads through the fxtwitter door (11 posts fetched, all read)

curl runs this sitting: `curl -s https://api.fxtwitter.com/<user>/status/<id>` for 11 posts, JSON saved to
%TEMP%/_ftx_*.json, then parsed and printed full-text with the repo venv (11/11 resolved, 0 failures,
0 login walls; one item degraded, noted below). Banked items carry a verbatim quote under 40 words from
the fetched JSON. None of the 11 post IDs exist in memory/corpus/LINKS.jsonl (grep = 0 for all 11) or in
watch/inbox/frontier_olm_adhoc/register.jsonl (grep = 0). All are genuinely new as banked X-door items.

### Items banked (strongest first)

1. sheriyuo (Xiuyu Li), "RL for Test-Time Scaling", 2026-06-01, article post, 135 likes.
   https://x.com/sheriyuo/status/2061382777623519284
   source-fetched: 2026-10-11. Read end to end: fxtwitter returned the full article body (36 text blocks,
   9,927 chars, extracted this sitting). It is a survey of why training-free test-time scaling hits a wall.
   Quote: "intrinsic rewards are safe only on small (sub-128 sample) sets, which makes them fine for
   test-time training but not a substitute for a real verifier in large-scale post-training."
   Why it matters: this is the evidence-threshold answer for RQ3. It names the Omega(sqrt(H)) verifier
   advantage (VB vs VF, ICML'25 spotlight), shows verifier-free SFT-of-traces is imitation around the
   policy mean, and shows intrinsic-reward TTRL lines universally rise-then-collapse at a Model Collapse
   Step. The estate's adaptation is ribs/skills (discrete, verifier-backed, human-gated); this article says
   weight-side adaptation without a real verifier signal flowing back into training is asymptotically
   suboptimal, which is exactly why the estate's receipt-graded pitfall corpus is the right food and
   why unelected self-digestion would collapse. Also names the OPD/SDFT/SDPO continual-learning drift the
   adhoc DIAL-OPD row sits inside. Overlap: grep catalog/catalog.jsonl "TTT-E2E|2604.06169|2603.19461|
   In-Place TTT|Hyperagents|2510.07841|Metan|Recuris" run this sitting; "sheriyuo" and post id
   2061382777623519284 appear nowhere in catalog or memory outside this session's own trajectory steps
   (memory/trajectory/steps.jsonl, session ids sess_dwf-dwfrun-af85b9b8...). Genuinely new.

2. tianle_cai, "In-Place Test-Time Training", 2026-04-08, ICLR 2026 Oral, 1024 likes.
   https://x.com/tianle_cai/status/2041705054886097155 (paper arXiv 2604.06169)
   source-fetched: 2026-10-11. Quote: "We repurpose the final projection matrix in every MLP block as
   fast weights. With an NTP-aligned objective and efficient chunk-wise updates, the model adapts on
   the fly." Why: RQ2 mechanism. No new modules, no pretraining required: existing MLP projections become
   the fast-weight substrate. This is the cheapest-published weight-adaptation substrate and it lives at
   the architecture layer the lora_pipeline module does not touch (graph degree 5, lens/graph.md:22), so it
   is an additive experiment for that module, not a redesign. Overlap: grep catalog "2604.06169" = 0,
   "In-Place TTT" = 0; memory hits only self-trajectory. New.

3. zhuokaiz, deep explainer of TTT-E2E, 2026-01-31, 216 likes.
   https://x.com/zhuokaiz/status/2017450185933439063
   source-fetched: 2026-10-11. Quote: "they lose badly on Needle-in-a-Haystack retrieval tasks - which
   actually makes sense. This method is doing compression: long-range info has to be squeezed into a
   fixed-size set of updated weights" (verbatim from the JSON; the source uses an em dash here, kept).
   Why: the JIT-law mechanism read at expert level. Two facts the estate needs: adaptation is
   EPISODE-BOUNDED (weights reset to W_0 after the sequence, explicitly "not persistent memory across
   sessions"), and it is LOSSY (exact retrieval dies first). The JIT fine-tuning law's "zero context cost"
   claim gets a precise price tag: what you gain in compression you lose in verbatim recall, which is fine
   for pitfall-bypass steering and fatal for citation-grade facts. Also the frame: long-context lines are
   "different points in one space where weights are the state, and gradient descent is the state update
   rule." Overlap: catalog "TTT-E2E" = 0 (the Tandon paper is not even in the raw arxiv sweep drops);
   post id 0 in LINKS and register. New.

4. emrecanacikgoz, test-time self-improvement (TT-SI), 2025-10-10, 138 likes.
   https://x.com/emrecanacikgoz/status/1976686817177911653
   source-fetched: 2026-10-11. Quote: "We investigate a new test-time self-improvement (TT-SI) algorithm
   that enables agents to self-improve using only one training instance per uncertain case during
   inference." Why: JIT-law direct. Its pipeline Self-Awareness -> Self-Data Augmentation ->
   Self-Improvement is the law's mapping 3 and 5 mechanized: sense the pitfall, mint one instance,
   adapt. One instance per detected weakness is the demand-precedes-organ trigger at its most frugal.
   Note: the related paper 2510.07841 has 3 catalog rows but all are the adhoc run's own sweep artifacts
   (_ftfull_2510.07841.html, _ftread_2510.07841.txt, _ft_2510.07841.html, grep this sitting), 0 register
   rows: the adhoc run fetched the paper and never confirmed it. The X post is the missing first-hand
   anchor. Overlap: stated; post id 0 in LINKS/register. New.

5. askalphaxiv, "The Dead Salmons of AI Interpretability" summary, 2026-01-12, 107 likes.
   https://x.com/askalphaxiv/status/2010630950431195308 (paper arXiv 2512.18792)
   source-fetched: 2026-10-11. Quote: "This paper argues we should treat LLM activation explanations as
   statistical/causal inference, where we test against meaningful alternative computational hypotheses
   and report uncertainty under an explicit model". Why: RQ4 protocol sentence, sharper than the drop
   card's paraphrase (watch/inbox/dead_salmon_airllm_drop_20261010/CARD.md read this sitting). It converts
   the card's negative-control amendment into a checklist: explicit alternative hypotheses, uncertainty
   under an explicit model. Overlap: the PAPER is known (catalog 1 row = the adhoc run's own abs-page
   artifact local_sovereign_agent/watch/inbox/frontier_olm_adhoc/sweep/_tmp_pages/abs_2512.18792.html,
   grep this sitting; plus the drop card). The POST and its protocol wording are new. Partial re-bank of
   paper knowledge, new door evidence.

6. fchollet, TTT framing, 2026-08-13, 35 likes.
   https://x.com/fchollet/status/2087823167049920721
   source-fetched: 2026-10-11. Quote: "Test-time training is the only form of test-time adaptation that
   is 'pure' deep learning, as opposed to neurosymbolic. It adapts in continuous latent space, as
   opposed to adapting in discrete symbol space." Why: RQ3 doctrine in one sentence. The estate adapts in
   discrete symbol space (ribs, skills, receipts, laws). Weight adaptation is a different axis, not a
   faster version of the same one. This sentence is the cleanest external statement of why the estate's
   ribs-first doctrine and a weights turn are complementary rather than rival: the descent protocol's
   cheap-first leg applies to the symbol-space layer first because that is where the estate's verifiers
   live. Overlap: post id and "fchollet" 0 in catalog/memory outside self-trajectory. New.

7. omarsar0, Hyperagents, 2026-03-25, 535 likes.
   https://x.com/omarsar0/status/2036828723878793335 (paper arXiv 2603.19461)
   source-fetched: 2026-10-11. Quote: "They introduce Hyperagents, self-referential agents where the
   self-improvement process itself is editable." Why: this is the descent protocol falsifier's target
   class (RIB_TEN_MINUTE_SELF falsifier 3 via lens/laws.md:108: "a wave must show one improvement to the
   improving MECHANISM itself from bytes"). DGM-Hyperagent numbers in the post: paper-review accuracy
   0.0 to 0.710; robotics reward design 0.060 to 0.372; transfer 0.630 on Olympiad math grading in an
   untrained domain. Measured, from the fetched post, not vendor marketing. Overlap: "2603.19461" = 0 in
   catalog, "Hyperagents" = 0 in memory knowledge dirs (targeted walk over burns/rib/research_packs/
   research_polished/corpus-LINKS/knowledge_graph/trajectory this sitting, biography corpus excluded as
   out of scope for ML content). New.

8. stanfordnlp, TTT-E2E announcement, 2026-01-12, 64 likes.
   https://x.com/stanfordnlp/status/2010807762893349067
   source-fetched: 2026-10-11. Quote: "LLMs can keep training at test-time with next-token prediction on
   the context, compressing experience into their weights." Why: canonical citation for items 2 and 3;
   the short official statement of the weights-as-memory claim the JIT law reorganizes around. Overlap:
   post id 0 in LINKS/register; catalog "TTT-E2E" = 0. New.

### Considered, not banked

- TheTuringPost, "The Missing Pieces in Recursive Self-Improvement", 2026-09-05, 110 likes,
  https://x.com/TheTuringPost/status/2096173534439465268. DEGRADED, per-recipe fallback: the door
  resolved the post but its full text is only an x.com article pointer ("https://x.com/i/article/
  2096168575819976705", verbatim from the fetched JSON); fxtwitter does not carry article bodies. The
  search-result snippet names Metan ("recursively adds layers that improve the agent's strategy") and
  Recuris ("evolves how agents apply experience through memory"). Snippet banked here with its URL and
  the degradation stated; no first-hand body read exists, so it does not make the top 8.
- askalphaxiv/2006079289163399451 (TTT long-context hype post, 2025-12-30, 316 likes): read, accurate,
  but fully covered by items 2, 3 and 8.
- TheAITimeline/1911633298704552301 (TTT for one-minute video generation): off-area, video generation
  not LLM adaptation.
- ValerioCapraro/2009607652372840525: dead-salmon fMRI history post, no adaptation content.

## The four research questions, answered from this sitting's reads

### RQ1. The 8 adhoc finds vs the JIT fine-tuning law: refine, contradict, restate, and the evidence status

Source bytes: watch/inbox/frontier_olm_adhoc/register.jsonl (8 finetuning-adaptation rows, grep-extracted
this sitting) and watch/inbox/fine_tuning_jit_law_20261010/CARD.md (read in full, 45 lines).

- EVIDENCE-BACKED now (3 of the card's 7 mappings):
  - Mapping 1/2 core claim (weights-timing differs from context-timing): the aTTT row (arXiv 2607.03441,
    register row 4) carries the first controlled matched-text A/B the card's falsifier 2 asks for:
    in-context injection 49.3 pct BELOW the 50.7 no-TTT baseline vs 54.3 as adapter update. Caveat: those
    numbers are quoted from the register row written by the adhoc run; I did not re-read the aTTT paper
    this sitting. External support, not internal replication.
  - Mapping 5 (demand precedes organ): Agentic-TTT (2610.12002, register row 5) supplies the GATE: an
    unpenalized policy OVERUSES test-time adaptation (0.256 to 0.510 utility with the learned policy;
    compute penalties cut compute ~30 pct while utility rises). The 03:00Z-drain twin in weight space,
    as the register row says.
  - Mapping 6 (dead-salmon rider): SGUID (2610.12367, register row 8) quantifies it: fewer than 25 pct of
    retrieved skills give useful distillation signal and unselected co-evolution DEGRADES (-0.3 naive vs
    +1.1 selected on Qwen3-4B HMMT25).
- REFINED (2):
  - The MedGemma row (1wywscq, register row 1) adds a SERVING BOUND the coinage never named: merge can
    silently eat the tune (83.8 pct agreement after nominal-scale merge, ~2x alpha/r discrepancy under
    Unsloth, bf16 rounding erasing 17-37 pct of delta elements, all per the register row).
  - The DIAL-OPD row (2610.11659, register row 7) refines WHAT to feed: token selection beats teacher
    scale (4B-with-selection beats 8B-without by up to 1.76 points, per the register row).
- FORCES A QUALIFIER (1): DPPM (2610.11776, register row 6) contradicts the card's mapping 2 as written.
  The card says "at small scale serving-it-live beats compressing-it" (CARD.md lines 17-19); DPPM is a 4B
  model where compressing wins (+21.26 over Full Context on PersonaMem-v2, 62.7x faster). The card's
  mechanism story survives only with a qualifier: the GPS retrieval verdict holds at the estate's
  10-shape scale WITH retrieval infrastructure in hand; a compiled-adapter hypernetwork is a different
  serving regime the card did not consider.
- RESTATES (2): MOLT (1wyvc8k) is the pitfall-bypass census as product (fit tests, base-vs-adapter eval
  as promotion gates = the card's instrument section); AgileRL Arena (1wdjk0y) is landscape.

Verdict: no longer pure operator coinage, but not yet estate-verified. The law is externally
evidence-backed on its core timing claim, its gate, and its food-hygiene rider, refined on serving and
selection, and qualified on the retrieval-vs-compression boundary. Falsifier 2 (CARD.md lines 43-45) has
still never been RUN by the estate: no controlled pitfall-bypass corpus fine-tune of ours exists. Status:
operator coinage with three external confirmations and two external bounds.

### RQ2. Universal Weight Subspace vs the lora_pipeline design and the GPU ladder

Source bytes: watch/inbox/unisub_drop_20261010/CARD.md (read in full), knowledge_graph.json lora_pipeline
cluster (grep this sitting: 1 module node "purpose": "LoRA Fine-Tuning Pipeline - Slashreboot Phase 2",
schema invariant lora_pipeline.v1, LAW rows: never upload training data; output is a LoRA adapter <100MB),
lens/graph.md:22 (degree 5) and :29-30 (zero doctrine/module edges), RIB_GPU_LADDER_20261001.md (read in
full; this box is AMD RX 5600 XT RDNA1 gfx1010, no MFMA, no cooperative matrix, no FP8, lines 4-7; five
gates lines 10-23; standing verdict ignore DeepGEMM on this box, lines 26-31).

- Design change: NO redesign is justified; an additive lane is. UWS's claims (per the card, abstract- and
  site-verbatim-backed there): shared low-dimensional spectral subspaces across 1100+ models WITHIN shared
  architectures, 100x compression by storing coefficients, task training by coefficient optimization,
  data-free merging. Every one of these composes with the module's existing laws: coefficients shrink the
  <100MB adapter payload further, and coefficient federation strengthens the never-upload-training-data
  law (exchange coordinates, not data). The card itself sizes it spec-class with a one-evening probe
  (spectral-decay overlap on two public LoRA adapters, falsifier = top-k principal directions of the
  deltas not aligning better than chance, CARD.md lines 46-49). With the knowledge graph showing zero
  doctrine/module edges (lens/graph.md:29-30), a UWS lane wired into lora_pipeline would also be the
  graph's first doctrine->module edge if the graph builder gains that relation.
- GPU-ladder compatibility: FULLY compatible with ignore-DeepGEMM. The five gates (RIB_GPU_LADDER_20261001
  .md:10-23) are about FP8/MoE QPS demand on NVIDIA tensor cores; UWS needs no such runtime. The probe is
  SVD-class linear algebra on small adapter matrices (CPU-class), and coefficient training, if it ever
  fires, rides the existing LoRA lane where "the quant lane (GGUF on current box) keeps winning per
  dollar" (rib lines 16-18). Honest caveat carried from the card (lines 52-55): preprint v2, within-
  architecture qualifier, zero replication by us. Bank the probe, not the mechanism.

### RQ3. Evidence threshold for a premium weight-adaptation turn under descent cheap-first

Source bytes: AGENTS.md descent protocol bullet (the ask's own citation), lens/laws.md:40 (descent
protocol rib cite), the sheriyuo article (read end to end this sitting), the aTTT/Agentic-TTT/SGUID
register rows, fchollet's framing (read this sitting), JIT card falsifier 2.

The threshold is NOT more external papers. Three of the law's seven mappings are externally
evidence-backed (RQ1), and every premium-turn prerequisite is now measurable locally and cheaply:

1. Demand gate: one RECURRING pitfall class that retrieval demonstrably fails to carry. Agentic-TTT's
   measured lesson is that adaptation without a demand-trigger over-fires and drains; the estate's own
   03:00Z drain law says the same. No recurring unretrievable pitfall on the books = no turn.
2. Matched-text A/B on OUR corpus shape: injection below baseline while adapter update above it (the
   aTTT 49.3 / 50.7 / 54.3 pattern) using our own pitfall-bypass folds. This is exactly JIT-card
   falsifier 2 and the ten-minute-self falsifier 2 (lens/laws.md:108), and it is a local free-lane
   experiment on a 1-8B adapter.
3. Food hygiene at birth: selected (SGUID: unselected co-evolution degrades; DIAL-OPD: selection beats
   scale) and merge-verified (MedGemma bound: probe post-merge agreement before trusting any tune).
4. Verifier signal, not vibes: the sheriyuo article's Omega(sqrt(H)) result says weight-side adaptation
   pays only when the verifier signal flows back into training; the estate's receipt-graded burn verdicts
   ARE that signal, which is the one input a premium turn would have that the collapse-prone intrinsic-
   reward lines do not.

Verdict: a premium turn is UNTIMED, not forbidden. The cheap-first leg is the local matched-text A/B
(threshold 2). One clean local win there converts the JIT law from externally evidence-backed to
estate-verified and only then does a premium checkpoint climb (per descent leg 3, one landed deliverable
per premium turn) buy anything the free lanes cannot.

### RQ4. Dead Salmons: applicable or landscape?

Applicable, and already half-wired into the estate's own adaptation hygiene; not pure landscape.

- Already banked as protocol: the drop card (read this sitting) folds it as a mandatory negative-control
  arm for the suppression-topology lane (CARD.md lines 21-25), the PHANTOM-NUMBER parallel to citation
  lint (lines 26-27), and the confidence-vs-bluffing law (line 28). Those are concrete amendments, not
  decoration.
- The JIT law's rider 6 IS the paper's thesis moved to training data: "a pitfall must be DETECTED under
  controls before its bypass is food, else you fine-tune on phantom pitfalls - dead salmon in the
  dataset" (CARD.md lines 30-31). SGUID then quantifies the adaptation-specific version: unselected
  self-improvement food degrades the loop (register row 8). So the estate's adaptation failure mode
  (fine-tuning on phantom pitfalls) has both the analogy and the measurement.
- The askalphaxiv post (read this sitting) adds the operational checklist the card paraphrased: test
  against meaningful alternative computational hypotheses and report uncertainty under an explicit model.
- Honest bound: the paper's home domain is interpretability explanations of model internals; its transfer
  to training-data curation is by analogy, and the estate has run zero probes with a negative-control
  arm so far (the suppression-topology lane is still pending operator GO per the drop card). Applicable
  in doctrine, unexercised in instrument.

## Receipt

- Fetched this sitting: 11 fxtwitter JSONs via curl (exit 0, sizes 1,832-29,933 bytes); 24 WebSearch
  queries; 0 door failures, 1 degraded item (TheTuringPost article-body pointer).
- Run this sitting: snowflake date decode over 14 IDs (repo venv python, listed above); grep counts over
  catalog/catalog.jsonl (1,136,889 rows per lens/corpus.md:3) for TTT-E2E, 2604.06169, 2603.19461,
  In-Place TTT, Hyperagents, 2512.18792 (1), Dead Salmons (0), 2510.07841 (3), Metan, Recuris; targeted
  memory walk over burns/rib/research_packs/research_polished/corpus-LINKS/knowledge_graph/trajectory/
  attention/press/steal/improve/briefs (biography corpus excluded by size and scope); per-post-ID greps
  over memory/corpus/LINKS.jsonl and the adhoc register (0 for all 11 candidates).
- Not run: no pytest, no paper full-text re-reads beyond what the adhoc run banked, no UWS probe, no
  local matched-text A/B.
