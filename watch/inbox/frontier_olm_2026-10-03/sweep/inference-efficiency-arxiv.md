# SWEEP: inference-efficiency via arXiv (frontier_olm 2026-10-03, second seat, five-question ask)

stamp: source-fetched: 2026-10-03

Note on this file's history: an earlier seat today left a write-up at this same path answering a
four-question variant (tokens/sec on consumer GPUs, agent-loop latency, cost-per-verdict,
structured-output throughput; its items 2609.31047 DynBranch, 2610.01108 AgSpec, 2610.00954
Tokenomics, 2610.01110 test-time computation, 2609.39972 UBTree, 2609.29707, with 2609.23742 and
2609.26693 already dropped as 20260928-sweep re-banks). Those are treated as KNOWN and excluded
from my bank list. This file REPLACES it with the run for the five-question ask. Separately, the
sibling quantization-and-compression seat today banked RATIO 2609.39801 (their item 1, read end
to end, quantization-and-compression-arxiv.md:14,48) and 2609.18005 Calibrated Instrument (their
line 6 history note); both excluded here as already-banked-today.

## Doors used, degradations honest

- export.arxiv.org/api/query Atom feeds: 8 queries (routing/router; cascade+small-model;
  speculative decoding; early exit; KV cache; efficient reasoning/overthinking/test-time scaling;
  rate-limit/quota x LLM; AMD/ROCm/consumer GPU). All returned full feeds, zero 403s.
- arxiv.org/abs/2609.18005 (the one abs page that answered; 7 parallel abs fetches timed out -
  parallel load, not a door ban; sequential and id_list batching then worked).
- export.arxiv.org id_list batch (2609.17008, 2609.14144, 2609.34712, 2609.32917, 2609.39109,
  2609.39801) - full abstracts verbatim, one call.
- arxiv.org/html full texts: READ end to end - 2609.34712v1, 2609.32917v1, 2609.39109v1,
  2609.39801v1, 2609.17008v1. 404 (no HTML render, not a degradation of a live door):
  2609.18005v1, 2609.14144v1. No fallback fabricated; those two are banked/considered at
  abstract depth and labeled so.
- The recipe's arxiv.org/list/cs.CL/recent and /list/cs.LG/recent doors: NOT run (API coverage
  sufficed). Reported as not run, not as success.

## Pass 1 (broad)

8 feeds, roughly 140 entries; in-window detailed consideration set of 34 named below. Window
2026-09-03..2026-10-03 as the feeds date them. Routing feed (20): 2610.01921, 2610.01153,
2610.00978, 2610.00663, 2610.00493, 2609.39445, 2609.39340, 2609.39109, 2610.00367, 2609.38936,
2609.38660, 2609.38585 FlexRouter, 2609.38108, 2609.38090 Mira, 2609.36926, 2609.36770,
2609.36724, 2609.36301, 2609.36222, 2609.36138. Cascade feed (20): 2610.02048, 2610.01478,
2609.38006 HARISSA, 2609.35279, 2609.34712 RSI-Router, 2609.34287, 2609.33204, 2609.32917
Planner-as-Router, 2609.31135, 2609.30709, 2609.30523, 2609.30096, 2609.35833, 2609.27725,
2609.26621, 2609.23992, 2609.23951, 2609.20152, 2609.19879, 2609.19705. Spec-decoding feed (20):
2610.01439 DRelay, 2610.01108, 2610.00894, 2610.00694, 2610.00623, 2609.39972, 2609.39549,
2609.38795, 2609.38697, 2609.38510, 2609.37617, 2609.37532, 2609.37170, 2609.37029, 2609.37007,
2610.00321, 2609.36590 SEED, 2609.34832, 2609.34538, 2609.34388. Early-exit feed (15): 2609.36590,
2609.29382, 2609.18005, 2609.17008 FlexEE, 2609.15131, 2609.14419, 2609.14144, 2609.11516,
2609.05275, 2609.04778, 2608.28846 (out of window), 2608.10251, 2608.08809, 2608.19232,
2608.00573. KV feed (20): 2610.01892, 2609.40127, 2609.40118, 2610.00412 EchoPress, 2609.39329,
2609.39131, 2609.39068 SparseEngine, 2609.38169, 2609.38121 WUSH-KV, 2609.38261, 2609.37261,
2609.37062 vSkipper, 2609.36546, 2609.36322 Periodic Weak Spots, 2609.36202, 2609.36032,
2609.35750, 2609.35629, 2609.35621, 2609.35591. Reasoning feed (15): 2610.01934, 2610.01110,
2610.00991, 2610.00541, 2609.40316, 2609.39801, 2609.39632, 2609.39334, 2609.39220, 2609.39109,
2609.38332, 2609.35748, 2609.35695, 2609.34639, 2609.33974. Rate-limit feed (15): nothing
in-window on provider rate-limit shapes; nearest are 2607.17525 FailureAtlas and 2607.15899
ContinuityBench (both 2026-07, outside window), 2608.17485 KeyPooling (2026-08-18, outside
window, prompt-cache isolation), 2608.00303 CrystalMem (outside window). AMD/consumer-GPU feed
(15): nothing in-window AMD-specific; nearest 2609.20250 (sub-3B models on an 8 GB consumer GPU,
feed-dated 2026-07-29, outside window), 2608.00008 (J/tok energy of local 0.5B/1.1B, outside
window).

