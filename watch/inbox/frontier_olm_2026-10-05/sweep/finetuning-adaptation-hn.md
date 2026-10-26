# frontier sweep: finetuning-adaptation via HN (2026-10-05)

source-fetched: 2026-10-05

Area: finetuning-adaptation. Feeds the operator-gated Gero-4B calibrator door
(commits de0f6a870 and f94adae8d) and the hf-agents-course shelf; the target is the
eval battery that un-parks the GB-class download decision
(`watch/inbox/frontier_olm_2026-10-05/lens/questions.md:121-143`).

## Door health (HN recipe)

- Algolia API (`hn.algolia.com/api/v1/...`) healthy all session: search_by_date,
  relevance search, and the items API (`/api/v1/items/{id}`, used to read full
  comment text verbatim, the JSON equivalent of fetching
  `news.ycombinator.com/item?id=...`).
- Two WebFetch calls timed out at 60s (LoRA relevance search; tool-calling
  by-date; later also academy.dair.ai and arxiv.org). Fallback per recipe spirit:
  same endpoints refetched with the repo venv python (`_hn_search.py`, 20 terms x
  two endpoints, urllib) and curl for article HTML. No fallback success is
  claimed beyond what the fetched bytes show.

## Pass 1: broad sweep (candidates)

Instruments: 6 WebFetch Algolia queries (first batch) + `_hn_search.py` batch
(277 raw rows, saved in this session's stdout log) + the earlier per-query WebFetch
hits. After filtering acronym noise (relevance search matches "SFT"/"GRPO"/"PEFT"
loosely: Navier-Stokes, Steam Frame, Pentagon stories), roughly 40 on-topic
in-window candidates (created_at >= 2026-09-05) were considered. The 30-candidate
floor is met. Abridged candidate list (objectID, pts, date, title):

1. 49923692, 638, 10-01, Clef: Open-weight decision models, and new RL fine-tuning platform
2. 49748553, 236, 09-18, Show HN: Cactus Needle 3: 8-29MB automation models can match DeepSeek V4 Flash
3. 49806430 noise; skipped. On-topic remainder:
4. 49807413, 10, 09-22, Ask HN: When is fine-tuning a small LLM worth it?
5. 49897103, 1, 09-29, Fine-tuning Qwen3.5-4B to replace Gemini Flash-Lite in a RAG pipeline
6. 49966238, 1, 10-05, Show HN: I finetuned 1.5B Qwen to near GPT-4o level bash generation perf
7. 49807276, 3, 09-22, Show HN: Shrewd: what I learned distilling LLM labels into local classifiers
8. 49826663, 1, 09-24, Turn Text into Actions with Needle, 14Mb (raspberrypi.com)
9. 49627340, 2, 09-09, FrogNano: Training a 4B Coding Agent via Online Task Synthesis (arxiv 2609.07925)
10. 49936786, 2, 10-02, SFT matches RL if you MCMC the training data first (arxiv 2610.02140)
11. 49880342, 2, 09-28, Recursive Self-Improvement via On-Policy Distillation (arxiv 2609.30652)
12. 49915039, 2, 09-30, Distillation Defenses Easily Break After Reinforcement Learning (arxiv 2609.35699)
13. 49611009, 1, 09-08, Stealing Reasoning Traces from Proprietary LLM APIs (arxiv 2608.09867)
14. 49912105 + dups, 09-30/10-01/10-04, Disrupting a coordinated model-distillation campaign (openai.com)
15. 49618622/49624585, 09-08/09-10, CISA advisory AA26-251A China distillation campaigns
16. 49879032, 92, 09-28, Jensen Huang says AI distillation is 'competition.'
17. 49836602, 11, 09-24, SkillOpt: Training Loop for Agent Skills (microsoft.github.io)
18. 49806630, 5, 09-22, DeepSeek Elastic Compute: sandbox infra for agentic training (arxiv 2609.22978)
19. 49833760, 33, 09-24, For Computer Use, the harness matters as much as the model (stagehand evals)
20. 49567153, 4, 09-15, What If the Adaptation Were a Model? (HF shadowpeft blog)
21. 49783349, 1, 09-21, DeltaTensors: Git for model fine-tunes
22. 49687253, 2, 09-13, Molt: thermally aware QLORA fine-tuning for Windows laptop GPUs
23. 49778955, 1, 09-20, QLoRA Explained (substack)
24. 49881077, 1, 09-28, Ask HN: Finetuning strategies
25. 49900316, 2, 09-29, Ask HN: frontier models internal, end of YC?
26. 49823444, 2, 09-23, Latent-GRPO and Continuous Reasoning Deep Dive
27. 49934012, 23, 10-02, Fixing GRPO's credit assignment problem (arxiv 2609.36178)
28. 49719027, 2, 09-15, Local LLM engine where a tool call cut by the token limit still parses
29. 49923378, 1, 09-30, Programmatic Tool Calling (OpenAI docs)
30. 49818370, 3, 09-23, LLM Benchmark for de-identification and synthesis (HF Privacy-Bench)
31. 49766109, 3, 09-19, What failed when I trained an object detector on synthetic images only
32. 49575804-range noise; skipped. Also considered: 49916604, 49909455, 49902789-range
    agent infra stories (ranked out: not finetuning).
33. 49537178, 09-02, Fine-tuning your LLM might be making it dumber (WINDOW EDGE: 3 days
    outside; topically core to RQ2, noted not banked)
34. 49538490, 09-02, FrontierHarness Eval: 9 harnesses, same model, cost per pass varies 17x (WINDOW EDGE)

## Pass 2: deep reads (12 sources read end to end)

Fetched artifacts kept as receipts in this directory: `_hn_items.py` output
(threads 49807413, 49966238, 49807276, 49897103, 49627340, 49748553, 49923692),
`_abs_mcmc.html`, `_abs_frognano.html`, `_abs_onpolicy.html`, `_abs_steal.html`,
`_abs_defenses.html`, `_shrewd_readme.md`, `_clef.html`, `_needle.html`.

### 1. duane.sh: Fine-tuning Qwen3.5-4B to replace Gemini Flash-Lite in a RAG pipeline (HN 49897103, 2026-09-29)

The strongest RQ1+RQ2 item in the window. Recipe: SFT over 24,000 examples
(from 25,206 sampled excerpts), one pass, LoRA rank 32 on Qwen3.5-4B, 1.6 hours,
about $7 on one rented H100; then DPO (4 contexts per 12,000 excerpts, temp 0.8)
and GRPO (100 steps, 25,600 graded contexts). Serves on an RTX 4090 24GB at about
1.3s per excerpt. Claim: "It makes fewer mistakes than Gemini 2.5 Flash-Lite at
71% less cost."

Eval battery (the Gero-4B un-parker): blind LLM-as-judge with position debiasing
("every system appears in every position equally often"), held-out sets the
systems never trained on (400 + 631 excerpts), a direct retrieval test (234
queries, top-1 62 to 76 percent), grader cross-validation ("they agreed 95% of
the time"), and one deterministic restatement check. Notably it contains NO
MMLU-style general-capability regression suite: the battery is task-local,
held-out, and adversarially validated. That is a minimum viable battery by
construction, not by benchmark folklore.

### 2. FrogNano: Training a 4B Coding Agent via Online Task Synthesis (arxiv 2609.07925, HN 49627340, 2026-09-09)

Abstract (fetched via curl, `_abs_frognano.html`): post-trained exclusively via
RL on around 1,500 SWE environments with synthetic tasks; online task synthesis
"creates tasks calibrated to the frontier of learnability for the current
checkpoint"; "competitive small coding agents can be trained with synthetic tasks
alone, without traditional distillation from larger models". Direct RQ1 answer for
repo navigation at under 2k environments, and RQ3: the pipeline is task
generation plus RL, no frontier teacher in the loop.

### 3. EasyCommand: finetuned 1.5B Qwen for bash generation (dirac.run, HN 49966238, 2026-10-05)

Story text (Algolia items API): "Purely a hobby side project to see how far I can
push a really small model, using (mostly) automated training pipelines"; 401,975
unique request/bash pairs, generated by LLMs and admitted by reviewer agents with
execution checks; full dataset released. "Models and data are Apache-2.0;
application and benchmark code are MIT." Results: 1.5B Q4_K_M 212/300 on
ALFA-updated vs GPT-4o's published 73.0 on original ALFA; untuned
Qwen2.5-Coder-1.5B baseline 54.0.

Two RQ2 findings worth stealing verbatim: "Exporting also changed checkpoint
rankings, so evaluating the actual quantized file became part of selection rather
than an afterthought" (eval the GGUF you ship, not the fp16 you trained), and the
specialist checkpoint that scored 217/300 but lost 63 internal passes was
rejected for the balanced one. Also the honest caveat: "These tests informed
development, not an independent holdout."

### 4. Shrewd: distilling LLM labels into local classifiers (github.com/sshah03/shrewd, HN 49807276, 2026-09-22)

README read directly (`_shrewd_readme.md`). "Turn repeated LLM classification
calls into a small, fast, local model for one fixed task." MIT licensed. The
eval-battery idea is the cleanest in the window: a few hundred hand-labeled
examples become "a locked test set that scores the LLM and the local model side
by side", plus a routed fallback with a statistical bound: "Reading a confidence
threshold off the evaluation curve broke a 2% disagreement budget in 3 to 8 of 10
runs. A threshold set with a statistical bound on held-out rows stayed within
it." Findings: "Prompt optimization helped some teachers, but gains on the
development split often disappeared on held-out data" and "Better teacher labels
did not always improve the student."

### 5. Clef: open-weight decision models + RL fine-tuning platform (Cloudflare, HN 49923692, 638 pts, 2026-10-01)

Blog fetched (`_clef.html` via curl) and 30+ comments read. Clef = frozen
Qwen3.8-27B + rank-256 LoRA; Clef-flash = frozen Qwen3.5-9B; both Apache 2.0 on
HF, Jev-API compatible, non-autoregressive decision head. Tool-calling numbers:
BFCL case-exact Clef-flash 98.76 vs Jev 95.75; When2Call Jev still leads 80.97 vs
72.37. Thread consensus on cost-of-entry: "If you have a very narrow use case you
can train a BERT based decision model on a laptop an hour if you have good data
to train it on" (233mhz), and porridgeraisin: "now everyone simply finetunes
qwen and makes a compared-to-regular-LLM vastly cheaper decision model. And it
works for majority of usecases." Calibration is the open dispute (Jev best of a
bad lot). Apache 2.0 weights: internal use is permitted, full stop.

### 6. Cactus Needle 3 thread (HN 49748553, 236 pts, 2026-09-18)

Read end to end via items API. Author: "Needle 3 is trained on 360B tokens of
structured data and we spend way more time on the generation pipeline than on the
model"; 70M of its 121M params are n-gram (engram) tables. Community eval
skeptism is the RQ2 lesson: IanCal's failure cascade ("I need a wee" -> plays
music) against the "can match DeepSeek V4 Flash" headline; hirako2000: "tell me
the anti use case clearly so that I don't have to find out myself";
janalsncm: "the dataset was at least as important as the modeling itself". A
narrow exact-match benchmark at 86.0 did not survive contact with paraphrase.
Gero-4B's battery needs both: the narrow scorer AND the paraphrase/transfer probe
duane.sh ran.

