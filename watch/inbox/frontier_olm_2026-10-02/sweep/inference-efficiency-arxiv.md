# SWEEP: inference-efficiency via arxiv (frontier_olm 2026-10-02)

- Seat: sweep-inference-efficiency-arxiv gopher.
- Stamp: source-fetched: 2026-10-02.
- Doors used: arXiv export API (export.arxiv.org/api/query) for 9 listing queries (one returned
  totalResults 0: "prompt cache" + "collision"), arxiv.org/abs pages, arxiv.org/html full text for
  6 deep reads, arxiv.org API id_list fetches, WebSearch for the vLLM upstream-fix check. No door
  403ed or degraded; the mcp web_reader door 1302-rate-limited mid-pass and I paired to the
  WebFetch/API doors per the doors law (watch/inbox/frontier_olm_2026-10-02/lens/doors.md:13-14).
- Pass 1: ~150 candidate listings considered from the last 30 days across queries: "KV cache"+recompute
  (30), "prefix caching" (30), "TTFT" (30), "SpikingBrain" (1), "cache invalidation" (15),
  "linear attention"+"serving" (20), "vLLM"+"cache" (20), agent+cost+cs.CL (20). Pass 2: 6 items read
  end to end (full text via arxiv.org/html): EfficientAgent, Preserving Provenance, SuffixReplay,
  SketchSSM, Tokenomics of Agentic SLM Ensembles, ATTUNER; plus the cua-speedrun abs page.
- Overlap instruments run this sitting: `grep -rilF "SpikingBrain"` and `grep -rilF "recompute" |
  grep -rilF "cached share"` over catalog/catalog.jsonl + memory/; then
  `grep -rlE "EfficientAgent|PrefixBench|SuffixReplay|Provenance in Shared KV|Who Pays for the KV|ATTUNER|SketchSSM|Tokenomics of Agentic|Cache-Induced Divergence|Contiguity, Not Importance|CacheReforge|CacheRepair|KVCMAS|Recomputation-Free"`
  over catalog/catalog.jsonl, memory/, and watch/inbox/frontier_olm_2026-10-02/; plus the same
  alternation against the 09-30 and 10-01 sweep DIGESTs (zero hits for the banked seven).
  Known-item hits found: Cache-Induced Divergence (2609.04748) in catalog + ARXIV_REGISTER +
  MAP_BACKFILL; Who Pays for the KV Cache (2609.24991) in ARXIV_REGISTER + MAP_BACKFILL +
  kv-agents-week lane; PrefixBench-H100 (2609.19657) in kv-agents-week + arxiv-memory-week lanes;
  Contiguity Not Importance + CacheReforge in catalog/kv-agents-week. Those five are NOT re-banked.
  SpikingBrain (2509.05276) is banked (catalog + memory/runs/gathering_expedition/). The seven
  banked below matched nothing in catalog, memory, the prior DIGESTs, or the 10-02 lens dir.

## Answers to the four research questions

### Q1. KV-recompute versus prefill beyond the banked 17.5/33.1/~49.4 pct decomposition and ~60 pct fill cliff

The decomposition is now hardware- and admission-conditioned, not flat:

