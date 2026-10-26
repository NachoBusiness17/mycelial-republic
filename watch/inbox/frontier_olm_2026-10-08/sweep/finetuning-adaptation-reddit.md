# Sweep: finetuning-adaptation via reddit - frontier OLM 2026-10-08

source-fetched: 2026-10-08. Seat: sweep-finetuning-adaptation-reddit.

## Door record (measured this sitting, degraded doors named, no fabricated fallbacks)

1. `old.reddit.com/r/{LocalLLaMA,MachineLearning,LocalLLM,ollama}/top.json?t=month&limit=50`
   via WebFetch: Reddit "Welcome" HTML shell, zero JSON (matches lens/doors.md:56-64
   walled verdict). Via curl with a browser UA + Accept json: HTTP 404, body literally
   `Not Found` (9 bytes, saved as `_raw/topjson_*.json`). This discharges the doors-lens
   OWED "curl + UA candidate": the candidate is dead too.
2. `www.reddit.com/r/LocalLLaMA/top/.rss?t=month` via curl: HTTP 200, 59,974 bytes, my
   own fetch this sitting (`_raw/my_rss_LocalLLaMA.xml`), byte-size identical to the
   sibling's 13:28 capture. RSS remains the one live listing door.
3. WORKING deep door: Arctic Shift archive API `arctic-shift.photon-reddit.com`
   (`/api/posts/ids?ids=`, `/api/posts/search?subreddit=&limit=&after=`,
   `/api/comments/search?link_id=`). 8 post fetches + 16 comment fetches this sitting,
   all HTTP 200. Pace law measured: 4s spacing drew `{"error":"Timeout. Maybe slow down
   a bit"}` and one 522; 8s spacing with the `t3_` link_id prefix cleared it. Comments
   for sub-48h threads need the `t3_` prefix form (bare id returned empty/timeout).
4. WebSearch site:reddit.com fallback: works, but returns 2024-2025 threads for this
   lane's terms (Finetune-vs-QLoRA 18g0vtp, VRAM table 18o5u0k, Unsloth 1ar7e4m et al);
   used as background only, nothing banked from it (all out of the 30-day window).

## Pass 1 (broad sweep, >=30 candidates: 1,900 posts + 100 RSS entries)

Instrument: paging script (repo venv python + curl, CREATE_NO_WINDOW) over
`/api/posts/search?subreddit=X&limit=100&after=1788825600` (epoch = 2026-09-08T00:00Z,
the 30-day window) for all four recipe subreddits: 500+500+500+400 = 1,900 unique
submissions (`_raw/ft_pool_1008.json`). Plus the 4 top-month RSS captures (25 entries
each, 2026-09-08..10-08). Keyword filter (logit/sampler/min_p/top_p/top_k/temperature/
lora/finetun/peft/unsloth/qlora/adapter/checkpoint/modelfile/distill/prompt-tun/embedding/
nomic...): 149 hits. Held-id filter: every thread id cited by ANY prior frontier bank
(sweep+steal, 10-01..10-08, 1,525 ids extracted by regex over the bank .md files)
removed: 132 NEW candidates. Census printed top-45 by score (in session log).

