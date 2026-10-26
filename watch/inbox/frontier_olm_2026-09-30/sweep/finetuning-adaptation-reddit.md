# Sweep: finetuning-adaptation via reddit - 2026-09-30

source-fetched: 2026-09-30. Area: finetuning-adaptation. Fetch instrument: the ask's recipe
door (WebFetch on old.reddit.com `top.json`) is DEGRADED on this seat: every old.reddit.com
path (json endpoint, HTML listing via WebFetch, individual comment pages, .rss) returns the
"Welcome to Reddit" shell or a login wall; www.reddit.com threads hit a bot-verification wall;
r/MachineLearning and r/ollama listings are login-walled / network-blocked ("whoa there,
pardner"). Working doors found and used:

1. `mcp__web_reader__webReader` on plain old.reddit.com listing pages
   (`/r/LocalLLaMA/top/?t=month`, `/r/LocalLLM/top/?t=month`) - returned full month-top
   listings (25 posts each). Pagination and search paths on old.reddit are login-walled.
2. `api.pullpush.io` archive API with a descriptive User-Agent (helper:
   `watch/inbox/frontier_olm_2026-09-30/sweep/_pullpush_fetch.py`) - `/submission/?ids=` and
   `/comment/?link_id=` returned full selftexts, exact `created_utc`, scores, and 40 top
   comments per thread. Its `/search/` endpoint is agent-blocked (HTTP 429, "does not provide
   free scraping resources for agents").
3. WebSearch `site:reddit.com` fallback per the recipe (used to locate candidate thread IDs).

## Pass 1: candidates considered (50 from the last 30 days)

r/LocalLLaMA top/month (25, ages relative to 2026-09-30): "Qwen3.6-35B-A3B is a massive local
release" (27d), "One local model to rule them all, you say?" (25d), "I'm done with using local
LLMs for coding. Everyone is chasing benchmarks" (19d), "Gemma 4 Compile x C4.6" (2d),
"New open weights just dropped: Kong AI" (1d), "Gemini 3 Pro is remarkable" (9d), "FLUX.2
[klein] is open sourced!" (1d), "GLM-5 is here!" (7d), "GPT 5.2 - Price cuts across the board,
74% less expensive" (10d), "It's over for Qwen" (4d), "Why are all 'open source' models
becoming AI generated clickbait" (3d), "PSA: If you need to install PyTorch Nightly..." (2d),
"Llama 4.5 Behemoth weights just released" (4d), "M3 Max 128GB unified memory review" (22d),
"Local models peaked for me on voice" (4d), "Wan 2.6 - a new era of local video generation"
(1d), "Qwen3.6-Coder is out!" (5d), "Any new model for image editing?" (12d), "The amount of
people local models pissed off..." (15d), "If NVIDIA's nemotron nano 12b v2 VL..." (23d),
"Qwen3.6-Preview is out!" (6d), "RAM manufacturers have been inflating DRAM prices..." (26d),
"What open-source model of the last 2 years truly changed everything for you?" (15d),
"Parakeet v3 released - local transcription" (17d), "RTX Super - 24GB or bust" (20d).

r/LocalLLM top/month (25, ages relative to 2026-09-30): "GLM-5 has landed!" (1d), "Mistral
releases Ministral 8B" (4d), "Building a coding agent that uses entirely free local models"
(11d), "GPT-OSS 20b is fantastic" (17d), "I built a coding agent that gets 87% on benchmarks
with a 4B parameter model, here's how" (25d), "12 Years of failed AI predictions, yet local
AI keeps winning" (8d), "GPT-OSS 120b: You don't need the cloud" (1d), "Self-hosting is my
permission slip" (2d), "I made a mini OpenAI-like app platform for my Pi" (13d), "Qwen3.6
live now" (6d), "My humble 2025 local AI setup" (14d), "I trained a language model from
scratch and got it running on an ESP32" (25d), "Local image editing workflows 2026" (3d),
"Gemma4 E2B/E4B: 89% compression" (9d), "GLM-5: local AI's biggest leap yet" (7d), "Model
Showdown: 2026 State of Open LLMs" (16d), "Local AI stack for privacy-first journaling"
(13d), "Tutorials for the Qwen3.6 family?" (5d), "Small models, big personality" (18d),
"Qwen3.6-27B on RTX 3090: tested 12 GGUF quants across HumanEval+/MBPP+" (21d), "I trained a
75M parameter LLM from scratch on 18B tokens" (12d), "MoE models make my Pi 5 useful" (24d),
"Local LLMs are saving my writing life" (10d), "NPU vs GPU for local LLM" (23d), "Best
open-source Whisper alternatives" (19d).

Verdict from pass 1: the current month-top of both subreddits is dominated by model releases,
memes, and hardware; ZERO finetuning/QLoRA recipe threads with retention measurements sit in
the 30-day top. The recipe canon lives in older evergreen threads (found via the WebSearch
fallback and read via the archive door). That absence is itself the Q1 finding.

## Pass 2: deep reads (6 threads, read end to end: selftext + top comments via pullpush)

1. **1rsqzua, 2026-03-13, 148 pts / 45 comments** - "I fine-tuned a 14B model that
   outperforms Claude Opus 4.6 on Ada code generation." QLoRA 4-bit via Unsloth + TRL
   SFTTrainer, rank 32 alpha 64 on q/k/v/o/gate/up/down, 1 epoch lr 2e-5 constant schedule,
   ~49 min/round on a rented H100, over a compiler-verified dataset of 3,430 Ada/SPARK pairs
   ("Every single training example passes `gnatmake -gnat2022 -gnatwa`"). Retention was
   MEASURED against a custom 1,000-prompt first-attempt-clean-compile benchmark (68.6% vs
   Claude Opus 4.6 42.1%) plus MultiPL-E HumanEval-Ada pass@1 (47.1% vs base 34.4%), not
   loss curves. The OP's own failure mode is the single most transferable line:
   "Full retrain from base each round on accumulated dataset (adapter continuation caused
   catastrophic forgetting at R2)" - they discarded round 2 and retrained from base. The
   v0.2 update in-thread rebuilt the eval with strict GNAT flags (72.0% vs Gemini 3.1 Pro
   56.6%, Opus 4.6 49.8%, GPT-5.4 46.0%, Grok 4 37.0%) and admitted "The old eval had
   issues: weaker flags, truncation bugs" (source wording had a dash; elided here for the
   seat dash law). Top comment (133 pts) on why this reads as real: "you have an actual
   ground-truth verifier. The compiler doesn't care about vibes."
