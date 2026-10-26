# LENS OF LENSES - 8 frontier areas for the sweep, frontier_olm 2026-09-30

Seat: lens-questions gopher. Inputs: the five sibling lenses banked this run, each read in full
this session: `watch/inbox/frontier_olm_2026-09-30/lens/corpus.md` (corpus lens),
`lens/laws.md` (laws lens), `lens/graph.md` (knowledge-graph lens), `lens/burns.md` (burns
lens), `lens/doors.md` (doors lens). Every holding below is cited to a lens line, which in turn
cites the estate byte. The 8 areas are the estate's standing area set, same slugs the 09-28
sweep used (`watch/inbox/frontier_olm_20260928/`, per burns.md:76-79); nothing here re-banks
that sweep's 21 confirmed finds (burns.md:82) or its standing-lane table (burns.md:39-54).

Dedupe law for the sweep (burns.md:90-91): a today-sweep over the same 8 areas x 4 doors with
the same date window would be a re-bank. Overlap against
`watch/inbox/frontier_olm_20260928/register.jsonl` row ids/titles is the cheap dedupe. Doors
state: arXiv / HN / fxtwitter live-verified 2026-09-30 (doors.md:9,21,48); reddit closed by the
lor2 login/403 wall (doors.md:41-44), mirrors (pullpush, redlib) are prior-session route-arounds,
not re-probed (doors.md:45).

---

## 1. open-and-local-language-models

**What we already hold:** AI/agent curricula mass in corpus/library (ms-genai 12,142,
ms-agents 9,429, zcode-zai-org 6,810, openai-cookbook 3,120, anthropic-courses 224; corpus.md:12,18);
arXiv shelf 3,776 rows (corpus.md:13,20); frontier intake thin - frontier_thinking shelf is 11
files (corpus.md:23). Funded set is glm-5.3-prime / qwen3.8-max-prime ($180 Nous) + grok-4.7,
Anthropic keys unfunded (laws.md:24); local janitors gemma:2b scut + gemma4 short worker
(AGENTS.md). Free-resource-landscape lane read green at 09-28: LLM7 free-class 4 to 3,
GLM-5.3-Flash dropped, Lightning lane FULLY DEAD, Featherless 22,059 served vs 28.6k counter
gap (burns.md:41,57-59). HN "local llm" door live, nbHits 2916 (doors.md:25-29).

**Questions for the sweep:**
1. Which open-weight models released since 2026-09-28 are credibly capable of taking the
   janitor/scut slots (gemma:2b, gemma4) on a consumer Windows host, per arXiv + HN signal -
   and which claims are self-reported benchmarks the funded tier would still need to verify
   (laws.md:23: free-seat output is sensing, never verification)?
2. Which providers or free tiers have replaced the dead Lightning lane and the dropped
   GLM-5.3-Flash rung since 09-28 (burns.md:57-59), and does the Featherless 22,059 vs 28.6k
   counter gap have a published explanation?
3. What does the high-signal local-LLM wave on HN (nbHits 2916 for "local llm"; top hit
   "Show HN: Clippy - 90s UI for local LLMs", 1122 points, doors.md:29) say about capability or
   UX thresholds the estate's local tier should adopt?
4. The frontier_thinking shelf holds 11 files (corpus.md:23): what repeatable arXiv-door
   harvest (door verified live 09-30, doors.md:14-18) fills it continuously, and which of the
   3,776 state/arxiv rows are stale past usefulness for this area?

**Estate map:** Feeds the driving-ladder funded set (memory/rib/RIB_DRIVING_LADDER_20260928.md)
and the free-lane sensing policy (memory/rib/RIB_FREE_USAGE_POLICY_20260823.md) plus the local
janitor tier in the queue lanes - decides which rungs local/open models can hold so the funded
budget is spent only where judgment demands it.

---

## 2. quantization-compression

**What we already hold:** The auto_quantize module is a top-linked module at 4 invariant links
(graph.md:24); those edges are among the 823/825 dangling ones (graph.md:13). The deliberate-ask
law names a quantize target as part of a strong ask (AGENTS.md clippy; laws.md:28). The
quantized-thought corpus self-marks every raw_count as inflated echo, provenance only
(laws.md:48-50,73). This week's carriers include quantizer-fallout (ball3) and quantizer-hygiene
(ball2) receipts (burns.md:108,111), contents not read by the burns seat.

