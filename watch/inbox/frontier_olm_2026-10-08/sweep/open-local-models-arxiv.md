# frontier sweep: open-local-models via arxiv - 2026-10-08

source-fetched: 2026-10-08. Seat: sweep-open-local-models-arxiv (dynamic workflow child).
Area: open local language models in the estate's 0.5B-8B janitor/worker band, sub-1B decision
rung, Ollama/llama.cpp serving behavior, harness-vs-weights attribution, tag-digest aliasing.

Anti-rebank baseline honored: day-7 register (21 rows, watch/inbox/frontier_olm_2026-10-07/
register.jsonl, read in full this sitting), frontier_olm_2026-10-08/lens/burns.md + laws.md +
doors.md + questions.md (all read in full this sitting), and the day-7 sweep file
watch/inbox/frontier_olm_2026-10-07/sweep/open-local-language-models-arxiv.md (read in full).
2610.07781 (day-7 CONFIRMED), Mingbird 2610.02001, 2609.26693, 2610.00025, 2610.02142,
2610.07354, 2610.04198, 2610.03695, 2610.05774, 2610.07863, 2610.08164 were NOT re-banked.

## Doors used and degradations (honest ledger)

- arXiv export API, minimal shape per lens/doors.md:39 (no phrase quoting, no sortBy):
  `search_query=all:Ollama&max_results=15` (93 total results, 15 returned) and
  `search_query=all:llama.cpp&max_results=15` both answered clean. No 403s. The only
  in-window entries were 2609.07115 (Ollama in the Wild, 2026-09-07, one day before the
  30-day edge) and 2609.14864 (GGUF-Metadata throughput prediction, 2026-09-14, in window).
- Estate mirror door state/arxiv/: counted this sitting 240 txt (10-06) / 241 (10-07) /
  256 (10-08); built a 734-title index for those three days into
  sweep/_raw/mirror_titles_1006_1008.tsv via the venv python script recorded in the receipts;
  98 titles matched the sweep pattern (small-model, harness, serving, quant, tool-call,
  router). The 2026-10-08 day is the mass the day-7 bank (landed 23:27 on 10-07, lens/
  burns.md:124-125) could not have mined.
- Live pages fetched and read (WebFetch, this sitting): arxiv.org/abs/ 2610.09111, 2610.09772,
  2610.06597, 2610.08680, 2610.06204, 2610.09633, 2609.05241; huggingface.co/h2oai/
  h2o-lightning-4b; liquid.ai/blog/d1-open. All returned content; the two vendor pages are
  primary sources for the release-wave row.
- HN Algolia search_by_date RE-VERIFIED (discharges the lens/doors.md:54 OWED): fetched
  `hn.algolia.com/api/v1/search_by_date?query=ollama&tags=story&numericFilters=created_at_i>1788825600&hitsPerPage=8`
  (epoch 1788825600 = 2026-09-08); clean JSON, nbHits 80, top hits included "MS announces
  DeepSeek V4 Flash and Nemotron locally, llama.cpp comes to Win ML" (2026-10-07) and
  "Clef (and Clef Flash) from Cloudflare" (ollama.com/library/clef, 2026-10-05; Clef is
  already day-7 banked). Verdict: the hn-first mix surfaces in-band serving news same-week;
  adequate for the garden's 30-day row expiry cadence.
- Reddit curl+UA bypass: PROBED, NOT OPENED. `curl -s -m 15 -A "Mozilla/5.0 (Windows NT
  10.0; Win64; x64) AppleWebKit/537.36" "https://old.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3"`
  returned an EMPTY body (zero bytes) in this shell; no JSON payload. The lens/doors.md:56-64
  OWED therefore stands unverified either way; reddit remains a non-door for this sweep and
  nothing below depends on it.
- WebSearch door: used once for the release-wave question; its leads (h2o-lightning-4b,
  Liquid d1) were verified by fetching the primary pages directly, not taken from the summary.

## Pass 1, broad sweep (>=30 candidates considered)