Held, verified NOT re-banked (the week's prior banks own these): 1wc6tka unswallow,
1wdasar Spanda, 1wlhh08/1wm88t6 hemmingway-1, 1wgzpli SHADOW-44M, 1wx0jtb DwarfStar,
1wqxbwa Binders, 1wuv6oh Hillock, 1wt0tot MMO swarm, 1wv1u54, 1wiijww (Ollama-vs-stack
taxonomy; held at candidate depth by the 10-03 window-2 adapter cluster, dropped by
today's sibling lane as consumer-setup; my deep read of its 56 comments confirmed it
adds nothing beyond what 1wyzwab's adapter-culture comments carry), plus the 10-03/05/
06/07 banked finetuning sets (TACO, Bonsai whitepaper, Humanlike-Chat, CLM, ratctl,
Swift, GRPO-0.5B, Gemma-3n scratchpad, RLF, MiMo, Opus distill, MTP-1.7B, FFT-optimizer
adjacent 1wyihlz surfaced NEW but unread past candidate depth - not banked).

## Pass 2 (deep reads: 15 threads read end to end this sitting)

First round (7 threads, all turned out HELD - bodies+comments fetched and read by me,
then dropped as re-banks, evidence in session): 1wiijww, 1wgzpli, 1wlhh08, 1wc6tka,
1wqxbwa, 1wdasar, 1wx0jtb. Their content is NOT re-asserted below except as cited
context from the prior banks that own them.

Second round (8 threads, all NEW, bodies + top comments read in full): 1wz5va3 (100 of
109 comments), 1wzn14o (22/22), 1wyzwab (12/11), 1wyycx6 (3/3), 1wybqq3 (5/5), 1wyui4o
(13/13), 1wz3pm2 (2/1), 1wyxukj (15/15). Raw JSON banked at `_raw/fa_comments_*` and
`_raw/ft_pool_1008.json`. Scores are Arctic Shift crawl-time snapshots.

## The eight banked items (strongest first)

### 1. EmbeddingGemma 2 release thread - the non-router use case in the wild (r/LocalLLaMA 1wz5va3, 2026-10-06, s=490, 109c)
- URL: https://www.reddit.com/r/LocalLLaMA/comments/1wz5va3/googleembeddinggemma2_hugging_face/
- Facts read: 740M total = 270M text + 170M vision + 300M audio encoders, one shared
  768-dim space over text/code/images/video/audio, 100+ languages, built on Gemma 4
  architecture, targeted at consumer hardware. Top comment (celine_aubry, 34 pts):
  "a 740M model that can embed text, images, video and audio into the same vector space
  is more useful to 99% of you than any 27B chat model you will ever run". jacky2060
  (27 pts): llama.cpp support merged (PR 30054) + ggml-org GGUF up. stoppableDissolution
  (19 pts): building one multimodal personal library search over mixed scrapes on it.
- Why (RQ5): the estate banked the model under models/ but killed its router use
  (GPS-embed, string keys 100.0 vs embedding-kNN 99.05). This thread is the answer to
  "what non-router use justifies residency": unified multimodal retrieval/clustering
  over estate mixed-media (screenshots, session audio, prose) at 740M, llama.cpp-served
  next to the janitors. Resident cost is one llama.cpp embedding slot, not a GPU judge.
- Overlap: catalog grep "embeddinggemma-2" = 9 rows (the banked model dir + sibling raw
  captures); the thread id appears in no prior bank (held-id check). Model held, thread
  and its use-case debate new.

### 2. LoRAs as persistent switchable skills - the adapter-as-shed question asked by the community itself (r/LocalLLaMA 1wyzwab, 2026-10-06, s=7, 11c)
- URL: https://www.reddit.com/r/LocalLLaMA/comments/1wyzwab/would_you_use_loras_as_persistent_switchable/
- OP proposes encoding skills/domain/style into switchable LoRA adapters instead of
  context/RAG. No-Refrigerator-1672 (8 pts) already runs it: "Heretic version of qwen
  3.8 converted into LoRA, which allows me to switch between normal and uncensored
  versions on the fly, without reload and without having both model weights in my vram".
  CoffeeToCode99 (3 pts): fit is behavior (style, coding standards, expert modes), not
  frequently-changing knowledge. Theio666 (1 pt) dissents: frontier instruction-following
  makes 3k context tokens cheaper than adapter management. No-Refrigerator-1672 (2 pts)
  names the culture gap: Unsloth-style finetuners "consciously choose to merge it and
  publish only the merged version", so switchable adapters stay scarce.
- Why (RQ2+RQ3): this is ReFold's reversible sha-addressed shed question (lens/burns.md
  P5) transposed onto adapters, from the field: per-seat adapter deltas, one base model
  resident, swap without reload. The restore door the thread exposes: adapter
  availability (authors merge-and-publish), and the estate's own P3 digest-pinning
  analog - an adapter swap must re-verify the base-animal fingerprint or a silent base
  upgrade orphans every shed.
- Overlap: "switchable skills" and "would you use loras" = 0 catalog rows; thread id in
  no prior bank. New.

### 3. Uniform GGUF quants silently break hybrid-attention deep thinking - serving-layer dominance, contested in-thread (r/LocalLLM 1wyui4o, 2026-10-06, s=2, 13c)
- URL: https://www.reddit.com/r/LocalLLM/comments/1wyui4o/uniform_gguf_quants_silently_break_qwen3827bs/
- OP: Qwen3.8-27B (Gated DeltaNet + full attention hybrid) under Unsloth Dynamic GGUFs
  (UD-Q4_K_XL/Q6_K_XL) tail-loops or dies mid-generation on long thinking tasks,
  reproduced on llama.cpp AND vLLM; "the same model family in a mixed-precision quant
  (NVFP4: FP8 on attention/recurrent layers, FP4 on MLP) converges in ~17K thinking
  tokens on the same prompt"; hypothesized mechanism: recurrent-state error accumulation
  under uniform integer quantization. Community contestation read in full: durden111111
  (6 pts) calls it bot content, "Q8 does way better than nvfp4"; KissMyShinyArse (2 pts):
  "UD quants are anything but uniform" (naming error); Choice_Celery9481 (2 pts) flags
  the KV-quant confound (kv f16 untested); EducationalRoom6325 (4 pts) independently
  corroborates Q6_K_XL long-context repetition fragments after ~40K tokens;
  fintip (1 pt) sees no problem on long tasks.
- Why (RQ1+RQ2): single-source and contested, but the failure CLASS (quant format x
  hybrid-attention recurrence x long-horizon generation) is exactly the estate's P6
  four-pinned-choices quant A/B spec: pin quant format AND kv dtype AND attention
  architecture before attributing janitor drift to the model. Also the estate's
  day-7 confirmed finding (serving layer dominates) with a mechanism attached.
- Overlap: "uniform gguf quants" = 0 catalog rows, no prior bank holds the id. The
  Bonsai/quant lanes banked adjacent quant threads; this one is new.

### 4. Finetuned 1.5B Qwen to generate bash at gpt-4o level, 400k synthetic examples, fully open (r/LocalLLaMA 1wybqq3, 2026-10-05, s=26, 5c)
- URL: https://www.reddit.com/r/LocalLLaMA/comments/1wybqq3/finetuned_15b_qwen_to_generate_bash_commands_at/
- OP (Comfortable-Rock-498) open-sourced dataset (dirac-run/ec-training-data), GGUFs
  (ec-1.5b, ec-0.6b) and CLI. The comment that matters: "I tried SmolLM 135M, SmolLM
  360M, Qwen3-0.6B, Qwen2.5-Coder-1.5B, Qwen3.5-0.8B, and Qwen3.5-2B. 2.5 coder 1.5B
  was showing the most consistent SFT gains". wingwing124 (4 pts) is already
  replicating on minicpm5 1B/2B and qwen3.5-2B with the same data.
- Why (RQ2): a janitor-class precedent (bash-command generation, 1.5B, hobby budget)
  where the finetune reportedly works AND the dominant variable was base-model choice,
  not tuning recipe. For the estate: if a janitor finetune is ever justified under the
  five-gate law, the cheap first experiment is base-selection across the pulled fleet
  (gemma:2b vs gemma2:2b-q5 vs qwen2.5:3b) on the SAME synthetic set, before any GPU
  spend. Dataset is open and pullable for that A/B at zero authoring cost.
- Overlap: "dirac-run"/"ec-1.5b" = 0 catalog rows; no prior bank holds the id. New.

### 5. Confidence-routing postmortem: label smoothing silently broke the 0.96 threshold (r/LocalLLM 1wz3pm2, 2026-10-06, s=2, 1c)
- URL: https://www.reddit.com/r/LocalLLM/comments/1wz3pm2/what_went_wrong_with_confidence_routing_in_my/
- OP runs a local computer-use agent: Qwen3.5 0.8B-first/4B-fallback, multiple-choice
  heads, route when lowest top-choice softmax < 0.96. Trained with fixed 0.95 soft
  targets; the label smoothing flattened calibrated confidence so the router silently
  mis-routed. blackpragmatism59: "the gap between top two options is definitely the
  move, I've seen that work way better than raw confidence for routing small models";
  holdout fix = generate tasks that break training-data structural patterns.
- Why (RQ5+RQ2): the estate's GPS-embed kill has a sibling failure mode here - routing
  keyed on a score the training pipeline itself distorts. If any future router returns,
  route on top-two margin, not raw probability, and never on a quantity the adapter
  was trained to flatten. Also a LoRA-hazard datapoint: soft targets eat calibration.
- Overlap: "confidence routing" token = 0 catalog rows (memory grep: see overlap
  receipts); no prior bank holds the id. New.

### 6. How do you decide whether to trust a community fine-tune? - the missing no-regression battery, confirmed as gap (r/LocalLLaMA 1wyxukj, 2026-10-06, s=2, 15c)
- URL: https://www.reddit.com/r/LocalLLaMA/comments/1wyxukj/how_do_you_decide_whether_to_trust_a_community/
- Practical-Collar3063 (8 pts): "Yes, massive yes. Most community made fine tunes
  perform worse overall than the base" - vetting is a small personal benchmark, nothing
  public. peligroso (4 pts): no public benchmarks trusted for finetunes. jacek2023
  (3 pts): follow known-good authors. OP's product question (side-by-side
  download-vs-base check) got yes-if-it-shows-regressions answers.
