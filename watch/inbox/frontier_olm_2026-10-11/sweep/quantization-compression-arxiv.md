# SWEEP: quantization-compression via arxiv (frontier_olm_2026-10-11)

source-fetched: 2026-10-11 - seat: sweep-quantization-compression-arxiv - doors: export.arxiv.org
API (WORKED this sitting, unlike the adhoc run's 429 wall), arxiv.org abs + HTML full text
via curl. Every quote below is verbatim from raw Atom XML or HTML fetched by this seat this
sitting (curl to $TEMP/arxiv_sweep_7.xml, _2.xml, _4.xml, $TEMP/focus_full.html), parsed
with the repo venv python (xml.etree). Exit-code-1 on the last holdings grep is grep's
no-match exit, not a tool failure.

## Pass 1 coverage (candidates, last 30 days)

84 candidates considered across three API queries, all sorted by submittedDate descending:
(1) all:"KV cache" AND all:quantization, max_results=30 (30 rows, 2610.11245 back to
2609.04098); (2) cat:cs.CL AND abs:"quantization", max_results=30 (30 rows of 1,312 total,
2610.12338 back to 2609.36965); (3) abs:"context compression" OR abs:"prompt compression"
OR abs:"memory compaction", max_results=25 (24 unique rows, 2610.11784 back to 2608.19047).
Window: entries span 2026-09-04 to 2026-10-08 by the published dates in my own XML; nothing
banked sits outside the 30-day preference this time.

## Pass 2 deep reads (this seat, this sitting)

13 items read at abstract level or beyond, each from a page I fetched:
- Verbatim abstracts from raw Atom XML (curl + venv python parse): 2609.30854, 2609.37590,
  2609.40118, 2610.09346, 2609.32459, 2610.06251, 2610.11245, 2610.00983, 2609.04875,
  2610.11214, 2610.12338, 2610.03027, 2610.10058.
- Full HTML body read: FOCUS 2609.37590v1 (737,559 bytes; intro, method 4.1-4.4, results
  tables incl. the AppWorld Acc/Steps/Pk/Dep table: No-compression 56.0 vs FIFO 45.8 vs
  Retrieval 27.4 vs LLMLingua 39.3 vs ACON-UT 51.2 vs FOCUS-O 56.5 vs FOCUS-D 64.9; the
  N-ablation table, diminishing returns beyond N=3; latency/cost table 40.2s / $5.96 vs
  47.2s / $9.47 uncompressed; the A.2 theory with the safety-certificate corollary).
- SoK abs HTML also fetched directly (42,983 bytes) as a fetch-check on the XML read.

## THE OVERLAP STORY: why this sweep banks 5, not 13

The overlap gate (greps vs catalog/catalog.jsonl, memory/, ARXIV_REGISTER.json, and ALL 13
days of sibling sweep dirs under watch/inbox/frontier_olm_*) caught 8 of my 13 reads as
already held. That census is itself the sharpest data point this sweep produces (feeds RQ1):
- 2610.11245 ReadKV: BANKED as item 3 by the 10-10 kv sweep (kv-cache-context-arxiv.md:43),
  same 0.66% quote, same overlap class. Re-bank declined.
- 2610.09346 OnlineQAT: held day-9 card + 10-10 delta bank (quant sweep item 6, full-text
  hardware-cost extraction). Re-bank declined.
- 2610.06251 HQQ shared stopping: banked day-6, re-banked-with-delta day-8 (10-10 quant
  sweep :76-77). Re-bank declined.
- 2610.00983 loss scale: "held day-8" per the 10-10 X sweep (:44,161). Re-bank declined.
- 2609.40118 ReCAP: banked by the 10-02 kv lane item 8 (:167-169 per the 10-04 kv sweep :21)
  + full-HTML deep read by the 10-03 agent-memory sweep (:15). Re-bank declined.
- 2609.04875 Execution-State Unlearning: full-HTML read by the 10-02 kv sweep (:21-22),
  "excluded as known" by the 10-05 quant sweep (:50-52). Re-bank declined.
- 2609.32459 Harness Effects: deep-read by the 09-28 sweep (ARXIV_REGISTER verdict REAL).
  Re-bank declined.
- 2609.30854 SoK and 2609.37590 FOCUS: held as census/abstract rows but NEVER banked as
  items; both carried forward below with full lineage.

## Answers to the four research questions (grounded this sitting)

### RQ1: why zero confirmed rows for quantization-compression across three sweeps

Three stacked causes, none of them "mined out" in the coverage sense:
1. THE CONFIRMATION STEP, NOT THE DOOR, IS WHERE ROWS DIED. The adhoc sweep for this exact
   area banked 8 items with full RQ verdicts and overlap statements
   (watch/inbox/frontier_olm_adhoc/sweep/quantization-compression-arxiv.md:102-129), yet
   register.jsonl holds zero rows for the area (my grep this sitting: finetuning-adaptation
   8, open-local-language-models 7, swarm-orchestration 6, kv-cache-context-engineering 2 =
   23 rows total). Register rows were minted where a steal card or $0 probe was distilled
   (frontier_olm_adhoc/DIGEST.md:10); the quant sweep's findings fed RIB_GPU_LADDER and
   corpus/steal targets (its Feeds section) but no card was distilled, so nothing carried
   into the register before the fold. Banked-in-a-sweep-file is not confirmed-in-a-register.
2. LABEL SPLIT. Quantization substance DID clear the bar under adjacent labels: the GSQ/RCO
   3.5-bit quantizer-laws row went in under open-local-language-models
   (frontier_olm_adhoc/DIGEST.md:34-43) and 2 KV-cache rows under kv-cache-context-engineering
   (same register grep). The area label bled from both sides.
3. THE AREA IS PRE-MINED TO THE BONE - and that is the measured fact of this sitting: 8 of
   my 13 deep reads were already held across 13 consecutive daily sibling sweeps (the
   collision census above, each with file:line). What remains unbanked is exactly the class
   my 5 items occupy: nominated-but-never-read candidates (SoK), census-listed-but-never-
   deep-read items (FOCUS, TaSQ, EncBank), and post-crawl arrivals (RAM-Net). A fourth
   generic pass would tie; the yield now lives in the gaps the daily census skips.

### RQ2: what kv_cache_compaction.md claims, and does the owed re-audit validate or strike it

The doc (memory/research_polished/kv_cache_compaction.md, read in full this sitting, 31
lines) claims an 11-pack synthesis: prefix-economics doctrine (DeepSeek flash 50x / pro 30x
cache ratios, corrected 09-25), live hit/miss telemetry, built spike detection, the Sept
compaction fight (recency null humiliates summarization hype), and 5 next actions. I ran the
owed provenance re-audit (burns.md:242) as a SPOT-CHECK, not the full audit:
- models/providers.py:558-570: VALIDATED. Both capture paths present verbatim
  (prompt_cache_hit_tokens and prompt_tokens_details.cached_tokens at :563-564, my sed read).
- Second call site ~:845-870: VALIDATED (same capture at :847-848).
- mag/cost_learn.py:144 _detect_spikes: VALIDATED, with MISS_SPIKE_THRESHOLD = 100_000 and
  MISS_RATIO_SPIKE = 0.20 at :140-141 exactly as the doc's finding 4 states.
- mag/cache_map.py:39-41 MODEL_RATES: flash hit 0.0028 / miss 0.14 = the 50x ratio
  VALIDATED. BUT :40 still carries deepseek-v4-pro 0.003625/0.435 = the stale pre-Sept-10
  120x table the doc itself flags as corrected (kv_cache_compaction.md:9,17): code has not
  caught up to the doc's own correction. One-line fix owed in cache_map.py.
- All cited module files exist (session_maze, cache_router, context_pack, cost_learn,
  auto_quantize, ollama_policy, contamination_tripwire: my ls this sitting).
VERDICT: the doc survives the spot-check and is safe to cite for the flash ratio, telemetry,
and built surfaces; the full re-audit (all 11 packs' external citations) remains larger than
what I ran and stays owed. The one strike-class finding is the stale pro absolutes IN CODE,
which the doc already registers ("re-pull pricing before any economic decision").

### RQ3: is the deliberate-ask quantize target (AGENTS.md:30) still right after the roster churn

Category error in the premise, resolved without a re-measure row: the "quantize target" is
defined by the rib the law points into as a CONTEXT-compression target, not a model or
bit-width pin: "Compress toward: the rails above, the record laws, the current board (what
is live, what is owed). Everything conversational is heat; only the frozen spec persists"
(memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md:64-68, read this sitting). It is
provider-agnostic by construction, and the rib carrying it (2026-10-07) postdates the
09-28 roster changes (Lightning dead, DeepSeek proven, burns.md:59-60), so the roster churn
cannot stale it. The roster-sensitive surface is PRICING, not the target: that lives in
mag/cache_map.py:40 (the stale pro absolutes, RQ2) where a re-measure row would actually
land, and kv_cache_compaction.md:17 already registers the re-pull duty. No new law surface
needed; if anything, a cache_map.py rate-row refresh is the actionable residue.

### RQ4: can distill-don't-dump be wired, and is distillation practiced in mag/ or only doctrine

Practiced, not just doctrine. The doctrine node is an island (exactly 1 occurrence of
"distill" in memory/knowledge_graph.json, zero edges; lens/graph.md:29-31), but the modules
implementing it exist and I read their docstrings this sitting:
- mag/distill.py:1-30: the LIQUID-INTELLIGENCE distillation machine, standing wave sw59-62,
  primitives boil/quantize/distill/trace/cycle, "MANY invariants collapse to ONE".
- mag/max_distill.py:1-11: SkillCandidate v1, "what fraction of a frontier model's verified
  advantage can be recovered as an automatically-extracted, mechanically-applicable policy
  executed by a cheap model on held-out states" - literal knowledge distillation practice,
  with max_distill_arms.py as the arms harness.
- mag/context_compression.py:1-14: the LLMLingua steal (f-005), 2-5x prompt compaction with
  its own laws; mag/verkle_compaction.py and mag/auto_quantize.py (L0-L5 levels, "Anomalies
  are NEVER quantized") complete the cluster.
The wiring gap is the GRAPH BUILDER's, not the estate's: no relation type expresses
doctrine->module (lens/graph.md:29-32), and the builder script was never located
(lens/graph.md:41). Wiring is one edge-type away: distill-don't-dump ->
mag/distill.py + mag/max_distill.py. External support from this sweep: OnlineQAT (held) is
the published on-policy version of "distill exactly the states the cheap student will
visit", which is max_distill's contract read back from the literature; EncBank (banked
below) is the same idea applied to encoder state reuse.

## Banked items (strongest first; 5 of 13 reads; overlap stated per item)

1. 2609.30854 The KV Cache Is the New Memory Wall (SoK, 2026-09-25, cs.DC/cs.LG/cs.PF,
   28pp, single author). FIRST BANK of a candidate the 10-09 kv sweep explicitly nominated:
   "2609.30854 (The KV Cache Is the New Memory Wall, SoK): estate holds stub + tmp xml; not
   read this session; census row only. Candidate for the next lane"
   (frontier_olm_2026-10-09/sweep/kv-cache-context-engineering-arxiv.md:56). Full lineage:
   09-28 kv lane marked it do-not-re-bank as a near hit (:119 per the 10-01 quant sweep
   :21); the 10-01 quant sweep read its abs twice but used it only as context, carrying two
   sentences (:46); never an item anywhere until now. Quote: "Paging and prefix sharing are
   lossless but address capacity, not bandwidth. Quantization and eviction cut bandwidth
   directly, with degradation that accelerates below 4-bit precision and turns
   discontinuous for eviction on position-sensitive tasks." Banked delta: the five-domain
   taxonomy (quantization, token eviction, KV paging, prefix caching, heterogeneous
   tiering), closed-form arithmetic intensity parameterized for H100/B200/MI300X, the
   three-regime structure, and the design rules. Feeds kv_cache_compaction.md's
   bibliography gap-fold G1 with the missing hardware-economics frame.
2. 2609.37590 FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents
   (2026-09-29; Microsoft; 5 authors). DELTA BANK on a held item: prior holdings carry
   only abstract-level stats (10-05 kv-x sweep :70-72 "-48% peak context, +8.9 pts task
   success"; 10-05 quant sweep abs-read :17,68; 10-06 kv sweep "excluded as known" :27;
   census mentions 10-09 :13 and 10-10 :14). My full-HTML read banks what none carried:
   the FIFO/recency arm LOSES 45.8 vs FOCUS-D 64.9 accuracy on AppWorld (no-compression
   56.0, Retrieval 27.4, LLMLingua 39.3), i.e. the published counterexample class where
   test-time causal scoring decisively beats the free recency null without offline
   training - the exact eval bar kv_cache_compaction.md:13 demanded. Plus: draft-model
   Monte Carlo with diminishing returns beyond N=3 rollouts, latency 40.2s and $5.96 vs
   47.2s/$9.47 uncompressed, and the A.2 safety-certificate corollary
   (d(u_i||u_i') <= U(s_i) <= u_i*m_i). Quote: "cutting peak context by up to 48% and
   dependency by 73% while improving task success by up to 8.9 percentage points over
   uncompressed execution."
3. 2610.03027 TaSQ: Tailoring the Quantization Space for 1-Bit KV Cache Compression
   (2026-10-02). First bank: raw abstract stub only (state/arxiv pull, ls grep 1),
   unregistered, never census-named in the 10-01..10-10 quant/kv sweeps I grepped.
   Extends the 10-01-banked WUSH-KV 2-bit transform line to the 1-bit VQ regime with
   RoPE-compatible transforms merged into projection weights, and it lands on the
   estate's shelf lineage: its implementation is SGLang (the lmcache-src/RadixAttention
   family, lens/corpus.md:15) on a single RTX 6000 Ada, with up to 14x larger batch sizes
   and 1.87x peak throughput vs BF16 (numbers normalized from the abstract's Unicode
   multiplication sign for ascii house law). Quote: "TaSQ consistently outperforms
   existing low-bit KV cache VQ baselines while preserving reasoning stability."
4. 2610.11214 Bridging KV-Cache Quantization and Linear Attention: From Theory to
   Pretrained Weight Migration (RAM-Net, 2026-10-08). FULLY NET-NEW: 0 raw-pull rows,
   0 register rows, 0 sibling-sweep mentions (greps this sitting) - post-dates the last
   full census. The theory unification the SoK's taxonomy implies but does not draw:
   per-entry KV compression and recurrent aggregation bridged via soft assignments over a
   discrete address space, with a pretrained-Transformer migration path. Quote: "Across
   nine pretrained Transformer models from 0.3B to 7B parameters, RAM-Net recovers an
   average of 87.1% of the teachers' accuracy gains over random guessing across six
   commonsense and knowledge tasks using only a 500M-token budget per model."
5. 2610.10058 Cache the Encoder Within: Compact, Reusable Memory across LLM Queries
   (EncBank, 2026-10-07). First bank: raw stub only, unregistered, never census-named.
   Generalizes the frozen-prefix doctrine one level up: cache computed MODEL state across
   queries (lower layers as a reusable document encoder + self-distilled suffix adapter),
   4-bit storage within one score point of native precision, adapter shared across
   precisions without quantization-specific retraining. Quote: "4-bit storage keeps each
   reported benchmark aggregate within one score point of native-precision EncBank."

## Overlap instruments

- Per-ID holdings greps run this sitting: catalog/catalog.jsonl phrase greps ("Memory Wall",
  "decision preservation", "Persistent Context Graphs", OnlineQAT, NanoHarness, Shared
  Stopping, ReadKV, Execution-State Unlearning, Optimization Imbalance) via two background
  exec logs (results consolidated in-file); per-ID `ls state/arxiv/*/ | grep -c <id>` for
  all 17 read IDs; per-ID ARXIV_REGISTER.json grep (2609.30854 = 1 row verdict REAL;
  2609.32459 = 1 row verdict REAL; all other banked IDs = 0); and the decisive layer,
  `grep -rl "<id>"` across all 13 sibling sweep dirs (frontier_olm_20260928 through
  frontier_olm_2026-10-10 + adhoc), which produced the collision census above.
- catalog.jsonl is a file census (title = filename, corpus.md:11): raw-pull hits are
  abstract mirrors, not analyses. "decision preservation" and one ReCAP hit resolved to
  this session's own trajectory log and the raw mirror respectively (false friends,
  inspected this sitting).

## Feeds

- memory/research_polished/kv_cache_compaction.md: the SoK's five-domain/three-regime frame
  and design rules belong in its bibliography next to the SGLang/CacheGen/CacheBlend line;
  FOCUS's FIFO-arm numbers belong beside the hermes PR #116246 evidence as the published
  keep/drop-decision line (it beats the recency null the doc's eval bar mandates);
  EncBank is the frozen-prefix doctrine generalized to reusable encoder state. RQ2 verdict:
  cite the doc, fix cache_map.py:40 first.
- memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md: no edit needed (RQ3); actionable residue is a
  mag/cache_map.py pro-rate refresh, owned by whoever next touches pricing.
- knowledge_graph.json wiring (RQ4): one edge type (doctrine_governs_module) + three seed
  edges (distill-don't-dump -> mag/distill.py, mag/max_distill.py;
  stable-prefix-for-cache -> mag/context_pack.py) would wire the loudest island; the
  builder script owner must mint the relation, a lens or sweep cannot.
- Percolator candidates: FOCUS and EncBank are the two steal-card-shaped items ($0-pattern
  adoptability, falsifiable against the estate's own transcripts and telemetry); TaSQ is
  the third if the estate ever serves long-context KV from its own SGLang-class stack.

## Honesty block

- Read end to end this ask: 13 verbatim abstracts from raw Atom XML I curled + 1 full HTML
  body (FOCUS) + the SoK abs HTML fetch-check. All quotes verbatim from those fetches.
  2609.32459 (harness effects) is held prior art (read 09-28, registered REAL); I read it
  at gist level only this sitting and do not bank it.
- Not read: any full PDF beyond FOCUS's HTML; the 71 unbanked candidates.
- Checks run this ask: 3 arxiv API queries + 3 id_list pulls + 2 HTML fetches via curl;
  overlap greps (catalog, memory, ARXIV_REGISTER, all 13 sibling sweep dirs - the last one
  caught 8 collisions the catalog/memory layer missed entirely); ls existence checks on 8
  mag/ files; sed/grep verification of 4 code citations inside models/providers.py,
  mag/cost_learn.py, mag/cache_map.py; knowledge_graph.json distill count (1); adhoc
  register area-count grep; ascii/em-dash scan on this file (2 non-ascii chars found and
  fixed this sitting; em-dash count 0).
- Not run: any pytest, any estate gate, the full 11-pack provenance re-audit (my RQ2 check
  is a spot-check of code citations only), any cache_map.py edit (code change is not a
  sweep act).
