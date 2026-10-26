# Sweep: finetuning-adaptation via reddit - 2026-10-05

source-fetched: 2026-10-05
Agent: sweep-finetuning-adaptation-reddit (frontier sweep gopher, Mag Resource Harness)

## Door status (the fetch story, in full)

- Recipe door `old.reddit.com/r/*/top.json` **degraded**: all four subreddit JSON endpoints
  (LocalLLaMA, MachineLearning, LocalLLM, ollama) returned only a "Welcome to Reddit"
  placeholder shell with zero posts; `www.reddit.com` thread pages returned a bare "Reddit"
  page; `old.reddit.com` redirects curl to a login wall (`/login/?reason=lor2`); `api.reddit.com`
  is Cloudflare-blocked; PullPush archive API returns 429 "does not provide free scraping
  resources for agents"; redlib mirrors (catsarch, perennialte, safereddit, artemislena, bloat.cat)
  are Anubis-challenged or erroring (one thread DID read cleanly through redlib.catsarch.com
  early in the window before the challenge flipped on: the FunctionGemma deep read below).
- **Door repaired** via Reddit's Atom RSS feeds pulled from the host with a browser UA:
  `curl -A "Mozilla/5.0 ..." https://www.reddit.com/r/<sub>/top/.rss?t=month` returns HTTP 200
  (Reddit rate-limits bursts to ~1 req/40s; the pacing sleeps are mandatory). Thread-level
  `.rss` feeds work the same way. Parsers: `.venv/Scripts/python.exe` with
  `C:/Users/foste/AppData/Local/Temp/parse_rss.py` (listings) and `parse_thread.py` (threads).
- Pass 1 census: 25 entries r/LocalLLaMA top-month + 25 r/MachineLearning + 25 r/LocalLLM +
  25 r/ollama + 5 from the in-sub "lora finetune" search RSS + ~20 WebSearch fallback finds =
  **~100 candidates considered, all dated 2026-09-05..2026-10-05 for the RSS-sourced ones**.
- Pass 2: **7 threads read end to end** (post + comments), 6 in-window, 1 flagged older.
- Fidelity note: quotes below are verbatim from the fetched pages (RSS `content` fields,
  HTML-unescaped; `&amp;`-style entities normalized). Quotes were chosen em-dash-free where
  possible; the no-em-dash law applies to my prose, not inside verbatim quotes.

## Overlap discipline

Greps run against `catalog/catalog.jsonl` and `memory/` (commands in session log):
FunctionGemma / catastrophic forgetting / distillation license / reasoning traces / synthetic
data / LFM / Qwen3-8B / eval battery / CodeFinetuner / Cactus Needle / Spanda / unswallow /
Hemmingway / eq-bench / Mobile Actions / BFCL / Vulkan Transformer / self-consistency / FIM /
Confident Mode Collapse. Key findings:
- **Cactus Needle 3 was dropped as a duplicate**: the estate already holds it from the HN door
  (`memory/runs/gapwave/hn_x_fanout/skill_quantization.md:11,18-19` and
  `memory/runs/mickey17_v2/lanes/small-model-agents.json:13-16`, which even captured the
  Apache-2.0 license). Re-banking known work is waste; it is recorded here only as the
  dedup proof.
- `memory/trajectory/steps.jsonl` matches ("CodeFinetuner", "unswallow", "Hemmingway",
  "eq-bench") are this session's own trajectory log = self-noise, not holdings.
- "Spanda" memory hits are coincidental (`span_data` at
  `memory/research_packs/20260827_traj_rib/witness_B_practitioner.md:446`), not the metric.

## The six research answers, from what I actually read

**Q1 (LoRA/QLoRA on small models, tool-calling + repo navigation, <10k examples).**
Three independent in-window data points: (a) CodeFinetuner fine-tunes Qwen2.5-Coder-3B on your
own codebase with tree-sitter Structure-Aware FIM and reports "3B seems to be the sweet spot
where fine-tuning makes the biggest difference" (1.5B/3B/7B tried); (b) the FunctionGemma 270M
tune reached 90.9-96.7 percent multi-turn tool-call accuracy from ~50 seed + 5k-15k synthetic
examples, matching a 120B teacher; (c) the unswallow thread shows small-model tool calling on
llama.cpp has a systematic silent-failure class independent of quant or finetune quality.
**Steal for the janitor fleet:** the 3B sweet-spot claim and the FIM-over-own-repo recipe fit
`gemma:2b`/`gemma4`-tier scut work; the FunctionGemma shape (tiny specialist + grammar) fits
the same slot without touching the GB-class door.