- Why (RQ2+RQ4): the 10-05 bank's queue item (held-out base-vs-tuned differential) is
  what this thread shows the community lacking. Any estate adapter shed needs the same
  battery as its merge gate; the estate instrument would be novel even by community
  standards.
- Overlap: no title/phrase catalog hits; id in no prior bank. New.

### 7. Local RAG second brain: embedder and hybrid retrieval picks in 2026 (r/LocalLLaMA 1wzn14o, 2026-10-07, s=16, 22c)
- URL: https://www.reddit.com/r/LocalLLaMA/comments/1wzn14o/local_rag_for_a_personal_second_brain_embedder/
- OP: SQLite + sqlite-vec + FTS5 hybrid on one user's ~50k chunks; asks whether embedder
  choice even matters at that scale. toothpastespiders (1 pt): "I was using 4B for a
  while but the difference in quality between the results of the two just wasn't
  significant enough to justify the overhead", impressed by embeddinggemma 2 after a
  half-day. seamonn (5 pts): the win is a reranker after fusion (Zerank 2), not a bigger
  embedder. KeyOne8943 (1 pt): bucket the eval by exact-entity / paraphrase /
  multi-constraint / nothing-found queries.
- Why (RQ5): at estate-scale corpora the answer mirrors the GPS-embed kill - embedder
  choice matters less than the fusion+rerank layer; the residency-justifying use for
  EmbeddingGemma 2 is the hybrid-retrieval leg (with FTS5, which the estate already
  runs: B2-465 FTS index) plus reranking, NOT routing. RRF-style fusion + eval buckets
  is a stealable instrument shape.