**Questions for the sweep:**
1. What 2026 quantization results (GGUF quants, AWQ, 1.58-bit and successors) show measured
   quality retention at janitor-class model scale on held-out evals rather than perplexity alone?
2. Do the 4 invariants linked to auto_quantize (graph.md:24) survive contact with current
   literature under the five-axis emergence test (invariant alignment first, then cost, quality,
   variance, generalization - laws.md:34), or are they stale claims needing funded-tier
   verification before promotion?
3. What does current work report about quantization-induced divergence in multi-sample /
   consensus decoding - does agreement survive aggressive quantization, extending the estate's
   consensus-illusion finding (laws.md:33)?
4. What quantize target belongs in a deliberate ask (frozen prefix + tight ask + output
   contract) so quantized outputs stay byte-verifiable and re-derivable per the map law
   (laws.md:35)?

**Estate map:** Feeds the percolator's auto_quantize module and its promote gate
(mag/percolator.py:264-272) plus the deliberate-ask law (AGENTS.md clippy) - decides which
quantization receipts can pass the gate as verified work instead of banked sensing.

---

## 3. agent-memory-continuity

**What we already hold:** The knowledge graph is almost entirely virtual: 823 of 825 edges fail
id resolution; the only two that resolve come from family:readable_first (graph.md:13); three
builder defects named with fix order (graph.md:37; mag/knowledge_graph.py:123 truncation at
:165, maps_to mismatch :85 vs :172). 757 knowledge nodes (400 knots, 217 doctrines, 140 steals)
have zero edges; only BM25 reaches them (graph.md:30). All 300 case_law nodes collapse to the
literal id `law:` (graph.md:19). Landscape family agent_memory and knowledge_graph_rag exist as
the connective tissue (graph.md:23). Open ribs: the world-rib contract (laws.md:61), the
self-mapping fold (laws.md:62), the SubtleMemory relational-memory benchmark as a cold edge
(laws.md:71). Own-memory is 355,237 rows, the single largest holding (corpus.md:26); FTS decay
is a standing daily-heal surface (AGENTS.md B2-465). Warm boot loads chain tip + Vercel URLs +
session brief into memory/warm_state.json (AGENTS.md).

**Questions for the sweep:**
1. What memory architectures in current frontier work (graph-RAG variants, causal-graph memory,
   episodic consolidation) address id-resolution and edge-integrity discipline - the exact class
   of defect the graph lens measured at 823/825 dangling (graph.md:13-19) - and is there a
   published id-normalization discipline worth stealing before applying the three-fix list at
   graph.md:37?
2. The world-rib contract (laws.md:61) asks what type a RIB lowers to before any renderer is
   built: what current world-model or memory-to-world work defines such lowering contracts, and
   does anything there resolve the two contested cathedral ties (descent order, gate style,
   laws.md:70)?
3. Does the SubtleMemory relational-memory benchmark exist beyond the cold claim edge
   (laws.md:71) - a published instrument for preservation vs retrieval vs reasoning
   discrimination the estate could adopt or fold?
4. How do current systems keep 350k+ row own-memory corpora queryable without index decay (the
   B2-465 disease, AGENTS.md): hierarchical consolidation, learned indexes, delta-only hot paths?
5. Which cross-session continuity mechanisms (chain-tip warm boot per AGENTS.md; session
   freeze/resume) publish measured benchmarks, so warm boot can be evaluated rather than
   asserted?

**Estate map:** Feeds mag/knowledge_graph.py (the three id defects and fix order at graph.md:37),
the warm-boot chain (mag/hermes_warm_boot.py into memory/warm_state.json), and the B2-465 FTS
heal loop (tools/corpus_fts_rebuild.py) - decides whether the estate's memory organs become a
navigable graph or stay isolated vertices reachable only by text search.

---

## 4. swarm-orchestration