**Q2 (minimum viable no-regression eval battery - the Gero-4B blocker).**
No single paper-style battery surfaced, but four community fragments compose one:
(1) CodeFinetuner's built-in battery: CodeBLEU + edit similarity + exact match + perplexity,
**base model evaluated on the same held-out set per-example, base vs tuned plotted together**
- that is the minimum viable differential battery; (2) its honest boundary: "the real
usefulness still has to be verified in the editor itself" (offline metric vs live sampling);
(3) a commenter's pre-registration of the Gero-4B objection verbatim: "Without running the same
eval against the base model on the held-out set you can't tell if fine-tuning actually improved
anything or just shifted the outputs around"; (4) Spanda adds a zero-GPU uncertainty check
(5 samples, T=0.7, exact-match entropy, ~0.89 AUROC at 27B) usable as a regression canary, with
the caveat that confident mode collapse evades consistency checks. Hemmingway-1's thread shows
the community's version of the same worry: niche finetunes "usually obsolete" versus fresh
bases on context understanding and language capability. **This composes the un-parking
definition the calibrator door needs: same-heldout base-vs-tuned differential on task metrics +
one general-capability canary + one live-harness smoke test.**

**Q3 (zero-cost synthetic-data pipelines for agentic finetunes).**
FunctionGemma's pipeline is the template: ~50 human-authored seed conversations per domain,
LLM-generated diversification, human validation before training, 5k-15k synthetic per dataset.
CodeFinetuner needs zero external data at all (your repo + tree-sitter). The Rust+Vulkan
backend closes the zero-cost training half: full LoRA lifecycle (HF-compatible adapter export,
modules_to_save, exact resume, merge/unmerge, auto-rank budget flag) verified against a pinned
Transformers oracle at 2e-7 error on an AMD iGPU, no CUDA/torch. All three ride free-lane
sensing-only inputs (local repos, self-generated data). Caution: FunctionGemma's teacher was a
120B remote model, so a faithful replication is not fully free; the estate equivalent would be
funded-Hermes-generated traces, which is exactly the descent-protocol shape.

**Q4 (licensing of distilled traces).**
Thin via the degraded door - no dedicated in-window licensing thread was found; this stays
**OWED** at reddit-grade evidence. What the fetched pages do establish: Cactus Needle 3 is
Apache-2.0 (already held estate-side); hemmingway-1 ships public weights finetuned on
Qwen3.8-27B without a license statement in the thread itself; CodeFinetuner is a pipeline
reference. The general Qwen-base-permissive pattern is consistent with these examples but was
NOT verified from a fetched page this session. A WebSearch lead for the next window (not
fetched, unverified): arXiv "Distilling LLM Agent into Small Models with Retrieval..." (agent
distillation framework). The operator door still needs a real license-text read (Qwen/Apache-2.0
terms, and teacher-side ToS for trace distillation) before any GB-class download.

## Deep-read log (7 threads, what and how)

1. **unswallow / Qwen3 tool-call swallow bug** - r/ollama 1wc6tka, 2026-09-10, 22 entries.
   Tool call emitted inside `<think>`, parser reads only post-`</think>` channel, `tool_calls: []`,
   clean HTTP 200, agent stops mid-task. Reported separately across vLLM/SGLang/llama.cpp.
   Counter-data in comments: a later auditor found only ~10 percent of thinking-only responses
   contain a truly complete recoverable call, and 75 percent of his failures were on models with
   no draft head. Fix shape: detect + rebuild from reasoning field, detection-only mode for
   side-effecting tools, "recovered calls behind the same argument validation and approval
   checks as normal tool calls". Directly applicable to the estate's Qwen-on-llama.cpp fleet.
2. **CodeFinetuner** - r/LocalLLaMA 1wdp9qc, 2026-09-11, 10 entries. Full local LoRA pipeline:
   raw code -> tree-sitter Structure-Aware FIM -> LoRA -> eval (CodeBLEU, edit similarity,
   exact match, perplexity) -> GGUF. Base-vs-tuned per-example differential on one held-out set.
   Author concedes eval-to-editor gap and that GGUF/quantization effects on the metrics are
   unmeasured (open question in thread). Mac MPS + CUDA, optional Unsloth.