2. **1nturn1, 2025-09-29, 975 pts / 96 comments** - "Full fine-tuning is not needed anymore."
   Thinking Machines "LoRA Without Regrets" blog: "Apply LoRA across every layer, not only
   attention [...] Train with a learning rate about 10x higher than what's used for full
   fine-tuning." Rank=1 sufficed for RL post-training; ~2/3 the compute. Comments calibrate
   it: danielhanchen (Unsloth, 142 pts) "You could always actually add knowledge to existing
   models with LoRA!"; the top counter (120 pts): the result is "LoRA is equivalent to FFT in
   some more cases than was previously common knowledge", FFT still needed for QAT and
   extensive instruction tuning; and the capacity bound (52 pts): "There is a limit to how
   much knowledge LoRa can hold before it degrades the original model.
   https://arxiv.org/abs/2502.14502v1" plus the dataset-quality rebuttal: "a lot of the
   'can't add new information with lora' assumptions comes down to poor datasets."
3. **1ln5l6b, 2025-06-29, 9 pts / 20 comments** - "Training Open models on my data for
   replacing RAG." The corpus-grade question in the wild: top answer (19 pts) notes "there
   are so very few documented cases of it working well for *knowledge*" once you exclude
   overfit models that broke everything else; brown2green: "It *is* possible to finetune a
   model so that it _memorizes_ the knowledge almost perfectly, without degrading too much its
   base capabilities, but memorization alone doesn't imply that it will be able to properly
   use that knowledge elsewhere," and layer choice matters ("avoiding to finetune layers where
   most of the base knowledge is stored helps to prevent capability degradation"). indicava's
   when-it-works recipe: months of data curation, a custom evaluation benchmark, a few
   thousand dollars of compute, iterative runs. Chaosdrifer's division of labor: "you
   finetune for format, RAG for context."
4. **1ndjxdt, 2025-09-10, 376 pts / 377 comments** - "AMA with the Unsloth team."
   danielhanchen: "people say it doesn't add knowledge or context in the model which is
   absolutely not true! That's actually the whole purpose of fine-tuning!" Practical
   janitor-class item: Unsloth 4-bit Dynamic quants "largely restore QLoRA fine-tuning &
   model accuracy by just selectively quantizing layers" (1-bit on unimportant layers, 6-8
   bit on important ones). Triage advice: start with RAG or the raw model, fine-tune only
   when those fail.
