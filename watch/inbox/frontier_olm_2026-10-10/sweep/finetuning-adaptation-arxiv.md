# Sweep: finetuning-adaptation via arxiv (2026-10-10)

source-fetched: 2026-10-10. Doors used: arXiv export API (`export.arxiv.org/api/query`, Atom renders as text, no 403s, no fallback needed) for pass 1; `arxiv.org/abs/<id>` pages for pass 2 deep reads. Seat: sweep-finetuning-adaptation-arxiv (dwfrun child).

## Pass 1: broad sweep

Four API queries (cs.CL LoRA/low-rank, cs.LG quantization-aware, cs.LG test-time training, cs.CL distillation+small-language-model), sorted by submittedDate descending. Candidates inside the 30-day window (since 2026-09-10): 46 items considered (8 QAT, 16 TTT, 15 LoRA/PEFT, 7 distillation). Pass-1 feeds rendered fully; the first LoRA query timed out once at 60s and succeeded on retry with a narrower phrase (`"low-rank adaptation"`).

## Pass 2: deep reads (11 abs pages fetched and read; 5 required)

Items banked, zero hits in catalog/catalog.jsonl (verified by `grep -F -c` per exact title). CORRECTION (post-submit, same session): a delayed overlap grep of memory/ plus the 2026-10-01 prior edition of this same sweep series (watch/inbox/frontier_olm_2026-10-01/sweep/, quantization-compression lane) shows items 4 and 6 were ALREADY deep-read and banked there on 10-01. They stay listed below as re-confirmations, not new banks. Effective NEW banks: 6 of 8.

GENUINELY NEW (no estate holding found, catalog + 10-01 sweep series both 0):
1. 2609.34924 Audit the Scaffold, Not the Checkpoint (2026-09-28)
2. 2610.05277 Mind the Gaps: ASTRA closed-form repair (2026-10-04)
3. 2610.05303 ASCENT: online agentic TTT (2026-10-04)
5. 2610.09202 CanonQ W2A4KV2 (2026-10-06)
7. 2609.38718 MetaSteer (2026-09-30)
8. 2610.05484 Universal TTT (2026-10-04)

RE-CONFIRMED, sibling-banked 10-01 (my read is independent; content agrees):
4. 2609.39223 QATFactory (2026-09-30): held in 10-01 sweep quantization-compression-arxiv.md + open-local-language-models-arxiv.md + DIGEST.md ("read this session", "strongest reproducible recipe")
6. 2609.39346 Reusable Latent Correction (2026-09-30): held in 10-01 sweep quantization-compression-arxiv.md ("Deep-read: abs page, twice")

Near-name collisions to disambiguate in the ledger (checked, all different works):
- Banked ASCENT (2610.05303) vs held "Ascent: An Agentic System over the Model Context Protocol" (catalog, ingested 2026-09-22) and vs the internal ASTRA campaign log titles containing lowercase "ascent".
- Banked ASTRA paper (2610.05277) vs the estate's internal ASTRA ask-campaign.

Held items confirmed by overlap grep and ALSO deep-read this session (not re-banked; enriching prior art):
- 2609.26708 Train Where the Quantized Model Goes (catalog id 445f345aa09f, state/arxiv/2026-09-23/)
- 2609.40063 LARC (id c4674865113f, state/arxiv/2026-10-01/)
- 2609.23449 PSD (id 6e4ae70b40b3, state/arxiv/2026-09-22/)
- 2610.12002 Agentic-TTT (id 6ae1751acd00, state/arxiv/2026-10-09/)

Key overlap discovery: the estate has a daily arxiv abstract-ingest lane banking `state/arxiv/<date>/<id>v1.txt` (1.4-2.2KB abstract dumps) with 1-2 day latency (2610.12002 submitted 10-08, ingested 10-09). Also: the estate's internal ASTRA is an ask-campaign (`ASTRA VS CHEAP`, blind-staged 2026-09-12, catalog rows `=== m03-astra-moonshot...`), NOT the arXiv paper 2610.05277; same name, different thing, so the paper is new but the ledger must disambiguate.

## Research-question answers

Q1 (living-weights falsifier; cheap distillation single-host): Audit-the-Scaffold gives the missing taxonomy: three regimes (fixed-class search, test-time training, scaffold rewriting) separated by whether the reachable edit set expands; "An auditor who checks whether a system's weights are frozen is checking the wrong thing." For RIB_LIVING_WEIGHTS_BY_NATURE the falsifier should be restated on the reachable edit set: a lesson class needs weight change only when no scaffold edit (receipt/rail/rib) expands reach to it. The cheap path now exists and is measured: ASTRA repairs via one closed-form linear system per sample, 2.7 s/sample, no optimizer or backward pass, 66.7% vs 48.4% Pass@1 over LoRA/AlphaEdit/STAR baselines (code-API drift, Python/Rust). ASCENT supplies the online mechanism: verified trajectories self-distilled (frozen self as hindsight teacher) into persistent LoRA fast weights, no external teacher. LARC (held) shows the minimal carrier: 12,288 trainable params on frozen MiniCPM5-1B with slow/fast states.