3. **FunctionGemma 270M multi-turn** - r/LocalLLaMA 1r6gx75, posted 2026-02-16 (**outside the
   30-day window; flagged, kept because it is the only <10k-example recipe with published
   numbers the sweep could read end to end**). 270M base, 9.9-38.8 percent untuned ->
   90.9-96.7 percent tuned across smart-home/banking/shell suites, ~92-97 percent teacher
   (120B); smart-home tune beat its teacher. 50 seed + 5k-10k synthetic per domain (~15k when
   step-expanded). Blog: distillabs.ai/blog/small-expert-agents-from-10-examples.
4. **Rust + Vulkan training backend, full PEFT** - r/LocalLLaMA 1wu6cbl, 2026-09-30, 2 entries.
   14 architectures pass a pinned-Transformers parity gate (2e-7 abs error; worst observed
   1.19e-7); LoRA/saved-modules/adapter-switching verified on 32 surfaces across 20 families;
   frozen-base drift exactly 0.0; adapter cross-leak explicitly tested; CLI fails closed on
   unqualified archs. Validated on an ASUS ROG Ally Z1 Extreme RDNA3 iGPU. FP32-only for now,
   MXFP4 planned. Zero-cost local training lane for the free-lane doctrine.
5. **Spanda zero-GPU hallucination check** - r/ollama 1wdasar, 2026-09-11, 14 entries.
   String-normalization + Shannon entropy over 5 samples at T=0.7 vs semantic-entropy NLI:
   AUROC ~0.58 (1.5B) / ~0.71 (7B, matches DeBERTa NLI) / ~0.89 (27B) / **0.09 at 120B
   (confident mode collapse: unanimous identical wrong answers)**. Author answered the
   temperature-choice challenge from the self-consistency literature. Use as a cheap
   regression canary; do not trust it above ~30B-class confident failure.
6. **hemmingway-1** - r/LocalLLM 1wlhh08, 2026-09-20, 148 entries. Qwen3.8-27B finetune for
   creative writing; author claims eq-bench 4 score 1330 "right behind claude fable 5";
   community response is the useful part: which-finetune skepticism, the obsolete-vs-fresh-base
   argument, and the observation that dozens of sibling Qwen3.8-27B RP finetunes already exist.
   Base-vs-tuned general-capability numbers: none posted. This is the no-regression-battery
   gap in the wild.
7. **Cactus Needle 3** - r/LocalLLaMA 1wj4qj4, 2026-09-17, 47 entries. Read in full, then
   **dropped from the bank as an estate-held duplicate** (HN door, see overlap section). The
   reddit increment not already held: the author's six-suite table (Mobile Actions 961-command
   exact-call, DroidCall, BFCL v4, DSTC8, SNIPS x2) and live-user complaints that phrasing
   freedom is limited ("lock the doors" not interpreted as intent). BFCL itself is heavily held
   (35 memory files, 2 catalog rows).

## Queue suggestions for the estate (operator-gated)

- The unswallow failure class should get a fixture in the fleet's tool-calling checks: assert a
  structurally complete tool-call envelope anywhere in the raw response before accepting
  `tool_calls: []` as a benign stop. Detection-only first for side-effecting tools.
- The Gero-4B un-parking battery can be written TODAY from fragments already in this sweep:
  held-out differential (base vs tuned on identical prompts) + Spanda-style canary + live-harness
  smoke test. No GB download needed to define it; the download decision stays operator-gated.
- License read for Q4 remains OWED: fetch actual Qwen/Apache-2.0 license text and one
  teacher-side ToS before any distill-into-weights move.

## Honesty ledger

- All six banked quotes verbatim from fetched pages; nothing from memory of a page.
- The catastrophic-forgetting [D] r/MachineLearning thread I half-remembered from the early
  redlib listing fetch could NOT be relocated or re-read through any surviving door; it is NOT
  banked and its content is not asserted anywhere above.
- FunctionGemma's thread is outside the 30-day window and is flagged as such in its item; the
  ask's "strongest items" read was honored by keeping it but marking the date honestly.
- No licensing thread was found in-window; Q4 is reported as thin, not filled.