1. EfficientAgent (2609.33762, 2026-09-27, code public at
   https://github.com/KunmingSHAO/efficientagent_release) measures the recompute side on agentic
   replays (SWE-bench Verified via OpenHands CodeActAgent; 4,427 calls, 147.1M prompt tokens).
   Without a host tier, 98.1 pct of prompt tokens were recomputed after eviction; sizing the host
   tier to the estimated reuse working set (11.4 GiB/rank at concurrency 16) cuts computed prefill
   76.7M to 5.3M tokens (93.1 pct) and makespan 209 to 128 min. The sign flips by GPU: offload beats
   recompute only where GPU compute per host-link byte is low (RTX 3090 and H20 at ~2.2-2.3K
   FLOP/byte); on H800 (~15.5K FLOP/byte) offloading slows every run 1.08-1.87x. Admission policy
   must be capacity-conditioned: a fixed write-admission filter wins below the working set and
   loses 4.3x prefill above it. This is a reproducer-ready law for the FAMILY_TABLE lanes: offload
   is not free, it is a per-hardware threshold. Caveat: replay measures serving performance on
   fixed trajectories, not free-generation task quality.
2. ATTUNER (2609.36722, 2026-09-29) removes recompute from the other direction: keep the artifact
   KV frozen, train query-side LoRA adapters (<0.05 pct of parameters) so cached keys/values are
   attended correctly; up to 3.73x speedup over full prefill out-of-domain with 0.5-1.8 pct TTFT
   overhead versus PIC, quality within 0.51-1.61 points of full prefill in-domain. It also gives
   the diagnosis the banked decomposition lacked: cached representations are faithful and positional
   mismatch is minor; the loss lives in attention routing across artifacts. No GPU model named in
   the text (OWED: hardware unverified); no code link found (OWED).
3. Reproduction outside the original stack: EfficientAgent ships code and spans three GPU families;
   Preserving Provenance (below) reproduces its findings across vLLM 0.9.2 and two SGLang releases.
   PrefixBench-H100 (2609.19657) is the estate-known characterization frame for exactly this
   reproduction question (kv-agents-week lane already carries its clone plan), not re-banked here.

### Q2. Cache-invalidation classes like the vLLM tool-schema key-order bug (78 to 95 pct cached share)

Direct hit, and the estate's banked bug class now has a systematic study with fixes implemented in
both stacks:

- Preserving Provenance in Shared KV Caches (2609.38706, 2026-09-30) names "provenance-blind
  reuse" and audits three vLLM 0.9.2 connectors (LMCache, SharedStorageConnector, Mooncake) plus
  SGLang 0.5.20 and 0.5.8.post1 HiCache, 12 models from 7 families (0.5B-32B), 160+ configurations,
  on RTX 6000 Ada and RTX PRO Blackwell hardware. Measured classes: cross-adapter collisions drop
  accuracy 0.94 to 0.64 (32 harmful flips vs 2 reversed, p<0.001); KV representation mismatch sends
  reasoning accuracy to zero at every size tested (298 of 299 paired flips harmful on sentiment);
  fp8 weight-version drift collides all forty prompts with 85 pct divergent outputs; salt omission
  enables 93 pct prompt identification at N=100 from timing. Incidence: 83.5 pct cross-provenance
  reuse upper bound (167/200), down to 1.5 pct with always-warm workers. Fix: a KV provenance
  contract (keys injective over computational and sharing provenance), implemented in vLLM and
  SGLang 0.5.20 across three cache paths at a hit-path cost within 0.34 ms, below run-to-run
  variation. OWED: no public code repo found in the paper page; upstream merge status in vLLM/SGLang
  releases not verified this sitting (repos not fetched).
- Upstream check (WebSearch 2026-10-02): no shipped upstream fix for the tool-schema key-order
  class itself was found. What exists: CVE-2025-25183, vLLM prefix-cache hash-collision DoS, fixed
  in v0.7.2 (https://www.miggo.io/vulnerability-database/cve/CVE-2025-25183); the open GitHub issue
  vllm-project/vllm#54487 on prefix-caching hash changing with cache-hash config; and the vLLM docs
  note on mechanisms "to reduce potential hash value collision"
  (https://docs.vllm.ai/en/v0.17.1/design/prefix_caching). So: the class is published and
  prototype-fixed in research code, CVE-fixed in its DoS variant, but not merged as a provenance
  contract upstream per this search. The estate's own defense stays the prefix-freeze law
  (byte-identical system/tool-schema prefix, memory/runs/gapwave/_owed_live_all.json:6759).

### Q3. Linear-attention, hybrid, or neuromorphic serving results with TTFT tables comparable to the banked SpikingBrain-7B table (7.3x at 256k to 26.5x at 1M on H100s)

- SuffixReplay (2609.33477, 2026-09-27) publishes real TTFT tables for hybrid linear-attention
  models (OLMo-Hybrid-7B, Qwen3.5-4B, Qwen3.6-27B-FP8) on a single 80 GB H800: median TTFT cuts of
  15-20 pct (ShareGPT), 20-40 pct (ToolMind ~5K), 55-70 pct (ToolMind beyond 16K); 3.9-5.1x median
  TTFT on an 8-session branching probe (369 ms to 72-94 ms); 2.3-4.3x SGLang throughput when the
  working set exceeds HBM; quality 91.4-100 pct of full prefill on LongBench/RULER. Different axis
  than SpikingBrain (prefix caching on hybrids vs prefill speedup on a native linear architecture)
  but the first table I found this pass that is directly comparable in shape on gate-admissible
  datacenter hardware (H800 passes arch/VRAM/software/workload gates; price trigger is the operator's
  call). Implementation is on SGLang v0.5.18, ~1.2K lines; no code repo found (OWED). Fail modes:
  recurrences without decay are out of scope; OLMo needs k=512 anchors; synchronized fixed-length
  hits can regress TTFT 121 vs 143-174 ms.
- SketchSSM (2609.33051, 2026-09-27) is decode-side only (no TTFT tables, so it does not meet the
  comparability bar): linear-attention kernel speedups 7.78x/5.22x/5.20x for Mamba-2/GDN/KDA and up
  to 2.64x decode throughput, evaluated on NVIDIA B300 including GLM 5.3 Flash (KDA) and Qwen3.8
  Flash-Next (GDN), weights NVFP4. Note for the estate: the session model's own family (GLM Flash)
  now has a published serving-efficiency treatment. B300 fails the estate's five GPU gates today
  (price trigger, memory/rib/RIB_GPU_LADDER_20261001.md:10-24).
- Neuromorphic: the "SpikingBrain" query returned only the original paper (2509.05276). No new
  SpikingBrain-class TTFT table post-10-01 was found this pass. Tail-Replay (2608.30310) and DASC
  (2608.30386) are older-than-30-day-edge hybrids already outside the window edge (08-31).

### Q4. Frontier's measured efficiency per landed deliverable (tokens or dollars per artifact)

No standard tokens-per-artifact denominator exists yet; the frontier's closest instruments:

- Beyond Leaderboards: Tokenomics of Agentic SLM Ensembles (2610.00954, 2026-10-01, post-10-01)
  defines goodput as "the ratio of useful final-output tokens to total compute tokens consumed by
  the system" and reports orchestration tokens at ~45-47 pct versus exploration ~25-31 pct; best
  ensemble 97.34 pct strict prompt accuracy vs gpt-5.4's 91.53 pct at lower cost per prompt. Absolute
  dollar figures live in figures, not transcribed text (OWED). Goodput is the nearest published
  neighbor of the descent falsifier's denominator (memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:71-74).
- cua-speedrun (2609.40284, 2026-09-30, https://cuaspeedrun.com) standardizes speed and cost
  benchmarking for computer-use agents across four benchmarks with uniform infrastructure, finding
  no single model family optimizes performance, speed, and cost simultaneously. Per-task cost and
  time on a reproducible rig is the closest per-deliverable meter in the agent space.
- Estate fold: hermes_burn usage.jsonl already banks tokens+cost per turn; the missing piece is the
  per-artifact join (usage row to landed deliverable), which the goodput definition and
  cua-speedrun's per-task accounting both support. No frontier work found that publishes
  dollars-per-landed-artifact as a first-class metric.

## OWED (carried, not asserted)

- vLLM/SGLang upstream merge status of the KV provenance contract: repos not fetched this sitting.
- ATTUNER hardware and code release: absent from fetched text.
- SuffixReplay code repo: absent from fetched text.
- Tokenomics absolute cost-per-sample dollars: in figures only.
- SketchSSM: no TTFT tables, so its Q3 comparability is decode-throughput only.
- The tool-schema key-order bug's own upstream fix: search found the CVE fix class and open issue
  #54487, not the schema-key fix; a targeted vLLM PR hunt is the next leg.
