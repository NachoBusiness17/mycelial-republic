# Sweep: kv-cache-context-engineering via arXiv (frontier_olm_2026-10-02)

source-fetched: 2026-10-02. Lane: sweep-kv-cache-context-engineering-arxiv (dynamic-workflow
actor). Doors: arXiv abs pages, arXiv export API (export.arxiv.org/api/query, Atom XML),
arxiv.org/html full texts, one particula.tech blog post, one z.ai-backed WebSearch. All arXiv
doors returned 200 with real metadata; no 403 or degradation on any arXiv fetch this sitting.
The WebSearch backend (z.ai web_search_prime) hit MCP error -429 rate limits twice before
succeeding on the third query shape; the successful query is quoted below. No door results are
fabricated; everything banked below was fetched and read this sitting.

## Method (what actually ran)

- Pass 1 candidates: five arXiv API listing queries, all sortBy=submittedDate descending:
  (a) all:"KV cache" AND all:agentic, 25 rows; (b) all:"KV cache" AND all:long-horizon, 25 rows;
  (c) all:"KV cache" AND all:security, 20 rows; (d) all:"context compaction" OR all:"memory
  compaction", 20 rows; (e) all:"KV cache" AND all:eviction, 20 rows. Union 110 rows listed,
  45+ distinct items dated 2026-09-02 or later (last 30 days) considered. SPLASH (2609.37626)
  and ActKV (2609.31395) recognized as already banked (monitor_lane_selfsteal_20261002.md:26-75
  and the 10-01 DIGEST register respectively) and excluded.
- Pass 2 end-to-end reads (7): KVarN full PDF (held locally, extracted with PyMuPDF, 17 pages /
  54,824 chars); particula.tech KV-quantization post; arxiv.org/html full texts of 2608.11242,
  2609.04875, 2609.27981, 2609.06853, 2609.39819. Plus abstract-level reads of 2609.40118,
  2609.33536, 2609.34060 and others via id_list batch fetch.
- Overlap instruments run this sitting: `grep -rilF "KVarN"` over catalog/, memory/,
  watch/inbox/ (21 files, decisive ones read); term scans over catalog/catalog.jsonl and
  memory/burns/LEDGER.jsonl for 25 title/id strings; `grep -rilF` per term over memory/,
  watch/inbox/, corpus/ for the seven shortlist names. Catalog hits for 2609.04875 (line
  443100), 2609.27981 (445476), 2609.40118 (806548) are abstract-only snapshots
  (state/arxiv/<date>/<id>v1.txt, 1.6 to 1.8 KB each); full texts are NOT held, so the deep
  reads below are additive, with overlap stated per item.

## RQ1: KVarN (arXiv 2606.03458) - CONFIRMED from two primaries; llama.cpp clause now sourced to a dated secondary, PR number still OWED

- Primary 1 (fetched this sitting): https://arxiv.org/abs/2606.03458 returns real metadata:
  "KVarN: Variance-Normalized KV-Cache Quantization Mitigates Error Accumulation in Reasoning
  Tasks", Muller, Bich, Boretti, Chang, Zhuang, Cavigelli (Huawei), submitted June 2, 2026,
  with a vLLM implementation link to github.com/huawei-csl/KVarN in the abstract.
- Primary 2 (already held by the estate, verified this sitting):
  memory/runs/gathering_expedition/p2_2606.03458.pdf, 874,189 bytes, sha256
  c437782e9352790102fde8561aaf2f74c930fed1b6cf44414c7d42ab57571739, landed by the gala
  librarian-expedition 2026-10-01T20:00Z per memory/runs/gathering_expedition/PAPERS_LANDING.json.
  Neither the 10-01 KVarN lane (DIGEST :111-115) nor the burns lens (:183) knew this PDF was on
  disk. Full-text extraction: "llama.cpp" 0 occurrences, "AIME25" 0 occurrences, "q8" 0
  occurrences; "Hadamard" 21, "AIME" 13, "2-bit" 9, "vLLM" 9. The paper benchmarks MATH500,
  AIME24 and HumanEval at 2-bit precision and claims error accumulation across autoregressive
  timesteps "driven primarily by incorrect token scales".
- The banked UNCONFIRMED status resolves: the paper is real, the method claim (Hadamard
  rotation + dual-scaling variance normalization on both axes of K and V) matches the archived
  Reddit selftext, and the vLLM speedup clause matches the abstract's implementation link.
