# Sweep: open-and-local-models via hn (2026-10-06)

source-fetched: 2026-10-06
seat: sweep-open-and-local-models-hn (workflow subagent)
doors used: HN Algolia (search_by_date with numericFilters, plus one relevance search),
HN item pages, arXiv export API (id_list reads + one sortBy=submittedDate query), the
banked r/LocalLLaMA Atom-RSS recipe (curl, browser UA), one blog page (jerrygamblin.com),
one HF dataset page, one vendor blog (liquid.ai). WebFetch quotes pass through the fetch
tool's extraction model; each banked quote carries that one step of mediation unless the
section marks it verbatim-from-XML.

## Instruments actually run this sitting

Pass 1 (broad, 30+ candidates): seven Algolia probes, all
`search_by_date?query=...&tags=story&numericFilters=created_at_i>1788652800`
(cutoff epoch 1788652800 = 2026-09-06T00:00:00Z, arithmetic: 1767225600 for 2026-01-01
plus 248 days). nbHits receipts: "decision model" 107, Kolibri 4, ollama 78,
"open weights" 17, gemma 138 (noise: German-name collisions, only the tej.as Kolibri
post surfaced), "agent harness" 42, "distillation harness" 0. One relevance search
"Harness-Aware Distillation": nbHits 0. Roughly 110 listing lines, 60+ distinct
in-window candidates. Reddit RSS recipe executed live: `curl -A "Mozilla/5.0 ...
Chrome/126..." https://www.reddit.com/r/LocalLLaMA/top/.rss?t=month` returned atom XML
(saved watch/inbox/frontier_olm_2026-10-06/tmp_rss_llamamonth.xml, 25+ entries parsed
with rg). arXiv `sortBy=submittedDate` recipe executed:
`cat:cs.CL AND abs:"open-weight"`, opensearch:totalResults 1149, top 20 listed.

Host instruments (read-only, this sitting): `ollama list` = 18 models; gemma:2b 1.7 GB,
gemma4:latest 9.6 GB, qwen2.5:7b 4.7 GB present; NO decision model pulled (no tev1,
nimble, Julia-1, Laya, Kev-4B, Clef, Gutsy, Wazn); no Kolibri. RAM: 67,058,352 KB total
(64.0 GB), 27,992,644 KB free (26.7 GB) at the moment of reading. GPU: AMD Radeon RX
5600 XT, AdapterRAM 4,293,918,720 (WMI reading; rib ID RDNA1 gfx1010,
memory/rib/RIB_GPU_LADDER_20261001.md:6). Disk C: 255,602,544,640 B free of 1,999,508,951,040.

Pass 2 (deep reads, fetched end to end): HN items 49933476, 49942706, 49946069; the
jerrygamblin.com CVE post; HF dataset LocalLLaMA/typed-decisions; liquid.ai d1 blog;
arXiv abstracts 2610.06625, 2610.03935, 2610.04403 (one id_list batch, then verbatim
excerpts per id), 2610.05778. Ten items read this sitting.

## OWED recipes closed this sitting

- doors.md:42-44 (hn search_by_date "OWED"): EXECUTED; receipts above.
- doors.md:28-29 (arXiv sortBy=submittedDate "NOT probed today"): EXECUTED; 1149 total
  on the open-weight query, sorted feed parsed.
- burns.md:73-74, 100-102 (banked RSS recipe): EXECUTED live; door returns fresh atom.

## Answer 1 (decision model vs gemma:2b per dollar, L15): contested wave, cell stays UNMEASURED

The 30-day window carries instrument-grade evidence on BOTH sides now, none of it ours.

Against generality: HN 49933476 (160 points, 73 comments, 2026-10-02) discusses a Red
Hat benchmark claiming decision models do not beat LLM-as-a-judge or traditional
classifiers. Commenter numbers from the thread: Jev confidence off ~6% average on
jev-sec-bench, the same as Qwen2.5-7b-instruct; on Banking 77 Jev did worst, "about 25
points off from reality"; batching closes much of the speed gap (n=20: 1.6x faster,
1.2x costlier, no accuracy loss). Counter in the same thread: another lab's own bench
has Jev ahead on multi-step reasoning, calibration, cost and latency; title
editorialization was flagged by two commenters. arXiv 2610.06625 (2026-10-05) finds JEV
matches or comes close to LLM capability on seven political science replications but
shows no cost advantage at OpenAI batch prices, with calibration advantages
inconsistent versus Qwen (abstract-level read via the fetcher's summary; the verbatim
excerpt is banked below).

