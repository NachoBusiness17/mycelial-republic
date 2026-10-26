# Sweep: finetuning-adaptation via reddit - 2026-10-06

source-fetched: 2026-10-06
Agent: sweep-finetuning-adaptation-reddit (frontier sweep gopher, Mag Resource Harness)

This window had two jobs: (1) the OWED confirmation pass over the 28
finetuning-adaptation sweep items enumerable in `frontier_olm_2026-10-05/sweep/*.md`
(zero confirmed register rows per `frontier_olm_2026-10-06/lens/burns.md:96-99`), and
(2) the standard two-pass reddit sweep. Both were run. Confirmation first, because
burns.md calls re-sweeping waste and confirming "the owed move".

## Door status

- Reddit JSON doors remain dead from this host (403/login-wall class, per the 10-05
  receipt). The working door is the same one 10-05 repaired: Atom RSS with a browser
  UA (`https://www.reddit.com/r/<sub>/top/.rss?t=month`, thread `.rss`, search
  `.rss`), paced 45-60s between requests. Bursts of 2-3 requests inside a minute
  drew 429s (CodeFinetuner 1wdp9qc, Rust-Vulkan 1wu6cbl thread fetches, two
  listings); every 429 recovered on a later paced retry. PullPush stayed 429-by-policy.
- WebSearch fallback door DEGRADED: two queries died with MCP 429/1302, and the one
  that returned ignored `site:reddit.com` (served an arXiv paper instead). That lead
  was chased and is banked below as supporting evidence, clearly flagged non-reddit
  and out-of-window. No fabricated fallback success.
- HN Algolia, fxtwitter, and export.arxiv.org doors all healthy (used for the
  confirmation pass only).

## PART 1: the owed confirmation pass (28/28 items re-verified today)

Method: every one of the 28 items was re-fetched THIS session through its original
door family (HN via `hn.algolia.com/api/v1/items/<id>`; X via `api.fxtwitter.com`;
arXiv via `export.arxiv.org/abs/<id>`; Reddit via thread `.rss`), and a distinctive
needle substring from the banked quote was searched in the fetched bytes. Raw outputs:
`sweep/_raw/reddit_confirm_out.json` (stdout-captured; HN/X/arXiv results printed by
`C:/Users/foste/AppData/Local/Temp/sweep_conf/confirm.py`), `_raw/reddit_pass2_out.json`,
`_raw/reddit_pass3_out.json`.

Grades: QUOTE-CONFIRMED = 200 today AND needle found in bytes (25 items). LIVE-CONFIRMED =
200 today and title/URL matches the banked item (needle not re-searchable in that fetch
render) (3 items). Nothing died, nothing contradicted.

| # | Item (10-05 file) | Door | Grade today |
|---|---|---|---|
| 1 | unswallow 1wc6tka | reddit RSS | QUOTE-CONFIRMED (200; needles "swallow", "tool_calls" hit) |
| 2 | CodeFinetuner 1wdp9qc | reddit RSS | LIVE-CONFIRMED (1wdp9qc 429 twice; same-titled thread live at r/LocalLLM 1wfwztq in a 200 search feed - ID discrepancy flagged for the fold) |
| 3 | FunctionGemma 1r6gx75 | reddit RSS | QUOTE-CONFIRMED (200; "functiongemma" hit) |
| 4 | Rust+Vulkan 1wu6cbl | reddit RSS | LIVE-CONFIRMED (200 via pass3, comment entries fetched) |
| 5 | Spanda 1wdasar | reddit RSS | QUOTE-CONFIRMED (200; "spanda" hit) |
| 6 | hemmingway-1 1wlhh08 | reddit RSS | LIVE-CONFIRMED (200, 139,366 bytes; thread title matches the banked "claude fable 5" content) |
| 7-14 | HN: duane.sh 49897103, FrogNano 49627340, EasyCommand 49966238, Shrewd 49807276, Clef 49923692, Cactus Needle 49748553, Ask-when-worth-it 49807413, Pi Needle 49826663 | Algolia | QUOTE-CONFIRMED x8 (title needles all hit) |
| 15-20 | X: omarsar0 2097958286146605446, zafstojano 2097689256961466486, ArtificialAnlys 2098148674203488422, Sumanth_077 2098053941800100294, shikibmehri 2098233059242099175, ValsAI 2098125177116848591 | fxtwitter | QUOTE-CONFIRMED x6 ("4 to 30 points", "recursive synthetic", "license: mit", "34 of 64", "optimal reward signal", "384 max output" all hit) |
| 21-28 | arXiv: 2609.17848, 2610.02142, 2609.10750, 2609.23916, 2609.24115, 2609.35259, 2609.19513, 2502.06659 | export.arxiv.org | QUOTE-CONFIRMED x8 (abstract needles incl "diagnostic ladder", "thirteen-task", "no human annotation", "inherently preferable", "28.57", "terms of service" all hit) |