- The llama.cpp kv-rotation clause (DIGEST :114 "UNSOURCED-OWED"): now attested by an
  independent dated secondary fetched this sitting, particula.tech
  /blog/kv-cache-quantization-accuracy-loss-benchmarks (Sebastian Mondragon, 2026-08-03):
  "On 2026-04-01, mainline llama.cpp merged a change that applies a normalized Hadamard
  rotation to Q, K and V before they are cached", with AIME25 numbers "31.7% to 37.1% at q8_0"
  post-rotation and the gloss "Even q8_0, the setting everyone calls lossless, moved 5.4 points
  from a change to how activations are laid out before caching." The clause's "tanks AIME25"
  wording is stronger than the source's measured 5.4-point recovery; and the blog still names
  NO PR number, so the original ruling stands with one amendment: the finding is no longer
  carrier-less, but a concrete ggml-org/llama.cpp PR reference remains OWED before the clause
  is repeated as sourced. WebSearch leads for that hop (not yet fetched): r/LocalLLaMA thread
  1s720r8 "In the recent kv rotation PR it was found that the existing q8 kv [cache lost
  quality]" and HN item 48739846.
- Queued action FIRED: arXiv 2606.03458 appended to
  memory/runs/corpus_gap_research/ARXIV_REGISTER.json results array (933 to 934 rows, verdict
  REAL, cited_in pointed at the 10-01 DIGEST UNCONFIRMED entry). The register's own
  tally/unregistered_count metadata fields were left untouched (single-line append as queued).

## RQ2: degradation curves over long agentic sessions - the serving papers do NOT publish them (negative finding), the modeling papers do

- KVTether (2609.39819, 09-30, full text read): manages KV for ReAct agents at the harness
  lifecycle level, and its longitudinal measurements are system-level only: zombie-KV
  occupancy ("up to 36.3% of LMCache's capacity"), wrong-direction LRU evictions
  ("71.0-95.0% of LRU evictions are wrong-direction"), hit ratios, latency, cost. No
  perplexity, no task-accuracy curves, no per-session quality metric. Same negative for
  ElasticKV (2609.33536, abstract-level): TTFT and P90 TTFT wins only.
- KVarN is the counter-example: it publishes exactly the degradation-curve surface the estate's
  KV degradation ladder targets, but for reasoning decode, not tool loops: quantization errors
  accumulate across decode timesteps, and it argues "current methods are evaluated under
  prefill-like settings", which is the same critique the ladder makes of single-turn perplexity
  gating.
- Implication for the ladder spec: the ladder will not find a ready-made agentic-session
  degradation curve in the 09-30 serving wave; its needle-bank-over-session-length design
  remains the missing instrument. Risk-Controlled Eviction (RQ4 below) supplies the
  per-request exceedance metric the ladder should adopt for its stop rule.

## RQ3: isolation and sanitization responses to the state-restore flaw class

- Forgetting Without Restarting (2609.04875, 09-04, full text read): execution-state unlearning
  for stateful agents. Threat model covers the exact banked class (state spans compressed
  summaries, plaintext memory, pending tool plans, and "under every serving API a KV cache";
  forget targets enter via revocation, secrets, or indirect injection). Scope limit stated
  honestly: within-session runtime state only, cross-tenant shared KV not discussed. Core
  results: exact unlearning needs at least T-tau+1 recomputed transitions (their method hits
  the bound, 9.3x fewer tokens than full reset, 133 vs 1235); every cheap baseline fails a
  six-probe audit (memory-delete is a behavioral no-op; forget-instruction scores Leak@probes
  1.00, and an introspection probe "what were you told to forget?" re-licenses the value at
  0.87-1.00; source-redaction still acts on a revoked preference in 80% of episodes; IFC-only
  leaks 0.92-1.00 through free text while IFC-plus-replay drops leakage to zero: "state
  cleanup and flow control are orthogonal"). Steal shape for the janitor host: provenance
  graph + checkpoint cropping ("cropping is restoring") + sanitized replay with shadow
  execution and call-ID dedup, paired with IFC.
- Contention-Induced Reliability Collapse (2609.06853, 09-06, full text read): the banked
  llama.cpp 200/200 cross-tenant number is a quiet-system number by this paper's showing: on a
  live multi-tenant vLLM server the KV timing side-channel effect size collapses from d=0.7789
  to d=0.2109 with just two synthetic workers, and "Concurrency-depth variance has the
  strongest measured relation with effect size (r=-0.416)". Two transfers: (a) the janitor
  host's own flaw measurements should be re-run under realistic concurrency before sizing the
  risk; (b) the paper's stated defense axis matches the estate's need: "cache isolation or a
  sharing policy that prevents untrusted principals from obtaining cross-tenant cache-hit
  signals" (it names SafeKV selective isolation and KVGov cryptographic cache-identity
  separation as prior defenses).
- KVCMAS (2609.34060, abstract-level, NOT banked as an item): shared-context KV correction for
  multi-agent systems; overlap note: named only as a grep term in the sibling lane
  inference-efficiency-arxiv.md:17 of this same fold, not banked there.

## RQ4: compaction that preserves law-critical context at the 96.6% removal scale, and worst-event reach measurement