**What we already hold:** Fan-out width law: workflow children get maxAttempts 0, keep
max_concurrency at 3 or less; Task agents ride the main-session retry path, measured clean at
widths 3/6/10/12 with width 10 banking 109.4M tok/h, 15-16 rung untested (AGENTS.md clippy).
Max-concurrency standing law: 50 workflow children ran clean; first rate-limit contact is a HOLD
signal, not a width cut (AGENTS.md). Orchestration tax at scale is a named unmeasured risk
(laws.md:68). The 09-28 mine's headline: promote gate is a bare counter
(mag/percolator.py:264-272) while the paired-blind gate sits unwired
(mag/seed_percolator.py:6-16); certified-decision acceptance (REUSE, arXiv 2609.33180) is the
named upgrade path (burns.md:86-89). Single-controller and operator-veto laws hold (laws.md:40).
World-models-multi-agent lane green but its driver restart is still NOT done (burns.md:44,67).
The workflow gate enforces per-item actors, pass-off, steering, incremental salvage, published
deliverable, receipts (AGENTS.md build discipline).

**Questions for the sweep:**
1. Does certified-decision acceptance (REUSE, arXiv 2609.33180, burns.md:89) still hold as the
   upgrade for the bare-counter promote gate (mag/percolator.py:264-272), and what newer gate
   designs (post 09-28) would wire the paired-blind gate (mag/seed_percolator.py:6-16) without
   fallback-branch creep?