For, on a real scut class: jerrygamblin.com (2026-10-04) ran Clef Flash and Clef 27B
locally in Ollama via /v1/systemone over all 27,489 CVEs of Aug 4 to Oct 3 2026: Flash
median 0.84 s/description, 27B median 2.0 s, total ~6.4 h, $0 on a MacBook Pro M5 Pro
64 GB; the Flash-screens/27B-re-reads cascade matched 128 of 129 hand labels, and the
author's law is "a small model is a fine screen and a poor judge" (27B overturned 54.8%
of Flash's no-impact flags).

Estate reading: neither side fills our routing cell; L15 (instruments only,
RIB_MODEL_GARDEN_ROUTING.md:46-53) keeps the decision-model rung UNMEASURED until the
30-prompt tool-call battery fires. What the sweep changes about the battery design:
score calibration (ECE/Brier/KL), because that is the wave's weak axis in both critical
sources; add a cascade arm (small screens, big re-reads flags), because that is the
shape that already won publicly on a scut class; expect no blanket per-dollar win.
Also: decision models are not a gemma:2b replacement, they are a different interface
(typed multi-question distributions, zero output tokens) that gemma:2b cannot emit at
all. The battery should therefore run TWO comparisons: per-dollar on overlapping scut
classes, and capability-per-dollar on typed-gate classes where gemma:2b cannot even
enter.

## Answer 2 (local lane battery cells): nothing earned routing dollars from public evidence; per-artifact law added

I fired no battery; the fill procedure (RIB_MODEL_GARDEN_ROUTING.md:202-209) and the
probe order (DIGEST.md:83-92) own that. Sweep contribution, three items:

1. Quant-condition law for every cell from arXiv 2610.04403 (2026-10-03): across 27
   GGUF-quantized models (0.35B-14B, down to Q2_K) on 429 rare-word definition probes,
   sub-2B models lose 20-67% of definitions under aggressive K-quants, models above ~3B
   are mostly robust, Q4_K_M stays clean at >=1B, damage is frequency-graded and NOT
   predicted by perplexity, and per-artifact validation is urged. The battery must name
   the exact GGUF artifact per cell (gemma:2b's own Q4_0 history is on record in
   memory/rib/RIB_GPU_LADDER_20261001.md:30-31).
2. New open decision-model candidates for the rung pull: InnerJev-4B and InnerJev-27B
   (arXiv 2610.03935, open weights via Reasoning-to-Readout Self-Distillation; 27B
   matches Jev on JEVal at ~0.1 s/query), Gutsy (~500 MB CPU decision model, four Show
   HNs in the window), Wazn-2B. Clef 18 GB was already banked day-5.
3. ollama list this sitting: the rung is not installed; nothing local can score a
   decision-model cell today.

## Answer 3 (five gates on this host): none pass by construction; the quant lane is the branch

The host GPU is AMD RX 5600 XT (RDNA1, gfx1010; WMI AdapterRAM 4.0 GB reading this
sitting). Gates 1 (SM90/SM100), 2 (24 GB VRAM) and 4 (CUDA 12.8 + vLLM) fail on this
host for every release, so no in-window open weight passes the five gates here; the
rib's own else-branch ("the quant lane keeps winning per dollar",
RIB_GPU_LADDER_20261001.md:17-19) is the operative lane. In-window open weights that
fit the host's quant lane (RAM, not VRAM):

- Ternary Bonsai 2, 27B at <6 GB claimed WebGPU-capable (r/LocalLLaMA RSS 2026-09-17);
  ALREADY on this box: ollama list shows hf.co/prism-ml/Ternary-Bonsai-2-27B-gguf:PTQ1_0
  6.6 GB pulled ~2026-09-24. The estate adopted this class before the sweep saw it.
- InnerJev-4B/27B (new, open, arXiv 2610.03935).
- Clef 18 GB (banked day-5), Kolibri 20.9 GiB floor (marginal, see Answer 4),
  Gutsy ~500 MB.
Closed or pending: d1 (Liquid AI) claims rivaling Jev and matching-or-beating GPT-6.1
Sol on four of six tasks at "19x to 200x less" cost with ~200-300 ms decisions, but the
blog says open weights are only promised "soon" (fetched this sitting); Mistral Large 4
"Le Chonk" 1T with open-weights release planned (Algolia 2026-10-06, today); Step 5
600B/27B promised Oct 15 (day-5 listing); Qwen 4 announced at Apsara (RSS 2026-09-22,
weights not seen by this sweep).

## Answer 4 (Kolibri fit and serve): fit is arithmetic-yes at the community floor; serve stays OWED