5. **1pvdwca, 2025-12-25, 17 pts / 13 comments** - "Should I be switching to DoRA instead of
   LoRA?" Domain CPT at ~200M medical tokens, GPU-poor. Claims in-thread: DoRA "decomposes
   weight updates into magnitude and direction... far more robust at lower ranks (e.g., r=8)"
   but 1.5-2x slower; counterpoint: "When I messed with DoRA on small 0.5B Danube3 model I
   didn't get any uplift," with alternatives GaLore, RSLoRA+LoRA+, or QLoRA on a bigger
   model. The forgetting tradeoff is named: LoRA "learns less but forgets less."
6. **1ram8tt, 2026-02-21, 13 comments** - "Is there a place where I can donate all my
   Claude/Codex/Gemini/OpenCode CLI chat history as training dataset?" Session-derived corpus
   norms: sanitize ("make sure there is no sensitive or private conversation... well
   'sanitized'"), HF datasets as the venue, and the volume gate: "Potentially not enough data
   for a PEFT." One commenter proposes exactly the estate's organ: "incrementally collects
   chat history on my machine, redacts sensitive information, and uploads to HuggingFace."

## Answers to the research questions (grounded)

- **Q1 (QLoRA/LoRA recipes since 09-28 with measured retention):** none found in the 30-day
  window on either subreddit's top/month; the strongest recipe evidence is 1rsqzua
  (2026-03-13): verifier-gated corpus, full retrain from base each round, 1 epoch lr 2e-5,
  retention measured as compile-rate on a fixed prompt set vs frontier baselines. Supporting
  recipe constants from 1nturn1: every-layer LoRA, lr ~10x FFT, rank-1 suffices for RL. The
  recipe class to steal for the 11,870-row seat_pool corpus (count per the ask, corpus.md:12;
  corpus.md itself is NOT in this repo, repo-wide findstr returned no hits): per-row
  machine-verifiable gates before training, adapter-continuation banned (fresh base each
  round), and a fixed held-out verdict set as the retention instrument.
- **Q2 (corpus-grade vs echo-inflated):** the estate's own bar already matches the surviving
  community practice: `.agents/skills/code-agent-data/SKILL.md:26-36` requires >=600 bytes AND
  a Result-class section, and names VAPOR as "mood summaries, 'made progress', plans without
  outcomes, unlabeled claims, self-praise". 1ln5l6b is the same filter from the other side:
  memorization without usability is the echo trap; SomeOddCodeGuy's "so very few documented
  cases" is the echo-inflation alarm at community scale. Content-read audit (verifier or
  contrast per row), not raw_count, is what separates the two; one estate corpus self-marking
  raw_count as inflated echo is per the ask, laws.md:50 (laws.md also absent from this repo;
  ask-provided).
- **Q3 (loop_gaps recursion; finetunable or not):** census run this session (exact command:
  `.venv/Scripts/python.exe -c` counter over `training/loop_gaps.jsonl`): 331 rows,
  2026-08-06T23:11Z to 2026-09-30T11:45Z; all-time top gap names: `lifecycle_waste:drainer`
  96, `lifecycle_gap:ollama` 95, `lifecycle_gap:dashboard` 21, `lifecycle_gap:drainer` 19,
  `test_gap_unique_xyz` 18 (annotated in-place as unit-test pollution per B2-79),
  `lifecycle_gap:lab` 16, `browser_env_not_wired` 16. Last-30d: drainer-waste 59, ollama-gap
  55, test-pollution 15. The recursive class is supervisor/lifecycle STATE FLIPS
  (should-be-on-but-off / should-be-off-but-on oscillation of drainer, ollama, remote_seats),
  i.e., infrastructure and config defects, not model behavior. No literature classifies that
  as a finetuning target: it is a control-loop bug. The adjacent model-side classification
  from 1nturn1 comments + arxiv 2502.14502: knowledge-capacity limits are real (architecture
  bound) but most observed "can't adapt" failures are dataset-quality (finetunable); current
  anti-forgetting recipes are OSFT (Red Hat, 2026-07-28, SVD-projected updates confined to the
  orthogonal subspace, ~48.4% vs ~23% average accuracy in their cited benchmarks) and
  pretraining replay during finetuning (smol.ai AINews, 2026-03-06).