2. What published multi-agent dispatch measurements exist at width 15-16 and above (the rung
   above the estate's measured width 10 / 109.4M tok/h) - does anyone report the orchestration
   tax the grok-4.5 critique named unmeasured (laws.md:68)?
3. How do current swarm systems treat first-contact rate limits: HOLD-and-retry-internal,
   backoff, pause, or reroute - does any published evidence refine the standing-law reading that
   first contact is a HOLD signal rather than a width cut (AGENTS.md max-concurrency law)?
4. The world-models-multi-agent driver restart is still NOT done as of the last ledger row
   (burns.md:67): what driver-supervision patterns (reaper design, process-tree/job-object
   attribution per the runaway-python opens, laws.md:66) close that gap class structurally?
5. What interagent pass-off reliability numbers or failure taxonomies are published for
   structured handoffs between agents - comparable to the estate's B2-443 workflow-child failure
   census (AGENTS.md) - that the workflow gate's pass-off requirement could be graded against?

**Estate map:** Feeds the dispatch-shape laws in AGENTS.md clippy (fan-out width + max
concurrency), the workflow gate and its registry (tools/workflow_gate.py,
memory/workflows/REGISTRY.jsonl), and the percolator promote/seed gates - decides lane widths,
gate wiring, and retry strategy for every burn wave and workflow fan-out.

---

## 5. finetuning-adaptation

**What we already hold:** Oral_history/seat_pools 11,870 + nacho_archaeology 2,981 rows are the
self-archaeology mass (corpus.md:12,22); the code-agent-data organ treats seat session tapes and
room.jsonl as the QLoRA training corpus. training/ carries arena_profiles, cost_ledger, events,
loop_gaps ledgers (git status). Two audit warnings: corpus domain labels are path-inferred, not
content-read, marked OWED (corpus.md:34); the quantized-thought corpus self-marks all raw_counts
as inflated echo (laws.md:50). Counsel law: licenses gate training-corpus eligibility; platform
ToS gates scraping (laws.md:42).

**Questions for the sweep:**
1. What QLoRA/LoRA recipes published since 09-28 make janitor-class local models reliably
   absorb procedural/domain adaptation from session-tape corpora like the estate's 11,870
   seat_pool rows, with measured retention on held-out tasks rather than loss curves?
2. Which estate training corpora are corpus-grade versus echo-inflated by a content-read audit -
   given domain labels are path-inferred and marked OWED (corpus.md:34) and one estate corpus
   self-marks every raw_count as inflated echo (laws.md:50)?
3. What does training/loop_gaps.jsonl show recurs across loops, and does current literature
   classify that gap class as adaptation failure (finetunable) versus architecture gap (not
   finetunable)?
4. When does distillation from funded primes (glm-5.3-prime, qwen3.8-max-prime) into local
   models beat direct dispatch on cost per correct verdict, with training/cost_ledger.jsonl as
   the baseline instrument and conditions named per the ONE-BUG law (laws.md:18)?
5. What license/ToS screens do current dataset papers apply to session-derived or
   conversation-derived corpora - does the counsel triage law (licenses gate training-corpus
   eligibility, laws.md:42) match emerging dataset-card and license practice?

**Estate map:** Feeds the code-agent-data organ (seat tapes to QLoRA corpus) and the training/
ledgers (arena_profiles, cost_ledger, loop_gaps), gated by the lawyer-boot triage
(memory/rib/RIB_LAWYER_BOOT_20260904.md) - decides whether the fleet's own transcripts become
finetuned successors or stay unevaluated mass.

---

## 6. kv-cache-context-engineering

**What we already hold:** corpus/library holds lmcache-src 2,331 rows, KV-cache serving internals
(corpus.md:12,21). The context_checkpoint and context_compression modules are top-linked at 4
invariant links each (graph.md:24) - edges currently dangling with the rest (graph.md:13). The
deliberate-ask shape is the estate's proven cache instrument: frozen prefix took cache hit ratio
6.5% to 98% and ~$161 to ~$3.60 at the same volume (laws.md:28); byte-identical asks for cache
hits is the playbook law (AGENTS.md). Cached snapshots are a correctness hazard - the ram-cache
stale-snapshot rib is the pattern fix (laws.md:36). The reddit door for this area hit the lor2
wall on 09-28 (doors.md:44) and stays closed.

**Questions for the sweep:**
1. What has landed in KV-cache serving/compression upstream of lmcache (2,331 estate rows,
   corpus.md:21) since the estate's copy - cross-session prefix reuse, paged/offload, shared
   KV across swarm siblings - and which pieces apply to the frozen-prefix discipline measured at
   6.5% to 98% hit ratio (laws.md:28)?
2. At what context length does janitor-class local model quality measurably collapse - what sets
   the real budget for context-pack and memweave structures, rather than the current unmeasured
   assumption?
3. Do the context_checkpoint / context_compression invariants (4 links each, graph.md:24)
   re-derive from current KV/context literature, or are they stale virtual edges needing the
   three-fix treatment before they carry meaning?
4. What context payload shape for swarm children (full pack vs delta vs rib pointer) has
   published reliability numbers, given the deliberate-ask form (frozen prefix + tight ask +
   output contract, laws.md:28) is the estate's only measured shape?
5. With the reddit door closed by the lor2 wall (doors.md:41-44), what community signal source
   (HN search_by_date, arXiv, mirrors) replaces it for this area without leaving a direct-recipe
   OWED?

**Estate map:** Feeds mag.cmd context-pack, the memweave doctrine (DOCTRINE_MEMWEAVE_20260810.md
via laws.md:26), and the context_checkpoint / context_compression module pair - decides how seats
receive context at minimum token cost with provider cache hits preserved.

---

## 7. evals-self-improvement

**What we already hold:** The consensus illusion is measured, not theorized: the flock agreed
with strong-remote 0/3 while carrying HIGH consensus strength (0.60-0.67), and single-local was
correct 3/3; the surrogate-action decode is the named root cause (laws.md:33); the
consensus-decode redesign is open (laws.md:58). The adversarial battery ran n=3 workloads - n is
tiny (laws.md:59). The emergence-boundary instrument (skill_ledger, five axes, longitudinal
compounding) is specified in the ribs; no rib shows it holding that boundary (laws.md:34,60).
Poisoning resistance rests on one pass (laws.md:67). The promote gate is a bare counter
(burns.md:87). A de-echoed frequency instrument for compiled laws is open (laws.md:73). The
byte-truth gates exist: census drift patrol tripwires B2-215/216/244/246/249 and the violation
ratchet (AGENTS.md). AH10 glm-vs-ds settled 2-0 tier-1 (AGENTS.md).

**Questions for the sweep:**
1. What 2026 eval frameworks measure consensus/agreement as a calibrated property decoupled from
   correctness - validating or refuting the consensus-illusion result (0/3 agreement at 0.60-0.67
   strength, laws.md:33) and informing the consensus-decode redesign (laws.md:58)?
2. What published harnesses would scale the adversarial battery from n=3 workloads to a real
   instrument (multi-hop reasoning, tool use, long context, deliberate RIB poisoning, pod-failure
   injection) - the rib's own named gap (laws.md:59)?
3. Does any published skill or A/B ledger learn an emergence boundary longitudinally under a
   five-axis decision rule (laws.md:34) - is there evidence the compounding signal exists outside
   the ribs' specification (laws.md:60)?
4. What gate designs replace bare-counter promotion with evidence-earned promotion (the
   certified-decision path, burns.md:89), and what eval would have caught the census 1,341
   hand-copied headline drift (the B2-215 tripwire disease, AGENTS.md) before it shipped?
5. For the de-echoed frequency instrument (laws.md:73): what current instrumentation (citation
   graphing, first-seen / last-seen / distinct-source metrics) measures a compiled law's real
   currency so weight is earned by evidence rather than echo?

**Estate map:** Feeds the percolator + invariant chain (mag/percolator.py, mag/seed_percolator.py)
and the self-improvement loop (mag.cmd improve), plus the byte-truth gates
(tools/census_drift_patrol.py, tools/violation_ratchet.py) - decides when a lesson is provably
learned twice and earns promotion versus staying a banked-but-unverified finding.

---

## 8. inference-efficiency

**What we already hold:** The driving ladder is code-as-law: only Hermes ($180 Nous,
glm-5.3-prime / qwen3.8-max-prime) and grok-4.7 are funded; hoarding funded budget while free
lanes grind is a named violation (laws.md:24). Janitors run local-first via Ollama (AGENTS.md).
The throughput envelope: workflow children 429/1302 on their own retries; Task agents measured
clean to width 12; the limit is rolling throughput, not width-only (AGENTS.md clippy). The
deliberate-ask efficiency proof: cache hit ratio 6.5% to 98%, ~$161 to ~$3.60 at the same volume
and speed (laws.md:28) - predating the current funded set. training/cost_ledger.jsonl and the
burn receipts are the cost instruments. Simulate only what is deterministic; live model calls
need a real run (laws.md:45).

**Questions for the sweep:**
1. What inference-efficiency techniques (speculative decoding, continuous batching, early exit,
   paged attention) are measured - with receipts, not vendor claims - at janitor-class scale on
   consumer Windows hardware in 2026?
2. What is the estate's actual cost per correct verdict per tier (local janitor, free lane,
   funded prime, grok-4.7) from training/cost_ledger.jsonl and burn receipts, and where is the
   crossover where funded beats local - has anyone computed this crossover, or is it OWED?