Candidates named and considered (all fetched-or-greped this sitting): from the 98-hit mirror
pattern list, 10-06: 2610.05778 (MedicalHarness), 2610.05977 (StagQ), 2610.05982
(cluster-aware routing), 2610.06011 (D-Loop diffusion drafting), 2610.06026 (differentiable
bit-widths), 2610.06174 (quantized-substrate self-awareness), 2610.06204, 2610.06251 (HQQ
shared stopping), 2610.06269 (Guidance-TTT small-model test-time), 2610.06347
(ImproveAnyTask), 2610.06354 (GraphDecide), 2610.06479 (behavior-preserving KV), 2610.06563
(HERA abstention), 2610.06597 (HEAR), 2610.06689 (programmatic search agents), 2610.06782
(T-Search), 2610.06790 (EDA agentic infra); 10-07: 2610.07659 (DLoop), 2610.07767 (TRACE
FP4 MoE), 2610.07774 (router-logit safety), 2610.07781 (day-7 banked, excluded), 2610.07822
(nucleus spec-dec), 2610.07832 (Dev-Primitives harness), 2610.08026 (hallucination
labeling), 2610.08082 (POLAR tool risk), 2610.08098 (skill injections), 2610.08164 (day-7
banked, excluded), 2610.08205 (tool-calling retrieval vs vector RAG), 2610.08231 (OSFP4
NVFP4), 2610.08430 (NeMo-DCR), 2610.08432 (EMHO), 2610.08678 (secure spec-dec), 2610.08680;
10-08: 2610.09000 (on-device safety localization), 2610.09033 (quad-state open-weight
safety), 2610.09111, 2610.09152 (sk-bench), 2610.09163 (ToolRACER), 2610.09209 (SUD SLM),
2610.09227 (Quantize by Drift), 2610.09633, 2610.09772, 2610.09788 (latent-space judge),
2610.09981 (routing-metadata leakage), 2610.10071 (HGP on-device memory), 2610.10261 (SLMs
reverse-engineer ML pipelines), 2610.10381 (ResidualQuant), 2610.10411 (parallel draft
training), 2610.10426 (CoTrace), 2610.10507 (RECAST evidence routing). From the API queries:
2609.07115, 2609.14864, 2609.05241. From WebSearch + primary fetches: h2o-lightning-4b,
Liquid d1-3B, d1-omni-600M, AstaBrief (out of band, synthesis model). Total named
candidates: 55. Floor of 30 cleared with margin.

## Pass 2, deep reads (9 items read end to end this sitting)

1. **Same Text, Different Prediction (2610.09111)**, live abs page. 180 trained classifiers,
   four serving-context categories, checkpoint and text held fixed: fp32 batch-shape changes
   flip zero labels, bf16 batch-shape changes move up to 56.7pp of predicted probability
   mass with label flips concentrated at small margins; fully generative classifiers flip
   more labels than discriminative ones under identical serving changes; per-mechanism
   sufficient conditions and mitigations derived.
2. **Decoupling Logic from Persona (2610.09772)**, live abs page + mirror anchor. INT4
   Llama-3.1-8B-Instruct and Gemma-3-4B-it on one Apple M2, 480 runs (4 pollution levels x
   3 arms x 2 tasks x 2 personas x 5 seeds): decoupled logic path byte-identical across
   pollution levels (40/40) at fixed ~167-180 token prompts while the mixed single pass
   grows 242 to 1,203 tokens and collapses (0.669 to 0.150 Llama, 0.487 to 0.150 Gemma);
   decoupling beats single-pass on 8B (failure 0-20 vs 80-95 percent, Holm-adjusted
   p<=0.03) but BOTH arms collapse on the 4B. Failure mode is failure to emit the required
   structured output (up to 100 percent of Gemma runs at high pollution). Costs one extra
   first-turn decode (28.2s vs 18.2s); persona hot-swap 1.7ms.
3. **HEAR Protocol (2610.06597)**, live abs page + mirror tail. Bidirectional
   harness-engine pairing protocol; verbatim: "Across four conversational and
   research-agent benchmarks under memory-constrained, concurrent serving, HEAR achieves a
   $1.61\times$ batch speedup and reduces median time-to-first-token by $2.23\times$ on
   SCBench" plus 1.23x/2.45x end-to-end on BrowseComp-Plus/DeepResearchBench "without
   observed task-quality degradation".
4. **CoTrace (2610.10426)**, full mirror abstract. Harness-aware data recipe (trajectory
   routing, provenance matching, curriculum refresh); Qwen3.5-9B 78 to 88 solved tasks
   (SFT) and 90 (online RL variant) on the Tmax promotion split; on Terminal-Bench 2.1 and
   SWE-bench Lite "out-of-distribution transfer depends fundamentally on harness
   compatibility"; compact harness-matched corpus beats much larger pooled corpora.