## Pass 2 (deep, end to end)

Five items read at full-HTML depth this seat: 2609.34712, 2609.32917, 2609.39109, 2609.39801
(read for dedup before the sibling overlap was found; not re-banked), 2609.17008. Two more at
abstract depth: 2609.14144 (id_list verbatim abstract; HTML 404), 2609.18005 (abs page; HTML 404).
Two considered at feed-abstract depth only: 2609.38006 HARISSA, 2609.36322 Periodic Weak Spots.

## Answers to the five research questions (this seat's evidence, no estate measurement run)

**RQ1 (0.8B-router result on the question-class split; can a tiny router fill UNMEASURED cells at
negligible cost?).** Not measured on the estate here - no grid cell was filled; instruments-only
law (memory/rib/RIB_MODEL_GARDEN_ROUTING.md:47-53 via lens/laws.md:30) forbids importing paper
numbers into cells. What the window adds: (a) RSI-Router routes at SUBTASK level, not task level,
and its ablations found direct difficulty-based routing underperforms random - consistent with
the estate's question-class axis (readable vs simulation, lens/laws.md:29) being the right
feature and raw difficulty the wrong one; (b) Planner-as-Router fills cells with NO trained
router at all (the planner assigns tiers, training-free) and still lands 44 percent cost cut for
2.9 points, but its own limitations section admits 54 tasks, plus-or-minus 6pp CIs, and NO
statistically separable accuracy gains - the transport-is-not-quality lesson
(lens/laws.md:31) in the paper's own words; (c) T-Router is NOT a dispatch router despite the
name (it is internal compute reuse inside one backbone) - its transfer is the 0.466-percent-
parameter RL uplift of a frozen 9B (83.64 vs 73.79 full GRPO), i.e. make the mid tier smarter
instead of routing asks down. Net: the window supports tiny-router cost fill for readable-class
asks only; nothing read validates a premium-to-small route for the simulation class (the estate
holds 0/5 there, lens/laws.md:29).

**RQ2 (rate-limit shapes; owed limit-kill census).** No in-window arXiv paper on provider
rate-limit shapes was found in any of the 8 queries (the rate-limit query returned only
outside-window infra papers: FailureAtlas 2607.17525 HTTP-200-corrupts-state taxonomy,
ContinuityBench 2607.15899 stateful multi-provider failover, KeyPooling 2608.17485 cross-account
prompt-cache reads - listed, not banked, all pre-window). The Groq/Gemini shapes the estate banked
(burns.md:99-101) got neither confirmation nor contradiction this window. The owed limit-kill
census probe (burns.md:119-123) remains owed; this sweep did not run it.

**RQ3 (LEDGER five-day silence: telemetry break or spend stop; which instrument answers).**
ANSWERED FROM BYTES THIS SESSION. The instrument is the usage.jsonl cross-check. Read: LEDGER
tail via Get-Content -Tail shows the last row ts 2026-09-28T13:45:00Z (agrees with
lens/burns.md:37-40). usage.jsonl counts via Select-String per date prefix: 2026-09-29 = 0,
2026-09-30 = 0, 2026-10-01 = 236, 2026-10-02 = 5, 2026-10-03 = 1034, 1275 lines total. Tail rows
read: 2026-10-03T22:56:32Z..22:56:47Z, DND0_beat7/8 ids, one ok:true claude-opus-5.5 dispatch at
cost_usd 0.0143, three ok:false zero-token rows. Verdict: the silence is a TELEMETRY BREAK of the
LEDGER.jsonl wave-ledger instrument, not a spend stop; per-dispatch tank accounting
(memory/runs/hermes_burn/usage.jsonl) stayed live through 2026-10-03T22:56Z. Caveats: usage.jsonl
covers hermes_burn dispatches only; and its tail is 3-of-4 failed zero-token rows - spend is
thin-but-alive, and the ok:false cluster is itself a finding (DND0 beats failing at dispatch).