- Overlap: "sqlite-vec"/"personal second brain" = 0 catalog rows; id in no prior bank
  (the Binders thread 1wqxbwa held by kv lanes is a different thread). New.

### 8. Closed-form weight surgery: 0.8B beats 2B on ARC-Challenge, zero backprop - with in-thread stats dispute and a repo bug (r/LocalLLaMA 1wyycx6, 2026-10-06, s=13, 3c)
- URL: https://www.reddit.com/r/LocalLLaMA/comments/1wyycx6/a_08b_model_just_beat_a_2b_model_on_arcchallenge/
- OP (DynamicTune): extract velocity flow from a teacher, transfer into a student "via
  closed-form linear algebra in ~12 minutes on consumer hardware. Zero backpropagation,
  zero training tokens, zero gradient descent"; claims 42.15% vs 41.10% (Qwen3.5-2B) on
  full ARC-Challenge, third-party verified on an NVIDIA L4 by TPN Bench. yoshihuka (0
  pts) catches that the 3.23-sigma figure applies to the +4.65pt gain over the 0.8B
  baseline, not the 2B comparison; R_Duncan (1 pt) found the repo scripts "try to load
  an inexistant pickle, then loads only 0.8B version".
- Why (RQ4): the eliminate-before-frontier map gains a technique class with ZERO estate
  instruments: closed-form/no-backprop capability transfer (sibling posts 1wyzco6,
  1wyx2w9 same project). If it survives replication it is the only adaptation method
  that fits a no-GPU estate (12 minutes, consumer hardware) - but the in-thread dispute
  means it is CONTested, not confirmed; treat as a catalog row with two open
  falsifiers (paired 2B stats; repo repro bug).