Fit, on instruments run this sitting: day-5 card floor 20.9 GiB (Sakura IQ2_XS) and
22.5-39.1 GB for 2.30-4.0 bpw (steal card, watch/inbox/frontier_olm_2026-10-05/steal/
open-local-language-models via arxiv.md:36) against 26.7 GB free RAM, 64.0 GB total,
238 GB free disk: the floor artifact fits both disk and free RAM with ~4 GB headroom;
total RAM (64 GB) matches the thread's own arithmetic. Community servings read this
sitting (HN 49942706, 698 points, 338 comments): ekidd, "You can probably run it
comfortably in 96B of RAM with a decent quant that doesn't lose too much", and
sspiff, "a mixed 8bit/4bit quant would fit easily inside 64GB of memory". In-thread
weak-axis confirmation: poor chained tool use and "spends way too many tokens on
overthinking" (tharkun__, martianvoid), consistent with the banked teardown (BFCL 39.8,
Terminal-Bench 27.7). Serve NOT attempted: the pull is download-gated and is probe
order item 4 (DIGEST.md:90); the falsifier stands (>=20/30 vs <=15/30 against
qwen2.5:7b). I did not pull 21 GB in a sweep.

## Answer 5 (HAD replication): zero HN presence; closest public replication found and it supports the harness-fixed control

Relevance search "Harness-Aware Distillation": nbHits 0; HAD (arXiv 2610.02858, banked
day-5) has no HN thread, so no public replication of its exact numbers exists on this
door. The strongest public neighbor is MedicalHarness (arXiv 2610.05778, 2026-10-05,
abstract fetched verbatim this sitting): five open-weight models x five agent
harnesses x 107 medical tasks, changing only the harness, plus an MH-Lab that switches
off context management, planning or tool exposure one at a time. Verbatim:
"We find that the harness and its interaction with the model account for about a
quarter of the outcome variance, and that no single harness is best across models and
tasks." Estate reading for the owed HAD head-to-head: swapping harness halves on
gemma:2b should move scores materially (~25% of variance in the public study), so the
harness-fixed control is necessary, and the swap probe should ablate one mechanism at
a time (MH-Lab's pattern) instead of swapping whole halves once. Catalog holds only an
intake abstract row (see overlap below); the analysis here is new.

## Banked items (8, strongest first)

Each: quote from the page fetched this sitting; overlap from rg runs over
catalog/catalog.jsonl and memory/ this sitting, plus day-5 file reads.

1. Decision models like Jev don't beat LLM-as-a-judge or traditional classifiers
   (HN 49933476, 160 points, 73 comments, 2026-10-02; article
   developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-
   traditional-guardrails). Quote: "On the OpenRouter Banking 77 benchmark Jev did the
   worst out of all the models, being about 25 points off from reality." Why: the
   strongest public counter-evidence to the decision-model headline, with calibration
   and batching numbers the estate battery should copy; the day-5 wave rows are all
   pro-wave, this is the first contested row. Overlap: rg 49933476|benchmarking ai
   decision models|decision models like jev over catalog+memory: 0 hits; day-5
   decision-model rows (DIGEST.md:71-81) hold none of it.
2. Decision Models vs. CVE Data (jerrygamblin.com, 2026-10-04; HN item 49957402).
   Quote: "a small model is a fine screen and a poor judge". Why: a real scut-class
   instrument (27,489 CVEs, 129 hand labels, 99.2% cascade accuracy, $0 local, Flash
   0.84 s median) running on the estate's own stack (Ollama /v1/systemone); the
   screen-then-judge cascade is the battery arm to add. Overlap: rg jerrygamblin|27,489|
   decision-models-vs-cve over catalog+memory and rg -l over the day-5 dir: all empty.
3. MedicalHarness: A Controlled Evaluation of LLMs and Agent Harnesses on Medical
   Tasks (arXiv 2610.05778, 2026-10-05). Quote: "We find that the harness and its
   interaction with the model account for about a quarter of the outcome variance, and
   that no single harness is best across models and tasks." Why: the closest public
   replication of HAD's thesis and the design template (MH-Lab one-mechanism-off) for
   the estate's harness-fixed head-to-head. Overlap: catalog holds only the intake
   abstract row ("778v1.txt", 1738 B, zone lsa, mtime 2026-10-06T06:30:05Z); no
   analysis held; day-5 dir rg -l: empty.
4. JEV versus LLMs: Accuracy, Cost and Calibration on Seven Political Science
   Replications (arXiv 2610.06625, 2026-10-05). Verbatim excerpt: "Large language
   models (LLMs) annotate and scale political text or constructs by generating text
   tokens. A new class of models, which TypeSafe markets as System One models,". Why:
   peer evidence that the decision-model cost advantage vanishes at batch prices and
   calibration wins are inconsistent versus Qwen, the exact axes the estate battery
   must score. Overlap: catalog intake row only ("625v1.txt", 1684 B, zone lsa, same
   mtime); analysis new.
5. Kolibri: A Sovereign Open-Weight Model (HN 49942706, 698 points, 338 comments,
   2026-10-03). Quote (ekidd): "You can probably run it comfortably in 96B of RAM with
   a decent quant that doesn't lose too much." Why: the thread is the fit/serve record
   for the owed Kolibri pull (96B/64GB RAM statements, weak multi-turn confirmation)
   and lands the same day as the tech-report dupe merge (49946069, read; moderation
   only). Overlap: day-5 holds the vendor blog and teardown card (steal/open-local-
   language-models via arxiv.md); catalog rg for kolibri: 0 (aleph hits are a litellm
   file and Mathlib Aleph.lean); this banks the thread's serving comments, not the blog.
6. General Decision Models: Benchmarking and Insights Beyond Jev (arXiv 2610.03935,
   2026-10-02). Verbatim excerpt: "General decision models, such as Jev, have recently
   emerged as efficient alternatives to LLMs for structured judgment and selection."
   Why: open InnerJev-4B/27B rung candidates, the bilingual JEVal battery (11,257
   instances, 36 datasets), and the counter-finding that in multi-step systems faster
   local choices lower task success as errors accumulate (abstract summary via fetcher),
   which cuts against using the rung inside long agent loops. Overlap: rg innerjev|jeval|
   2610.03935: catalog hits are "jevals_readme" substring noise (6), memory LINKS.jsonl
   same; the paper is not held.
7. Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write
   Rare Words They Can No Longer Define (arXiv 2610.04403, 2026-10-03). Verbatim
   excerpt: "Post-training quantization to the GGUF format's mixed-precision K-quants
   is commonly how open-weight language models reach consumer hardware, yet its effect".
   Why: the per-artifact quant-condition law for every local battery cell (sub-2B
   20-67% definition loss, Q4_K_M clean at >=1B, damage not predicted by perplexity).
   Overlap: rg 2610.04403|saying, not knowing|rare words they can no longer over
   catalog+memory: 0 hits.
8. Typed Decisions: an open benchmark for decision models (HF dataset
   LocalLLaMA/typed-decisions, Apache-2.0; HN item 49929523, 2026-10-02). Quote:
   "A model gets one piece of unstructured state and answers five typed questions
   about it at once, and every answer is a probability distribution, not a single
   label." Why: a ready-made decision-model battery (400-case test / 2,000 decisions,
   accuracy/KL/Brier/ECE) so the rung probe need not hand-roll one; caveat banked
   alongside: gold labels are the mean of three samples from a ~4B teacher and teacher
   self-agreement 0.735 is the ceiling. Overlap: dataset URL absent from catalog
   (rg LocalLLaMA/typed-decisions: 0); two name-adjacent papers ARE in lsa intake
   ("Decide, Don't Generate...", "From Retrieval to Typed Decisions...") and are not
   this dataset.