**RQ4 (deepseek thinking re-scope moving an ask-class premium to mid; cost-per-blind-point).**
No estate measurement was run here; cost-per-blind-point (lens/laws.md:31) stays champion and
unchanged. Window evidence adjacent to the re-scope (53f56d0f3, burns.md:180-183): RATIO shows
PTQ inflates overthinking on QUANTIZED reasoning models and training-free token penalties cut CoT
up to 51.3 percent while ADDING up to 9.8 accuracy - i.e. the mid tier's thinking cost is
controllable at the token level, per-stack (AWQ vs GPTQ corrections differ, matching the
estate's per-stack measurement law); T-Router shows a frozen mid-size backbone can be lifted past
full-parameter GRPO at 0.466 percent of the parameters - an alternative to re-routing asks:
upgrade the mid tier instead. Neither moves an ask-class by itself; both equip the mid tier.

**RQ5 (which techniques measurably help the gemma janitors on RX 5600 XT; ignore-DeepGEMM
verdict).** (a) Early exit is the most transferable class: FlexEE's own numbers show the gains
GROW as memory tightens (1.27x at 0 percent offload vs 3.16x at 50 percent offload, Llama2-7B;
3.29x at 75 percent), and its stated sweet spot is small-batch memory-constrained serving - the
6 GB RX 5600 XT regime - but it was measured on an NVIDIA RTX PRO 6000 96 GB with FlexGen-style
CPU offload, so portability to RDNA1 is unmeasured, algorithm-level only. (b) Depth calibration
(2609.14144): per-deployment exit-threshold tuning raised exit rates up to 59pp - the per-
deployment analog of the estate's question-class routing; abstract depth only (HTML 404). (c)
Speculative decoding: the window's drafter-tree papers (DRelay, UBTree, EAGLE-class) all assume a
second model resident; on 6 GB running gemma:2b there is no drafter headroom, so the self-
speculative variant class (SEED 2.7x on 4B-scale, feed depth; FlexEE's training-free self-
speculation, full read) is the one that fits. (d) KV reuse: the estate already banks the
frozen-prefix win (6.5 to 98 percent cache hit, memory/rib/RIB_SELF_MY_EFFICIENCY.md via
lens/laws.md:23); the window's fresh contribution is a caution, Periodic Weak Spots: chunked KV
compression has phase-dependent retrieval holes up to 40pp - relevant when the janitors' contexts
get compressed. (e) ignore-DeepGEMM stands: nothing read contradicts lens/laws.md:90; the NVFP4
land (quant seat's Minima findings) confirms accelerator-native-kernel dependence, and this
window produced zero AMD-portable kernels. The steal remains the JIT-plus-disk-cache pattern.

## Overlap greps (commands run)

Select-String -SimpleMatch per ID over catalog/catalog.jsonl: 2609.34712 = 0, 2609.32917 = 0,
2609.39801 = 1 (sibling-quant banked; excluded), 2609.17008 = 1 (auto-digest row only),
2609.14144 = 0, 2609.39109 = 0, 2609.18005 = 1 (sibling-quant known; excluded), 2609.36322 = 0.
The three 1-hits resolve to the state/arxiv auto-digest pipeline: state/arxiv/2026-09-16/
2609.17008v1.txt, state/arxiv/2026-09-17/2609.18005v1.txt, state/arxiv/2026-10-01/2609.39801v1.txt
(Get-ChildItem name listing run this session). Memory curated dirs (memory/rib, memory/frontier,
memory/lenses, memory/percolator, memory/press, memory/runs/hermes_burn; *.md,*.jsonl,*.json):
ZERO hits for all 8 titles and IDs. Sibling sweeps today (this run's sweep/*.md and
frontier_olm_20260928/sweep/*.md): hits only in quantization-and-compression-arxiv.md lines 6/14/48
and quantization-and-compression-x.md line 146, all naming RATIO 2609.39801 / 2609.18005 - both
excluded from my bank. Honest scope limit: full recursive grep of all of memory/ (session JSONLs
included) NOT run, for runtime - same limit the earlier seat declared.

## OWED / not run

- No estate grid cell filled, no A/B fired: the Q4_K_M-vs-q8_0 probe, the limit-kill census, and
  a cost-per-blind-point re-measure under the thinking re-scope all remain owed and untouched.
- 2609.14144 full text: HTML 404; only the verbatim abstract read. PDF not fetched.
- 2609.38006 HARISSA and 2609.36322 Periodic Weak Spots: feed-abstract depth only, banked as
  such with lower confidence.
- The recipe's /list/cs.CL and /list/cs.LG doors not run (API sufficed); reported, not faked.
- RQ2 has no in-window arXiv evidence at all; if the estate wants rate-limit shape intel, arXiv
  is the wrong door - provider status pages and the owed census probe are the instruments.

## Banked items (strongest first; receipts in the submitted result)

1. RSI-Router 2609.34712 (full read) - subtask-level small-model routing, 8.1-82.2 percent cost
   cut at par-or-better performance; difficulty-only routing underperforms random.
2. Planner-as-Router 2609.32917 (full read) - training-free plan-time tier routing, 44 percent
   cost cut for 2.9 points; its own CIs admit no separable accuracy gain.
3. FlexEE 2609.17008 (full read) - KV-compatible early exit + self-speculation; gains grow with
   memory pressure (1.27x to 3.29x) - the offloading regime the janitor tier lives in.
4. T-Router 2609.39109 (full read) - 0.466-percent-parameter RL beats full GRPO on a frozen 9B;
   NOT a dispatch router; the mid-tier-upgrade lever.
5. One Size Does Not Fit All 2609.14144 (abstract depth) - per-deployment exit calibration, +59pp
   exit rates; only traffic-aware threshold tuning was worthwhile of three ways.
6. HARISSA 2609.38006 (feed depth) - inference-time self-checks within one point of CoT at 2.7x
   lower latency for LOCAL deployments - janitor-tier CoT replacement candidate.
7. Periodic Weak Spots 2609.36322 (feed depth) - chunked KV compression retrieval varies up to
   40pp by phase - caution for compressed-context janitor serving.