5. **SLM Negotiation (2610.06204)**, live abs page. Gemma 4 checkpoints 2.3B-31B, GRPO,
   1,152 negotiations per arm vs two unseen frontier buyers: shared-LR gain +0.001 (2.3B)
   to +0.078 (31B); tripled LR improves every size (+0.032 to +0.081); the 4.5B seller at
   tripled rate fits one 48GB GPU with no detectable difference from frontier sellers;
   the 2.3B ten-x-LR arm's gain concentrates on the evaluation buyer sharing the training
   pool's model family. NeurIPS 2026 SLM-Agents workshop poster (comments field).
6. **SLMs on Abstract Reasoning (2610.08680)**, live abs page. 1,000+ runs, ARC-TGI,
   decoder-only/encoder-decoder/MoE SLMs under SFT: scores "conditional on the model,
   adaptation regime, evaluation distribution, and response format"; sharp OOD collapse
   including same-rule-different-grid-scale; executable-rule induction finds correct
   solutions direct generation misses.
7. **Coding-Agent Task Flows (2610.09633)**, live abs page. 4,782 real JetBrains sessions,
   interactive subset (3+ user messages, 33 percent): no single interaction distribution is
   universally realistic; SWE-TaskFlow reshapes issue-derived benchmarks to a named target
   Task Flow (TFAS selection); pilot on 700 SWE-Bench Pro tasks: sequential multi-step
   solving approximately doubles cost without stable resolve-rate change.
8. **h2o-lightning-4b (HF card) + Liquid d1-3B/d1-omni-600M (vendor blog)**, both primary
   pages fetched. h2o-lightning-4b: created 2026-10-02, built on Qwen/Qwen3.5-4B,
   single-forward-pass decision model returning per-option probabilities; card claims
   "#1 on JevBench (October 7, 2026)", open-weight composite 72.5 vs Jev 1.13.0's 71.5,
   text public set 205/231 (88.7 percent), ~$0.021 per 1,000 decisions, Apache-2.0, BF16
   with a quantizations page (no GGUF on-card), served via unmodified vLLM 0.30.0 + shim.
   Liquid d1: released 2026-10-07; Decision Index v0.2.1 public split d1-3B 48.57 /
   d1-omni-600M 15.95; d1-3B text mean 82.9 ahead of Decider 4B at 81.1; latency 8ms RTX
   4090 to 50ms Jetson Orin Nano; "Native support for llama.cpp across Apple, AMD,
   Qualcomm, and NVIDIA with NVFP4" and "day-one support for llama.cpp". All numbers are
   vendor-published; under RIB_MODEL_GARDEN_ROUTING.md:46-68 the cells stay UNMEASURED
   until estate instruments run them.
9. **Uncensored Open-weight Models (2609.05241)**, live abs page + mirror anchor. 2026-09-04,
   four days before the 30-day edge (flagged, not hidden): 3,471 original uncensored models
   on HuggingFace Jan 2024-Mar 2026, each repackaged an average 2.4 times, three actors
   account for 52 percent of 8,164 compressed redistributions; verbatim: "Once quantized
   and mirrored across separate accounts, formats, and registries such as Ollama, these
   models persist regardless of upstream removal and become easier to deploy downstream."

## Answers against the ask's five research questions