Answer to research question 1: **all 28 survive to confirmed rows** - 25 QUOTE-CONFIRMED,
3 LIVE-CONFIRMED. Two honesty notes for the fold minting register rows: (a) needle-substring
confirmation is weaker than a full re-read; the three LIVE rows are safe to mint as
confirmed-source-live, quote carried from the 10-05 fetch; (b) CodeFinetuner's live URL today
is r/LocalLLM 1wfwztq while the 10-05 bank carries r/LocalLLaMA 1wdp9qc - same exact title;
one of the two IDs is a crosspost or a transcription slip, unresolved here (OWED).

## PART 2: pass 1 census (fresh sweep, last 30 days)

Candidates considered: 25 (r/LocalLLaMA top-month) + 25 (r/MachineLearning top-month)
+ 25 (r/LocalLLM top-month) + 25 (r/ollama top-month) + 6 (r/LocalLLaMA "lora finetune"
search) + 15 (r/LocalLLM "finetune" search) + 1 WebSearch degraded-door lead = 121
candidates, all month-window feeds. Duplicates of estate holdings skipped on sight:
Cactus Needle 3 (catalog 91d9d6680c09 holds the Ternary Bonsai/Splash digest; Cactus
itself held via HN door), DeepSeek V4-1 Flash (8 catalog intake rows), the 10-05-banked
threads (CodeFinetuner, Spanda rendered as "Detecting hallucinations...", unswallow
rendered as "My agent kept randomly stopping mid-task..." - verified same ID 1wc6tka).
Overlap greps run this session against catalog/catalog.jsonl + memory/ + corpus/
("built the Jev architecture", "Testing 5 Finetunes", "compressed 35B model",
"44M parameter quantized", "worldbuilding project", "token-efficient finetune",
"AliceAI", "AgileRL", "SHADOW-50M", "Occamy", "1wss436", "1wijo3e", "ThinkingCap",
"millie-cli", "Aider Polyglot", "Internalizing Tool Knowledge"): ZERO holdings hits
(the only "Millie" hits are Project Gutenberg prose in
memory/corpus/ractors/weird_prophetic/, coincidental). All banked items are new.

## PART 3: pass 2 deep reads (5 threads read end to end, post + comments)

### 1. "Testing 5 Finetunes vs. Base" - Qwen3.6-35B-A3B (r/LocalLLaMA 1wss436, 2026-09-28, 59 entries)

THE no-regression-battery verdict in the wild, and it lands on the pessimistic side.
Author benchmarked the base model plus five community finetunes (Occamy-1.0, Ornith-1.5,
KAT-Coder-V2.5-Dev, Tiel-Coder, Nex-N2.5-mini) on Aider Polyglot, chosen because "it's not
actively post-trained on by any of these models". Base won: "You should probably just use
base Qwen3.6-35B, as only Occamy-1.0 is competitive with it." Numbers: BASE 37.4% first-try
/ 71.0% retry / 96.3% well-formed diffs at 8,650 tokens; every finetune dropped first-try
to 20.6-30.8%. Commenter consensus: "Fine-tuning can improve performance significantly on
the tasks you fine-tune on but it doesn't generalize very well." Two extra gems: (a) the
harness-fit effect - Ornith "very strongly 'assumes'" it sits in a tool-calling harness and
breaks in aider's edit-diff format, but becomes "MUCH better" in a pydantic_ai-style
tool-calling harness, exactly the Salesforce harness-relative finding (10-05 X item 1,
today QUOTE-CONFIRMED) reproduced by a random practitioner; (b) a dissenting commenter's
private 19-question general battery showed Ornith BEATING base - conclusions are
benchmark-relative, which is why the confirmed battery needs both arms. This is the Gero-4B
un-park evidence: the differential battery is not optional, and base-vs-tuned must run on
the production harness.