- **Q4 (distillation vs direct dispatch):** the estate baseline instrument exists and is
  healthy: `training/cost_ledger.jsonl` census this session: 2,439 rows, 2026-08-06 to
  2026-09-30, seat mix ollama 1,765 / deepseek 494 / glm 44 / grok 32, actual-side fields
  include usd_est, billable_tokens, cache_hit_tokens, cache_miss_tokens, pricing_coverage.
  External economics: tianpan.co "Knowledge Distillation Economics" (2026-04-09) reports
  18x-37x per-query savings depending on student size, with an explicit break-even: distill
  only above a stable query-volume threshold; arxiv "Cost-of-Pass" frames cost-per-task the
  way the ONE-BUG law (per the ask, laws.md:18; file absent from repo) wants conditions named.
  Distillation from the funded primes (glm-5.3-prime / qwen3.8-max-prime) beats direct
  dispatch when (a) the verdict shape is stable and high-volume, (b) teacher verdicts are
  already banked with verdict+correction contrast (the corpus-grade row), and (c) the
  student runs free on ollama. NOT verified here: the estate has no per-verdict cost split
  join in this session; any "already cheaper" claim is OWED, not asserted.
- **Q5 (license/ToS screens on session-derived corpora):** the counsel triage law is real and
  on disk: `memory/rib/RIB_LAWYER_BOOT_20260904.md:13` assigns review of "licenses
  (training-corpus eligibility), platform ToS (what we scrape" and `:28-29` orders a "corpus
  LICENSES.md audit [...] the NC-trap and no-license calls double-checked" (a dash inside the
  source quote elided for the seat dash law). Emerging practice matches it: HF dataset cards
  carry explicit NC screens (nvidia/CantTalkAboutThis-Topic-Control-Dataset-NC;
  unsloth/alpaca-cleaned under CC BY-NC 4.0 per search results), and the community norm for
  session-derived data (1ram8tt) is sanitize-then-publish with an acknowledged ToS gray zone.
  The triage law is ahead of or level with practice; no drift found.

## Overlap checks (what ran)

- catalog/catalog.jsonl (691,788 rows, counted via PowerShell Measure-Object): python counter
  over the full file for distinctive phrases. Hits: `thinkingmachines` 2 (intake filenames,
  e.g. catalog/catalog.jsonl:581322 `fan_belady-lruk_thinkingmachines_inkling-small`),
  `catastrophic forgetting` 1 (state/arxiv/2026-09-11/2609.11447v1.txt, sound-event
  classification paper), `held-out` 5 (the estate's own CHORD v3/v4 gates and UF-122
  retrieval-eval specs). Zero hits for: 1rsqzua, Ada code generation, Steelman, LoRA Without
  Regrets, Unsloth AMA, danielhanchen, donate all my, DoRA, replacing RAG, orthogonal
  subspace, OSFT, Cost-of-Pass, pretraining replay, Dynamic GGUF, adapter continuation,
  knowledge distillation.
- memory/ curated surfaces (memory/rib, memory/press, memory/frontier, memory/attention.md):
  grep -r -l for Steel, LoRA Without Regrets, catastrophic forgetting, DoRA, chat history,
  OSFT: 0 files each. A full-tree memory/ grep was started and KILLED for time (memory/ holds
  large transcript jsonl); reported as partial, not complete.

## OWED / limits

- corpus.md and laws.md cited by the ask are NOT in this repo (repo-wide findstr over
  *.md/*.jsonl/*.json: no hits); their claims (11,870 seat_pool rows; path-inferred labels;
  echo-inflated raw_count; ONE-BUG law; counsel triage law) are treated as ask-provided, and
  the counsel law independently verified at memory/rib/RIB_LAWYER_BOOT_20260904.md:9,13,28-29.
- Dates for the 50 pass-1 listing candidates are relative ages ("N days ago" at fetch,
  2026-09-30); exact post timestamps were not retrievable for them. Deep-read item dates are
  exact (pullpush created_utc, converted with python datetime).
- The full memory/ tree overlap grep is partial (curated dirs only).
- The estate-side per-verdict distillation-vs-dispatch comparison (Q4) was NOT computed; only
  the ledger census ran.
