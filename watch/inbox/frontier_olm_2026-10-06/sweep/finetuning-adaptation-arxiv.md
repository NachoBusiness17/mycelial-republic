# sweep: finetuning-adaptation via arxiv (frontier_olm_2026-10-06)

source-fetched: 2026-10-06. Gopher lane: sweep-finetuning-adaptation-arxiv. This sitting had
two jobs: (1) the OWED confirmation pass over the 28 finetuning-adaptation sweep items
enumerable in frontier_olm_2026-10-05/sweep/*.md (finetuning-adaptation-arxiv.md 8 banked,
-hn.md 8, -reddit.md 6, -x.md 6; zero confirmed register rows per
watch/inbox/frontier_olm_2026-10-06/lens/burns.md:96-99), and (2) a fresh 30-day arXiv sweep
with its own two passes. Estate target: the skills pack monoculture
(mag/skills_pack.py + mag/skill_ledger.py) and the memlance leg of the descent protocol
(memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md leg 7).

## Doors used

arXiv Atom API via export.arxiv.org (4 calls: one 9-id confirmation batch, three
search queries sorted by submittedDate descending). arxiv.org /html/ full texts
(7 fetches, all HTTP 200). HN Algolia items API (10 calls). fxtwitter API (6 calls).
Reddit thread RSS with browser UA (11 attempts: 2 succeeded; 5 hit HTTP 429 at 8 s
pacing and again at 50 s pacing) with Arctic Shift as the working substitute
(1 call, 4 posts returned). duane.sh, raspberrypi.com, raw.githubusercontent.com,
huggingface.co API (5 calls). Total candidates considered in pass 1: 90 unique arXiv
ids across the three queries (dedup by id, list in raw/sweep_q*.xml), of which about
55 fall inside the 2026-09-06..2026-10-06 window; plus the 28 confirmation targets.

Door degradation, honestly: reddit RSS 429s at any pacing under a minute from this host
today (the 10-06 lens already recorded the JSON doors dead; RSS is now flaky too, Arctic
Shift carried the confirmation pass: raw/conf_arcticshift.json). The fxtwitter ARTICLE
door degraded again for article 2097606900745457664 (title and preview_text resolve, the
content field came back empty, 2 chars), so the zafstojano body could not be re-verified
today; the 10-05 full-body read stands as their fetch, mine is pointer-level only. No 403s
elsewhere; no fabricated fallback success.

## Part 1: the OWED confirmation pass (28 items, verdict per item)

Method: every primary URL re-fetched this sitting (raw bytes banked under
raw/conf_*.{xml,json,html,md}); each banked quote grepped verbatim against the fresh
bytes; claims checked at the level the fetched bytes support. Instruments: curl +
repo venv python (re/html/json extraction), grep counts reported below.

CONFIRMED, 26 of 28 (quote verbatim on the fresh fetch, headline claims hold):

arXiv lane (8/8):
1. 2609.17848 SFT or RL for Tool-Calling Agents. Abstract carries "SFT with LoRA is the
   strongest in-distribution method throughout the 0.6B-32B range and best in 15 out of 18
   experimental settings" and the full text (raw/conf_2609.17848_full.html, 134,806 B,
   HTTP 200) carries all three 4B numbers verbatim: "88.0% versus 80.4%", "30.4% versus
   22.8%", "47.6% versus 44.1%". Hyperparameter line items (r=32, lr 1e-4) sit in tables my
   text extraction did not isolate; the headline recipe claim is confirmed at two levels.
2. 2610.02142 Keyword Harnesses Fail Open. Abstract carries "costs minutes of CPU time" and
   the 0.660-vs-0.650 pair and 0/6-vs-6/6 verbatim-reproduction numbers.
3. 2609.10750 When Synthetic Data Hurts. Abstract carries "improves in-distribution
   retrieval but it causes catastrophic forgetting" verbatim; 34,396 skills confirmed.
4. 2609.23916 Time-Incremental CPT. Abstract carries "What does it cost? Almost nothing" and
   "stays within 0.01 of the base for every model" verbatim.
5. 2609.24115 EDGEGEN. Abstract carries "fully automated closed-loop system that requires no
   human annotation" verbatim.
6. 2609.35259 On-Policy or Off-Policy. Abstract carries "challenge the view that on-policy
   rollouts are inherently preferable" verbatim.
7. 2609.19513 QVAC Genesis III. Abstract carries "+28.57" ARC-E figure; now at v2; license
   still unstated on the abstract page (the OWED stands).
8. 2502.06659 Who Taught You That. Abstract carries the ToS sentence verbatim; v3.

HN lane (6/8 clean, 2 caveats):
9. FrogNano 2609.07925 (now v4). Abstract carries "around 1,500 SWE environments", "creates
   tasks calibrated to the frontier of learnability for the current checkpoint", and
   "trained with synthetic tasks alone, without traditional distillation from larger
   models" verbatim. HN story 49627340 live via Algolia.
10. Shrewd (HN 49807276). Fresh fetch of the README
    (raw/conf_shrewd_readme.md, 41,004 B, byte-identical size to the 10-05 bank) carries
    "locked test set" (4 occurrences), "statistical bound on held-out rows", and the
    "Reading a confidence threshold off the evaluation curve broke a 2% disagreement
    budget" passage verbatim.
11. Clef (HN 49923692). Thread live (118,456 B JSON); the 233mhz laptop-hour comment and the
    "everyone simply finetunes qwen" comment confirmed verbatim in the fresh tree; the BFCL
    98.76 figure re-verified against the 10-05 fetched blog bytes
    (frontier_olm_2026-10-05/sweep/_clef.html: 1 hit) since the live thread JSON does not
    carry it.
12. Cactus Needle 3 (HN 49748553). "360B tokens" and "generation pipeline" confirmed in the
    fresh thread JSON.
13. Ask HN worth-it (HN 49807413). Both banked comments confirmed verbatim ("almost never
    worth it now", "sample size of data").
14. RPi Needle (HN 49826663). Article live (HTTP 200, 133,686 B, correct slug
    /turn-text-input-into-actions-with-needle-a-14mb-function-calling-llm/); "14MB
    function-calling model", "using the CPU alone", "fine-tuned locally on a laptop",
    "Apache 2.0", "function_calls" all confirmed in the fresh fetch.
15. CAVEAT, duane.sh (HN 49897103). Blog live (HTTP 200, 82,356 B). Confirmed verbatim:
    "fewer mistakes than Gemini" + "71% less cost", "1.6 hours", "every position equally
    often", "95% of the time". The "rank 32" phrase did not match my extraction (likely
    rendered as rank-32/rank=32 in a table); the claim's substance (LoRA on Qwen3.5-4B,
    24k examples, blind position-debiased judge battery) is confirmed. Confirmed with a
    wording caveat.
16. CAVEAT, EasyCommand (HN 49966238). Post text confirmed ("Purely a hobby side project"
    verbatim in the author's fresh comment). The exact license sentence from the 10-05 bank
    ("Models and data are Apache-2.0; application and benchmark code are MIT") is NOT in
    today's item JSON (the comment text differs from what the 10-05 seat read). The
    load-bearing half is confirmed at the artifact level: HF API returns
    license:apache-2.0 for all four dirac-run model repos AND the ec-training-data dataset
    (raw/conf_ec_data.json). The MIT-application-code half is OWED (their non-HF code page
    not located this sitting). Confirmed with an owed half.

Reddit lane (6/6, door-assisted):
17. unswallow (r/ollama 1wc6tka). Arctic Shift post body confirms the whole failure class
    verbatim: call "sitting inside the reasoning block, wrapped in <think> tags", "never
    made it out into the tool_calls field", "perfectly valid 200", reported separately
    against vLLM/SGLang/llama.cpp, rebuild-from-reasoning library. Repo link live.
18. CodeFinetuner (r/LocalLLaMA 1wdp9qc). Post body confirms the pipeline (tree-sitter
    Structure-Aware FIM, CodeBLEU/edit-sim/exact-match/perplexity, GGUF) and the honest
    boundary verbatim: "the real usefulness still has to be verified in the editor
    itself". The "3B sweet spot" quote is comment-level on the 10-05 reading, not in the
    post body; carried, not re-verified.
19. FunctionGemma (r/LocalLLaMA 1r6gx75, out-of-window flagged). Post body carries 90.9,
    96.7, and the 120B teacher verbatim. Title confirms 10-39% to multi-turn numbers.
20. Rust+Vulkan PEFT (r/LocalLLaMA 1wu6cbl). Full RSS fetch (HTTP 200): 2e-7 parity target,
    1.19e-7 worst observed, modules_to_save, merge/unmerge, ROG/Ally/Z1 hardware, FP32-only
    all confirmed verbatim in the fresh fetch.
21. Spanda (r/ollama 1wdasar). Full RSS fetch: "Shannon entropy", T=0.7, AUROC 0.89 and
    0.09 confirmed; "semantic entropy" as a phrase not in the render (the 10-05 reading
    had it as semantic-entropy NLI context).
22. hemmingway-1 (r/LocalLLM 1wlhh08). Arctic Shift post body carries the eq-bench 1330
    claim and the fable-5 comparison verbatim.

X lane (5/6 clean, 1 partial):
23. omarsar0 2097958286146605446. All three quotes verbatim in the fresh fxtwitter JSON:
    "Performance dropped on all seven tasks", "adopts the expert's planning strategy
    without the competence to execute it", "The same fine-tuning helps under the unevolved
    harness".
24. ArtificialAnlys 2098148674203488422. "License: MIT", "552B parameters", "~4x less per
    token" all verbatim. The V4.1-Flash-is-MIT datum for RQ4 stands re-confirmed.
25. Sumanth_077 2098053941800100294. "34 of 64 harness changes" and "2 of 9 final harness
    versions" verbatim.
26. shikibmehri 2098233059242099175. Both data-factory quotes verbatim.
27. ValsAI 2098125177116848591. "384 max output tokens" and "temperature 1" verbatim.
28. PARTIAL, zafstojano 2097689256961466486. Pointer, author, title ("Recursive Synthetic
    Improvement") and preview_text resolve fresh; the article content field is empty from
    fxtwitter today (door degraded for article bodies again, exactly the risk the 10-05
    seat flagged). The 10-05 full-body read is not re-verified; the two laws banked from it
    (accumulate-don't-replace; "One does not simply 'distill' RL environments") stay
    carried-at-source-strength, not confirmation-seat strength.

Verdict for the register: 28 items re-fetched, zero contradicted, 26 confirmed (24 clean +
2 with stated caveats), 1 partial (X2, door-degraded body), 1 clean-with-owed-half (H3
EasyCommand MIT code half). All 28 survive to confirmed rows under the 10-05 fold's
register schema, with the two caveats and one owed half carried on their rows. Raw receipts:
raw/conf_arxiv_batch.xml, conf_2609.17848_full.html, conf_hn_*.json (x9),
conf_reddit_*.xml (x2), conf_arcticshift.json, conf_fx_*.json (x6), conf_duanesh.html,
conf_needle_rpi.html, conf_shrewd_readme.md, conf_ec_data.json.

## Part 2: fresh sweep, pass 1 (90 candidates)

Three queries (raw/sweep_q1_lora_agents.xml, sweep_q2_forget_distill.xml,
sweep_q3_peft.xml; all HTTP 200, 72-78 KB each), sorted by submittedDate, deduped by id:
90 unique items, about 55 in-window (2026-09-27..10-05 cohort; the window floor of 30
candidates is met by the in-window set alone). Notable pass-1-only candidates not
deep-read: 2610.06243 RoSA rotational sparse adaptation; 2610.05748 MOLT GPU memory
sharing with opportunistic fine-tuning; 2610.00685 backdoor purification for LoRA-tuned
LLMs via null-space projection; 2610.04269 self-reflection fine-tuning against prompt
injection; 2610.04740 locally deployable agentic co-scientist on small models. Name
collision noted: arXiv 2610.05748 "MOLT" is unrelated to the HN "Molt" QLoRA-laptop thread
from the 10-05 HN sweep (different artifact, do not merge).

## Part 2: fresh sweep, pass 2 (6 deep reads, all full-text HTML fetched and read)

### 1. Offline Guidance, Online Reasoning: Reusing LLM Feedback for Small Language Models (2609.39346, 2026-09-30)

Full text read (raw/deep_2609.39346.html, 469,486 B). Reusable Latent Correction (RLC):
a black-box LLM is called OFFLINE once; its natural-language guidance on a failed SLM
trajectory is converted into a persistent corrective experience in the SLM's hidden
space, stored in an external bank, and retrieved at inference by the SLM's current
reasoning state. The SLM's parameters never change and no LLM is called online. Numbers:
"RLC improves the average performance of a 7B SLM by 7.97 percentage points, bringing it
on par with a 32B SLM. It also improves the performance of a 14B SLM by 5.93 percentage
points, achieving results comparable to those of 72B LLMs on several tasks." Bank built
from GSM8K+MATH training sets, 14,973 problems. Code released
(github.com/ZBH031/reusable-latent-correction). Estate map: this is the missing organ
between the memlance (same-render bend, proven below) and skill_ledger (case-law rows
folded as prose): a correction bank keyed by reasoning state, retrieved per turn, zero
weight changes, exactly the decision-rung shape (frozen base + retrieval). It is the
strongest confirmed-external answer to the prompt-monoculture gap in the estate map.

### 2. How To Train Your World Model: Fine-tuning vs RAG for LM-based World Modeling (2610.02542, 2026-10-01)

Full text read (raw/deep_2610.02542.html, 374,269 B). Five environments (embodied, web
navigation, social), systematic FT-vs-RAG comparison: fine-tuned world models win 15/20
reward settings, BUT the paper states plainly "there are often cases where simple
prompting baselines match or outperform finetuning", and "RAG-based approaches prove more
data-efficient, while fine-tuning approaches disproportionately benefit from scaling the
amount of experience collected". Their hybrid (parametric core dynamics + retrieval from
an actively maintained memory store) beats both. Estate map: this is the direct RQ2 shape
(prompt route vs weight route) with the field's own verdict: at modest data scales the
prompt route frequently ties, FT wins when experience scales, and the best system is a
hybrid of both, which is literally skills_pack (prompt) + skill_ledger (learned
corrections). The paper's counterfactual-intervention error-rate estimator for the
retrieval stage is a bonus instrument for any correction-bank retrieval audit.

### 3. No Model Required: Text Entropy Rate Filtering Mitigates Iterative Fine-Tuning Collapse (2610.01493, 2026-10-01)

Full text read (raw/deep_2610.01493.html, 267,633 B). The Kontoyiannis entropy-rate
estimator computed from raw text via match-length statistics, "with no model of any kind":
a $0, deterministic, stdlib-implementable filter. In a six-generation QLoRA collapse
experiment on Llama-3.1-8B, logprob-based filtering (the established baseline) gave no
significant text-diversity benefit on any metric (p > 0.23) while h_k-filtering gave +42%
unique trigrams, +30% vocabulary, -19% repetition (all p < 0.001); validated as entropy
proxy (beta 0.924) and collapse detector (rho +0.454) across 4 domains and 1,520
documents. Estate map: the free-lane synthetic-data doctrine (janitor-generated,
executor-verified trajectories) gains its quality gate: filter the graft corpus by
entropy rate before it enters any finetune or prompt pack, no GPU and no model call
required. Directly implements the descent protocol's falsifier discipline for synthetic
corpora.

### 4. A Fine-Grained Analysis of the LoRA Fine-Tuning Landscape with Implications for Data Selection (2610.06542, 2026-10-05)

Full text read (raw/deep_2610.06542.html, 1,089,547 B). LoRA-RIP: a data-dependent
restricted-isometry metric for the cross-entropy objective along LoRA-relevant low-rank
directions. Central claim: "the appropriate adapter rank should depend on the quality of
the data-induced optimization geometry, rather than on the model alone"; sufficient
over-parameterization at the LoRA-RIP-determined rank eliminates spurious local minima,
and the metric enables principled data selection under a fixed rank budget; "rank and
data quality are two coupled resources that should be jointly considered". Estate map:
when the QLoRA-on-case-law run ever fires, rank selection comes from the corpus geometry
(the 4,559 decision rows' conditioning), not from a rank-16-vs-32 folklore table; and the
same metric doubles as a corpus-quality score for the prompt-pack arm.

### 5. ASCENT: Online Test-Time Training of Long-Horizon Agents via Self-Distillation of Verified Experience (2610.05303, 2026-10-04)

Full text read (raw/deep_2610.05303.html, 643,293 B). Online Agentic Test-Time Training:
the agent's own verifier-accepted trajectory becomes privileged information fed to a
frozen initial copy of the same model, whose next-token predictions along that trajectory
are distilled into persistent LoRA fast weights; "without an external reference solution
or stronger teacher"; invalid-action turns removed before distillation; improves success
on ALFWorld, WebShop, AppWorld as experience accumulates and transfers to held-out
scenes. Estate map: this is the training-side twin of the estate's replay-mix doctrine
(executor-verified trajectories as the only learning signal), and it needs no teacher
budget, which fits the free-lane sensing doctrine; the LoRA fast-weights update is the
organ the estate's autonomous lanes currently lack.

### 6. Efficient Task Adaptation in Large Language Models: A Survey of Weight-Based, Prompt-Based, and Embedding-Based Adaptations (2610.00928, 2026-10-01)

Full text read (raw/deep_2610.00928.html, 565,499 B). Unified taxonomy: task information
encoded in weights (PEFT), in prompts (in-context learning, prompt optimization), or as
injected task embeddings; includes knowledge editing and soft prompts. The survey's own
honest center: these paradigms have "largely evolved within individual paradigms, leaving
their cross-paradigm relationships and trade-offs underexplored". Estate map: the RQ2
question (prompt pack vs weight finetune at equal token budget) is an open cross-paradigm
question the field has not standardized; the estate's bake-off would not be re-running a
known result. Also supplies the vocabulary for the hybrid design (2610.02542 above).

## Overlap gate (run before banking)

Command pattern: `rg -i --max-filesize 8M "<term>" catalog/catalog.jsonl` and the same
over memory/ (14 terms, this sitting). Results: 2610.00928 and 2610.02542 = ZERO hits in
both (genuinely new). 2610.01493, 2610.06542, 2609.39346 = one catalog row each, all
state/arxiv daily abstract snapshots (2026-10-02, 2026-10-06, 2026-10-01 ingests,
1,574-2,026 B); the deep reads here are the first full-text consumption. 2610.05303 =
zero id hits; the 5 "ASCENT" catalog hits are a different paper (Ascent: agentic system
over MCP, clinical data) plus estate campaign logs, acronym collision only. "Kontoyiannis"
= zero everywhere. None of the six duplicates the 10-05 bank or any register row.

## RQ answers (the four research questions)

RQ-confirmation: 26/28 survive clean-or-caveated (detail in Part 1); register-ready.

RQ-prompt-vs-QLoRA: the equal-token-budget bake-off was NOT run this sitting and must not
be claimed. What this sitting established: (a) the field's closest evidence (2610.02542,
deep-read) says prompting frequently ties finetuning at modest data scales and FT wins
when experience scales, with a hybrid winning overall; (b) the estate-side corpus is not
300 rows: mag/skill_ledger.py's ledger at memory/improve/skill_ledger.jsonl counts 4,559
skill_ledger.decision.v1 rows plus 4,896 skill_fired.v1 receipts (measured this sitting
by schema count; the ask's "300 case-law rows" figure is stale against the disk bytes);
(c) VRAM: this host's GPU is an AMD Radeon RX 5600 XT with 6,425,673,728 bytes (5.98 GiB)
measured from the registry HardwareInformation.qwMemorySize (key 0000, this sitting);
(d) the GPU-ladder workload gate (L30, laws.md:57: arch, VRAM, price trigger, software,
workload must ALL hold) FAILS on arch and software regardless of VRAM arithmetic: RDNA1
(Navi 10) has no ROCm support on any OS and no CUDA, so the bitsandbytes/QLoRA stack
cannot run here; the Rust+Vulkan lane (confirmed R4) is FP32-only today. Verdict: the
QLoRA arm routes to a rented GPU (the confirmed duane.sh recipe: 4B LoRA for ~$7/1.6 h on
one rented card) or waits for the operator-gated ladder; the prompt-pack arm is runnable
here today at $0 (ollama gemma:2b live, verified via /api/tags this sitting). The bake-off
harness (held-out scut battery + token-budget accounting + base-vs-tuned differential per
the confirmed battery fragments) is specifiable now but was not built in this window.

RQ-methods-for-the-rungs: post-confirmation, the methods that apply at the decision-model
rung and 2b janitor class: RLC correction bank (frozen weights, retrieval per turn - the
decision-rung shape); the h_k entropy filter (any synthetic graft, $0); LoRA-RIP rank law
(any adapter graft, including Clef-class frozen+LoRA); the confirmed battery fragments
(2610.02142 CPU-minute ladder, 2609.23916 13-task macro-average, 2609.10750 triangle with
EWC/LwF/embedding-anchor); EDGEGEN spec-driven edge cases; 2609.17848's LoRA-beats-full-FT
across 0.6B-32B. Corpus note (corpus.md:27,33,41): the 162 nonredistributable reference
PDFs stay reference-only; all six confirmed method papers above have public arXiv pages,
so corpus/papers (2 ledger rows today) can grow with redistributable abstract+link rows
without touching the nonredistributable shelf. The decision-model wave itself (144M-27B,
/v1/systemone) remains sweep-level per burns.md:92-95: NOT confirmed this sitting; my H5
confirmation covers the Clef thread's own text, not the wave's rows 1-2.

RQ-memlance falsifier: DESIGNED AND RUN. Instrument: paired render A/B on the local
janitor - arm A (unlanced) and arm B (lanced with ONE seed line planted among context
lines, never addressed as an instruction, per .agents/skills/memlance/SKILL.md), gemma:2b
via ollama, temperature 0, fixed seed, determinism control (arm A run twice, byte-identical
or the measurement voids). 5 tasks, hit = B names the seed's token, A does not, outputs
differ. Result: determinism control PASSED; hits 5/5 (each unlanced arm declined to
answer, each lanced arm answered with the seeded content: rates.yaml, 8126, ledger team,
bees, gemma2:2b-instruct). Script and result banked:
raw/memlance_falsifier.py, raw/memlance_falsifier_result.json. Verdict: descent protocol
leg 7 is NOT prompt theater at the janitor class - a fired memlance measurably changes the
next output, 5/5 against the skill's own 2/5 bar. Scope, honest: this proves the
same-render mechanism on gemma:2b; it does not prove cross-session mesh hits or
premium-seat legs, and it uses planted fact seeds, not the skill's adversarial
poisoning test (the skill's ban arm ran zero lances against harmed targets; untested).

## Not done / OWED

- The QLoRA-vs-prompt bake-off itself: not run (no CUDA host; harness not built).
- EasyCommand's MIT-application-code half: not located; OWED.
- zafstojano article body: door-degraded today (content field empty); the 10-05 read
  stands unverified-by-me.
- Decision-model wave rows 1-2 (llama.cpp blog, Ollama blog): not re-fetched; the wave's
  confirmation remains owed to whoever runs it.
- The corpus graft: no paper was copied into corpus/papers this sitting (would need the
  librarian lane; named as the follow-up).