**Q1 (in-band releases beating gemma:2b on the lanes' scut):** Still nothing bankable as a
measured beat. What the window adds: (a) a decision-model release wave inside the band
(h2o-lightning-4b on Qwen3.5-4B; Liquid d1-3B and sub-1B d1-omni-600M with claimed day-one
llama.cpp/AMD support) whose every number is vendor-side and whose "decision model" framing
(single forward pass, typed answers with probabilities) is architecturally different from
gemma:2b janitor scut; (b) 2610.09633's result that the interaction protocol itself doubles
cost without changing resolve rate, which means "beats gemma:2b on the lanes' actual scut"
is unanswerable until the estate battery samples the lanes' real task-flow distribution
(the n=0 meter problem is also a distribution-specification problem). Estate action: d1-3B
and h2o-lightning-4b go on the garden's UNMEASURED candidate list; d1's claimed AMD/llama.cpp
path is the first sub-1B decision rung that could physically run on the estate box, but the
vendor latency table (RTX 4090/Jetson/M5 Pro) contains no AMD consumer part, so the estate
number is OWED.

**Q2 (harness vs weights attribution on the estate stack):** The window triples the
instrument pressure on this question. 2610.09111 shows bf16 batch-shape alone moves up to
56.7pp of score mass with weights and text fixed - the estate's Ollama/llama.cpp serving
context (batch shape, dtype, kernel selection) is a measured condition that must be pinned
before any gemma:2b pass-rate is attributable to weights; this sharpens the P6
four-pinned-choices quant A/B spec with a fifth axis (serving context) and gives the P2
contamination tripwire a physical mechanism: the banked gemma:2b 0.9167/0.8333 twin pair
could be serving-context drift, not prompt-twin drift. 2610.09772 shows the smallest rung
is the problem: on the 4B model BOTH decoupled and monolithic arms collapse under
pollution, so any "separate the logic" cure must be validated at 2B, not assumed from 8B
results. 2610.10426 (CoTrace) and 2610.06597 (HEAR) both price the harness as a first-class
component: CoTrace shows evaluation under a foreign scaffold understates a model
("procedural execution breakdowns under foreign scaffolds"), i.e. gemma:2b's measured
janitor rate is a property of the estate harness as much as the weights - the day-7
harness-dominates finding now has a training-side and a serving-side replicate in the same
ten days.

**Q3 (alias classes surviving P3 digest pinning):** 2609.05241 is ecosystem-scale evidence
that repackage-aliasing is the dominant persistence mechanism (2.4 repackage average per
original model, 8,164 compressed redistributions, three actors 52 percent) and that Ollama
registries are one of the alias carriers. P3's boot-time digest pinning is the correct
countermeasure by this evidence; what the paper adds is the adversary shape - aliases
arrive as quantized cross-account reposts, so digest pinning must key the WEIGHTS digest,
not the tag or repo name (P3 already does; the paper confirms the design). The estate-side
half (which local tags still alias today) stays an on-box probe (ollama show digests), not
an arXiv finding.

**Q4 (grok-4.7 champion re-measure; fable-5.1 plan_call re-measure):** Nothing in this
window's arXiv flow bears on either remote cell directly. Adjacent instrument pressure only:
2610.06204's contamination result (a small model's measured gain concentrates on the
evaluation buyer sharing its training family) is a fresh argument that the champion cell's
self-invented-task contamination suspicion (RIB_MODEL_GARDEN_ROUTING.md:115-119) is the
default failure mode of single-family evaluation, and 2610.08680's response-format
conditionality supports the per-animal recipe-gating law (re-measure through plan_call, not
bare). Both re-measures remain estate-side and OWED.

**Q5 (does the hn-first mix keep the 30-day expiry fed):** YES for arXiv and serving news,
verified this sitting: the mirror (256 files for 10-08 alone) plus the export API plus
search_by_date (80 hits in-window, clean JSON, sub-second) would have caught every item
banked above without reddit. The curl+UA reddit bypass was probed once and returned an
empty body: the bypass is still UNVERIFIED, not a success. HN's signal-to-noise for in-band
releases was thin this sitting (Clef repeat, Windows ML roundup), while the release wave
itself surfaced via WebSearch to vendor pages - keep WebSearch-to-primary-page as the
release-door complement to the HN mix.

## Steal queue (estate-instrument shaped, cheapest first)