Q2 (QA/low-rank vs babelfish record path, measured): quality-side measurements at janitor scale now exist: CanonQ at W2A4KV2 on LLaMA3-1B/3B/8B and Qwen3-1.7B (up to 14.28x lower WikiText-2 ppl, up to 57.9% higher zero-shot accuracy vs prior SOTA; MobileLLM-Pro-1B +41.7% HumanEval); QATFactory exports Q4_K straight to llama.cpp/vLLM, no lossy conversion, LoRA training mode supported (experiments 8B-230B on H100s though); held 2609.26708 lifts 2.79-bit MATH-500 retention 35%->70%. NOT MEASURED anywhere: adaptation cost in labor/documentation units comparable to babelfish's 2,778 claim lines -> 151 invariant / 109 instrument / 2058 register rows (fa0927b93). The weights-vs-records cost falsifier remains estate-original work; no paper runs it. OWED: a single-host gemma-2b QAD run with hours-logged vs hours-of-rib-authoring for the same lesson class.

Q3 (steering-free covering rails): partially. RLC covers the guidance class: one-off black-box LLM guidance converted to persistent hidden-space corrections retrieved by reasoning state, no parameter updates, no online calls (reasoning benchmarks only, no agentic loop). But the strongest online method (ASCENT) abandons steering-free and writes LoRA; MetaSteer moves the other direction, compiling steering into low-rank attention adapters with zero-shot concept transfer. The frontier is converging on rails-as-weights from both sides. No paper shows TTT acquiring rule-like workflow law (estate receipts class); nearest is Vision-ARC rule induction (2609.21181, not banked, vision domain). Audit-the-Scaffold independently supports the estate's rail habit AND its fan-out width law: best-of-k width buys rate not budget; on 30 same-family workers failure overlap is maximal and majority voting fails 42% of tasks (diversity, not width, lifts the ceiling).

Q4 (academic gap blocking?): No. The export API door works (this sweep ran on it), and the estate's own daily ingest lane already holds 4 of my 11 deep-read candidates as abstract rows within 1-2 days of submission. The real remaining delta is read-tier digestion (the lane banks 1.4-2.2KB abstracts, not method detail); the 30,751 course rows cover pedagogy, not 30-day-fresh methods. This sweep's 8 banked reads are that digestion. OnlineQAT 2610.09346 (Qwen3-1.7B) confirmed already held day-9 prior art; not re-banked.

## Driving-ladder feed

Whether a finetuned local model buys a rung is now cheaply testable in the estate's own runtime: QATFactory (Q4_K -> llama.cpp, LoRA mode) + CanonQ-class recipes at 1-1.7B mean a quantization-aware-finetuned janitor deployable via Ollama GGUF with measured retention numbers to beat (CanonQ W2A16KV16 MobileLLM-Pro-1B, OnlineQAT W3A16 Qwen3-1.7B). SHERPA cheap-first leg: PSD (held) shows Qwen3-0.6B/1.7B matching GPT-4.1-mini on LoCoMo memory tasks with zero teacher logits, single-host at both train and deploy.

## Honesty ledger

- All reads were arxiv.org abs pages (abstract + listed metadata); no full-text PDF/HTML bodies were read this session (OWED if method internals are needed: ASTRA's linear-system formulation, ASCENT's population-target analysis).
- QATFactory/ASCENT/uTTT page-listed compute details were absent; where a number appears above it is from the abstract page, cited in the SweepResult quote or why fields.
- The first background grep through memory/ completed late (after submission); it surfaced `QATFactory` in memory/trajectory/steps.jsonl, which traced to the 10-01 sibling sweep's own overlap commands, which led to the correction above: QATFactory and Reusable Latent Correction were sibling-banked on 10-01. The submitted JSON's overlap fields for those two items said "catalog 0, genuinely new"; the catalog counts are real but the inbox sweep layer is also a holding surface. This file carries the correction; downstream readers trust this file over the JSON note for those two rows.
- Grep verification commands run this session (all against repo root): `grep -F -c "<exact title>" catalog/catalog.jsonl` for all 8 banked + 5 held titles; `grep -r -l -F "<title>" watch/inbox/frontier_olm_2026-10-01/` for all 8 banked titles (2 hits: QATFactory, Reusable Latent Correction); context reads of the matched sibling files.