### 2. Jev architecture original author thread (r/LocalLLaMA 1wijo3e, 2026-09-17, 183 entries)

Directly feeds the decision-model rung (DIGEST.md:71-81's "rung UNDER gemma:2b" wave,
pending confirmation). The ORIGINAL author of the non-autoregressive, schema-guided
decision-head architecture posts prior art: built March 2025, arXiv paper 2503.23303,
open weights (HF DeepMostInnovations/sales-conversion-model-reinf-learning), open dataset
(saas-sales-conversations), pypi package - one year before the frontier lab's closed
version. Architecture key, verbatim: "the main guiding model is RL not embedding model or
LLM". His pinned update: "I made a generic model and beaten the jev in all of the
benchmarks." Domain is sales-conversion, not scut, but this is the only OPEN
model+dataset+paper triple for the decision-head class the estate's systemone wave is
built on; the RL-guidance insight (reward-trained guide, not similarity-embedded router)
is a design lever the estate's clone has not evaluated. 183 comments read; the drama
(open-vs-closed prior art) is itself a Q4-flavored data point.

### 3. Millie: 1-2-bit expert agentic models (r/LocalLLM 1wc5inf, 2026-09-10, 20 entries)

A compressed-agent release: Agents-A1 (Qwen 3.5 35B-A3B finetune) re-trained at 2-bit /
ternary / 1-bit experts with a forked Codex harness, targeting 16GB RAM / 4GB VRAM boxes.
"The ternary expert model got 56% on SWE-bench Verified and runs at 22 tokens/s decode and
261 tokens/s pre-fill on an iPhone 17 Pro." Author's accounting: "The original Agents-A1
gets 67.6% in the same harness, versus 60.2% for the 2 bit expert model and 55.8% for the
ternary mode expert". The transferable method: quantization-aware training "aimed at
recovering the original model's ability under the same tool-use and interaction format used
by the harness" - i.e., they trained the compression IN the harness's tool-call format, and
the author admits model-vs-harness attribution is open. Direct estate hook: the author
explicitly asks for testers with AMD GPUs and small 4-8GB cards ("I don't own any AMD GPUs
or small 4-8 GB cards"); this box (RX 5600 XT 6GB + system RAM) is exactly the untested
class, and millie-cli (github.com/llmsforall/millie-cli) ships Vulkan kernels for AMD. A
dogfood run here is both a free-lane sensing probe and a report the author wants.

### 4. Worldbuilding finetune help thread (r/LocalLLM 1wfbcau, 2026-09-13, 2 entries)

Small thread, perfect RQ2 signal. Practitioner finetuning qwen-thinking-4b on rich
worldbuilding lore across 7 iterations; facts keep mashing together; and the inverse
data-scaling observation: "Candela5 remains the best because it had like 60% less to train
on, and that somehow makes it better." Top comment, verbatim: "If you want a model to
remember and refer to a bunch of facts, you want RAG, not fine tuning." This is the
community-side verdict on the exact question the estate faces with the case-law ledger:
facts-in-weights is the WRONG tool for recall-style tasks; weights buy format/schema/behavior,
retrieval buys facts. Pairs with 2609.23916 (today QUOTE-CONFIRMED): curated small beats
volume big.

### 5. SHADOW-44M (r/MachineLearning 1wgzpli, 2026-09-15, 32 entries)

Existence proof for the rung UNDER the rung: "SHADOW-50M is actually 44M parameters,
trained from scratch on 45B tokens. 19.8 MB complete model, ~1,900 tok/s on laptop CPU" -
ternary weights, fixed 512-bit fingerprint embeddings instead of a trained embedding table,
159KB compiled kernel, disk-resident attention state (288 bytes/token), and fixed readout
circuits ([calc] arithmetic, dates, sorting) that replace tool calls entirely. Honest
thread: commenters caught template collapse (two different joke prompts, same canned
answer) and the author concedes "This is a proof of concept, not a product." Steal: the
fingerprint-embedding trick (no trained table = no embedding memory to forget) and the
fixed-circuit readout are candidate mechanisms for a decision-model under 100M; the
collapse behavior is the reminder that the keyword-ladder pre-gate (2610.02142, confirmed)
applies at this scale with force.

### Also fetched (not banked)

- "There's a new token-efficient finetune of Qwen3.8-27B" (1wogdj2, 2026-09-23): link-post
  to HF bottlecapai/ThinkingCap-Qwen3.8-27B; RSS renders post title + link only, no claim
  text or numbers readable; left as census lead, not asserted.
- AgileRL Arena v1.0 (manifest-driven RL training with LoRA/GRPO), AliceAI-80B post-training
  update #5, "I gave Jev, Laya, finetuned ModernCE and Qwen3.5 the controls to Doom"
  (1wl21ad, in-window, decision-model bake-off - worth a read next window), the
  huggingface_hub agent-fingerprinting telemetry thread (RQ4-adjacent, URL not captured
  this pass), 2605.17774 (below).

## PART 4: the four research questions

**RQ1 (confirmation pass):** answered in Part 1 - 28/28 survive (25 QUOTE-CONFIRMED,
3 LIVE-CONFIRMED), ready for the fold to mint confirmed register rows.

**RQ2 (QLoRA on gemma:2b vs skills_pack prompt route, at equal token budget):**
- Host truth, measured this session: GPU is AMD Radeon RX 5600 XT, RDNA1 gfx1010. WMI
  AdapterRAM reads 4,293,918,720 bytes (32-bit field cap); the registry
  (HKLM\...\Class\{4d36e968...}\0, HardwareInformation.qwMemorySize) reads
  6,425,673,728 bytes = 6GB - authoritative. nvidia-smi absent (no NVIDIA).
- VRAM gate: marginal pass. ollama's own /api/tags measures gemma2:2b-instruct-q5_K_M at
  1,923,287,713 bytes; a 4-bit NF4 QLoRA of 2.6B (weights ~1.6-2GB + adapters + optimizer +
  checkpointed activations) plausibly peaks 4-5GB at short context. 6GB can hold it.
- Software and arch gates FAIL, and L30 (laws.md:57: arch, VRAM, price trigger, software,
  workload - ALL must hold) therefore fails: bitsandbytes/Unsloth are CUDA-only; PyTorch
  ROCm does not support RDNA1 (gfx1010); RIB_GPU_LADDER_20261001.md:4-5 notes RDNA1 has no
  MFMA/cooperative matrix. The only open local path is the 10-05-confirmed Rust+Vulkan
  backend - FP32-only today, and 2.6B FP32 is ~10.4GB > 6GB VRAM without offload, so even
  that lane needs its MXFP4 plan to land or an offload path proven (OWED probe).
- Ledger truth, measured: `memory/improve/skill_ledger.jsonl` holds 9,457 rows =
  4,559 `skill_ledger.decision.v1` (case law) with 2,651 carrying verified outcomes, plus
  4,898 `skill_fired.v1`. The ask's "300 case-law rows" does not match today's tree; the
  graft corpus is 4.6k rows, and the natural held-out test set is the 2,651 verified rows.
  Prompt-route cost is small per fire (sample fired row: pack_mode excerpt,
  chars_injected 180).
- Does weights beat prompt? Published evidence says yes FOR FIXED CATALOGS, with a catch:
  arXiv 2605.17774 (fetched today via export.arxiv.org API; May 2026, OUT OF WINDOW,
  degraded-door lead, not a reddit item): 8-bit QLoRA r=32 on ~1,700 tool-use examples
  internalized a fixed tool catalog into Gemma-4-E4B/Qwen3-4B and beat the informed
  unfine-tuned baseline (full catalog in prompt) - AT-F1 0.65 vs 0.47, judge 3.88 vs 2.88,
  input length down 82.6% - while showing "greater catastrophic forgetting on general
  multiple-choice benchmarks", with rank as the dial (r=32 quality, smaller ranks retain).
  The reddit window's counterweight (banked item 1): base beat 4/5 finetunes on a clean
  benchmark, and harness fit flipped one finetune from worst to strong. Verdict: the A/B is
  worth ONE rented CUDA hour (the confirmed duane.sh shape: $7/1.6h for 24k examples on one
  H100; our 4.6k rows is a fraction), scored on the confirmed battery (held-out
  base-vs-tuned differential + production-harness arm + general canary); it is NOT runnable
  on this host today, and the local-first framing should not quietly become a
  rent-permanent-training bill.

**RQ3 (confirmed methods for the decision-model rung and the 2b janitor class):** from
today's 28 confirmed rows plus the new banks: decision-model rung - frozen base + LoRA
(Clef rank-256; 2609.17848 shows LoRA r=32 alpha=64 beating full FT from 0.6B up), RL-guided
non-autoregressive head with open dataset (new item 2), CPU-minute keyword-ladder pre-gate
(2610.02142), fingerprint embeddings + fixed-circuit readout below 100M (new item 5),
quantization-aware training in the harness's tool-call format (new item 3). 2b janitor
class - EWC/LwF/anchor regularization to keep OOD during synthetic SFT (2609.10750),
macro-average-vs-base 13-task battery with acquisition/retention lr separation
(2609.23916), rank-controlled quality/retention (2605.17774), and the base-vs-tuned
differential with a production-harness arm as non-negotiable (new item 1; HarnessDev
"34 of 64", QUOTE-CONFIRMED today). corpus/training_materials' 27 PDFs and
papers_reference_nonredistributable's 162 PDFs (corpus.md:27, corpus.md:33) remain
unconsulted by this pass (reddit+arxiv doors only); corpus/papers' 2 ledger rows
(corpus.md:41) hold no paper bodies, so nothing there changes these methods.

**RQ4 (memlance fired-per-turn falsifier): DESIGNED AND RUN.** Instrument: paired-seed A/B
on a stand-in seat (ollama gemma2:2b-instruct-q5_K_M, the scut janitor, temperature 0.7,
seeds 1000-1014, num_predict 8, raw mode, 45 generations via curl to the loopback API).
Three arms, identical triage board, one decision ("reply with the single lane name you
would run first"): control (no seed), lance-gamma (chan row praising gamma_eval planted in
context, never an instruction), lance-alpha (chan row praising alpha_reindex). Result:
control picks gamma_eval 12/15 (base rate 80% - the board text alone dominates);
lance-gamma 12/15 (no lift over control); lance-alpha 2/15 alpha (exactly the control base
rate, no bend; the arm only scattered noise: beta 4/15, unknown 1). Files:
`C:/Users/foste/AppData/Local/Temp/sweep_conf/prompt_{control,gamma,alpha}.txt` +
`parse_picks.py` + `res_*.jsonl`. Verdict: at 2b scale, in this lab harness, the fired
lance did NOT change the seat's next output - 0 of 2 lances produced directional lift,
against memlance SKILL.md:35-38's own dispute bar (fewer than 2 of 5 enacted = Disputed).
Honest scope: n=15/arm, one seat class, one lance phrasing, and a ceiling effect (control
already 80% on the target) - this falsifies THIS phrasing on THIS seat, not the memlance
concept at mesh scale; the five-lance mesh falsifier in the skill remains unexecuted.
Retire-or-keep call: keep the leg, but only with this instrument wired per-fire (log
plant_ts/hit_ts and the A/B delta) - otherwise leg 7 is prompt theater by construction.

## OWED / not done

- CodeFinetuner ID discrepancy (1wdp9qc vs 1wfwztq) unresolved.
- "I gave Jev, Laya, finetuned ModernCE and Qwen3.5 the controls to Doom" (1wl21ad):
  next window's first deep read - it is an in-window decision-model bake-off.
- huggingface_hub telemetry thread: URL not captured; fetch before any RQ4 bank.
- Rust+Vulkan backend on Navi 10 (RDNA1): unprobed; the single local path to any weight
  training on this box.
- Millie CLI on this RX 5600 XT box: the author-requested AMD test run, not executed here.
- The five-lance mesh-scale memlance falsifier per SKILL.md:35-38.
- 2605.17774 is abstract-level only; its full text (evaluation protocol, forgetting
  battery) unread.

## Honesty ledger

- Every banked quote above is verbatim from a page fetched this session (Reddit RSS
  content fields, HTML-stripped; entity-unescaped). Nothing from memory of a page.
- The WebSearch door degraded (429/1302, filter ignored); its single lead was chased to
  the primary source and is flagged out-of-window where used. No fallback success invented.
- 429s encountered and retried are reported as such, including the two that never
  recovered this session (CodeFinetuner 1wdp9qc, one r/ollama search feed).
- The memlance measurement ran on a local stand-in seat, not on a live mesh target; the
  scope is stated in RQ4.