- Overlap: "dynamictune" = 0 catalog rows; ids in no prior bank. New.

## RQ verdicts (from this sitting's reads only)

- RQ1 (logit_bias profile as adapter substitute): no thread in the 30-day window tests
  logit_bias specifically (keyword "logit" hit zero on-topic posts; the strongest
  adjacent evidence stays the banked 1wc6tka unswallow + 1wz3pm2's head-level fix
  class: parse/route-level corrections dominate). The P6 A/B remains estate-owed; the
  field's fixes are all serving-layer (template, jinja, parse, kv dtype, quant format),
  consistent with the day-7 finding.
- RQ2 (LoRA/PEFT under five-gate law): field evidence now splits cleanly: behavior/
  style adapters work and are switchable at one-base-weights cost (1wyzwab), knowledge
  adapters are the weak half; base-model choice can dominate the finetune itself
  (1wybqq3); most community finetunes regress something and nobody measures it
  (1wyxukj). A janitor LoRA is justifiable ONLY with the no-regression battery first;
  the battery is missing everywhere.
- RQ3 (ReFold shed -> adapter deltas): the community independently runs the pattern
  (Heretic-as-LoRA hot-swap, no reload, one VRAM residency). Restore-door hazards
  named: merged-only publishing culture (adapters unavailable), silent base-model
  upgrades orphaning adapters (estate P3 analog), and calibration drift from training
  choices (1wz3pm2) - a shed must store adapter+base-fingerprint pair.
- RQ4 (technique census): NEW technique with zero estate instruments: closed-form
  weight surgery (item 8). Held from prior banks: LoRA/QLoRA/GRPO/distill/merges all
  have receipts. Prompt-tuning proper: still zero Reddit field evidence this window.
- RQ5 (embedding residency): justified non-router uses, both field-verified: unified
  multimodal (text+image+video+audio) retrieval/clustering at 740M on llama.cpp
  (item 1), and the hybrid FTS5+vector+rerank leg where embedder size matters less
  than fusion+rerank at small-corpus scale (item 7). Router use stays dead.

## Honesty ledger

- Every quote above is verbatim from JSON fetched this sitting (files under _raw/).
  Scores are crawl-time snapshots, not live.
- Item 3 is contested in-thread (bot accusations, KV-quant confound, one
  corroboration); banked as a failure-class + spec consequence, not as fact.
- Item 8's headline stat is disputed in-thread and its repo has a reported repro bug;
  banked as CONTested with falsifiers named.
- The memory/ grep for new-item tokens ran as a background job; its result is recorded
  in the overlap receipts line of the submitted result (if it returned only run-log
  echo files, that is stated; nothing was banked on the assumption it came back clean).
- Not done: no live verification of any Hugging Face/llama.cpp links inside thread
  bodies (PR 30054, ggml-org GGUF, dirac-run dataset) - cited as claims read, not
  fetched. No pytest run (not asked).