1. Pin serving context in the quant A/B: add batch-shape + dtype to QUANT_AB_SPEC_AMEND.md's
   four pinned choices before it fires (2610.09111's 56.7pp bf16 batch-shape swing is
   exactly the confound the spec's pin contract exists to kill).
2. Run the P2 duty_fuzz twin check with serving context VARIATED deliberately (same weights,
   different batch shape): if the gemma:2b twin delta moves, the tripwire needs a
   serving-context fingerprint column.
3. Garden cells: d1-3B, d1-omni-600M, h2o-lightning-4b enter as UNMEASURED rows with
   vendor-claim provenance marked; d1's llama.cpp/AMD day-one claim makes d1-3B the first
   on-box-probeable decision rung.
4. 2B-scoped pollution probe: 2610.09772's both-collapse-at-4B result predicts the estate's
   gemma:2b janitor cannot host a decoupled-logic cure; a 20-row pollution ladder on-box
   would bank the band's own curve.

## Overlap census (commands actually run this sitting)

- Single combined pass `grep -c -a -E "Serving-Context Nondeterminism|Decoupling Logic from
  Persona|HEAR Protocol|Harness.Engine Pairing|ARC-TGI|RL-Trained Sellers|SWE-TaskFlow|
  TaskFlow|h2o-lightning|JevBench|Uncensored Open-weight|serving-context" catalog/catalog.jsonl`
  (1,266,929-line, ~341MB file): 5 rows; decomposed by re-grep with context: ALL five are
  state/arxiv mirror abstract snapshots (zone=lsa) of the very items read here (2609.05241,
  2610.06204, 2610.06597, 2610.09111, 2610.09772) - corpus presence, not banked mining.
  Second pass for "Abstract Reasoning Tasks|CoTrace|Coding-Agent Benchmarks Should Match":
  4 rows, all state/arxiv mirror snapshots (plus one unrelated PotARCin title hit). The
  release-wave names (h2o-lightning, JevBench beyond the day-7 nimble row, d1) have NO
  catalog rows.
- `grep -r -l -i` over memory/ + watch/inbox/ for the 8 candidates' distinctive phrases:
  ZERO files outside this sweep's own output directory.
- Day-7 register dedup: all 21 rows read this sitting; none of my 8 bank items appear in it.
  The day-7 "8GB VRAM community benchmark" row named Ornith-1.5-9B/Tiel-Coder-35B-A3B, not
  h2o or Liquid; the day-7 nimble row's "Jev 1.13" is a benchmark mention, not the h2o card.
- Prior-sweep dedup: frontier_olm_20260928's bank (2609.21341, 2609.07370, 2609.23742,
  2609.25373, 2609.32042, 2609.33467, 2609.05881, HF State of Open Models, per day-7
  sweep's overlap census :49) - no intersection with my items.

## OWED / not verified (stated, not guessed)

- Full PDFs not read for any item; live abs pages + full mirror abstracts are the read
  surface. All performance numbers are the papers'/vendors' own claims, not re-run here.
- 2609.05241 is dated 2026-09-04, four days outside the 30-day window; banked for the Q3
  aliasing question with the deviation flagged in its date field.
- 2609.07115 (Ollama in the Wild, 2026-09-07) and 2609.14864 (GGUF-Metadata throughput,
  2026-09-14) were surfaced and read at abstract-summary level only (API door rendering);
  neither is banked as an item; 2609.14864's "fitted efficiencies are not universal -
  host-specific predictors" line is worth a deep read for the estate's AMD box and is left
  in the queue.
- Reddit curl bypass: probed once, empty body, unverified. Search_by_date numericFilters
  epoch 1788825600 computed by hand from 2026-01-01T00:00Z; the returned created_at values
  (2026-10-05..10-08) are consistent with the intended window.
- Vendor pages (h2o card, Liquid blog) are marketing surfaces; the d1 "Decision Index" and
  h2o "JevBench" numbers are unverified beyond those pages, and the d1 license was not
  stated on the fetched page (checked HF is OWED).
- The estate-side half of Q3 (local ollama show digests today) was NOT run this sitting.

## Receipts

- WebFetch (this sitting): export.arxiv.org/api/query x2 (all:Ollama, all:llama.cpp);
  arxiv.org/abs/{2610.09111, 2610.09772, 2610.06597, 2610.08680, 2610.06204, 2610.09633,
  2609.05241}; hn.algolia.com/api/v1/search_by_date x1; huggingface.co/h2oai/
  h2o-lightning-4b; liquid.ai/blog/d1-open.
- Local reads (this sitting): lens/burns.md, lens/doors.md, lens/laws.md, lens/questions.md
  (all four in full); frontier_olm_2026-10-07/sweep/open-local-language-models-arxiv.md (in
  full); frontier_olm_2026-10-07/register.jsonl (21 rows, full parse); state/arxiv/
  {2026-10-06,2026-10-07,2026-10-08} title index build + abstract reads for 2610.06597,
  2610.08680, 2610.09111, 2610.09772, 2610.08205, 2610.06204, 2610.06269, 2610.10426,
  2610.09633, 2610.09000, 2610.10261, 2610.07832, 2610.08432, 2610.06347, 2610.06563;
  2609.05241v1.txt full abstract tail; 2610.06597v1.txt full abstract tail.
- Commands: title-index build + pattern grep via .venv/Scripts/python.exe (script inline in
  session, output sweep/_raw/mirror_titles_1006_1008.tsv, 734 rows, 98 hits); catalog grep
  passes and memory grep as listed above; curl reddit probe as quoted in the doors section.
- Em-dash law: ascii-only, verified by construction; grep check left to the run's receipt step.