### 7. Ask HN: When is fine-tuning a small LLM worth it? (HN 49807413, 2026-09-22)

11 top-level comments read. Practitioner priors split: minimaxir: "It's worth it
if a) you have a decent sample size of data for your problem and b) you have a
cost-effective infra to host it." speedgoose: "I think it's almost never worth it
now. An up to date LLM with a good few-shot prompt, or an agentic LLM will likely
outperform a small finetuned LLM, at a lower cost with more flexibility."
muzani's counterexample: categorization tasks where the label policy lives in
examples, not instructions, and style mimicry, are the cases where finetuning
still wins. Maps directly onto the estate: janitor-class models doing
fixed-schema work (Gero-4B calibrator = exactly muzani's case).

### 8. Raspberry Pi: Needle 14MB function-calling model (HN 49826663, 2026-09-24)

Article fetched via curl (`_needle.html`). "a 14MB function-calling model, turns
plain English into local actions on a Raspberry Pi 5, using the CPU alone";
out-of-scope inputs return an empty function_calls list; "Needle can also be
fine-tuned locally on a laptop for a particular set of tools"; both model and
runtime "released under Apache 2.0." No accuracy benchmark in the article; the
HN thread on Needle 3 (item 6) supplies the skepticism.

### Also read (RQ4 enforcement context, all in-window)

- arxiv 2609.35699 "Distillation Defenses Easily Break After Reinforcement
  Learning": "any distillation defense that leaks sufficient information to
  reconstruct approximate reasoning traces is likely ineffective"; RL after
  distillation lowers the attack bar; simple API-obtainable data suffices.
- arxiv 2608.09867 "Stealing Reasoning Traces from Proprietary LLM APIs":
  encrypted CoT blocks are interchangeable across sessions/users/models; jailbreak
  "circumvents anti-distillation mechanisms... across Anthropic, OpenAI, and
  Google"; 315,320 scraped blocks yielded 367 PII artifacts and 182 credentials.
- OpenAI "Disrupting a coordinated model-distillation campaign" (HN 49912105,
  09-30, dup stories 49918573/49949746) and CISA AA26-251A: enforcement is active,
  ToS-plus-technical, and aimed at competitors at scale.

## Answers to the four research questions

RQ1 (LoRA/QLoRA on small models, tool-calling + repo navigation, under 10k
examples): the window's honest answer is that under-10k works only for narrow,
fixed-schema tasks: FrogNano (4B coding agent, RL over ~1,500 synthetic SWE
environments), Shrewd (hundreds of hand labels to a local classifier), the Clef
thread's laptop-hour decision models, Needle (millions of params, one job).
Broad-capability finetunes in the window used far more: duane.sh 24k SFT (+12k
DPO + 25.6k graded contexts), EasyCommand 402k pairs, Needle 3 360B tokens.
Recipes converge on: frozen base + LoRA (rank 32 for 4B RAG work, rank 256 for
27B decision models), 1 GPU, hours not days, quantize-then-eval.

RQ2 (minimum viable no-regression battery, the Gero-4B blocker): three batteries
observed, in ascending cost. (a) Shrewd: locked hand-labeled test set, teacher
and student scored side by side, threshold set by statistical bound on held-out
rows, not by reading the eval curve. (b) duane.sh: blind position-debiased
LLM-as-judge + held-out excerpts + grader-vs-judge agreement (95%) + one
deterministic restatement check + direct behavioral probe; no MMLU anywhere.
(c) EasyCommand: narrow benchmark + internal execution suite + evaluate the
shipped quantized file + reject specialist checkpoints that lose internal passes.
None of the three runs a public general-capability suite; the window's minimum
viable battery is task-local held-out probes with an adversarially validated
grader, plus a transfer probe to catch the ALFA-style "learned the answers, not
the skill" failure ("A 0.6B model improved from 8/72 to 64/72 on time-related
training requests. On separate time-transfer requests, it stayed at 1/18.").

RQ3 (zero-cost synthetic pipelines): three reproducible shapes. (a) FrogNano:
online task synthesis calibrated to the learnability frontier, no teacher model.
(b) OPSD (arxiv 2609.30652, abstract already held in state/arxiv): "a second
frozen copy of the student model, now given the ground truth in its context,
serves as the teacher", zero external API calls. (c) EasyCommand: generator LLMs
+ reviewer agents + execution checks, dataset released Apache-2.0. Cactus's
"data was honestly most of the work" is the thread consensus. The free-lane
doctrine fits (a) and (b) exactly; (c) fits if the generator lanes are free
(gemma janitors + free-tier sensing per the driving ladder).

RQ4 (licensing of distilling frontier reasoning traces): the window's signal is
enforcement-side, not license-text-side. I did not fetch any provider ToS pages,
so no ToS claim is made here. What the window shows: labs actively disrupt
distillation campaigns (OpenAI/Kimi, CISA advisory), two 2026 papers show
technical defenses are weak against RL-after-distillation and that API-obtained
data alone already buys reasoning gains. The clean paths the window endorses:
Apache-2.0 weights with permissive data (EasyCommand, Clef, Needle), and
teacher-free distillation (OPSD) where nothing was taken from anyone. Any
frontier-trace diet for Gero-4B should route through the funded-lane API terms
review, an operator call, not a sweep assertion.

## Overlap ledger (grep evidence)

- catalog/catalog.jsonl + memory/ grepped case-sensitively for 14 distinctive
  terms. NO_HITS: FrogNano, EasyCommand, Cactus Needle, dirac.run, duane.sh,
  Shrewd, Stealing Reasoning Traces, Qwen3.5-4B, learnability frontier, When is
  fine-tuning a small LLM, on-policy distillation (lowercase check clean).
- ALREADY HELD (abstract-only, state/arxiv daily ingest; excluded from the 8):
  2610.02140 (`state/arxiv/2026-10-02/2610.02140v1.txt`), 2609.35699
  (`state/arxiv/2026-09-29/2609.35699v1.txt`), 2609.30652
  (`state/arxiv/2026-09-28/2609.30652v1.txt`). The HN placement adds no
  substantive signal (2 pts, 0 comments each).
- False-positive note: a case-insensitive GEPA grep matches UsagePage /
  Messagepath / messageParts substrings; the only real GEPA catalog row is
  AdaGEPA (arxiv 2609.39927), adjacent, not a duplicate.

## Not done / OWED

- Provider ToS text for RQ4: not fetched, not asserted.
- EasyCommand LoRA hyperparameters (rank/lr): the post links training notes but
  does not include them; OWED if the estate adopts the recipe.
- FrogNano full text: only the abstract was read (curl); the 1,500-environment
  count and claims are the authors'.
- academy.dair.ai FrogNano write-up page timed out twice (WebFetch); arxiv abs
  used instead.
- Pass-1 stdout log (277 rows) lives in this session's exec log; the abridged
  candidate list above is the durable record.