3. Does the measured envelope finding (rolling throughput limit, first contact = HOLD, AGENTS.md)
   match any published provider rate-limit model or heavy-user dispatch report?
4. What energy/time ceiling applies to overnight local inference (offpeak queue, pile
   classification), and which efficiency gains are worth the complexity at the estate's real
   workload scale (janitor cycles, burn waves, a 9.34s test suite)?
5. Does the deliberate-ask economics (6.5% to 98% hit ratio, $161 to $3.60, laws.md:28) still
   hold against current glm-5.3-prime / grok-4.7 pricing, or does the paid-tier shape need a
   re-measure with instrument, moment, and context named per the ONE-BUG law (laws.md:18)?

**Estate map:** Feeds the driving-ladder routing (memory/rib/RIB_DRIVING_LADDER_20260928.md) and
tier laws (AGENTS.md clippy), training/cost_ledger.jsonl accounting, and the offpeak/local
janitor deployment - decides cost per verdict across local/free/funded tiers and when to spend
the funded budget the operator ordered spent.

---

## OWED by this seat

- All holdings above are cited to the five sibling lens files, not re-derived: I did not re-run
  the corpus count, the graph parse, the ledger parse, or the door probes this ask. The sibling
  lenses carry their own instruments and OWED lists (corpus.md:33-36, doors.md OWED items).
- The JSON result submitted alongside this file is the same 8 areas, 3-5 questions each, estate
  maps verbatim in substance.
