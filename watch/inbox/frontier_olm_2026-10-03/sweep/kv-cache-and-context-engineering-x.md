# SWEEP: kv-cache-and-context-engineering via X (frontier_olm 2026-10-03)

source-fetched: 2026-10-03

Seat: sweep-kv-cache-and-context-engineering-x. SUPERSESSION NOTE: this file
rebuilds over an earlier same-day pass at this path (corpus.md:3 precedent:
rebuild, re-verify every number with my own runs, disclose). That pass claimed
the fxtwitter door "could not be exercised once, not even to 403"; my retest
this sitting found the X door INTERMITTENTLY degraded, not dead: two of my
site:x.com queries returned bare x.com links (status path stripped), two
returned full status URLs, and 6 of 6 fxtwitter status resolutions returned
code 200 with full text. One fxtwitter ARTICLE id resolved 404 (body
unresolvable; banked as snippet per the recipe fallback, stated below). Every
item in this file was fetched and read BY ME this sitting; nothing is adopted
from the prior pass.

House laws held: ascii only, no em or en dashes in my prose; every claim cites
what was read or run this sitting; overlap greps run before banking; nothing
asserted from memory.

## Doors exercised (my runs, with receipts in this sweep dir)

- WebSearch site:x.com, 4 queries: (1) "KV cache prefix caching 2026" -> first
  attempt hit the search backend rate limit (error 1302), retry returned ONE
  hit with a stripped link (bare https://x.com); (2) "context engineering agent
  memory 2026" -> one hit, stripped link; (3) "arXiv KV cache eviction paper
  September 2026" -> 7 hits with FULL status URLs; (4) "cached tokens pricing
  agent cost savings" -> 10 hits with full status URLs; (5) "structured
  context OR context folding OR ACE" -> leaked off-site (chatpaper results),
  census-only.
- fxtwitter (api.fxtwitter.com/i/status/<id>): 6 status resolutions code 200
  (HEI, Memoirs, CSVisionPapers, cognition, BrandonWaselnuk, mark_k), 1
  article-id resolution 404. Raw JSON banked at sweep/_fx_*.json.
- OWED DOORS for Q1 (burns.md:114-115 names "the kv-cache arxiv lane's not-run
  WebSearch and /list doors" as owed; the ask routes them through this seat):
  I ran BOTH myself this sitting. arXiv export query
  (all:"prefix cache" OR all:"prompt caching" OR all:"prefix caching",
  submittedDate desc, 25 entries -> sweep/_x_owed_arxiv_q1.xml); HN Algolia
  search_by_date "prefix caching" since 2026-09-03 (69 hits ->
  sweep/_x_owed_hn_q1.json). The sibling arXiv lane file
  (kv-cache-and-context-engineering-arxiv.md) shows the lane's arXiv door was
  also independently cleared this fold; my runs stand as the seat's own
  execution of the owed doors.
- WebFetch: github.com/ranxianglei/billion-context (full extract),
  huggingface.co/papers/2606.16824 (full extract).
- arXiv export API id_list fetches (verbatim abstracts read): 2609.24991,
  2609.16617, 2609.30738, 2609.22528 (WRONG ID, a math paper; my fetch error,
  corrected with 2606.22528 next call - disclosed, not papered over),
  2606.22528, 2608.11392, 2606.16824, 2510.04618 (ACE date verification),
  2609.27354 + 2609.33717 (Q3 adjacency).

## Pass 1 census (my candidates, window 2026-09-03..10-03)

In-window candidates considered (33): the three X-resolved eviction posts
(Beyond Mean Attention 2609.30738 Sep 28 via @HEI; ValueDiff 2609.23314 Sep 23
via @Memoirs; DeltaS 2609.27470 Sep 28 via @CSVisionPapers); BrandonWaselnuk
GLM-migration + double-billing post (Sep 24); undated X snippets: Wulfie Bain
(cache-busting agents, WebSockets), "Assembling Context That Will Not Lie You
Into a Million-Dollar Loss" (ACE/ICLR 2026 pointer), @danielmisrael eviction
pitfalls, @haileysch__ bespoke-eviction-tooling; owed-door arXiv entries:
SparseEngine 2609.39068, Preserving Provenance 2609.38706, CADOC 2609.37012,
TempoKV 2609.35065, Identical Runs 2609.33812, RelaxKV 2609.33503, Suffix
Replay 2609.33477, Tessera 2609.32999, AgentReplay 2609.32283, RR-Evict
2609.32278, KV memory wall 2609.30854, Harness Tokenomics 2609.28919, Fancy
Eviction v2 2609.28870, KV Cache Working Set 2609.27746, Who Pays 2609.24991,
Total Cost of Agency 2609.23790, Divergence Timing 2609.16617, py-kvcache
2609.11744, Constraint-Driven CE 2609.27354, SelfSuite 2609.33717; HN in-window
items: Context Language Models 49931278 (Oct 2), Jeff Jev 0.8B 49888773
(Sep 29), Ask HN Qwen3.8 harness 49822338 (Sep 23), LRU-is-harder 49682856
(Sep 13, HELD), OpenRouter 49666018 (Sep 11), Prompt Trees 49637425 (Sep 10,
considered by the HN sibling), Cerebras Qwen 49567415 (Sep 4).
Out-of-window set-asides (dated by my fetches): Cognition post Sep 1 and
mark_k post Sep 1 (2 days early; Cognition banked below WITH the disclosure,
mark_k used in the Q1 verdict text only), nateherk Anthropic-tokens article
(May 21), Lance Martin prompt-caching deep dive (2025-era id), KV-Batching
serving post (Aug 26), Zen_with_AI probabilistic-eviction post (Aug-era id),
Context-Folding 2510.11967 / AgentFold 2510.24699 / ACE 2510.04618 (2025/early
2026; ACE used for Q3 verdict only).

## Overlap baseline (my greps, run before banking)

rg over catalog/catalog.jsonl (917,885 rows) and memory/ (agent_state, ghost,
biography_backup excluded from the walk), case-sensitive unless said:

- "billion-context", "ranxianglei": 0 catalog rows, 0 memory files. CLEAN.
- "2606.16824" + "CacheWise": 0 catalog rows; 1 memory file,
  memory/research_polished/kv_cache_compaction.md:13 - held as a bibliography
  NAME inside the occupied-field list (PBKV, KVFlow, CacheWise, RoleKV,
  TokenCake) with gap-fold G1. Numbers were NOT held. Extension disposition.
- "2609.24991" + "unalloc": 0 catalog rows, 0 memory files. CLEAN.
- "2606.22528" + "Governance Decay" + "ConstraintRot": 0 catalog rows; memory
  holds the TERM only (case-insensitive re-check):
  memory/research_packs/COMPACTION_ALGO_RESEARCH_20260919.md:32 names
  "governance decay" as a failure mode with NO id and NO numbers, and
  kv_cache_compaction.md carries 1 case-insensitive hit. Extension
  disposition.
- "2608.11392" + "Guardrail Survival" + "Kwartler": 0 catalog rows, 0 memory
  files. CLEAN.
- "2609.16617" + "Divergence Timing": 1 catalog row (the unread daily abstract
  pull state/arxiv), 0 memory files, 0 sibling-sweep rows. CLEAN NEW.
- "2609.30738" + "Beyond Mean Attention": 1 catalog row (unread pull), 0
  memory files. Read by me; used in the Q5 verdict, not banked as an item.
- "Over 95% of tokens" (Cognition), "Waselnuk" + status id: 0 catalog rows, 0
  memory files. CLEAN.
- Sibling-lane anti-rebank (my grep over this sweep dir's *.md): RR-Evict,
  Tessera, CADOC, KVSET/Working Set 2609.27746, RelaxKV, Suffix Replay,
  Preserving Provenance, Identical Runs are already banked by the 0928 / 09-30
  / 10-01 sweeps. NOT re-banked here. The same-fold HN sibling owns
  gauravapiscean/agentic-kv-cache; the arXiv sibling owns PatchKV, EchoPress,
  Beyond Token Savings, ARSM, SparseEngine.

## Pass 2 deep reads (fetched and actually read by me this sitting)

### 1. billion-context - READ, BANKED (strongest find)

github.com/ranxianglei/billion-context, read end to end via WebFetch. An npm
proxy between coding agents and Anthropic/OpenAI APIs that folds long sessions
in small reversible ranges: injected tools compress / decompress /
search_context / acp_status; "summaries are written in small ranges, can be
decompressed on demand, and the cache prefix stays intact"; rule of thumb
"compression itself costs <=2% - a healthy session sits at 95-97%" prefix hit;
self-measurement "4.5 months, three hosts, 174,327 model calls, 18.76B
cumulative input tokens, zero window violations on 204,800-token models";
status "Early", 500+ mock tests passing, real-model integration the next
milestone; target list includes hermes, zcode, omp, pi, opencode. This is the
estate's feed-structures-not-prose doctrine plus the byte-identical-prefix law
productized by someone else; the estate hook is mag.cmd context-pack and the
frozen-RIB thin-tail shape (kv_cache_compaction.md). Self-reported numbers,
unverified by us; named as such.

### 2. CacheWise 2606.16824 - READ, BANKED as extension

arXiv abstract fetched verbatim (sweep/_x_abs_cachewise.xml) + HF papers page
read. "CacheWise reduces KVCache evictions by up to 2-2.6x and improves total
agent session completion time by up to 3.5x." Mechanism: prefix-aware
scheduling + reuse-aware eviction guided by tool-call metadata (tool name and
arguments; TF-IDF/KMeans clustering of argument strings; eviction in
decreasing predicted time-to-next-reuse, an approximation of Belady); ~2,500
lines of Python on vLLM, replacing LRU with a prediction-driven heap; traces
are real Claude Code sessions (~10M tokens, CATraces). The estate held the id
name-only (kv_cache_compaction.md:13); this read banks the measured content.
G1 boundary stated: its win may live in the scheduling layer upstream, not in
the eviction policy itself; confronting it with the LRU-leaf null is the open
probe.

### 3. Who Pays for the KV Cache? 2609.24991 - READ, BANKED (clean new primary)

Abstract read verbatim. "We present unalloc, an open-source tool that joins
OpenCost, LiteLLM, OpenAI and Anthropic cost data into one exact ledger and
reports the share of spend with no owner." Findings at the seams: in a
CONSTRUCTED multi-pod scenario (synthetic allocations, not observed billing -
the paper says so) leader-only owner labels leave 66% of the GPU bill
unowned; the natural fallback key misassigns 61% to a Helm chart name while
the headline unallocated share falls to 4%; enabling every source double
counts gateway spend. This is the dollar-denominated twin of the estate's
question 2: where the budget is money, the binding problem is attribution, not
hit rate. Caveat carried: one of the case studies is explicitly constructed.

### 4. Governance Decay 2606.22528 - READ, BANKED as extension

Abstract read verbatim (my first fetch grabbed 2609.22528 by typo - a Hilbert
Schmidt frames paper - corrected in the next call; both disclosed). "violation
rises from 0% with the policy in full context to 30% after compaction,
reaching 59% for some models"; survival keeps 0%, dropping the constraint
reaches 38%; a Compaction-Eviction Attack defeats every evaluated model;
Constraint Pinning (training-free) is the mitigation. Out of the 30-day window
(published 2026-06-21, updated 06-27) - banked because the estate held the
term with no id, no benchmark, no numbers (COMPACTION_ALGO_RESEARCH
_20260919.md:32), so this is a genuinely new primary for the holdings. Direct
falsifier under memlang: a compactor that feeds prose back instead of pinned
structures deletes law, silently.

### 5. AI Guardrail Survival under Single-Cycle Agentic Self-Summarization
### 2608.11392 - READ, BANKED (clean new primary)

Abstract read verbatim. "Our central finding is that a presence check is not a
safety check": degraded rule residues look like rules but do not act like
them; behavioral replay gaps of +34 and +57 points; rule-form items are
retained substantially more often than prominence-matched facts, which is why
presence audits feel adequate. Published 2026-08-11 (2 days past the window
edge on its update; disclosed). The estate's verkle-anchored registries are
the external ground truth this paper says detection requires.

### 6. Divergence Timing and Cumulative Disagreement under KV-Cache Eviction
### 2609.16617v2 - READ, BANKED (clean new primary, in-window)

Abstract read verbatim. "SnapKV at 50% retention enters divergence later and
less often than SnapKV-512 or recent-token retention with the same 50%
prompt-cache budget"; exact decomposition: expected mismatch fraction = first
mismatch + post-divergence exposure x mismatch rate; on 288 documents
post-divergence exposure accounts for 85-90% of aggregate mismatch gaps
(Llama-3.1-8B / Qwen2.5-7B). This grounds the estate's byte-identical-asks
law in theory: eviction-induced divergence is real, measurable, and
back-loaded into post-divergence exposure, which a full-prefix-reload pattern
avoids entirely.

### 7. Cognition post - READ, BANKED (X door, date 2 days before window, disclosed)

fxtwitter resolution code 200 (sweep/_fx_cognition.json), posted Tue Sep 01:
"Over 95% of tokens from a coding task are cached tokens. Fable 5.1 dropped
the price of cached tokens by 4x, making it much more efficient for coding as
a whole, despite higher uncached prices." The strongest public money-side
datum for Q1. Self-reported vendor-adjacent claim; date named.

### 8. BrandonWaselnuk post - READ AS SNIPPET, BANKED LOW (fallback per recipe)

fxtwitter resolved the post (code 200, Thu Sep 24, article title "What We
Learned Moving Our Agent Loops from Anthropic to GLM") but the ARTICLE body
id resolved 404; the double-billing claim exists only as the search-result
snippet: "some OpenAI-compatible APIs include cached tokens inside
prompt_tokens, causing double-billing in cost pipelines that assume disjoint
buckets." Banked with the degradation stated in the note; confidence 0.5.

## Research question verdicts (all five, grounded in my reads)

Q1 (prefix-reuse gains that beat or bound the measured 98 pct / ~$3.60,
lens/laws.md:23): nothing I found BEATS it. The published money-side bounds:
Cognition >95% cached-token share on real coding tasks + 4x cached-price cut;
mark_k's Sep 1 post (read, not banked): cache reads $0.25/M down from $1.00,
Anthropic estimating ~25% cheaper typical and up to 45% for highly agentic
workloads; serving-side, CacheWise reports evictions down 2-2.6x and session
completion up to 3.5x (throughput, not dollars per unit of work); the held
agentic-kv-cache external anchor is 83.48% at 8k blocks. The estate's own
instrument measured 93.876% hit at anchor on real trails
(memory/runs/lru_null_arm/lru_null_arm_results.json, verdict.holds true).
Nobody publishes dollars-per-correct-verdict; the estate's 44x cost lever
stands unbounded-from-above by this window's literature.

Q2 (does the 4,800-char budget transfer to paid tiers; what rule does
prefix_cache_sim predict per tier): the number does NOT transfer; the shape
does. tools/prefix_cache_sim.py is char-denominated by design (docstring
lines 1-24; the budget is mag/context_pack.py:67's janitor pack budget);
tools/lru_null_arm.py:95-100 fixes budget 4800 chars, 256-char blocks,
1024-char frozen prefix. What the sim predicts (banked results file): hit
rate is decided by ASSEMBLY at fixed capacity (frozen_append 0.9388 vs
frozen_window 0.3762 vs volatile 0.0013 at the same 8192-block anchor) and
saturates in capacity at ~4x pack (0.9335 at 4x vs 0.9388 at 16x and
unbounded). The per-tier transfer rule is therefore: keep the frozen prefix
byte-stable and >= provider cache-eligibility minimum, keep the tail
append-only, size cache/working set >= 4x, and convert hit rate to dollars
per tier with that tier's cached/uncached price ratio; 4,800 chars (~1,200
tokens) is a janitor-side pack constraint, not a cache parameter. Where the
budget IS dollars, the binding problem moves to attribution and metering:
Who Pays 2609.24991 (unalloc; seams, double counting) and the Waselnuk
double-billing trap are the two external instruments to diff a
mag/inference_budget.py dollar ledger against.

Q3 (which context shapes minimize tokens-per-correct-verdict; any post-10-02
paper measuring structure-vs-prose directly): NO post-10-02 paper found on my
doors (newest "context engineering" submission on the arXiv export door:
Sep 27). The measured structure-vs-prose evidence remains: ACE 2510.04618v3
(fetched by me: pub 2025-10-06, upd 2026-03-29; "context collapse, where
iterative rewriting erodes details over time" is cured by "structured,
incremental updates"); Governance Decay (surviving constraint = 0%
violations vs dropped = 38%; Constraint Pinning); Guardrail Survival
(rule-form text survives compaction better than prominence-matched facts).
For the estate: frozen RIB prefixes + pinned invariants + claritas faces ARE
the pinning pattern, and the estate's own routing law (question class
explains 36.3 pct of score variance, lens/laws.md:29) is ahead of the public
literature on tokens-per-correct-verdict, which no one publishes.

Q4 (one tool enforcing byte-identical asks across the seven bypass surfaces;
closing the cache contract and the EMPTY_REASONING gap with a single
instrument): the mechanism already exists in shape: mag/inference_budget.py
(docstring lines 8-12) is "the single source both carriers (tools/hermes_burn
.py, tools/model_garden.py) import" for recipes, the empty-content
classifier, and the ONE sanctioned terminal reaction; the seven bypass
surfaces are named at RIB_INFERENCE_BUDGET_20261001.md:100-114
(stealth_driver, duel_harness, tesuji_fire, lane_runner, lite_scale,
wave_fire, ds_workhorse). Closing the gap is a code change (import + an
ask-bytes hash pin on the rendered prefix, refuse dispatch on drift), not a
research question. External nearest-neighbors found: billion-context's
byte-exact prefix-affinity fallback and the estate-held truth-auditor
five-check attestation (per HN sibling Q3); Divergence Timing 2609.16617
supplies the theory that a broken prefix contract is measurable and
back-loaded. No public single-instrument analog exists on my doors.

Q5 (eviction policy for the repeated-boot pattern where every seat reloads
the same rib chain tip): the null wins, again. For a hot shared prefix,
recency keeps the tip resident; my reads this window add the boundary
conditions: CacheWise's Belady-approximation needs tool-call metadata and
pays off where sessions churn; Beyond Mean Attention 2609.30738 (abstract
read; in-window Sep 25; catalog row is an unread pull) shows the
eviction-scoring arms race (attention dispersion + MMR-style redundancy
penalty, +1.1 macro on LongBench at budget 64) is CHAT-long-context-shaped;
DeltaS and ValueDiff (X posts read via fxtwitter) are streaming-video and
sink-suppression settings; Divergence Timing 2609.16617 shows policy choice
matters through post-divergence exposure, which identical reloads avoid.
Estate rule: byte-identical tip + capacity >= 4x working set (measured
saturation) + TTL covering the boot cycle; eviction sophistication is
decoration for this pattern (the G1 law's own consequence clause,
tools/lru_null_arm.py:173-174).

## Not banked, disposition stated

mark_k Sep 1 post (read; used in Q1 verdict text only - window edge),
Beyond Mean Attention / DeltaS / ValueDiff (X+abstract reads; Q5 verdict
text only - eviction-scoring literature, no estate-shape win), nateherk May
21 article (out of window), danielmisrael / haileysch__ / Wulfie Bain /
Assembling-Context posts (no resolvable status id on my queries; snippets
only, kept in census), SelfSuite 2609.33717 + Constraint-Driven CE 2609.27354
(abstracts read; adjacency for Q3, no direct structure-vs-prose measurement),
all prior-sweep-banked arXiv items listed in the census.

## Carried to SweepResult (strongest first)

1. billion-context (new primary, doctrine-exact, Q3/Q4).
2. CacheWise 2606.16824 (name-only holding now carries numbers; Q5/Q1).
3. Who Pays 2609.24991 (clean new, Q2 dollar attribution).
4. Governance Decay 2606.22528 (term-only holding now carries id+benchmark; Q3).
5. Guardrail Survival 2608.11392 (clean new primary, Q3).
6. Divergence Timing 2609.16617 (clean new primary, in-window, Q5/Q4 theory).
7. Cognition post (Q1 money bound; 2 days before window edge, disclosed).
8. Waselnuk post (snippet-only fallback, degradation stated; Q2/Q4).