## Listing-level candidates (seen, not banked, with reasons)

- d1 vision decision model (liquid.ai blog fetched): closed weights today, promise of
  open weights "soon"; fails the open-weight criterion for now.
- Gutsy (4 Show HN posts, one repo): repeat-posting pattern; no independent evaluation
  read; candidate for the rung pull list only.
- Wazn-2B (HF numidlabs/wazn-2b-v0.1, 2026-10-04): listing only.
- Jeva.cpp fork (49878572): JEV-compatible API over any LLM; overlaps the thread's
  "EBNF grammar + logprobs reproduce Jev behavior" argument; no numbers fetched.
- Red Hat thread siblings: jerrygamblin CVE post (banked, item 2), synthpop
  calibration post (title-only), kitsuno laya-in-shadow (title-only), AnthusAI
  hard-decisions bench (title-only), Decision Index 0.2.1 (70 open reproductions,
  listing only), vLLM "Decision 2.0" (listing only), d1 (above).
- Mistral Large 4 Le Chonk 1T (today, listing), Qwen 4 Apsara announcement (RSS
  09-22, listing), Ternary Bonsai 2 (RSS 09-17, already on box, Answer 3).
- Mingbird agent-harness-for-2B (49909962): paper detail already read day-5 via
  alphaxiv (frontier_olm_2026-10-05/sweep/open-local-language-models-arxiv.md:9);
  thread not re-banked.

## Honest gaps / not run

- No battery fired, no model pulled, no serving test: the Kolibri pull and the
  decision-model battery remain probe-order items (DIGEST.md:89-90); every verdict
  cell stays UNMEASURED per L15.
- The Red Hat article body was read only through its HN thread discussion plus
  commenter-cited numbers; the article page itself was not fetched.
- arXiv 2610.06625 and 2610.03935 findings ride the fetcher's abstract summaries
  (verbatim excerpts banked); full texts not read.
- The RSS feed returned top-of-month titles only (no scores); Jev ad-fatigue mods
  thread (09-23) read as title only.
- The day-5 decision-model headline stays a lead: nothing banked today confirms or
  kills it for OUR scut classes; both public sides now carry numbers, ours do not.

No em-dashes in this file. Every quantity traces to a fetch, command, or file line
named above.