- Lost in Compaction (2608.11242, 2026-07-31, full text read; outside the 30-day window, banked
  anyway as a genuinely new primary that instruments a concept the estate already holds):
  defines Session Constraints (user instructions that are not the task but bind the session,
  e.g. "Before you run a command, send a message, or make a change, show me what you're about
  to do and wait for my go-ahead" - the effect-broker gate in constraint form) and ships the
  COMPINT benchmark (100K-token contexts x chat / agentic / research scenarios; retention,
  compliance, and effect-retention metrics). Headlines: compactors "retain only 17% of injected
  SCs on average" at roughly 182x compression; most compactors score worse than no compaction;
  the proposed SC-aware extractor holds over 90% retention; per-event retention for the best
  commercial compactor swings from 98% down to 6.7%, and one open-model compactor drops to 0%
  across all five constraint types. This is the estate's 96.6% single-event removal caught as a
  systematic, measurable surface, and it is the direct instrument upstream of the reach-ratio
  meter: retention and compliance per event, not average recall.
- Governance-decay overlap: the concept is already estate-known
  (memory/research_packs/COMPACTION_ALGO_RESEARCH_20260919.md:32 "governance decay:
  summarization silently eroding agent alignment (2026 arXiv)"); 2608.11242 is the measured
  benchmark behind the concept, so it banks as instrumentation, not as a new thesis.
- Risk-Controlled KV-Cache Eviction (2609.27981, 09-23, full text read; catalog holds
  abstract-only): the worst-event reach instrument the ladder lacked. Defines material
  degradation as a per-request exceedance V_tau(X;pi)=1{U_full-U_pi > tau}, deployment risk as
  its population frequency, and certifies eviction policies with finite-sample guarantees
  (Learn-then-Test), falling back to full KV when nothing certifies. Headlines: "a small
  average loss can hide requests whose utility degrades materially"; SnapKV certifies at 75%
  retention on LongBench but NO tested policy certifies on RULER-32K; certification selects
  retention 5 to 10 points higher than empirical thresholding; and mixture-level certificates
  still hide per-task risk as high as 29% (RULER CWE). This maps one-to-one onto the estate's
  worst-event reach problem: replace "utility" with "law-critical context reach" and the
  exceedance-probability certificate becomes the reach-ratio meter's acceptance test.
- Persistent Context Graphs / ReCAP (2609.40118, 09-30, abstract read; catalog holds
  abstract-only snapshot from 2026-10-01): compaction policy that keeps an attention-derived
  importance/dependency graph instead of re-summarizing: reduces compaction and cold-restoration
  latency "by approximately 95% on both Qwen3-Coder and gpt-oss" versus Codex's summarization,
  roughly halves historical context per call at comparable quality, and improves
  Lost-in-Conversation code accuracy by 19.8 and 41.2 points over full history. Steal shape:
  the cold-restore leg matters for the estate's session-restore path (the same path as the
  banked llama.cpp state-restore flaw).

## Item list (strongest first, all read this sitting)

1. Lost in Compaction (2608.11242, 2026-07-31) - constraint-retention benchmark; RQ4 headline.
2. Risk-Controlled KV-Cache Eviction (2609.27981, 2026-09-23) - exceedance-probability
   certification; the worst-event instrument.
3. KVarN (2606.03458, 2026-06-02) - RQ1 confirmation from two primaries; clause amended.
4. particula.tech KV quantization post (2026-08-03) - the dated secondary that sources the
   llama.cpp kv-rotation clause (merge date 2026-04-01, AIME25 numbers, no PR number).
5. Forgetting Without Restarting (2609.04875, 2026-09-04) - state-restore sanitization
   mechanism with failed-baseline census.
6. Contention-Induced Reliability Collapse (2609.06853, 2026-09-06) - load dependence of
   KV side-channel measurements; quiet-system caveat for the banked 200/200.
7. KVTether (2609.39819, 2026-09-30) - agentic KV lifecycle management; negative finding: no
   quality-degradation curves published.
8. Persistent Context Graphs / ReCAP (2609.40118, 2026-09-30) - compaction policy with
   cold-restore numbers; abstract-level read.

## Door health and window caveats

- All arXiv doors healthy (abs, export API, html). WebSearch rate-limited twice (MCP -429) then
  succeeded; recipe fallback not needed beyond that.
- 2608.11242 (2026-07-31) and particula.tech (2026-08-03) predate the 30-day window; both
  banked as genuinely new primaries for their research questions, flagged here per the burns
  lens window rule (new confirmed finds must be post-10-01 or carry a genuinely new primary).
- Not fetched, named for the next lane: r/LocalLLaMA 1s720r8 and HN 48739846 (the concrete
  llama.cpp rotation PR number chase); SafeKV and KVGov primaries (defense mechanisms named by
  2609.06853); the KVarN GitHub repo itself (not fetched; the paper page and PDF were
  sufficient for RQ1).
